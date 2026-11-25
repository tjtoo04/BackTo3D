"""Something with a position, a radius and a sprite."""

from pgzero.builtins import Actor

import combat
import settings
from animation import Animator


class Entity:
    """A body on the floor, drawn from an animation set."""

    def __init__(self, animation_set, x, y, radius, frame_rate=settings.FRAME_RATE):
        self.animator = Animator(animation_set, frame_rate)
        self.actor = Actor(self.animator.image(), pos=(x, y))
        self._sprite = self.animator.image()
        self.radius = radius
        self.vx = 0.0
        self.vy = 0.0
        self.dead = False

    @property
    def x(self):
        return self.actor.x

    @property
    def y(self):
        return self.actor.y

    def place(self, x, y):
        self.actor.pos = (x, y)

    def clamp(self, room):
        """Keep the body inside the walkable floor."""
        x, y = combat.clamp_to_rect(
            self.actor.x, self.actor.y, self.radius, *room.floor
        )
        self.actor.pos = (x, y)

    def sync_sprite(self):
        """Push the current frame to the sprite when it changes."""
        name = self.animator.image()
        if name != self._sprite:
            self._sprite = name
            self.actor.image = name

    def draw(self, screen):
        screen.blit(self._sprite, self.actor.topleft)
