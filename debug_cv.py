import cv2
import os

print(f"OpenCV Version: {cv2.__version__}")
data_path = cv2.data.haarcascades
print(f"Cascades Path: {data_path}")

files = os.listdir(data_path)
print("Available Cascades:")
for f in files:
    print(f" - {f}")
