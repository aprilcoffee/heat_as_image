from pythonosc import udp_client
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer
import config
import random
import threading

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
        self.parler_client = udp_client.SimpleUDPClient(
            config.PARLER_IP,
            config.PARLER_PORT
        )
        self.pending_prompt = None

    def prompt_handler(self, address, *args):
        """Handle incoming OSC messages for prompt changes"""
        if args and isinstance(args[0], str):
            if address == "/changePrompt":
                config.image_prompts = [args[0]]
                print(f"Replaced prompts with new prompt: {args[0]}")
                # Send only to Parler first
                self.pending_prompt = args[0]
                self.parler_client.send_message("/prompt", args[0])
            elif address == "/prompt":
                # For random prompts, follow same pattern
                self.pending_prompt = args[0]
                self.parler_client.send_message("/prompt", args[0])

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