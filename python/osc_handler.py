from pythonosc import udp_client
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer
import config

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

    def prompt_handler(self, address, *args):
        """Handle incoming OSC messages for prompt changes"""
        if args and isinstance(args[0], str):
            # Replace all prompts with the new one
            config.image_prompts = [args[0]]
            print(f"Replaced prompts with new prompt: {args[0]}")
            
            # Immediately send new prompt to Processing and TouchDesigner
            self.processing_client.send_message("/prompt", args[0])
            self.touchdesigner_client.send_message("/prompt", args[0])
            self.parler_client.send_message("/prompt", args[0])
            
    def start_osc_server(self):
        """Start OSC server to listen for incoming messages"""
        dispatcher = Dispatcher()
        dispatcher.map("/changePrompt", self.prompt_handler)
        
        server = BlockingOSCUDPServer(
            (config.OSC_SERVER_IP, config.OSC_SERVER_PORT), 
            dispatcher
        )
        print(f"OSC Server listening on port {config.OSC_SERVER_PORT}")
        server.serve_forever()

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