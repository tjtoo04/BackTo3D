"""An enemy that waits, winds up, then charges in a straight line."""

import random

import combat
import settings
from animation import AnimationSet
from entities.enemy import Enemy

CUBE_ANIMATIONS = AnimationSet(
    "cube",
    {
        "idle": ["idle"],
        "moving": ["moving_1", "moving_2", "moving_3"],
        "attack": ["attack_1", "attack_2", "attack_3"],
        "hurt": ["hurt"],
        "death": ["death"],
    },
    rates={"attack": 12},
)


class ChomperCube(Enemy):
    IDLE = "idle"
    WINDUP = "windup"
    CHARGE = "charge"
    RECOVER = "recover"

    def __init__(self, x, y):
        super().__init__(CUBE_ANIMATIONS, x, y, settings.CUBE_RADIUS, settings.CUBE_HP)
        self.mode = self.IDLE
        self.timer = random.uniform(0.3, settings.CUBE_IDLE_TIME)
        self.charge_x = 0.0
        self.charge_y = 0.0

    def think(self, dt, player, room):
        self.timer -= dt
        if self.mode == self.IDLE:
            self.vx = self.vy = 0.0
            if self.timer <= 0.0:
                self.mode = self.WINDUP
                self.timer = settings.CUBE_WINDUP_TIME
                self.charge_x, self.charge_y = combat.unit_vector(
                    player.x - self.x, player.y - self.y
                )
        elif self.mode == self.WINDUP:
            self.vx = self.vy = 0.0
            if self.timer <= 0.0:
                self.mode = self.CHARGE
                self.timer = settings.CUBE_CHARGE_TIME
                self.vx = self.charge_x * settings.CUBE_CHARGE_SPEED
                self.vy = self.charge_y * settings.CUBE_CHARGE_SPEED
        elif self.mode == self.CHARGE:
            if self.timer <= 0.0:
                self.mode = self.RECOVER
                self.timer = settings.CUBE_RECOVER_TIME
                self.vx = self.vy = 0.0
        else:
            self.vx = self.vy = 0.0
            if self.timer <= 0.0:
                self.mode = self.IDLE
                self.timer = settings.CUBE_IDLE_TIME

    def animation_state(self):
        if self.hurt_flash > 0.0:
            return "hurt"
        if self.mode == self.WINDUP:
            return "attack"
        if self.mode == self.CHARGE:
            return "moving"
        return "idle"
