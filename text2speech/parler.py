import torch
from parler_tts import ParlerTTSForConditionalGeneration
from transformers import AutoTokenizer
import sounddevice as sd
import time
from pythonosc import udp_client
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer
import threading
import gc

# Network configuration
PARLER_IP = "127.0.0.1"
PARLER_PORT = 9000
PARLER_RESPONSE_PORT = 9001

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
        self.response_client = udp_client.SimpleUDPClient("127.0.0.1", PARLER_RESPONSE_PORT)
        # Add audio thread tracking
        self.current_audio_thread = None

    def play_audio(self, audio_arr):
        try:
            sd.play(audio_arr, self.model.config.sampling_rate)
            sd.wait()
            print("Audio played successfully!")
        except Exception as e:
            print(f"Audio playback error: {e}")
            # Try to reset sound device
            try:
                sd.stop()
            except:
                pass
        finally:
            gc.collect()  # Force garbage collection

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
                
                # Send completion message BEFORE playing audio
                self.response_client.send_message("/audio_complete", text)
                
                print("Playing audio...")
                def play_audio():
                    sd.play(audio_arr, self.model.config.sampling_rate)
                    sd.wait()
                    print("Audio played successfully!")
                
                audio_thread = threading.Thread(target=play_audio)
                audio_thread.start()
                
            except Exception as e:
                print(f"Error occurred: {e}")
                # Try to reset sound device on error
                try:
                    sd.stop()
                except:
                    pass

    def start_osc_server(self):
        """Start OSC server to listen for incoming messages"""
        try:
            dispatcher = Dispatcher()
            dispatcher.map("/prompt", self.prompt_handler)
            
            server = BlockingOSCUDPServer(
                (PARLER_IP, PARLER_PORT), 
                dispatcher
            )
            print(f"Parler TTS listening on {PARLER_IP}:{PARLER_PORT}")
            server.serve_forever()
        except Exception as e:
            print(f"Server error: {e}")

def main():
    parler = ParlerHandler()
    parler.start_osc_server()

if __name__ == "__main__":
    main()