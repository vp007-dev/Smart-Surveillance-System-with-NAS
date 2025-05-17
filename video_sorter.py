import os
import shutil
import cv2
from tqdm import tqdm
from ultralytics import YOLO
import datetime

WITH_PEOPLE = r"D:\camerarecording\xiaomi_camera_videos\788b2ac589b8\With_people"
NO_ACTIVITY = r"D:\camerarecording\xiaomi_camera_videos\788b2ac589b8\No_activity"
UNKNOWN_EVENT = r"D:\camerarecording\xiaomi_camera_videos\788b2ac589b8\Unknown_event"

DETECTION_CLASS = 'person'
MAX_FRAMES = 100

model = YOLO("yolov8n.pt")

def analyze_video(video_path):
    cap = cv2.VideoCapture(video_path)
    detected = False
    frame_count = 0

    while cap.isOpened() and frame_count < MAX_FRAMES:
        success, frame = cap.read()
        if not success:
            break

        results = model(frame, verbose=False)
        for result in results:
            if result.boxes:
                for cls in result.boxes.cls:
                    label = model.names[int(cls)]
                    if label == DETECTION_CLASS:
                        detected = True
                        break

        frame_count += 1

    cap.release()
    return detected

def process_all_videos():
    video_files = [f for f in os.listdir(RAW_FOLDER) if f.endswith(('.mp4', '.avi', '.mov'))]
    
    if not video_files:
        print("No videos found.")
        return

    print(f"Found {len(video_files)} video(s). Starting analysis...\n")

    for video in tqdm(video_files, desc="Analyzing", unit="video"):
        full_path = os.path.join(RAW_FOLDER, video)

        try:
            if analyze_video(full_path):
                shutil.move(full_path, os.path.join(WITH_PEOPLE, video))
            else:
                shutil.move(full_path, os.path.join(NO_ACTIVITY, video))
        except Exception as e:
            print(f"Error with {video}: {e}")
            shutil.move(full_path, os.path.join(UNKNOWN_EVENT, video))

    print("Done. All videos have been processed.")

if __name__ == "__main__":
    today = datetime.datetime.now().strftime('%Y%m%d')
    
    for hour in range(0, 100):
        hour_str = f"{hour:02}"
        folder_name = today + hour_str
        RAW_FOLDER = f"D:\\camerarecording\\xiaomi_camera_videos\\788b2ac589b8\\{folder_name}"
        
        if not os.path.exists(RAW_FOLDER):
            print(f"Skipping missing folder: {RAW_FOLDER}")
            continue

        print(f"\nProcessing folder: {RAW_FOLDER}")
        process_all_videos()
