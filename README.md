# Heat as Image

Real-time GPU temperature visualization system using TouchDesigner's Stream Diffusion, Processing, and AI voice synthesis.

## Requirements
- NVIDIA GPU (RTX series recommended)
- Windows 10/11
- Python 3.8+
- TouchDesigner 2023+
- Processing 4
- CUDA Toolkit 12.1
- [Stream Diffusion for TouchDesigner](https://derivative.ca/community-post/asset/stream-diffusion-touchdesigner) - Real-time image generation in TouchDesigner

## Installation

### Python Setup
```bash
python -m venv venv
.\venv\Scripts\activate

pip install python-osc
pip install sounddevice
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
pip install parler-tts
pip install transformers
```

### TouchDesigner Setup
1. Install TouchDesigner
2. Install Stream Diffusion:
   - Follow installation guide at [StreamDiffusion](https://github.com/cumulo-autumn/StreamDiffusion)
   - Download model files
   - Configure CUDA paths
3. Open project file (.toe)

### Processing Setup
1. Install Processing
2. Install oscP5 library via Tools → Add Tool
3. Open project file (.pde)

## Configuration
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

## Usage
1. Start TouchDesigner project
2. Run Processing sketch
3. Start Parler:
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
- Real-time GPU monitoring
- Dynamic text-to-speech
- Dual-layer diffusion control:
  - Main steps (port 7001): Direct control of diffusion strength
  - Sine wave variation (port 7002): Continuous subtle changes
- Automatic prompt generation
- Temperature/camera mode switching

## Project Structure 

## Acknowledgments
- [Stream Diffusion for TouchDesigner](https://derivative.ca/community-post/asset/stream-diffusion-touchdesigner) for real-time image generation
- [Parler TTS](https://github.com/parler-tts/parler-tts) for voice synthesis
- TouchDesigner and Processing communities 