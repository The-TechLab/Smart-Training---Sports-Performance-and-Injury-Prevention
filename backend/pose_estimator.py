import cv2
import numpy as np
from .utils.math_utils import compute_angle, get_midpoint

# Try to import mediapipe; if unavailable, fall back to stub mode
try:
    import mediapipe as mp
except ImportError:  # pragma: no cover
    mp = None


class PoseEstimator:
    """
    Wraps MediaPipe Pose (or stub) for detecting human pose landmarks
    with joint angle computation.

    The `detect` method returns a dictionary with:
    - joints: dict mapping joint names to (x, y) pixel coordinates
    - angles: dict of computed joint angles in degrees
    - score: overall pose confidence
    """

    # MediaPipe landmark indices for key joints
    LANDMARK_INDICES = {
        'NOSE': 0,
        'LEFT_EYE': 2,
        'RIGHT_EYE': 5,
        'LEFT_EAR': 7,
        'RIGHT_EAR': 8,
        'LEFT_SHOULDER': 11,
        'RIGHT_SHOULDER': 12,
        'LEFT_ELBOW': 13,
        'RIGHT_ELBOW': 14,
        'LEFT_WRIST': 15,
        'RIGHT_WRIST': 16,
        'LEFT_HIP': 23,
        'RIGHT_HIP': 24,
    }

    def __init__(self, model_type: str = "mediapipe"):
        self.model_type = model_type.lower()
        # If mediapipe is not available, force stub mode
        if mp is None:
            self.model_type = "stub"
            print("[WARN] MediaPipe not available, using stub mode")
        
        if self.model_type == "mediapipe":
            self.mp_pose = mp.solutions.pose
            self.pose = self.mp_pose.Pose(
                static_image_mode=False,
                model_complexity=1,
                enable_segmentation=False,
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5,
            )
            print("[INFO] MediaPipe Pose initialized")
        else:
            # Stub mode – no model loaded
            self.pose = None
            print("[INFO] Pose estimator in stub mode")

    def _extract_joints(self, results, frame_shape):
        """
        Extract joint coordinates from MediaPipe results.
        
        Returns dict mapping joint names to (x, y) pixel coordinates.
        """
        h, w, _ = frame_shape
        joints = {}
        
        for joint_name, idx in self.LANDMARK_INDICES.items():
            try:
                lm = results.pose_landmarks.landmark[idx]
                # Convert normalized coordinates to pixels
                x = int(lm.x * w)
                y = int(lm.y * h)
                # Check visibility (optional, MediaPipe provides this)
                visibility = getattr(lm, 'visibility', 1.0)
                if visibility > 0.5:  # Only use visible landmarks
                    joints[joint_name] = (x, y)
                else:
                    joints[joint_name] = None
            except (IndexError, AttributeError):
                joints[joint_name] = None
        
        return joints

    def _compute_angles(self, joints):
        """
        Compute joint angles from extracted joints.
        
        Returns dict of angles in degrees.
        """
        angles = {}
        
        # LEFT ELBOW ANGLE: shoulder -> elbow <- wrist
        angles['LEFT_ELBOW'] = compute_angle(
            joints.get('LEFT_SHOULDER'),
            joints.get('LEFT_ELBOW'),
            joints.get('LEFT_WRIST')
        )
        
        # RIGHT ELBOW ANGLE: shoulder -> elbow <- wrist
        angles['RIGHT_ELBOW'] = compute_angle(
            joints.get('RIGHT_SHOULDER'),
            joints.get('RIGHT_ELBOW'),
            joints.get('RIGHT_WRIST')
        )
        
        # For shoulder angle, we need a torso reference point
        # Use midpoint between shoulders as approximate torso center
        torso_center = get_midpoint(
            joints.get('LEFT_SHOULDER'),
            joints.get('RIGHT_SHOULDER')
        )
        
        # LEFT SHOULDER ANGLE: torso_center -> shoulder <- elbow
        angles['LEFT_SHOULDER'] = compute_angle(
            torso_center,
            joints.get('LEFT_SHOULDER'),
            joints.get('LEFT_ELBOW')
        )
        
        # RIGHT SHOULDER ANGLE: torso_center -> shoulder <- elbow
        angles['RIGHT_SHOULDER'] = compute_angle(
            torso_center,
            joints.get('RIGHT_SHOULDER'),
            joints.get('RIGHT_ELBOW')
        )
        
        return angles

    def detect(self, frame) -> dict:
        """
        Detect pose landmarks and compute angles in a BGR frame.

        Parameters
        ----------
        frame : np.ndarray
            BGR image from OpenCV

        Returns
        -------
        dict
            {
                "joints": dict mapping joint names to (x, y) tuples,
                "angles": dict mapping angle names to degrees (float or None),
                "score": float (overall confidence)
            }
            Returns empty dict {} if no pose detected or in stub mode.
        """
        if self.pose is None:
            # Stub mode
            return {}
        
        # Convert BGR to RGB as required by MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(rgb_frame)
        
        if not results.pose_landmarks:
            # No person detected
            return {}
        
        # Extract joints
        joints = self._extract_joints(results, frame.shape)
        
        # Compute angles
        angles = self._compute_angles(joints)
        
        # Overall score (use average visibility if available)
        score = 1.0  # Could compute from landmark visibilities if needed
        
        return {
            "joints": joints,
            "angles": angles,
            "score": score,
        }

