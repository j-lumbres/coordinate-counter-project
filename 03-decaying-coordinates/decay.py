import numpy as np


def compute_linear_decay(time_diff, decay_rate):
    # Decays linearly to zero once time_diff reaches decay_rate
    return np.clip(1.0 - time_diff / decay_rate, 0.0, 1.0)


def compute_exponential_decay(time_diff, decay_rate):
    # Decays asymptotically — never reaches zero, slower to fade initially
    return np.exp(-time_diff / decay_rate)


class CoordinateActivator:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = np.zeros((height, width), dtype=np.int64)
        self.latest_global_timestamp = 0

    def update(self, x, y, t):
        self.grid[y][x] = t
        self.latest_global_timestamp = max(self.latest_global_timestamp, t)

    def get_decay_at_time(self, render_time, decay_fn, decay_rate):
        time_diff = render_time - self.grid

        decay = np.where(time_diff >= 0, decay_fn(time_diff, decay_rate), 0.0)
        return np.clip(decay, 0.0, 1.0)


def build_frames(df, width, height, capture_interval, decay_rate):
    activator = CoordinateActivator(width, height)

    next_capture_time = 0
    linear_frames = []
    exponential_frames = []

    for row in df.itertuples():
        x, y, t = int(row.x), int(row.y), int(row.t)

        while t >= next_capture_time:
            activator.latest_global_timestamp = next_capture_time

            linear_grid = activator.get_decay_at_time(next_capture_time, compute_linear_decay, decay_rate)
            exponential_grid = activator.get_decay_at_time(next_capture_time, compute_exponential_decay, decay_rate)

            linear_frames.append({"time": next_capture_time, "grid": linear_grid})
            exponential_frames.append({"time": next_capture_time, "grid": exponential_grid})

            next_capture_time += capture_interval

        activator.update(x, y, t)

    # Final frame after all events
    activator.latest_global_timestamp = t
    linear_frames.append({"time": t, "grid": activator.get_decay_at_time(t, compute_linear_decay, decay_rate)})
    exponential_frames.append({"time": t, "grid": activator.get_decay_at_time(t, compute_exponential_decay, decay_rate)})

    return linear_frames, exponential_frames
