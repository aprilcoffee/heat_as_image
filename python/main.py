import time
import random
import threading
import subprocess
from network_utils import get_network_info
from gpu_utils import get_gpu_stats
from osc_handler import OSCHandler
import config

def main():
    get_network_info()
    
    osc_handler = OSCHandler()
    
    # Start OSC server in a separate thread
    server_thread = threading.Thread(target=osc_handler.start_osc_server)
    server_thread.daemon = True
    server_thread.start()
    
    prompt_interval = 0
    try:
        while True:
            # Get GPU stats and send via OSC
            stats = get_gpu_stats()
            osc_handler.send_gpu_stats(stats)
            
            # Send random prompts every 5 seconds
            prompt_interval += 1
            if prompt_interval >= 10:  # 50 * 0.1s = 5 seconds
                prompt = random.choice(config.image_prompts)
                osc_handler.processing_client.send_message("/prompt", prompt)
                osc_handler.touchdesigner_client.send_message("/prompt", prompt)
                prompt_interval = 0
                    
            time.sleep(0.1)  # Small delay to prevent excessive CPU usage
    except KeyboardInterrupt:
        subprocess.run(['nvidia-smi', '-pl', str(config.init_power_Consumption)])
        return

if __name__ == "__main__":
    main() 