import time
import threading
import subprocess
from network_utils import get_network_info
from gpu_utils import get_gpu_stats, run_temperature_control, update_target_temperature
from osc_handler import OSCHandler
import config
from prompts import get_next_prompt_pair
import sys

def main():
    get_network_info()
    
    # Initialize OSC handler
    osc_handler = OSCHandler()
    
    # Start OSC server in a separate thread
    server_thread = threading.Thread(target=osc_handler.start_osc_server)
    server_thread.daemon = True
    server_thread.start()
    
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
    
    # Stop OSC server
    try:
        if hasattr(osc_handler, 'server'):
            osc_handler.server.shutdown()
    except Exception as e:
        print(f"Warning: Could not shutdown OSC server: {e}")
    
    sys.exit(0)  # Make sure to exit cleanly

if __name__ == "__main__":
    main() 