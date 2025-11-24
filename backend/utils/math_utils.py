import numpy as np
import math


def compute_angle(a, b, c):
    """
    Compute the angle at point b formed by points a-b-c.
    
    Parameters
    ----------
    a : tuple (x, y)
        First point (e.g., shoulder)
    b : tuple (x, y)
        Vertex point where angle is measured (e.g., elbow)
    c : tuple (x, y)
        Third point (e.g., wrist)
    
    Returns
    -------
    float
        Angle in degrees [0, 180], or None if computation fails
    
    Examples
    --------
    For elbow angle:
        a = shoulder, b = elbow, c = wrist
    For shoulder angle:
        a = torso_center, b = shoulder, c = elbow
    """
    if a is None or b is None or c is None:
        return None
    
    try:
        # Convert to numpy arrays for vector math
        a = np.array(a, dtype=float)
        b = np.array(b, dtype=float)
        c = np.array(c, dtype=float)
        
        # Create vectors from b to a and b to c
        v1 = a - b  # vector from elbow to shoulder
        v2 = c - b  # vector from elbow to wrist
        
        # Compute magnitudes
        mag1 = np.linalg.norm(v1)
        mag2 = np.linalg.norm(v2)
        
        # Guard against zero-length vectors
        if mag1 < 1e-6 or mag2 < 1e-6:
            return None
        
        # Compute dot product and angle
        dot_product = np.dot(v1, v2)
        cos_angle = dot_product / (mag1 * mag2)
        
        # Clamp to [-1, 1] to avoid numerical errors in arccos
        cos_angle = np.clip(cos_angle, -1.0, 1.0)
        
        # Compute angle in radians then convert to degrees
        angle_rad = np.arccos(cos_angle)
        angle_deg = np.degrees(angle_rad)
        
        return angle_deg
        
    except Exception:
        return None


def get_midpoint(p1, p2):
    """
    Get the midpoint between two points.
    
    Parameters
    ----------
    p1, p2 : tuple (x, y)
        Two points
    
    Returns
    -------
    tuple (x, y)
        Midpoint coordinates, or None if invalid
    """
    if p1 is None or p2 is None:
        return None
    
    try:
        x = (p1[0] + p2[0]) / 2
        y = (p1[1] + p2[1]) / 2
        return (x, y)
    except Exception:
        return None


def get_angle_color(angle, min_val=80, max_val=160):
    """
    Get a color based on angle value for visual feedback.
    
    Parameters
    ----------
    angle : float
        Angle in degrees
    min_val : float
        Minimum angle threshold
    max_val : float
        Maximum angle threshold
    
    Returns
    -------
    tuple (B, G, R)
        BGR color for OpenCV
        
    Color coding:
        - Flexed (< min_val): Green
        - Extended (> max_val): Blue
        - Mid-range: Yellow
    """
    if angle is None:
        return (255, 255, 255)  # White for unknown
    
    if angle < min_val:
        return (0, 255, 0)  # Green (flexed)
    elif angle > max_val:
        return (255, 0, 0)  # Blue (extended)
    else:
        return (0, 255, 255)  # Yellow (mid-range)
