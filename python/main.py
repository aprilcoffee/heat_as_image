import time
import threading
import subprocess
import os
from network_utils import get_network_info
from gpu_utils import get_gpu_stats, run_temperature_control, update_target_temperature
from osc_handler import OSCHandler
import config
from prompts import get_next_prompt_pair
import sys
from pythonosc import udp_client
import psutil

def cleanup_existing_processes():
    """Kill any existing Python processes that might be using our ports"""
    try:
        current_pid = os.getpid()
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if (proc.info['name'] == 'python.exe' and 
                    proc.info['pid'] != current_pid and 
                    proc.info['cmdline']):
                    cmdline = ' '.join(proc.info['cmdline'])
                    if any(keyword in cmdline for keyword in ['main.py', 'parler.py', 'osc_handler']):
                        print(f"Terminating existing process (PID: {proc.info['pid']}): {cmdline}")
                        proc.terminate()
                        proc.wait(timeout=3)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.TimeoutExpired):
                pass
    except Exception as e:
        print(f"Warning: Could not cleanup existing processes: {e}")

def main():
    # Clean up any existing processes first
    cleanup_existing_processes()
    
    get_network_info()
    
    # Initialize OSC handler
    osc_handler = OSCHandler()
    
    # Start OSC server
    osc_handler.start_osc_server()
    
    # Give the server a moment to start
    time.sleep(0.5)
    
    prompt_interval = 0
    current_prompt_pair = None
    
    try:
        while True:
            # Run temperature control
            stats = run_temperature_control()
            
            if stats:
                # Send temperature data to Processing
                osc_handler.processing_client.send_message("/gpu/temperature", float(stats['temperature']))
                osc_handler.processing_client.send_message("/gpu/power_draw", float(stats['power_draw']))
                osc_handler.processing_client.send_message("/gpu/power_target", float(stats['power_target']))
            
            # Get GPU stats and send via OSC
            stats = get_gpu_stats()
            osc_handler.send_gpu_stats(stats)
            
            # Send prompts every 10 seconds (or 8 seconds if generate is None)
            prompt_interval += 1
            
            # Determine interval based on current prompt pair
            # Default to 10 seconds for normal prompts
            interval_threshold = 100  # 100 * 0.1s = 10 seconds
            
            if current_prompt_pair and current_prompt_pair.get("generate") is None:
                # Use 8 seconds for temperature monitoring mode
                interval_threshold = 80  # 80 * 0.1s = 8 seconds
            
            if prompt_interval >= interval_threshold:
                current_prompt_pair = get_next_prompt_pair()
                print(f"Sending prompt: {current_prompt_pair}")
                osc_handler.prompt_handler("/prompt", current_prompt_pair)
                prompt_interval = 0
                    
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\nShutting down...")
        cleanup_and_exit(osc_handler)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        cleanup_and_exit(osc_handler)

def cleanup_and_exit(osc_handler):
    """Clean up resources and exit gracefully"""
    try:
        # Reset power limit to initial value
        subprocess.run(['nvidia-smi', '-pl', str(config.init_power_Consumption)])
    except Exception as e:
        print(f"Warning: Could not reset power limit: {e}")
    
    # Clean up OSC handler (closes all clients including Parler)
    try:
        osc_handler.cleanup()
    except Exception as e:
        print(f"Warning: Could not cleanup OSC handler: {e}")
    
    # Stop OSC server
    try:
        if hasattr(osc_handler, 'server'):
            osc_handler.server.shutdown()
    except Exception as e:
        print(f"Warning: Could not shutdown OSC server: {e}")
    
    # Try to stop Parler TTS process if it's running
    try:
        # Send a shutdown signal to Parler via OSC
        print("Sending shutdown signal to Parler TTS...")
        shutdown_client = udp_client.SimpleUDPClient("127.0.0.1", 9000)
        shutdown_client.send_message("/shutdown", "exit")
        shutdown_client._sock.close()
        
        # Also try to find and kill Parler processes more reliably
        import psutil
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if proc.info['name'] == 'python.exe' and proc.info['cmdline']:
                    cmdline = ' '.join(proc.info['cmdline'])
                    if 'parler.py' in cmdline:
                        print(f"Terminating Parler process (PID: {proc.info['pid']})...")
                        proc.terminate()
                        proc.wait(timeout=3)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.TimeoutExpired):
                pass
    except Exception as e:
        print(f"Warning: Could not stop Parler process: {e}")
    
    sys.exit(0)  # Make sure to exit cleanly

if __name__ == "__main__":
    main() 