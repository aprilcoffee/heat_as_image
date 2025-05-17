import time
import random
import threading
import subprocess
from network_utils import get_network_info
from gpu_utils import get_gpu_stats
from osc_handler import OSCHandler
import config
from prompts import image_prompts

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
            
            # Send random prompts every 10 seconds
            prompt_interval += 1
            if prompt_interval >= 100:  # 100 * 0.1s = 10 seconds
                prompt = random.choice(image_prompts)
                osc_handler.prompt_handler("/prompt", prompt)
                prompt_interval = 0
                    
            time.sleep(0.1)  # Small delay to prevent excessive CPU usage
    except KeyboardInterrupt:
        subprocess.run(['nvidia-smi', '-pl', str(config.init_power_Consumption)])
        return

if __name__ == "__main__":
    main() 