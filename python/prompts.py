# TouchDesigner step control instructions
TD_INSTRUCTIONS = {
    "ORIGINAL": "::steps=50",     # Full original image
    "CREATIVE": "::steps=0",      # Maximum diffusion
    "BALANCED": "::steps=25",     # Mix of original and creative
    "SLIGHT_DIFF": "::steps=40",  # Mostly original with slight diffusion
    "HEAVY_DIFF": "::steps=10"    # Mostly diffused with slight original
}

# Detailed narrative prompts that tell the thesis story chronologically
PROMPT_PAIRS = [
    # Opening sequence
    # First temperature check
    {
        "generate": None,
        "display": "GPU_TEMP_MONITOR",
        "show_temp": True,
        "target_temp": 75
    },
    {
        "generate": f"A Grphaical Processing Unit {TD_INSTRUCTIONS['ORIGINAL']}",
        "display": "This is a GPU",
        "show_temp": False
    },
    {
        "generate": f"A GPU {TD_INSTRUCTIONS['BALANCED']}",
        "display": "This is also a GPU",
        "show_temp": False
    },
    {
        "generate": f"A computer screen displays Python code: 'from diffusers import DiffusionPipeline, import torch, model = stable-diffusion-v1-5' with execution errors visible {TD_INSTRUCTIONS['SLIGHT_DIFF']}",
        "display": "Initializing diffusion pipeline dependencies",
        "show_temp": False
    },
    {
        "generate": f"Multiple windows open on a desktop showing AI-generated landscapes being processed through additional filters in Processing software {TD_INSTRUCTIONS['HEAVY_DIFF']}",
        "display": "Processing: post-generation image analysis",
        "show_temp": False
    },
    {
        "generate": f"A student tries to run Stable Diffusion on an outdated laptop, receiving error messages about insufficient VRAM and CUDA compatibility {TD_INSTRUCTIONS['BALANCED']}",
        "display": "CUDA ERROR: insufficient VRAM detected",
        "show_temp": False
    },
    {
        "generate": f"Computer screen showing progressive iterations of an image feedback loop, with purple noise patterns becoming increasingly dominant {TD_INSTRUCTIONS['CREATIVE']}",
        "display": "Feedback loop iteration: pattern analysis",
        "show_temp": False
    },
    {
        "generate": f"Researchers examine Hugging Face documentation and code diagrams of the Stable Diffusion pipeline components {TD_INSTRUCTIONS['BALANCED']}",
        "display": "System architecture analysis: pipeline components",
        "show_temp": False
    },
    {
        "generate": f"Testing interface showing CLIP model scoring different faces: 87% match between Asian face and 'dumpling', 92% match between white face and 'schnitzel' {TD_INSTRUCTIONS['CREATIVE']}",
        "display": "CLIP model: semantic analysis report",
        "show_temp": False
    },
    {
        "generate": f"Visualization of word embeddings and image features as points in a high-dimensional space, with similar concepts clustering together {TD_INSTRUCTIONS['CREATIVE']}",
        "display": "Vector space mapping: semantic clusters",
        "show_temp": False
    },
    {
        "generate": f"Diagram of U-Net architecture showing an image being compressed to 32x32 pixels then reconstructed with preserved details {TD_INSTRUCTIONS['SLIGHT_DIFF']}",
        "display": "U-Net compression ratio: 32x32",
        "show_temp": False
    },
    {
        "generate": f"Animation showing pure random noise gradually transforming into a recognizable image through multiple denoising steps {TD_INSTRUCTIONS['HEAVY_DIFF']}",
        "display": "Denoising diffusion process: step n of 1000",
        "show_temp": False
    },
    {
        "generate": None,
        "display": "GPU_TEMP_MONITOR",
        "show_temp": True,
        "target_temp": 60
    },
    {
        "generate": f"A Grphaical Processing Unit {TD_INSTRUCTIONS['ORIGINAL']}",
        "display": "This is a GPU",
        "show_temp": False
    },
    {
        "generate": f"A GPU {TD_INSTRUCTIONS['BALANCED']}",
        "display": "This is also a GPU",
        "show_temp": False
    },
    {
        "generate": f"Close-up of GPU fans spinning rapidly as temperature readout shows 85°C during image generation tasks {TD_INSTRUCTIONS['BALANCED']}",
        "display": "GPU thermal analysis in progress",
        "show_temp": False
    },
    {
        "generate": f"Mining operation in Spruce Pine, North Carolina extracting high-purity quartz with 99.9999999% purity levels {TD_INSTRUCTIONS['CREATIVE']}",
        "display": "Silicon source: 99.9999999% pure SiO2",
        "show_temp": False
    },
    {
        "generate": f"Industrial facilities in Japan where silicon is formed into perfect ingots and sliced into wafers {TD_INSTRUCTIONS['BALANCED']}",
        "display": "Wafer fabrication process initialized",
        "show_temp": False
    },
    {
        "generate": f"Workers in white clean-room suits with full face coverage handling silicon wafers with specialized tools under yellow light {TD_INSTRUCTIONS['CREATIVE']}",
        "display": "Clean room protocol: class 10 environment",
        "show_temp": False
    },
     {
        "generate": None,
        "display": "GPU_TEMP_MONITOR",
        "show_temp": True,
        "target_temp": 50
    },
    {
        "generate": f"Massive ASML EUV lithography machine with complex optics shooting 13.5nm wavelength light to print circuits {TD_INSTRUCTIONS['BALANCED']}",
        "display": "EUV lithography: λ=13.5nm",
        "show_temp": False
    },
    {
        "generate": f"Aerial view of TSMC's massive fabrication plants in Hsinchu Science Park, Taiwan {TD_INSTRUCTIONS['HEAVY_DIFF']}",
        "display": "Semiconductor fab: 5nm process node",
        "show_temp": False
    },
    {
        "generate": f"Water trucks delivering supplies to TSMC during Taiwan's 2021 drought while surrounding farmland appears dry {TD_INSTRUCTIONS['ORIGINAL']}",
        "display": "Resource allocation: H2O priority override",
        "show_temp": False
    },
    {
        "generate": None,
        "display": "GPU_TEMP_MONITOR",
        "show_temp": True,
        "target_temp": 50
    },
    {
        "generate": f"Map showing Taiwan's strategic position with overlay of semiconductor supply routes and military tensions {TD_INSTRUCTIONS['BALANCED']}",
        "display": "Supply chain topology analysis",
        "show_temp": False
    },
    {
        "generate": f"NVIDIA CEO Jensen Huang meeting with TSMC founder Morris Chang, sharing tofu pudding as a symbolic gesture {TD_INSTRUCTIONS['SLIGHT_DIFF']}",
        "display": "Strategic partnership: GPU-FAB integration",
        "show_temp": False
    }, 
    {
        "generate": None,
        "display": "GPU_TEMP_MONITOR",
        "show_temp": True,
        "target_temp": 40
    },
    {
        "generate": f"Social media feed showing multiple AI-generated images in Studio Ghibli style based on personal photos {TD_INSTRUCTIONS['CREATIVE']}",
        "display": "Style transfer algorithm: analyzing results",
        "show_temp": False
    },
    {
        "generate": f"Exhibition showing artworks by Sam Ghantous and Nadim Abbas addressing semiconductor production through installations {TD_INSTRUCTIONS['BALANCED']}",
        "display": "Hardware visualization protocol",
        "show_temp": False
    },
    {
        "generate": f"A Taiwanese artist standing between silicon wafers and screens, touching both physical and digital elements of AI {TD_INSTRUCTIONS['HEAVY_DIFF']}",
        "display": "Interface: human-silicon interaction",
        "show_temp": False
    },
    {
        "generate": f"Laptop with fan running, generating subtle heat waves while displaying both code and images on screen {TD_INSTRUCTIONS['CREATIVE']}",
        "display": "Thermal output monitoring system",
        "show_temp": False
    },
    {
        "generate": None,
        "display": "GPU_TEMP_MONITOR",
        "show_temp": True,
        "target_temp": 50
    },
    {
        "generate": f"A GPU {TD_INSTRUCTIONS['BALANCED']}",
        "display": "This is also a GPU",
        "show_temp": False
    },
    {
        "generate": f"A GPU {TD_INSTRUCTIONS['CREATIVE']}",
        "display": "This is also a GPU",
        "show_temp": False
    }
]

# Current prompt index tracker
current_prompt_index = 0

def get_next_prompt_pair():
    """Returns the next prompt pair in sequence"""
    global current_prompt_index
    prompt_pair = PROMPT_PAIRS[current_prompt_index]
    current_prompt_index = (current_prompt_index + 1) % len(PROMPT_PAIRS)
    return prompt_pair

# Time periods for different modes (in seconds)
DIFFUSION_PERIODS = {
    "FAST_CREATIVE": 5,     # Quick creative variations
    "SLOW_ORIGINAL": 15,    # Longer periods of original image
    "MIXED": 10,           # Balanced timing
    "TRANSITION": 0.05     # Smooth transition timing between steps
} 