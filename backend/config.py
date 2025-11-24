import os
from dotenv import load_dotenv

load_dotenv()  # Load .env if present

class Config:
    """Configuration holder loading from environment with defaults."""

    def __init__(self):
        # Camera settings
        self.CAMERA_INDEX = int(os.getenv("CAMERA_INDEX", "0"))
        self.FRAME_WIDTH = int(os.getenv("FRAME_WIDTH", "1280"))
        self.FRAME_HEIGHT = int(os.getenv("FRAME_HEIGHT", "720"))
        self.DISPLAY_WINDOW_NAME = os.getenv("DISPLAY_WINDOW_NAME", "SmartTrainingHUD")

        # Video saving options
        save_video_env = os.getenv("SAVE_VIDEO", "true").lower()
        self.SAVE_VIDEO = save_video_env == "true"
        self.OUTPUT_DIR = os.getenv("OUTPUT_DIR", "data/processed")
        self.OUTPUT_FILENAME = os.getenv("OUTPUT_FILENAME", "training_session")

        # Pose model selection
        self.POSE_MODEL_TYPE = os.getenv("POSE_MODEL_TYPE", "mediapipe")

        # Logging
        self.LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
        # HUD display toggle (true = show window, false = run headless)
        display_hud_env = os.getenv("DISPLAY_HUD", "true").lower()
        self.DISPLAY_HUD = display_hud_env == "true"

        # Ensure output directory exists
        os.makedirs(self.OUTPUT_DIR, exist_ok=True)
