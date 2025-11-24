import numpy as np
import cv2
from backend.pose_estimator import PoseEstimator

def test_stub_pose_estimator_returns_empty():
    estimator = PoseEstimator(model_type="stub")
    dummy_frame = np.zeros((480, 640, 3), dtype=np.uint8)
    result = estimator.detect(dummy_frame)
    assert result == {}  # Stub should return empty dict
