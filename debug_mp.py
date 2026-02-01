import sys
print(f"Python Version: {sys.version}")
try:
    import mediapipe
    print(f"MediaPipe imported. Location: {mediapipe.__file__}")
    print(f"Dir: {dir(mediapipe)}")
    
    try:
        import mediapipe.python.solutions
        print("mediapipe.python.solutions imported successfully")
    except ImportError as e:
        print(f"Failed to import mediapipe.python.solutions: {e}")

    try:
        from mediapipe import solutions
        print("from mediapipe import solutions SUCCESS")
    except ImportError as e:
        print(f"from mediapipe import solutions FAILED: {e}")

except ImportError as e:
    print(f"Failed to import mediapipe: {e}")
