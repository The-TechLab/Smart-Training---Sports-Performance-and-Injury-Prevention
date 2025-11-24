import argparse
import os
import sys
import cv2
from datetime import datetime

from .config import Config
from .utils.logging_utils import setup_logging
from .utils.timing_utils import FPSTracker
from .video_io import init_capture, init_writer, show_frame, cleanup
from .pose_estimator import PoseEstimator
from .hud_overlay import HUDOverlay
from .session_controller import start_session_cli
from .session_paths import SessionPaths


def parse_args():
    parser = argparse.ArgumentParser(description="Smart Training Tracking Module")
    parser.add_argument('--no-save', action='store_true', help='Override SAVE_VIDEO to false')
    return parser.parse_args()


def main():
    print("[DEBUG] Starting Smart Training Tracker...")
    args = parse_args()
    cfg = Config()
    
    # ========== CLI SESSION SETUP ==========
    # Run interactive CLI to get session context
    session_info = start_session_cli()
    
    # Create session paths and directory structure
    paths = SessionPaths(base_dir="data/athletes", session_info=session_info)
    
    print(f"[DEBUG] Camera index: {cfg.CAMERA_INDEX}, Display HUD: {cfg.DISPLAY_HUD}")
    # Override save video if flag provided
    if args.no_save:
        cfg.SAVE_VIDEO = False

    setup_logging(cfg.LOG_LEVEL)

    # Initialize video capture
    print(f"[DEBUG] Attempting to open camera {cfg.CAMERA_INDEX}...")
    cap = init_capture(cfg.CAMERA_INDEX, cfg.FRAME_WIDTH, cfg.FRAME_HEIGHT)
    if not cap.isOpened():
        print(f"[ERROR] Cannot open camera index {cfg.CAMERA_INDEX}")
        sys.exit(1)
    print("[DEBUG] Camera opened successfully!")

    # Initialize pose estimator
    pose_estimator = PoseEstimator(model_type=cfg.POSE_MODEL_TYPE)

    # Initialize HUD overlay with session context
    hud = HUDOverlay(cfg, session_info=session_info)

    # Initialize video writer using session path
    writer = None
    if cfg.SAVE_VIDEO:
        writer = init_writer(paths.video_path, cfg.FRAME_WIDTH, cfg.FRAME_HEIGHT, fps=30)
        print(f"[INFO] Saving processed video to {paths.video_path}")

    fps_tracker = FPSTracker()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[WARN] Frame capture failed, exiting loop.")
            break

        pose_data = pose_estimator.detect(frame)
        fps = fps_tracker.update()
        frame = hud.draw(frame, pose_data, fps)

        # Show window only if HUD display is enabled
        if cfg.DISPLAY_HUD:
            show_frame(cfg.DISPLAY_WINDOW_NAME, frame)
            if cv2.waitKey(1) & 0xFF in (ord('q'), 27):
                break
        else:
            # headless mode minimal pause
            cv2.waitKey(1)

        if writer:
            writer.write(frame)

    cleanup(cap, writer)
    cv2.destroyAllWindows()
    print(f"\n✅ Session complete! Data saved to: {paths.session_dir}")


if __name__ == "__main__":
    main()
