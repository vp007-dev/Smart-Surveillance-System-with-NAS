# 🧠 Smart Surveillance System with NAS, AI Face Recognition, and Video Sorting

> Smart Surveillance uses AI for face recognition and tracking in video footage. Integrated with NAS, it auto-sorts videos into categorized folders based on identified faces, offering an efficient and automated security solution.

![Surveillance Banner](https://sdmntpreastus2.oaiusercontent.com/files/00000000-84e0-61f6-a3d6-b3d5bd59b3c9/raw?se=2025-05-17T18%3A04%3A04Z&sp=r&sv=2024-08-04&sr=b&scid=00000000-0000-0000-0000-000000000000&skoid=02b7f7b5-29f8-416a-aeb6-99464748559d&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2025-05-17T01%3A32%3A21Z&ske=2025-05-18T01%3A32%3A21Z&sks=b&skv=2024-08-04&sig=fj0YFVDdn8HoxErX%2BtBnRecr%2BWxCXHKkfAlz1jVtIRc%3D)

---

## 📦 Features

- 🎯 **AI Face Recognition**  
  Detect and identify known faces from surveillance footage.

- 🔍 **Face Tracking**  
  Track individuals across frames and multiple video files.

- 🧠 **Automated Video Sorting**  
  Automatically sort and organize footage based on recognition results.

- 📁 **NAS Integration**  
  Connects to NAS (SMB/NFS) for accessing and storing large video datasets.

- ⚙️ **Modular & Scalable**  
  Easy to plug into existing systems and extend functionality.

---

## 🛠️ Technologies Used

| Technology         | Purpose                     |
|--------------------|-----------------------------|
| Python             | Core programming language   |
| OpenCV             | Video processing            |
| face_recognition   | Facial detection & encoding |
| NumPy / Pandas     | Data processing             |
| Flask / FastAPI    | (Optional) web interface    |
| NAS (SMB/NFS)      | Network storage access      |

---

## 🗂️ Project Structure

smart-surveillance/
├── ai_module/
│ ├── face_detector.py
│ ├── face_tracker.py
│ ├── video_sorter.py
├── data/
│ ├── known_faces/
│ ├── videos_input/
│ ├── videos_processed/
├── utils/
│ ├── nas_handler.py
│ └── logger.py
├── main.py
├── requirements.txt
└── README.md

---
## 🎯 How It Works


1. 📥 **Video Input**  
   Videos are pulled from a NAS directory using Python NAS-handling utilities.

2. 👁️ **Face Detection & Recognition**  
   Each frame is scanned using `face_recognition`. Known faces are matched, unknowns logged.

3. 🔄 **Tracking and Tagging**  
   Detected faces are tracked using OpenCV’s correlation tracking.

4. 🗃️ **Sorting and Archiving**  
   Videos are moved to categorized folders:
   - `videos_processed/known/`
   - `videos_processed/unknown/`
   - `videos_flagged/`

---

---

## ⚙️ Installation

```bash
git clone https://github.com/your-username/smart-surveillance.git
cd smart-surveillance
pip install -r requirements.txt
