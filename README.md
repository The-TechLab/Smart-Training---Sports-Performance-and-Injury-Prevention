# Smart Training – Sports Performance and Injury Prevention (Tracking Module)

## Project Overview

This repository contains the **initial tracking module** for the Smart Training project, focusing on real‑time webcam video capture, pose estimation, and a heads‑up display (HUD) overlay. The goal is to provide a lightweight, offline solution for sports performance and injury‑prevention research.

## Features (Phase 1)
- Webcam video capture using OpenCV.
- Pose estimation via MediaPipe (or a stub implementation).
- HUD overlay drawing keypoints, skeleton, FPS, and debug info.
- Optional saving of the processed video to `data/processed/`.

## Prerequisites
- Python **3.10+**
- A webcam attached to your computer.
- (Recommended) Virtual environment (`venv`).

## Setup
```bash
# Clone the repository (placeholder URL)
# git clone <repo-url>

cd "Smart Training - Sports Performance and Injury Prevention"

# Create and activate a virtual environment
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy example env file and edit as needed
cp .env.example .env
# Edit .env to adjust camera index, resolution, etc.
```

## Running the Tracker
```bash
python -m backend.main            # Run with default settings
python -m backend.main --no-save   # Override SAVE_VIDEO at runtime
```

Press **`q`** or **Esc** to exit the window.

## Project Structure
```
Smart Training - Sports Performance and Injury Prevention/
│   README.md
│   .env.example
│   .env               # ignored in .gitignore
│   requirements.txt
│   .gitignore
│
├─ backend/
│   ├─ __init__.py
│   ├─ main.py
│   ├─ config.py
│   ├─ pose_estimator.py
│   ├─ hud_overlay.py
│   ├─ video_io.py
│   └─ utils/
│       ├─ __init__.py
│       ├─ logging_utils.py
│       └─ timing_utils.py
│
├─ data/
│   ├─ raw/            # raw videos (if recorded)
│   ├─ processed/      # HUD‑annotated output videos
│   └─ models/         # pose model weights (optional)
│
├─ experiments/
│   └─ notebooks/
│       └─ pose_debug.ipynb
│
└─ tests/
    ├─ __init__.py
    ├─ test_pose_estimator.py
    └─ test_hud_overlay.py
```

## Next Steps
- Integrate more advanced pose models.
- Support multiple cameras.
- Add analytics and athlete profiling layers.

---
*Happy coding!*
