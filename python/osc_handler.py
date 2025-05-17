from pythonosc import udp_client
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer
import config
from prompts import TD_INSTRUCTIONS, image_prompts
import random
import threading
import time
import math

class OSCHandler:
    def __init__(self):
        self.processing_client = udp_client.SimpleUDPClient(
            config.PROCESSING_IP, 
            config.PROCESSING_PORT
        )
        self.touchdesigner_client = udp_client.SimpleUDPClient(
            config.TOUCHDESIGNER_IP, 
            config.TOUCHDESIGNER_PORT  # 7000 for main
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
        self.pending_prompt = None
        self.current_steps_main = 25  # For port 7001 (main)
        self.target_steps_main = 25
        self.current_steps_sine = 35  # For port 7002 (sine wave, different range)
        self.sine_center = 35  # Center point for sine wave
        self.sine_amplitude = 15  # How far it deviates from center
        self.sine_speed = 0.1  # How fast it oscillates
        self.sine_time = 0
        self.transition_active = False
        self.transition_thread = None
        self.transition_speed = 1

    def transition_steps(self):
        """Smoothly transition between current and target steps"""
        while self.transition_active:
            # Handle main steps (port 7001)
            if self.current_steps_main != self.target_steps_main:
                if self.current_steps_main < self.target_steps_main:
                    self.current_steps_main = min(self.current_steps_main + self.transition_speed, self.target_steps_main)
                else:
                    self.current_steps_main = max(self.current_steps_main - self.transition_speed, self.target_steps_main)
                
                self.td_steps_client1.send_message("/steps", self.current_steps_main)
            
            # Handle sine wave steps (port 7002)
            self.sine_time += self.sine_speed
            sine_value = self.sine_center + self.sine_amplitude * math.sin(self.sine_time)
            self.td_steps_client2.send_message("/steps", sine_value)
            
            time.sleep(0.05)
            
            if self.current_steps_main == self.target_steps_main:
                self.transition_active = False

    def prompt_handler(self, address, *args):
        if args and isinstance(args[0], str):
            prompt = args[0]
            step_instruction = None
            
            # Check for special instructions
            for instruction in TD_INSTRUCTIONS.values():
                if instruction in prompt:
                    step_instruction = int(instruction.split('=')[1])
                    prompt = prompt.replace(instruction, "")  # Remove instruction
                    break
            
            # First send to Parler and wait for audio to start
            self.parler_client.send_message("/prompt", prompt)
            
            # When we receive audio completion signal, then:
            # 1. Start the step transition
            if step_instruction is not None:
                self.target_steps_main = step_instruction
                
                # Stop existing transition if running
                if self.transition_active:
                    self.transition_active = False
                    if self.transition_thread:
                        self.transition_thread.join()
                
                # Start new transition
                self.transition_active = True
                self.transition_thread = threading.Thread(target=self.transition_steps)
                self.transition_thread.daemon = True
                self.transition_thread.start()
            
            # 2. Send to Processing and TouchDesigner
            self.processing_client.send_message("/prompt", prompt)
            self.touchdesigner_client.send_message("/prompt", prompt)

    def audio_complete_handler(self, address, *args):
        """Handle audio completion messages"""
        if args and isinstance(args[0], str):
            if self.pending_prompt == args[0]:  # Verify it's the same prompt
                print(f"Audio complete, sending to visual clients: {args[0]}")
                self.processing_client.send_message("/prompt", args[0])
                self.touchdesigner_client.send_message("/prompt", args[0])
                self.pending_prompt = None

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