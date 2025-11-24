import numpy as np
import cv2
from backend.hud_overlay import HUDOverlay


def test_hud_overlay_draws_on_frame():
    cfg = type('Cfg', (), {
        'DISPLAY_WINDOW_NAME': 'TestWindow',
        'LOG_LEVEL': 'INFO'
    })()
    hud = HUDOverlay(cfg)
    # Create dummy frame
    frame = np.zeros((480, 640, 3), dtype=np.uint8)
    # Dummy pose data with two landmarks and bbox
    pose_data = {
        'landmarks': [
            {'name': 'LEFT_SHOULDER', 'x': 100, 'y': 150, 'z': 0, 'visibility': 1.0},
            {'name': 'RIGHT_SHOULDER', 'x': 200, 'y': 150, 'z': 0, 'visibility': 1.0},
        ],
        'bbox': (90, 140, 210, 160),
        'score': 0.9,
    }
    out_frame = hud.draw(frame.copy(), pose_data, fps=30.0)
    # Ensure output is an ndarray and unchanged shape
    assert isinstance(out_frame, np.ndarray)
    assert out_frame.shape == frame.shape
    # Simple check: some pixel should be non-zero after drawing
    assert np.any(out_frame != 0)
