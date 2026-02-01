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
    def __init__(self):
        self.is_recording = False
        self.frames = []
        self.thread = None
        self.start_time = 0
        
        if PYAUDIO_AVAILABLE:
            self.audio = pyaudio.PyAudio()
            self.FORMAT = pyaudio.paInt16
            self.CHANNELS = 1
            self.RATE = 44100
            self.CHUNK = 1024
            self.use_mock = False
        else:
            self.audio = None
            self.FORMAT = 8 # Mock width
            self.CHANNELS = 1
            self.RATE = 44100
            self.CHUNK = 1024
            self.use_mock = True
            
        self.stream = None

    def start_recording(self):
        if self.is_recording:
            return
            
        self.is_recording = True
        self.frames = []
        self.start_time = time.time()
        
        if self.use_mock:
            print("Starting MOCK recording (silence).")
            return

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
        
        # Stop real recording
        if self.thread:
            self.thread.join()
            self.thread = None
            
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None
            
        # Handle Mock data generation if needed
        if self.use_mock and not self.frames:
            # Generate silent frames for the duration
            duration = time.time() - self.start_time
            # Create dummy silence
            num_frames = int(self.RATE * duration)
            # 16-bit silence is all zeros
            silence = b'\x00\x00' * num_frames
            self.frames = [silence]
            
        return self._save_file(output_filename) if output_filename else None

    def _save_file(self, filename):
        full_path = os.path.join(Config.DATA_DIR, filename)
        
        try:
            wf = wave.open(full_path, 'wb')
            wf.setnchannels(self.CHANNELS)
            # For mock, we default to 2 bytes (16-bit) if audio obj is missing
            sample_width = self.audio.get_sample_size(self.FORMAT) if self.audio else 2
            wf.setsampwidth(sample_width)
            wf.setframerate(self.RATE)
            wf.writeframes(b''.join(self.frames))
            wf.close()
            return full_path
        except Exception as e:
            print(f"Error saving file: {e}")
            return None

    def terminate(self):
        if self.audio:
            self.audio.terminate()
