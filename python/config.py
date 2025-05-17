# GPU Power Configuration
init_power_Consumption = 450
power_Consumption = init_power_Consumption
center = 50

# Network Configuration
PROCESSING_IP = "127.0.0.1"
PROCESSING_PORT = 12000

TOUCHDESIGNER_IP = "127.0.0.1"
TOUCHDESIGNER_PORT = 7000
TOUCHDESIGNER_STEPS_PORT1 = 7001
TOUCHDESIGNER_STEPS_PORT2 = 7002

PARLER_IP = "127.0.0.1"
PARLER_PORT = 9000
PARLER_RESPONSE_PORT = 9001

OSC_SERVER_IP = "127.0.0.1"
OSC_SERVER_PORT = 8000

# Animation Configuration
TRANSITION_SPEED = 1  # Steps per update
TRANSITION_DELAY = 0.05  # Seconds between updates
DEFAULT_STEPS = 25  # Default middle value for diffusion steps

# Remove any image_prompts as they're now in prompts.py 