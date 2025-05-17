import os
import shutil
import cv2
import datetime
from tkinter import *
from tkinter import filedialog, messagebox, scrolledtext
from tqdm import tqdm
from ultralytics import YOLO
from threading import Thread

model = YOLO("yolov8n.pt")
DETECTION_CLASS = 'person'

class VideoAnalyzerGUI:
    def __init__(self, master):
        self.master = master
        master.title("YOLO Video Analyzer")
        master.geometry("700x550")
        master.configure(bg="#1e1e1e")

        self.folder_path = StringVar()

        Label(master, text="Select Base Folder:", bg="#1e1e1e", fg="white").pack(pady=5)
        folder_frame = Frame(master, bg="#1e1e1e")
        folder_frame.pack()
        Entry(folder_frame, textvariable=self.folder_path, width=60).pack(side=LEFT, padx=5)
        Button(folder_frame, text="Browse", command=self.browse_folder).pack(side=LEFT)

        Button(master, text="Start Analysis", bg="#007acc", fg="white", command=self.start_analysis).pack(pady=10)
        Button(master, text="Open Webcam & Detect", bg="#007acc", fg="white", command=self.open_webcam).pack(pady=5)

        Label(master, text="Logs:", bg="#1e1e1e", fg="white").pack()
        self.log_box = scrolledtext.ScrolledText(master, height=20, width=80, bg="#252526", fg="white", insertbackground="white")
        self.log_box.pack(padx=10, pady=10)

    def browse_folder(self):
        path = filedialog.askdirectory()
        if path:
            self.folder_path.set(path)

    def start_analysis(self):
        if not self.folder_path.get():
            messagebox.showerror("Error", "Please select a folder first.")
            return
        Thread(target=self.process_day).start()

    def process_day(self):
        base_folder = self.folder_path.get()
        today = datetime.datetime.now().strftime('%Y%m%d')

        for hour in range(0, 100):
            hour_str = f"{hour:02}"
            folder_name = today + hour_str
            raw_folder = os.path.join(base_folder, folder_name)

            if not os.path.exists(raw_folder):
                self.log(f"[SKIP] {raw_folder} not found.")
                continue

            self.log(f"\n[PROCESSING] {raw_folder}")
            self.process_all_videos(raw_folder)

    def process_all_videos(self, raw_folder):
        with_people = os.path.join(raw_folder, "With_people")
        no_activity = os.path.join(raw_folder, "No_activity")
        unknown_event = os.path.join(raw_folder, "Unknown_event")

        os.makedirs(with_people, exist_ok=True)
        os.makedirs(no_activity, exist_ok=True)
        os.makedirs(unknown_event, exist_ok=True)

        video_files = [f for f in os.listdir(raw_folder) if f.endswith(('.mp4', '.avi', '.mov'))]

        if not video_files:
            self.log("No videos found.")
            return

        self.log(f"Found {len(video_files)} video(s). Starting analysis...\n")

        for video in tqdm(video_files, desc="Analyzing", unit="video"):
            full_path = os.path.join(raw_folder, video)

            try:
                annotated_name = f"annotated_{video}"
                annotated_path = os.path.join(raw_folder, annotated_name)

                detected = self.analyze_and_annotate_video(full_path, annotated_path)

                if detected:
                    shutil.move(annotated_path, os.path.join(with_people, video))
                    self.log(f"✔️ Person Detected → {video}")
                else:
                    shutil.move(annotated_path, os.path.join(no_activity, video))
                    self.log(f"⭕ No Activity → {video}")

                os.remove(full_path)
            except Exception as e:
                shutil.move(full_path, os.path.join(unknown_event, video))
                self.log(f"❌ Error with {video}: {e}")

    def analyze_and_annotate_video(self, video_path, output_path):
        cap = cv2.VideoCapture(video_path)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        detected = False

        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                break

            results = model(frame, verbose=False)[0]

            if results.boxes:
                for box in results.boxes:
                    cls_id = int(box.cls[0])
                    label = model.names[cls_id]
                    conf = float(box.conf[0])

                    if label == DETECTION_CLASS:
                        detected = True

                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, f'{label} {conf:.2f}', (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

            out.write(frame)

        cap.release()
        out.release()
        return detected

    def open_webcam(self):
        Thread(target=self.run_yolo_on_webcam).start()

    def run_yolo_on_webcam(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            self.log("❌ Unable to access webcam.")
            return

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            results = model(frame, verbose=False)[0]

            if results.boxes:
                for box in results.boxes:
                    cls_id = int(box.cls[0])
                    label = model.names[cls_id]
                    conf = float(box.conf[0])

                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, f'{label} {conf:.2f}', (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

            cv2.imshow("Live YOLO Detection", frame)
            if cv2.waitKey(1) & 0xFF == 27:
                break

        cap.release()
        cv2.destroyAllWindows()

    def log(self, message):
        self.log_box.insert(END, message + "\n")
        self.log_box.see(END)

if __name__ == "__main__":
    root = Tk()
    app = VideoAnalyzerGUI(root)
    root.mainloop()
