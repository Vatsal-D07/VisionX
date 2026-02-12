import streamlit as st
import cv2
import numpy as np
import tempfile
import os
from ultralytics import YOLO
from PIL import Image

# -------------------------
# Page Config & Styling
# -------------------------
st.set_page_config(
    page_title="YOLOv8 Object Detection",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a premium look
st.markdown("""
<style>
    /* Main Background */
    .stApp {
        background-color: #0e1117;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #00e5ff !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Buttons */
    .stButton>button {
        background-color: #00e5ff;
        color: #000000;
        border-radius: 8px;
        font-weight: bold;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #00b8cc;
        color: white;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #161b22;
    }
    
    /* Cards/Containers */
    .css-1r6slb0 {
        border-radius: 15px;
        padding: 20px;
        background-color: #1f2937;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# -------------------------
# Model Loading
# -------------------------
@st.cache_resource
def load_model():
    # Downloads model automatically if not found
    return YOLO("yolov8n.pt")

try:
    model = load_model()
except Exception as e:
    st.error(f"Error loading model: {e}")
    st.stop()

# -------------------------
# Sidebar Settings
# -------------------------
st.sidebar.title("⚙️ Settings")
st.sidebar.markdown("---")

confidence = st.sidebar.slider("Confidence Threshold", 0.0, 1.0, 0.25, 0.05)
mode = st.sidebar.radio("Select Mode", ["Image Detection", "Video Detection", "Live Webcam"])

st.sidebar.markdown("---")
st.sidebar.info("YOLOv8 Object Detection System\n\nCollege Project Submission")

# -------------------------
# Helper Functions
# -------------------------
def process_frame(frame, conf):
    """Run inference and draw boxes."""
    results = model(frame, conf=conf)
    annotated_frame = results[0].plot()
    return annotated_frame

# -------------------------
# Main App Logic
# -------------------------

st.title("👁️ Intelligent Object Detection System")
st.markdown("### Powered by YOLOv8 and Streamlit")

if mode == "Image Detection":
    st.write("#### 📸 Upload an Image")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    
    if uploaded_file:
        col1, col2 = st.columns(2)
        
        # Display original
        image = Image.open(uploaded_file)
        with col1:
            st.image(image, caption="Original Image", use_container_width=True)
        
        # Process
        with st.spinner("Detecting objects..."):
            np_img = np.array(image)
            # Convert RGB to BGR for OpenCV
            np_img = cv2.cvtColor(np_img, cv2.COLOR_RGB2BGR)
            
            annotated_frame = process_frame(np_img, confidence)
            
            # Convert back to RGB for display
            annotated_rgb = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
        
        with col2:
            st.image(annotated_rgb, caption="Detected Objects", use_container_width=True)
            
        # Optional: Show detection data
        with st.expander("See Detection Details"):
            st.json(model(np_img, conf=confidence)[0].summary())

elif mode == "Video Detection":
    st.write("#### 🎥 Upload a Video")
    uploaded_video = st.file_uploader("Choose a video...", type=["mp4", "avi", "mov"])
    
    if uploaded_video:
        # Save temp file
        tfile = tempfile.NamedTemporaryFile(delete=False) 
        tfile.write(uploaded_video.read())
        tfile.close()
        
        cap = cv2.VideoCapture(tfile.name)
        
        st_frame = st.empty()
        
        stop_button = st.button("Stop Processing")
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret or stop_button:
                break
            
            # Process
            annotated_frame = process_frame(frame, confidence)
            
            # Display
            annotated_rgb = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
            st_frame.image(annotated_rgb, caption="Processing Video...", use_container_width=True, channels="RGB")
        
        cap.release()
        os.remove(tfile.name)

elif mode == "Live Webcam":
    st.write("#### 🔴 Live Webcam Feed")
    st.warning("Ensure your camera is enabled. Press 'Start' to begin.")
    
    run = st.checkbox('Start Webcam')
    FRAME_WINDOW = st.image([])
    
    if run:
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            st.error("Could not open webcam.")
        else:
            while run:
                ret, frame = cap.read()
                if not ret:
                    st.error("Failed to capture image")
                    break
                
                annotated_frame = process_frame(frame, confidence)
                
                # Streamlit requires RGB
                annotated_rgb = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
                FRAME_WINDOW.image(annotated_rgb)
            
            cap.release()
    else:
        st.info("Webcam is stopped.")

