"""Sprite frame cycling.

An animation set maps a state name to a list of frame names inside one image
folder. A state with no frames falls back to `idle`.
"""

FALLBACK_STATE = "idle"


class AnimationSet:
    """The frames available to one actor, grouped by state."""

    def __init__(self, folder, states, rates=None):
        self.folder = folder
        self.states = {
            state: [f"{folder}/{frame}" for frame in frames]
            for state, frames in states.items()
        }
        self.rates = rates or {}

    def frames(self, state):
        """Frame image names for a state, falling back to idle."""
        return self.states.get(state) or self.states[FALLBACK_STATE]

    def frame_rate(self, state, default):
        return self.rates.get(state, default)


class Animator:
    """Tracks the current state and frame of one actor."""

    def __init__(self, animation_set, frame_rate):
        self.animation_set = animation_set
        self.frame_rate = frame_rate
        self.state = FALLBACK_STATE
        self.elapsed = 0.0
        self.index = 0

    def play(self, state):
        """Switch to a state. Switching to the current state keeps the frame."""
        if state == self.state:
            return
        self.state = state
        self.elapsed = 0.0
        self.index = 0

    def update(self, dt):
        frames = self.animation_set.frames(self.state)
        if len(frames) <= 1:
            self.index = 0
            return
        rate = self.animation_set.frame_rate(self.state, self.frame_rate)
        step = 1.0 / rate
        self.elapsed += dt
        while self.elapsed >= step:
            self.elapsed -= step
            self.index = (self.index + 1) % len(frames)

    def image(self):
        """The image name to draw this frame."""
        frames = self.animation_set.frames(self.state)
        return frames[self.index % len(frames)]
