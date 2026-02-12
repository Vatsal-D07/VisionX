import os
import urllib.request

def download_file(url, filename):
    if not os.path.exists(filename):
        print(f"Downloading {filename}...")
        try:
            urllib.request.urlretrieve(url, filename)
            print(f"✅ Saved to {filename}")
        except Exception as e:
            print(f"❌ Failed to download {filename}: {e}")
    else:
        print(f"ℹ️ {filename} already exists.")

def main():
    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)
    
    # Official YOLOv8 samples
    image_url = "https://ultralytics.com/images/bus.jpg"
    video_url = "https://github.com/intel-iot-devkit/sample-videos/raw/master/people-detection.mp4"

    download_file(image_url, "data/sample.jpg")
    download_file(video_url, "data/sample.mp4")

if __name__ == "__main__":
    main()
