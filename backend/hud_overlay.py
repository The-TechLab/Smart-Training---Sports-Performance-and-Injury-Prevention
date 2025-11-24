import cv2
import numpy as np
from .utils.math_utils import get_angle_color


class HUDOverlay:
    """
    Draws a colorful exoskeleton HUD with pose landmarks, skeleton lines,
    and joint angle labels.

    The exoskeleton visualizes:
    - Head tracking (nose, eyes)
    - Hand tracking (wrists)
    - Arm tracking (shoulders, elbows, wrists)
    - Real-time joint angles (elbow and shoulder flexion/extension)
    """

    def __init__(self, config, session_info=None):
        self.cfg = config
        self.session_info = session_info
        
        # Color scheme (BGR format for OpenCV)
        self.colors = {
            'head': (255, 255, 0),        # Cyan for head
            'left_arm': (255, 100, 100),  # Light blue for left arm
            'right_arm': (255, 0, 255),   # Magenta for right arm
            'joints': (0, 255, 0),        # Green for joints
            'hands': (0, 165, 255),       # Orange for hands
            'torso': (200, 200, 200),     # Light gray for torso
            'text': (255, 255, 255),      # White for text
        }
        
        # Drawing parameters
        self.joint_radius = 6
        self.hand_radius = 10
        self.head_radius = 8
        self.line_thickness = 3
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.font_scale = 0.6
        self.font_thickness = 2

    def _draw_skeleton_line(self, frame, p1, p2, color, thickness=None):
        """Draw a line between two joints if both are valid."""
        if p1 is not None and p2 is not None:
            thickness = thickness or self.line_thickness
            cv2.line(frame, tuple(map(int, p1)), tuple(map(int, p2)), color, thickness)

    def _draw_joint(self, frame, point, color, radius=None):
        """Draw a filled circle at a joint location."""
        if point is not None:
            radius = radius or self.joint_radius
            cv2.circle(frame, tuple(map(int, point)), radius, color, -1)
            # Add a white outline for better visibility
            cv2.circle(frame, tuple(map(int, point)), radius, (255, 255, 255), 1)

    def _draw_angle_label(self, frame, point, angle, name=""):
        """Draw angle value as text near a joint."""
        if point is None or angle is None:
            return
        
        # Round angle to integer
        angle_int = int(round(angle))
        text = f"{angle_int}°"
        
        # Get color based on angle value
        color = get_angle_color(angle)
        
        # Offset text position slightly from joint
        x, y = int(point[0]), int(point[1])
        text_pos = (x + 15, y - 15)
        
        # Draw text with black outline for readability
        cv2.putText(frame, text, text_pos, self.font, self.font_scale,
                    (0, 0, 0), self.font_thickness + 2, cv2.LINE_AA)
        cv2.putText(frame, text, text_pos, self.font, self.font_scale,
                    color, self.font_thickness, cv2.LINE_AA)

    def _draw_exoskeleton(self, frame, joints, angles):
        """Draw the full colorful exoskeleton with angles."""
        if not joints:
            return
        
        # 1. Draw torso connection (shoulders)
        self._draw_skeleton_line(
            frame,
            joints.get('LEFT_SHOULDER'),
            joints.get('RIGHT_SHOULDER'),
            self.colors['torso'],
            thickness=2
        )
        
        # 2. Draw LEFT ARM (blue)
        # Shoulder to elbow
        self._draw_skeleton_line(
            frame,
            joints.get('LEFT_SHOULDER'),
            joints.get('LEFT_ELBOW'),
            self.colors['left_arm']
        )
        # Elbow to wrist
        self._draw_skeleton_line(
            frame,
            joints.get('LEFT_ELBOW'),
            joints.get('LEFT_WRIST'),
            self.colors['left_arm']
        )
        
        # 3. Draw RIGHT ARM (magenta)
        # Shoulder to elbow
        self._draw_skeleton_line(
            frame,
            joints.get('RIGHT_SHOULDER'),
            joints.get('RIGHT_ELBOW'),
            self.colors['right_arm']
        )
        # Elbow to wrist
        self._draw_skeleton_line(
            frame,
            joints.get('RIGHT_ELBOW'),
            joints.get('RIGHT_WRIST'),
            self.colors['right_arm']
        )
        
        # 4. Draw head connections (nose to shoulders)
        nose = joints.get('NOSE')
        if nose:
            # Simple neck visualization
            self._draw_skeleton_line(frame, nose, joints.get('LEFT_SHOULDER'),
                                     self.colors['head'], thickness=2)
            self._draw_skeleton_line(frame, nose, joints.get('RIGHT_SHOULDER'),
                                     self.colors['head'], thickness=2)
        
        # 5. Draw joints
        # Shoulders
        self._draw_joint(frame, joints.get('LEFT_SHOULDER'), self.colors['joints'])
        self._draw_joint(frame, joints.get('RIGHT_SHOULDER'), self.colors['joints'])
        
        # Elbows
        self._draw_joint(frame, joints.get('LEFT_ELBOW'), self.colors['joints'])
        self._draw_joint(frame, joints.get('RIGHT_ELBOW'), self.colors['joints'])
        
        # Hands (wrists) - larger circles
        self._draw_joint(frame, joints.get('LEFT_WRIST'), self.colors['hands'],
                        radius=self.hand_radius)
        self._draw_joint(frame, joints.get('RIGHT_WRIST'), self.colors['hands'],
                        radius=self.hand_radius)
        
        # Head (nose) - larger circle
        self._draw_joint(frame, joints.get('NOSE'), self.colors['head'],
                        radius=self.head_radius)
        
        # Eyes (smaller)
        self._draw_joint(frame, joints.get('LEFT_EYE'), self.colors['head'], radius=4)
        self._draw_joint(frame, joints.get('RIGHT_EYE'), self.colors['head'], radius=4)
        
        # 6. Draw angle labels
        # Left elbow angle
        self._draw_angle_label(
            frame,
            joints.get('LEFT_ELBOW'),
            angles.get('LEFT_ELBOW'),
            "L Elbow"
        )
        
        # Right elbow angle
        self._draw_angle_label(
            frame,
            joints.get('RIGHT_ELBOW'),
            angles.get('RIGHT_ELBOW'),
            "R Elbow"
        )
        
        # Left shoulder angle
        self._draw_angle_label(
            frame,
            joints.get('LEFT_SHOULDER'),
            angles.get('LEFT_SHOULDER'),
            "L Shoulder"
        )
        
        # Right shoulder angle
        self._draw_angle_label(
            frame,
            joints.get('RIGHT_SHOULDER'),
            angles.get('RIGHT_SHOULDER'),
            "R Shoulder"
        )

    def _draw_hud_info(self, frame, pose_data, fps):
        """Draw FPS, pose status, and session information."""
        h, w = frame.shape[:2]
        
        # Draw session context banner (top center) if session_info is available
        if self.session_info:
            self._draw_session_banner(frame, w)
        
        # FPS (top-left)
        if fps is not None:
            fps_text = f"FPS: {fps:.1f}"
            cv2.putText(frame, fps_text, (10, 30), self.font, 0.7,
                       (0, 0, 0), 3, cv2.LINE_AA)
            cv2.putText(frame, fps_text, (10, 30), self.font, 0.7,
                       self.colors['text'], 2, cv2.LINE_AA)
        
        # Pose status (top-right)
        if pose_data and pose_data.get('score', 0) > 0:
            status_text = "POSE: OK"
            status_color = (0, 255, 0)  # Green
        else:
            status_text = "POSE: LOST"
            status_color = (0, 0, 255)  # Red
        
        text_size = cv2.getTextSize(status_text, self.font, 0.7, 2)[0]
        text_x = w - text_size[0] - 10
        cv2.putText(frame, status_text, (text_x, 30), self.font, 0.7,
                   (0, 0, 0), 3, cv2.LINE_AA)
        cv2.putText(frame, status_text, (text_x, 30), self.font, 0.7,
                   status_color, 2, cv2.LINE_AA)
    
    def _draw_session_banner(self, frame, frame_width):
        """Draw session context banner at top center of frame."""
        player = self.session_info.get('player', {})
        sport = self.session_info.get('sport', '').replace('_', ' ').upper()
        exercise = self.session_info.get('exercise', '')
        
        # Build banner text
        player_name = player.get('full_name', 'Unknown')
        player_num = player.get('number', '')
        player_pos = player.get('position', '')
        
        if exercise:
            exercise_display = exercise.replace('_', ' ').title()
            banner_text = f"{sport} - {exercise_display} - {player_name} #{player_num} ({player_pos})"
        else:
            banner_text = f"{sport} - {player_name} #{player_num} ({player_pos})"
        
        # Calculate text size and position (centered)
        font_scale = 0.65
        thickness = 2
        text_size = cv2.getTextSize(banner_text, self.font, font_scale, thickness)[0]
        text_x = (frame_width - text_size[0]) // 2
        text_y = 60
        
        # Draw semi-transparent background rectangle
        padding = 10
        rect_x1 = text_x - padding
        rect_y1 = text_y - text_size[1] - padding
        rect_x2 = text_x + text_size[0] + padding
        rect_y2 = text_y + padding
        
        overlay = frame.copy()
        cv2.rectangle(overlay, (rect_x1, rect_y1), (rect_x2, rect_y2), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)
        
        # Draw border
        cv2.rectangle(frame, (rect_x1, rect_y1), (rect_x2, rect_y2), (0, 255, 255), 2)
        
        # Draw text
        cv2.putText(frame, banner_text, (text_x, text_y), self.font, font_scale,
                   (0, 0, 0), thickness + 2, cv2.LINE_AA)
        cv2.putText(frame, banner_text, (text_x, text_y), self.font, font_scale,
                   (0, 255, 255), thickness, cv2.LINE_AA)  # Yellow/Cyan color

    def draw(self, frame, pose_data: dict, fps: float = None):
        """
        Draw the complete HUD overlay on the frame.

        Parameters
        ----------
        frame : np.ndarray
            BGR image from OpenCV
        pose_data : dict
            Output from PoseEstimator.detect() with 'joints' and 'angles'
        fps : float, optional
            Current FPS for display

        Returns
        -------
        np.ndarray
            Frame with HUD overlay drawn
        """
        if not pose_data:
            # No pose detected - just draw status info
            self._draw_hud_info(frame, pose_data, fps)
            return frame
        
        joints = pose_data.get('joints', {})
        angles = pose_data.get('angles', {})
        
        # Draw the exoskeleton with angles
        self._draw_exoskeleton(frame, joints, angles)
        
        # Draw HUD info (FPS and status)
        self._draw_hud_info(frame, pose_data, fps)
        
        return frame

