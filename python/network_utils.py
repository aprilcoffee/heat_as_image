import socket
import subprocess
import sys

def get_network_info():
    """Get and print IP address and WiFi network information"""
    # Get IP address
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        ip_address = s.getsockname()[0]
    except Exception:
        ip_address = '127.0.0.1'
    finally:
        s.close()

    # Get WiFi network name (SSID)
    wifi_name = "Not Found"
    try:
        if sys.platform == "darwin":  # macOS
            cmd = "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -I"
            output = subprocess.check_output(cmd.split()).decode('utf-8')
            for line in output.split('\n'):
                if ' SSID:' in line:
                    wifi_name = line.split(': ')[1].strip()
        elif sys.platform == "win32":  # Windows
            cmd = "netsh wlan show interfaces"
            output = subprocess.check_output(cmd.split()).decode('utf-8')
            for line in output.split('\n'):
                if 'SSID' in line and 'BSSID' not in line:
                    wifi_name = line.split(':')[1].strip()
        else:  # Linux
            cmd = "iwgetid -r"
            wifi_name = subprocess.check_output(cmd.split()).decode('utf-8').strip()
    except:
        pass

    print(f"\nNetwork Information:")
    print(f"IP Address: {ip_address}")
    print(f"WiFi Network: {wifi_name}\n") 