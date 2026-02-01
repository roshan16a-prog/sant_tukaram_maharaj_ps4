try:
    import pyaudio
    PYAUDIO_AVAILABLE = True
except ImportError:
    PYAUDIO_AVAILABLE = False
    print("Warning: PyAudio not found. Audio recording will be disabled.")

import wave
import threading
import time
import os
from src.config import Config

class AudioRecorder:
    def __init__(self):
        self.is_recording = False
        self.frames = []
        self.thread = None
        if PYAUDIO_AVAILABLE:
            self.audio = pyaudio.PyAudio()
            self.FORMAT = pyaudio.paInt16
        else:
            self.audio = None
            self.FORMAT = None # Mock
            
        self.stream = None
        
        # Audio Config
        self.CHANNELS = 1
        self.RATE = 44100
        self.CHUNK = 1024

    def start_recording(self):
        if self.is_recording:
            return
            
        if not PYAUDIO_AVAILABLE:
            print("Audio recording unavailable.")
            return

        self.is_recording = True
        self.frames = []
        
        try:
            self.stream = self.audio.open(format=self.FORMAT, channels=self.CHANNELS,
                            rate=self.RATE, input=True,
                            frames_per_buffer=self.CHUNK)
            
            self.thread = threading.Thread(target=self._record_loop)
            self.thread.start()
        except Exception as e:
            print(f"Error starting recording: {e}")
            self.is_recording = False

    def _record_loop(self):
        while self.is_recording and self.stream:
            try:
                data = self.stream.read(self.CHUNK)
                self.frames.append(data)
            except Exception as e:
                print(f"Error recording chunk: {e}")
                break

    def stop_recording(self, output_filename=None):
        if not self.is_recording:
            return None
            
        self.is_recording = False
        if self.thread:
            self.thread.join()
            
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
            
        return self._save_file(output_filename) if output_filename else None

    def _save_file(self, filename):
        full_path = os.path.join(Config.DATA_DIR, filename)
        
        wf = wave.open(full_path, 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(self.audio.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(self.frames))
        wf.close()
        
        return full_path

    def terminate(self):
        if self.audio:
            self.audio.terminate()
