import subprocess
import time
import re
import random
from pythonosc import udp_client
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer
import threading
import socket
import netifaces
import sys
from config import power_Consumption, center

# Default values
init_power_Consumption = 450
power_Consumption = init_power_Consumption
target_temperature = 50  # Default target temperature

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
        
        return {
            'temperature': float(stats[0]),
            'utilization': float(stats[1]),
            'memory_used': float(stats[2]),
            'memory_total': float(stats[3]),
            'power_draw': float(stats[4]),
            'power_target': float(power_Consumption)
        }
    except:
        return None

def control_temperature(target_temp=50):
    """Control GPU temperature to reach target temperature"""
    try:
        stats = get_gpu_stats()
        if stats is None:
            return
        
        global power_Consumption
        current_temp = stats['temperature']
        
        if target_temp is not None:
            # Adjust power to reach target temperature
            if current_temp < target_temp:
                power_Consumption = min(500, power_Consumption + 5)
            elif current_temp > target_temp:
                power_Consumption = max(150, power_Consumption - 5)
        else:
            # Normal temperature control around center
            if current_temp > center:
                power_Consumption = max(150, power_Consumption - 5)
            else:
                power_Consumption = min(500, power_Consumption + 5)

        subprocess.run(['nvidia-smi', '-pl', str(power_Consumption)], capture_output=True)
        return stats
        
    except:
        return None

def update_target_temperature(new_target):
    """Update the target temperature for the control loop"""
    global target_temperature
    target_temperature = new_target

def run_temperature_control():
    """Run one iteration of temperature control"""
    return control_temperature(target_temp=target_temperature) 