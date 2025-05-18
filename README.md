# Heat as Image

A real-time generative image processing system that transforms GPU temperature into visual art through Stream Diffusion, Processing, and AI voice synthesis.

## Requirements
### Hardware
- NVIDIA GPU (RTX series recommended)
- Proper power supply and cooling
- Audio output device

### Software
- Windows 10/11
- NVIDIA CUDA Toolkit 12.1
- TouchDesigner 2023+
- Processing 4
- Python 3.8+
- NDI Tools

## Detailed Installation

### 1. GPU and CUDA Setup
1. Install NVIDIA GPU drivers
2. Install CUDA Toolkit 12.1
3. Verify installation:
```bash
nvcc --version
nvidia-smi
```

### 2. Python Environment
```bash
python -m venv venv
.\venv\Scripts\activate

# Core dependencies
pip install python-osc
pip install sounddevice
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
pip install streamdiffusion

# Voice synthesis
pip install parler-tts
pip install transformers
```

### 3. TouchDesigner Setup
1. Install TouchDesigner
2. Install [Stream Diffusion for TouchDesigner](https://derivative.ca/community-post/asset/stream-diffusion-touchdesigner)
3. Configure Stream Diffusion:
   - Set up model paths
   - Configure CUDA settings
   - Test standalone operation
4. Open project file (.toe)

### 4. Processing Setup
1. Install Processing
2. Add Libraries:
   - Tools → Add Tool → Libraries
   - Install "oscP5"
   - Install "NDI" for video streaming
3. Open project file (.pde)

### 5. NDI Setup
1. Install NDI Tools
2. Configure NDI inputs/outputs in TouchDesigner
3. Verify NDI stream reception in Processing

## Network Configuration
Edit `config.py` for network settings:
```python
PROCESSING_PORT = 12000
TOUCHDESIGNER_PORT = 7000
TOUCHDESIGNER_STEPS_PORT1 = 7001  # Main diffusion
TOUCHDESIGNER_STEPS_PORT2 = 7002  # Sine wave variation
PARLER_PORT = 9000
PARLER_RESPONSE_PORT = 9001
OSC_SERVER_PORT = 8000
```

## System Architecture
1. GPU Temperature Monitoring → OSC Communication
2. Stream Diffusion Processing in TouchDesigner
3. NDI Video Stream Pipeline
4. Processing Visualization
5. Voice Synthesis Feedback

## Usage
1. Start TouchDesigner project
2. Launch Processing sketch
3. Start Parler service:
```bash
cd text2speech
python parler.py
```
4. Run main program:
```bash
cd python
python main.py
```

## Features
- Real-time GPU temperature monitoring
- Dual-layer diffusion control:
  - Main steps (port 7001): Direct temperature influence
  - Sine wave variation (port 7002): Continuous subtle changes
- Dynamic text-to-speech generation
- NDI video streaming
- Temperature/camera mode switching

## Project Structure
```
heat_as_image/
├── python/
│   ├── config.py          # Configuration settings
│   ├── prompts.py         # Prompt lists and instructions
│   ├── main.py           # Main program
│   ├── osc_handler.py    # OSC communication
│   ├── gpu_utils.py      # GPU monitoring
│   └── network_utils.py  # Network utilities
├── text2speech/
│   └── parler.py         # Text-to-speech handler
└── processing/
    └── processing.pde    # Processing visualization
```

## License
MIT License

Copyright (c) 2024 aprilcoffee

[Standard MIT License text...]

## Authors
[aprilcoffee](https://github.com/aprilcoffee)

## Acknowledgments
- [Stream Diffusion for TouchDesigner](https://derivative.ca/community-post/asset/stream-diffusion-touchdesigner)
- [Parler TTS](https://github.com/parler-tts/parler-tts)
- TouchDesigner and Processing communities
- U-Net architecture and its applications in real-time image processing