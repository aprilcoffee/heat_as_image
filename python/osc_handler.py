from pythonosc import udp_client
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer
import config
from prompts import TD_INSTRUCTIONS, PROMPT_PAIRS
import random
import threading
import time
import math
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

    def audio_complete_handler(self, address, *args):
        """Handle audio completion messages"""
        if args and isinstance(args[0], str):
            if self.current_steps_main == self.target_steps_main:  # Verify it's the same prompt
                print(f"Audio complete, sending to visual clients: {self.current_steps_main}")
                self.processing_client.send_message("/prompt", self.current_steps_main)
                self.touchdesigner_client.send_message("/prompt", self.current_steps_main)

    def start_osc_server(self):
        """Start OSC server to listen for incoming messages"""
        dispatcher = Dispatcher()
        dispatcher.map("/changePrompt", self.prompt_handler)
        
        # Create separate server for Parler responses
        parler_dispatcher = Dispatcher()
        parler_dispatcher.map("/audio_complete", self.audio_complete_handler)
        
        server = BlockingOSCUDPServer(
            (config.OSC_SERVER_IP, config.OSC_SERVER_PORT), 
            dispatcher
        )
        parler_server = BlockingOSCUDPServer(
            (config.OSC_SERVER_IP, config.PARLER_RESPONSE_PORT), 
            parler_dispatcher
        )
        
        # Start both servers in threads
        server_thread = threading.Thread(target=server.serve_forever)
        parler_thread = threading.Thread(target=parler_server.serve_forever)
        server_thread.daemon = True
        parler_thread.daemon = True
        server_thread.start()
        parler_thread.start()

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

        # Send steps as integers but keep transition smooth
        while current_int != target_int:
            if current_int < target_int:
                current_int += 1
            else:
                current_int -= 1
            
            # Send integer steps to TouchDesigner
            self.touchdesigner_client.send_message("/steps", current_int)
            time.sleep(0.05)  # Adjust timing for smooth integer transitions
        
        self.current_steps_main = self.target_steps_main
        self.transition_active = False

    def set_steps(self, step_instruction):
        """Start transition to new step value"""
        self.target_steps_main = step_instruction
        if not self.transition_active:
            self.transition_thread = threading.Thread(target=self.transition_steps)
            self.transition_thread.daemon = True
            self.transition_thread.start() 