import subprocess
import time
import re
import random
from pythonosc import udp_client
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer
import threading
import socket
import netifaces
import sys

# Default values
init_power_Consumption = 450
power_Consumption = init_power_Consumption
center = 45

# List of creative image prompts
image_prompts = [
    "silicon wafers glowing in clean room lights",
    "transistors etched in crystalline patterns",
    "NVIDIA engineers crafting GPU dies",
    "AMD fabrication plants humming with energy",
    "semiconductor masks aligning precisely",
    "TSMC clean rooms buzzing with activity",
    "RTX chips emerging from silicon foundries",
    "circuit traces flowing like digital rivers",
    "Intel engineers testing processor cores",
    "photolithography beams etching circuits",
    "GPU dies arranged in perfect formation",
    "clean room workers in bunny suits dancing",
    "molten silicon cooling into perfect wafers",
    "quantum tunneling in nanometer gates",
    "ray tracing cores lighting up benchmark tests"
    ]

def get_network_info():
    """Get and print IP address and WiFi network information"""
    # Get IP address
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't need to be reachable
        s.connect(('10.255.255.255', 1))
        ip_address = s.getsockname()[0]
    except Exception:
        ip_address = '127.0.0.1'
    finally:
        s.close()

    # Get WiFi network name (SSID)
    wifi_name = "Not Found"
    try:
        if sys.platform == "darwin":  # macOS
            cmd = "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -I"
            output = subprocess.check_output(cmd.split()).decode('utf-8')
            for line in output.split('\n'):
                if ' SSID:' in line:
                    wifi_name = line.split(': ')[1].strip()
        elif sys.platform == "win32":  # Windows
            cmd = "netsh wlan show interfaces"
            output = subprocess.check_output(cmd.split()).decode('utf-8')
            for line in output.split('\n'):
                if 'SSID' in line and 'BSSID' not in line:
                    wifi_name = line.split(':')[1].strip()
        else:  # Linux
            cmd = "iwgetid -r"
            wifi_name = subprocess.check_output(cmd.split()).decode('utf-8').strip()
    except:
        pass

    print(f"\nNetwork Information:")
    print(f"IP Address: {ip_address}")
    print(f"WiFi Network: {wifi_name}\n")

def get_gpu_stats():
    try:
        # Run nvidia-smi command to get multiple GPU properties
        result = subprocess.run([
            'nvidia-smi',
            '--query-gpu=temperature.gpu,utilization.gpu,memory.used,memory.total,power.draw',
            '--format=csv,noheader,nounits'
        ], capture_output=True, text=True, check=True)
        
        # Parse the comma-separated values
        stats = result.stdout.strip().split(',')
        
        # Adjust power consumption based on temperature
        global power_Consumption
        temp = float(stats[0])
        
        if temp > center:
            power_Consumption = max(150, power_Consumption - 5)
        else:
            power_Consumption = min(500, power_Consumption + 5)

        
        subprocess.run(['nvidia-smi', '-pl', str(power_Consumption)], capture_output=True)
        
        return {
            'temperature': temp,
            'utilization': float(stats[1]),
            'memory_used': float(stats[2]),
            'memory_total': float(stats[3]),
            'power_draw': float(stats[4]),
            'power_target': float(power_Consumption)
        }
    except:
        return None

def prompt_handler(address, *args):
    """Handle incoming OSC messages for prompt changes"""
    global image_prompts, processing_client, touchdesigner_client
    if args and isinstance(args[0], str):
        # Replace all prompts with the new one
        image_prompts = [args[0]]
        print(f"Replaced prompts with new prompt: {args[0]}")
        
        # Immediately send new prompt to Processing and TouchDesigner
        processing_client.send_message("/prompt", args[0])
        touchdesigner_client.send_message("/prompt", args[0])

def start_osc_server():
    """Start OSC server to listen for incoming messages"""
    dispatcher = Dispatcher()
    dispatcher.map("/changePrompt", prompt_handler)
    
    server = BlockingOSCUDPServer(("127.0.0.1", 8000), dispatcher)
    print("OSC Server listening on port 8000")
    server.serve_forever()

def send_gpu_stats_osc():
    # Set up OSC clients for Processing and TouchDesigner
    global processing_client, touchdesigner_client
    processing_client = udp_client.SimpleUDPClient("127.0.0.1", 12000)
    touchdesigner_client = udp_client.SimpleUDPClient("127.0.0.1", 7000)
    
    # Start OSC server in a separate thread
    server_thread = threading.Thread(target=start_osc_server)
    server_thread.daemon = True  # Thread will close when main program exits
    server_thread.start()
    
    prompt_interval = 0
    try:
        while True:
            # Get GPU stats and send via OSC
            stats = get_gpu_stats()
            if stats is not None:
                # Send to Processing
                processing_client.send_message("/gpu/temperature", stats['temperature'])
                processing_client.send_message("/gpu/utilization", stats['utilization']) 
                processing_client.send_message("/gpu/memory_used", stats['memory_used'])
                processing_client.send_message("/gpu/memory_total", stats['memory_total'])
                processing_client.send_message("/gpu/power_draw", stats['power_draw'])
                processing_client.send_message("/gpu/power_target", stats['power_target'])
                
                # Send random prompts to TouchDesigner and Processing every 5 seconds
                prompt_interval += 1
                if prompt_interval >= 10:  # 50 * 0.1s = 5 seconds
                    prompt = random.choice(image_prompts)
                    touchdesigner_client.send_message("/prompt", prompt)
                    processing_client.send_message("/prompt", prompt)
                    #touchdesigner_client.send_message("/gpu/power_target", stats['power_target'])

                    prompt_interval = 0
                    
            time.sleep(0.1)  # Small delay to prevent excessive CPU usage
    except KeyboardInterrupt:
        subprocess.run(['nvidia-smi', '-pl', str(init_power_Consumption)])
        return  # Exit the function when interrupted

if __name__ == "__main__":
    get_network_info()  # Print network info before starting
    send_gpu_stats_osc()
