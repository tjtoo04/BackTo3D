"""An enemy that circles the hero and spits a tear now and then."""

import math
import random

import combat
import settings
from animation import AnimationSet
from entities.enemy import Enemy

SPIDER_ANIMATIONS = AnimationSet(
    "spider",
    {
        "idle": ["idle"],
        "moving": ["moving"],
        "attack": ["attack"],
        "hurt": ["hurt"],
        "death": ["death"],
    },
)


class PaperclipSpider(Enemy):
    def __init__(self, x, y):
        super().__init__(
            SPIDER_ANIMATIONS, x, y, settings.SPIDER_RADIUS, settings.SPIDER_HP
        )
        self.orbit_angle = random.uniform(0.0, math.tau)
        self.shoot_timer = random.uniform(0.9, settings.SPIDER_SHOOT_INTERVAL)

    def think(self, dt, player, room):
        self.orbit_angle += dt * 1.6
        target_x = player.x + math.cos(self.orbit_angle) * settings.SPIDER_ORBIT
        target_y = player.y + math.sin(self.orbit_angle) * settings.SPIDER_ORBIT
        self.vx, self.vy = combat.scaled_velocity(
            target_x - self.x, target_y - self.y, settings.SPIDER_SPEED
        )

        self.shoot_timer -= dt
        if self.shoot_timer <= 0.0:
            self.shoot_timer = settings.SPIDER_SHOOT_INTERVAL
            self.attack_pose = 0.25
            room.spawn_enemy_tear(
                self.x,
                self.y,
                combat.angle_from_direction(player.x - self.x, player.y - self.y),
            )

    def animation_state(self):
        if self.hurt_flash > 0.0:
            return "hurt"
        if self.attack_pose > 0.0:
            return "attack"
        return "moving"
