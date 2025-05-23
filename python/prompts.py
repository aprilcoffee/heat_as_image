# TouchDesigner step control instructions
TD_INSTRUCTIONS = {
    "ORIGINAL": "::steps=50",     # Full original image
    "CREATIVE": "::steps=0",      # Maximum diffusion
    "BALANCED": "::steps=25",     # Mix of original and creative
    "SLIGHT_DIFF": "::steps=40",  # Mostly original with slight diffusion
    "HEAVY_DIFF": "::steps=10"    # Mostly diffused with slight original
}

# Initialize target temperature
TARGET_TEMPERATURE = 50

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
        "display": "Diffusion pipeline dependencies",
        "show_temp": False
    },
    {
        "generate": f"Multiple windows open on a desktop showing AI-generated landscapes being processed through additional filters in Processing software {TD_INSTRUCTIONS['HEAVY_DIFF']}",
        "display": "Post-generation image analysis",
        "show_temp": False
    },
    {
        "generate": f"A student tries to run Stable Diffusion on an outdated laptop, receiving error messages about insufficient VRAM and CUDA compatibility {TD_INSTRUCTIONS['BALANCED']}",
        "display": "Insufficient VRAM detected",
        "show_temp": False
    },
    {
        "generate": f"Computer screen showing progressive iterations of an image feedback loop, with purple noise patterns becoming increasingly dominant {TD_INSTRUCTIONS['CREATIVE']}",
        "display": "Pattern analysis",
        "show_temp": False
    },
    {
        "generate": f"Researchers examine Hugging Face documentation and code diagrams of the Stable Diffusion pipeline components {TD_INSTRUCTIONS['BALANCED']}",
        "display": "System architecture analysis",
        "show_temp": False
    },
    {
        "generate": f"Testing interface showing CLIP model scoring different faces: 87% match between Asian face and 'dumpling', 92% match between white face and 'schnitzel' {TD_INSTRUCTIONS['CREATIVE']}",
        "display": "Semantic analysis report",
        "show_temp": False
    },
    {
        "generate": f"Visualization of word embeddings and image features as points in a high-dimensional space, with similar concepts clustering together {TD_INSTRUCTIONS['CREATIVE']}",
        "display": "Vector space mapping",
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
        "display": "Clean room protocol",
        "show_temp": False
    },
    {
        "generate": f"Massive ASML EUV lithography machine with complex optics shooting 13.5nm wavelength light to print circuits {TD_INSTRUCTIONS['BALANCED']}",
        "display": "EUV lithography=13.5nm",
        "show_temp": False
    },
    {
        "generate": f"Aerial view of TSMC's massive fabrication plants in Hsinchu Science Park, Taiwan {TD_INSTRUCTIONS['HEAVY_DIFF']}",
        "display": "Semiconductor fab",
        "show_temp": False
    },
    {
        "generate": f"Water trucks delivering supplies to TSMC during Taiwan's 2021 drought while surrounding farmland appears dry {TD_INSTRUCTIONS['ORIGINAL']}",
        "display": "Resource allocation: H2O priority override",
        "show_temp": False
    },
    {
        "generate": f"A high-end GPU running at maximum capacity, fans spinning rapidly to dissipate heat {TD_INSTRUCTIONS['BALANCED']}",
        "display": "GPU thermal management active",
        "show_temp": False
    },
    {
        "generate": f"A GPU running at maximum capacity, fans spinning rapidly to dissipate heat {TD_INSTRUCTIONS['CREATIVE']}",
        "display": "thermal management active",
        "show_temp": False
    },
    {
        "generate": None,
        "display": "GPU_TEMP_MONITOR",
        "show_temp": True,
        "target_temp": 50
    },
    {
        "generate": f"A GPU {TD_INSTRUCTIONS['CREATIVE']}",
        "display": "This is also a GPU",
        "show_temp": False
    },
    {
        "generate": f"Map showing Taiwan's strategic position with overlay of semiconductor supply routes and military tensions {TD_INSTRUCTIONS['BALANCED']}",
        "display": "Supply chain topology analysis",
        "show_temp": False
    },
    {
        "generate": f"NVIDIA CEO Jensen Huang meeting with TSMC founder Morris Chang, sharing tofu pudding as a symbolic gesture {TD_INSTRUCTIONS['SLIGHT_DIFF']}",
        "display": "Strategic partnership",
        "show_temp": False
    }, 
    {
        "generate": f"Industrial furnaces at The Quartz Corp and Covia Corp facilities purify silicon to 99.9999999% purity levels through multiple refinement processes {TD_INSTRUCTIONS['HEAVY_DIFF']}",
        "display": "The purest material on Earth",
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
        "display": "Style transfer algorithm",
        "show_temp": False
    },
    {
        "generate": f"Exhibition showing artworks addressing semiconductor production through installations {TD_INSTRUCTIONS['BALANCED']}",
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
        "generate": f"A computer GPU {TD_INSTRUCTIONS['HEAVY_DIFF']}",
        "display": "This is also a GPU",
        "show_temp": False
    },
    {
        "generate": f"Automated polishing machines smooth silicon wafers to atomic-level flatness in ultra-clean manufacturing environments {TD_INSTRUCTIONS['SLIGHT_DIFF']}",
        "display": "Polishing wafers to mirror-perfect surfaces",
        "show_temp": False
    },
    {
        "generate": f"NVIDIA engineers in Santa Clara designing GPU architecture layouts on computer screens, creating the blueprint for RTX 4090 chips {TD_INSTRUCTIONS['CREATIVE']}",
        "display": "NVIDIA designs the GPU architecture but doesn't manufacture",
        "show_temp": False
    },
    {
        "generate": f"Chemical etching and deposition processes adding multiple layers to create three-dimensional transistor structures {TD_INSTRUCTIONS['CREATIVE']}",
        "display": "Building 3D transistor structures through hundreds of process steps",
        "show_temp": False
    },
    {
        "generate": f"Automated testing equipment checking each GPU die for functionality before packaging {TD_INSTRUCTIONS['HEAVY_DIFF']}",
        "display": "Testing billions of transistors for defects",
        "show_temp": False
    },
    {
        "generate": f"GPU dies being cut from wafers and sorted - functional chips separated from defective ones {TD_INSTRUCTIONS['SLIGHT_DIFF']}",
        "display": "Yield sorting determines which chips pass quality control",
        "show_temp": False
    },
    {
        "generate": f"Completed GPU chips being shipped from Taiwan to graphics card manufacturers worldwide {TD_INSTRUCTIONS['HEAVY_DIFF']}",
        "display": "Global distribution of finished semiconductors",
        "show_temp": False
    },
    {
        "generate": f"ASUS, MSI, and EVGA facilities installing GPU chips onto circuit boards with power connectors and cooling systems {TD_INSTRUCTIONS['BALANCED']}",
        "display": "Graphics card manufacturers add cooling and power systems",
        "show_temp": False
    },
    {
        "generate": None,
        "display": "GPU_TEMP_MONITOR",
        "show_temp": True,
        "target_temp": 60
    },
    {
        "generate": f"A GPU {TD_INSTRUCTIONS['BALANCED']}",
        "display": "This is also a GPU",
        "show_temp": False
    },
    {
        "generate": f"A computer GPU {TD_INSTRUCTIONS['SLIGHT_DIFF']}",
        "display": "This is also a GPU",
        "show_temp": False
    },
    {
        "generate": f"Shipping containers loaded with thousands of graphics cards departing Asian ports for global distribution {TD_INSTRUCTIONS['HEAVY_DIFF']}",
        "display": "Global supply chain delivers GPUs to end users",
        "show_temp": False
    },
    {
        "generate": f"Consumer unboxing an RTX 4090 graphics card and installing it into a PC for AI image generation work {TD_INSTRUCTIONS['BALANCED']}",
        "display": "From Spruce Pine sand to AI artist's workstation",
        "show_temp": False
    },
    {
        "generate": f"The installed RTX 4090 running Stable Diffusion code, generating heat as it processes the same seven lines of code from the thesis beginning {TD_INSTRUCTIONS['BALANCED']}",
        "display": "The circle completes: Sand becomes heat through computation",
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