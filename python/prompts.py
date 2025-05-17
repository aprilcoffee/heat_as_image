# TouchDesigner step control instructions
TD_INSTRUCTIONS = {
    "ORIGINAL": "::steps=50",     # Full original image
    "CREATIVE": "::steps=0",      # Maximum diffusion/creativity
    "BALANCED": "::steps=25",     # Mix of original and creative
    "SLIGHT_DIFF": "::steps=40",  # Mostly original with slight diffusion
    "HEAVY_DIFF": "::steps=10"    # Mostly diffused with slight original
}

# List of creative image prompts with explicit TD instructions
image_prompts = [
    # Original/Clear prompts
    f"Engineers in clean room suits inspect silicon wafers under bright LED arrays {TD_INSTRUCTIONS['ORIGINAL']}",
    f"Precision robotic arms carefully position semiconductor components {TD_INSTRUCTIONS['ORIGINAL']}",
    
    # Balanced/Mixed prompts
    f"Laser beams dance across silicon masks as GPU cores take shape {TD_INSTRUCTIONS['BALANCED']}",
    f"Clean room workers orchestrate the flow of wafers through machines {TD_INSTRUCTIONS['BALANCED']}",
    
    # Creative/Heavy diffusion prompts
    f"Quantum particles dance through transistor gates in cosmic patterns {TD_INSTRUCTIONS['CREATIVE']}",
    f"Digital dreams crystallize into silicon reality {TD_INSTRUCTIONS['CREATIVE']}",
    
    # Slight diffusion prompts
    f"TSMC engineers monitor advanced chip fabrication processes {TD_INSTRUCTIONS['SLIGHT_DIFF']}",
    f"Photolithography beams trace intricate patterns into semiconductor wafers {TD_INSTRUCTIONS['SLIGHT_DIFF']}",
    
    # Heavy diffusion prompts
    f"Silicon spirits weave digital spells in the clean room mist {TD_INSTRUCTIONS['HEAVY_DIFF']}",
    f"Nanoscale architects build crystal castles of computation {TD_INSTRUCTIONS['HEAVY_DIFF']}"
]

# Time periods for different modes (in seconds)
DIFFUSION_PERIODS = {
    "FAST_CREATIVE": 5,     # Quick creative variations
    "SLOW_ORIGINAL": 15,    # Longer periods of original image
    "MIXED": 10,           # Balanced timing
    "TRANSITION": 0.05     # Smooth transition timing between steps
} 