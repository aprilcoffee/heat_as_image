import torch
from parler_tts import ParlerTTSForConditionalGeneration
from transformers import AutoTokenizer
import sounddevice as sd
import time
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer
import threading

# Network configuration
PARLER_IP = "127.0.0.1"
PARLER_PORT = 9000

def load_model():
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    model = ParlerTTSForConditionalGeneration.from_pretrained("parler-tts/parler-tts-mini-v1").to(device)
    tokenizer = AutoTokenizer.from_pretrained("parler-tts/parler-tts-mini-v1")
    return model, tokenizer, device

class ParlerHandler:
    def __init__(self):
        self.model, self.tokenizer, self.device = load_model()
        self.description = "Cate Blanchett, speaking in a slow and emotional way"
        self.input_ids = self.tokenizer(self.description, return_tensors="pt").input_ids.to(self.device)

    def prompt_handler(self, address, *args):
        """Handle incoming OSC messages for text-to-speech"""
        print(f"Received message on {address}: {args}")
        if args and isinstance(args[0], str):
            text = args[0]
            try:
                print(f"Generating audio for: {text}")
                start_time = time.time()
                
                prompt_input_ids = self.tokenizer(text+"    ", return_tensors="pt").input_ids.to(self.device)
                generation = self.model.generate(input_ids=self.input_ids, prompt_input_ids=prompt_input_ids)
                audio_arr = generation.cpu().numpy().squeeze()
                
                generation_time = time.time() - start_time
                print(f"Audio generated in {generation_time:.2f} seconds")
                
                print("Playing audio...")
                # Play audio in a separate thread to not block OSC server
                def play_audio():
                    sd.play(audio_arr, self.model.config.sampling_rate)
                    sd.wait()
                    print("Audio played successfully!")
                
                audio_thread = threading.Thread(target=play_audio)
                audio_thread.start()
                
            except Exception as e:
                print(f"Error occurred: {e}")

    def start_osc_server(self):
        """Start OSC server to listen for incoming messages"""
        dispatcher = Dispatcher()
        dispatcher.map("/prompt", self.prompt_handler)
        
        server = BlockingOSCUDPServer(
            (PARLER_IP, PARLER_PORT), 
            dispatcher
        )
        print(f"Parler TTS listening on {PARLER_IP}:{PARLER_PORT}")
        server.serve_forever()

def main():
    parler = ParlerHandler()
    parler.start_osc_server()

if __name__ == "__main__":
    main()