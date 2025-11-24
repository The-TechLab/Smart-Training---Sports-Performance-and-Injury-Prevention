import time
from collections import deque

class FPSTracker:
    """Simple FPS calculator using a rolling window of timestamps.

    Parameters
    ----------
    averaging_window: int, optional
        Number of recent frames to average over (default 30).
    """

    def __init__(self, averaging_window: int = 30):
        self.window = averaging_window
        self.timestamps = deque(maxlen=self.window)
        self.last_time = None

    def update(self) -> float:
        """Record a new frame timestamp and return the current FPS estimate.

        Returns
        -------
        float
            Estimated frames per second. Returns 0.0 if insufficient data.
        """
        now = time.time()
        if self.last_time is None:
            self.last_time = now
            self.timestamps.append(now)
            return 0.0
        self.timestamps.append(now)
        # Compute FPS based on time difference between oldest and newest timestamps
        if len(self.timestamps) >= 2:
            elapsed = self.timestamps[-1] - self.timestamps[0]
            if elapsed > 0:
                fps = (len(self.timestamps) - 1) / elapsed
                return fps
        return 0.0
