
import sys
import mediapipe as mp

with open("debug_out.txt", "w") as f:
    f.write(f"Python: {sys.version}\n")
    f.write(f"MP Path: {mp.__file__}\n")
    f.write(f"Dir(mp): {dir(mp)}\n")
    
    try:
        from mediapipe import solutions
        f.write("from mediapipe import solutions: OK\n")
    except Exception as e:
        f.write(f"from mediapipe import solutions: FAIL {e}\n")

    try:
        import mediapipe.python.solutions
        f.write("import mediapipe.python.solutions: OK\n")
    except Exception as e:
        f.write(f"import mediapipe.python.solutions: FAIL {e}\n")
