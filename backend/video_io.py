import cv2
import os


def init_capture(camera_index: int, frame_width: int, frame_height: int) -> cv2.VideoCapture:
    """Initialize and configure a cv2.VideoCapture.

    Sets the desired width and height if the camera supports them.
    """
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        return cap
    # Try to set resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)
    return cap


def init_writer(output_path: str, frame_width: int, frame_height: int, fps: int = 30) -> cv2.VideoWriter:
    """Create a cv2.VideoWriter for saving processed video.

    Uses the MP4V codec which works on most platforms.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))
    return writer


def show_frame(window_name: str, frame):
    """Display a frame in an OpenCV window.

    Handles window creation on first call.
    """
    cv2.imshow(window_name, frame)


def cleanup(capture: cv2.VideoCapture, writer: cv2.VideoWriter = None):
    """Release resources and destroy OpenCV windows."""
    if capture is not None:
        capture.release()
    if writer is not None:
        writer.release()
    cv2.destroyAllWindows()
