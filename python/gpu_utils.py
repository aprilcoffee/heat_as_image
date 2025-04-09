import subprocess
from config import power_Consumption, center

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

        #subprocess.run(['nvidia-smi', '-pl', str(power_Consumption)], capture_output=True)
        
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