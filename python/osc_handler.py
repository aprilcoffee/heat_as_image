from pythonosc import udp_client
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import ThreadingOSCUDPServer
import config
from prompts import TD_INSTRUCTIONS, PROMPT_PAIRS
import random
import threading
import time
import math
import socket
from gpu_utils import update_target_temperature
from config import center

class OSCHandler:
    def __init__(self):
        self.processing_client = udp_client.SimpleUDPClient(
            config.PROCESSING_IP, 
            config.PROCESSING_PORT
        )
        self.touchdesigner_client = udp_client.SimpleUDPClient(
            config.TOUCHDESIGNER_IP, 
            config.TOUCHDESIGNER_PORT
        )
        self.td_steps_client1 = udp_client.SimpleUDPClient(
            config.TOUCHDESIGNER_IP,
            7001  # First step control
        )
        self.td_steps_client2 = udp_client.SimpleUDPClient(
            config.TOUCHDESIGNER_IP,
            7002  # Second step control
        )
        self.parler_client = udp_client.SimpleUDPClient(
            config.PARLER_IP,
            config.PARLER_PORT
        )
        self.current_steps_main = 25
        self.target_steps_main = 25
        self.current_steps_sine = 35  # For port 7002 (sine wave, different range)
        self.sine_center = 35  # Center point for sine wave
        self.sine_amplitude = 15  # How far it deviates from center
        self.sine_speed = 0.1  # How fast it oscillates
        self.sine_time = 0
        self.transition_active = False
        self.transition_thread = None
        self.transition_speed = config.TRANSITION_SPEED  # Use speed from config

    def prompt_handler(self, address, *args):
        """Handle incoming OSC messages for prompt changes"""
        if args and isinstance(args[0], dict):
            prompt_pair = args[0]
            
            if prompt_pair.get("show_temp", False):
                target_temp = prompt_pair.get("target_temp", 50)
                update_target_temperature(target_temp)
                # Display mode will be handled by the continuous temperature control
                self.processing_client.send_message("/display/mode", 1)
                # Send simple text to Parler (can be None or "This is a GPU")
                display_text = prompt_pair.get("display")
                if display_text:
                    self.parler_client.send_message("/prompt", display_text)
                return
            
            # Normal temperature control
            self.processing_client.send_message("/display/mode", 0)
            
            # Handle regular prompt pair
            generate_prompt = prompt_pair["generate"]
            display_prompt = prompt_pair["display"]
            
            # Extract step instruction from generate prompt
            for instruction in TD_INSTRUCTIONS.values():
                if instruction in generate_prompt:
                    step_instruction = int(instruction.split('=')[1])
                    generate_prompt = generate_prompt.replace(instruction, "").strip()
                    self.set_steps(step_instruction)
                    break
            
            # Send to Parler first
            self.parler_client.send_message("/prompt", display_prompt)
            
            # Send generation prompt to TouchDesigner
            self.touchdesigner_client.send_message("/prompt", generate_prompt)
            
            # Send display prompt to Processing
            self.processing_client.send_message("/prompt", display_prompt)

    def check_port_available(self, host, port):
        """Check if a port is available"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.bind((host, port))
                return True
        except OSError:
            return False
    
    def start_osc_server(self):
        """Start OSC server to listen for incoming messages"""
        try:
            # Check if port is available
            if not self.check_port_available(config.OSC_SERVER_IP, config.OSC_SERVER_PORT):
                print(f"Warning: Port {config.OSC_SERVER_PORT} is already in use.")
                print("Trying to find an available port...")
                
                # Try alternative ports
                for alt_port in range(config.OSC_SERVER_PORT + 1, config.OSC_SERVER_PORT + 10):
                    if self.check_port_available(config.OSC_SERVER_IP, alt_port):
                        print(f"Using alternative port: {alt_port}")
                        server_port = alt_port
                        break
                else:
                    print("No available ports found. Starting without OSC server...")
                    return
            else:
                server_port = config.OSC_SERVER_PORT
            
            dispatcher = Dispatcher()
            dispatcher.map("/changePrompt", self.prompt_handler)
            
            self.server = ThreadingOSCUDPServer(
                (config.OSC_SERVER_IP, server_port), 
                dispatcher
            )
            
            print(f"OSC server starting on {config.OSC_SERVER_IP}:{server_port}")
            # Start the server in a separate thread
            server_thread = threading.Thread(target=self.server.serve_forever)
            server_thread.daemon = True
            server_thread.start()
            
        except Exception as e:
            print(f"OSC server error: {e}")
            print("Continuing without OSC server...")

    def send_gpu_stats(self, stats):
        """Send GPU stats to Processing and TouchDesigner"""
        if stats is not None:
            # Send to Processing
            self.processing_client.send_message("/gpu/temperature", stats['temperature'])
            self.processing_client.send_message("/gpu/utilization", stats['utilization']) 
            self.processing_client.send_message("/gpu/memory_used", stats['memory_used'])
            self.processing_client.send_message("/gpu/memory_total", stats['memory_total'])
            self.processing_client.send_message("/gpu/power_draw", stats['power_draw'])
            self.processing_client.send_message("/gpu/power_target", stats['power_target']) 

    def set_display_mode(self, show_temperature):
        """Switch Processing display between temperature and camera
        show_temperature: True to show temperature, False to show camera"""
        self.processing_client.send_message("/display/mode", 1 if show_temperature else 0)

    def set_diffusion_mode(self, mode):
        """Control diffusion steps for different visual effects"""
        if mode == "ORIGINAL":
            self.td_steps_client1.send_message("/steps", 50)
            self.td_steps_client2.send_message("/steps", 50)
        elif mode == "CREATIVE":
            self.td_steps_client1.send_message("/steps", 0)
            self.td_steps_client2.send_message("/steps", 0)
        elif mode == "BALANCED":
            self.td_steps_client1.send_message("/steps", 25)
            self.td_steps_client2.send_message("/steps", 25)

    def transition_steps(self):
        """Smoothly transition between step values"""
        self.transition_active = True
        current_int = int(self.current_steps_main)
        target_int = int(self.target_steps_main)

        while current_int != target_int:
            if current_int < target_int:
                current_int += 1
            else:
                current_int -= 1
            
            # Use config ports and send to both TD clients
            self.td_steps_client1.send_message("/steps", current_int)
            self.td_steps_client2.send_message("/steps", current_int)
            time.sleep(config.TRANSITION_DELAY)  # Use config delay
        
        # Final value
        self.current_steps_main = self.target_steps_main
        self.td_steps_client1.send_message("/steps", int(self.target_steps_main))
        self.td_steps_client2.send_message("/steps", int(self.target_steps_main))
        self.transition_active = False

    def set_steps(self, step_instruction):
        """Start transition to new step value"""
        self.target_steps_main = step_instruction
        if not self.transition_active:
            self.transition_thread = threading.Thread(target=self.transition_steps)
            self.transition_thread.daemon = True
            self.transition_thread.start()
    
    def cleanup(self):
        """Clean up OSC clients and threads"""
        try:
            # Stop any active transitions
            self.transition_active = False
            
            # Wait for transition thread to finish if it's running
            if self.transition_thread and self.transition_thread.is_alive():
                self.transition_thread.join(timeout=1.0)
            
            # Close all UDP clients
            if hasattr(self, 'processing_client'):
                self.processing_client._sock.close()
            if hasattr(self, 'touchdesigner_client'):
                self.touchdesigner_client._sock.close()
            if hasattr(self, 'td_steps_client1'):
                self.td_steps_client1._sock.close()
            if hasattr(self, 'td_steps_client2'):
                self.td_steps_client2._sock.close()
            if hasattr(self, 'parler_client'):
                self.parler_client._sock.close()
            
            print("OSC clients closed successfully")
        except Exception as e:
            print(f"Warning: Error during OSC cleanup: {e}") 