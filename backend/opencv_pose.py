"""
OpenCV DNN-based pose estimator using MoveNet or OpenPose models.
This is a fallback when MediaPipe is not available.
"""
import cv2
import numpy as np
import urllib.request
import os


class OpenCVPoseEstimator:
    """
    Pose estimator using OpenCV DNN with MoveNet Thunder model.
    Works without MediaPipe dependency.
    """
    
    # Joint mapping for the model
    KEYPOINT_NAMES = [
        'NOSE',           # 0
        'LEFT_EYE',       # 1
        'RIGHT_EYE',      # 2
        'LEFT_EAR',       # 3
        'RIGHT_EAR',      # 4
        'LEFT_SHOULDER',  # 5
        'RIGHT_SHOULDER', # 6
        'LEFT_ELBOW',     # 7
        'RIGHT_ELBOW',    # 8
        'LEFT_WRIST',     # 9
        'RIGHT_WRIST',    # 10
        'LEFT_HIP',       # 11
        'RIGHT_HIP',      # 12
        'LEFT_KNEE',      # 13
        'RIGHT_KNEE',     # 14
        'LEFT_ANKLE',     # 15
        'RIGHT_ANKLE',    # 16
    ]
    
    def __init__(self):
        """Initialize with a simple body keypoint detector."""
        print("[INFO] Initializing OpenCV DNN Pose Estimator...")
        
        # For now, create a stub that generates random test poses
        # In production, you would load an actual TFLite or ONNX model here
        self.dummy_mode = True
        print("[INFO] OpenCV Pose Estimator initialized (demo mode)")
    
    def detect(self, frame):
        """
        Detect pose in frame.
        
        Returns same format as MediaPipe estimator:
        {
            'joints': dict of joint_name -> (x, y),
            'angles': dict (computed separately),
            'score': float
        }
        """
        h, w = frame.shape[:2]
        
        # Generate a centered demo skeleton for testing
        # This simulates a person standing in the center
        center_x = w // 2
        center_y = h // 2
        
        # Simulate a T-pose
        joints = {
            'NOSE': (center_x, center_y - 100),
            'LEFT_EYE': (center_x - 20, center_y - 110),
            'RIGHT_EYE': (center_x + 20, center_y - 110),
            'LEFT_EAR': (center_x - 35, center_y - 105),
            'RIGHT_EAR': (center_x + 35, center_y - 105),
            'LEFT_SHOULDER': (center_x - 80, center_y - 50),
            'RIGHT_SHOULDER': (center_x + 80, center_y - 50),
            'LEFT_ELBOW': (center_x - 120, center_y + 20),
            'RIGHT_ELBOW': (center_x + 120, center_y + 20),
            'LEFT_WRIST': (center_x - 140, center_y + 90),
            'RIGHT_WRIST': (center_x + 140, center_y + 90),
            'LEFT_HIP': (center_x - 50, center_y + 80),
            'RIGHT_HIP': (center_x + 50, center_y + 80),
        }
        
        # Return empty to show the real issue
        return {}
