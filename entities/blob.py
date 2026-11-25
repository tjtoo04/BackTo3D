"""A slow chaser that wobbles as it rolls."""

import math
import random

import combat
import settings
from animation import AnimationSet
from entities.enemy import Enemy

BLOB_ANIMATIONS = AnimationSet(
    "blob",
    {
        "idle": ["idle"],
        "moving": ["moving_1", "moving_2", "moving_3"],
        "attack": ["attack"],
        "hurt": ["hurt_1", "hurt_2"],
        "death": ["death"],
    },
)


class Blob(Enemy):
    def __init__(self, x, y):
        super().__init__(BLOB_ANIMATIONS, x, y, settings.BLOB_RADIUS, settings.BLOB_HP)
        self.wobble = random.uniform(0.0, math.tau)

    def think(self, dt, player, room):
        self.wobble += dt * 2.4
        speed = settings.BLOB_SPEED * (1.0 + 0.14 * math.sin(self.wobble))
        self.vx, self.vy = combat.scaled_velocity(
            player.x - self.x, player.y - self.y, speed
        )
