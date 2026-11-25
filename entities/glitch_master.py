"""The boss."""

import math

import combat
import progression
import settings
from animation import AnimationSet
from entities.enemy import Enemy

BOSS_ANIMATIONS = AnimationSet(
    "boss",
    {
        "idle": ["idle"],
        "moving": ["moving_1", "moving_2", "moving_3"],
        "attack": ["attack"],
        "hurt": ["hurt"],
        "death": ["death"],
    },
)


class GlitchMaster(Enemy):
    """Fires bursts and, from phase two, dashes at the hero."""

    def __init__(self, x, y):
        super().__init__(BOSS_ANIMATIONS, x, y, settings.BOSS_RADIUS, settings.BOSS_HP)
        self.burst_timer = 1.5
        self.bursts = 0
        self.spin = 0.0
        self.dash_timer = 0.0
        self.dash_x = 0.0
        self.dash_y = 0.0
        self.phase = 1

    def current_phase(self):
        return progression.boss_phase(combat.health_ratio(self.hp, self.max_hp))

    def think(self, dt, player, room):
        self.phase = self.current_phase()
        self.spin += dt * (2.0 + 0.6 * self.phase)

        self.dash_timer = combat.step_timer(self.dash_timer, dt)
        if self.dash_timer > 0.0:
            self.vx = self.dash_x * settings.BOSS_DASH_SPEED
            self.vy = self.dash_y * settings.BOSS_DASH_SPEED
        else:
            distance = math.hypot(player.x - self.x, player.y - self.y)
            if distance > 130.0:
                speed = settings.BOSS_SPEED * (1.0 + 0.3 * (self.phase - 1))
                self.vx, self.vy = combat.scaled_velocity(
                    player.x - self.x, player.y - self.y, speed
                )
            else:
                self.vx = self.vy = 0.0

        self.burst_timer -= dt
        if self.burst_timer <= 0.0:
            self.burst_timer = settings.BOSS_BURST_INTERVAL / (
                1.0 + 0.28 * (self.phase - 1)
            )
            self.fire(room, player)

    def fire(self, room, player):
        self.bursts += 1
        if self.phase == 1:
            self.radial(room, 10, 0.0)
        elif self.phase == 2:
            self.radial(room, 12, self.spin * 22.0)
        else:
            self.radial(room, 16, self.spin * 28.0)
        self.attack_pose = 0.45

        if self.phase >= 2 and self.bursts % 2 == 0:
            self.dash_timer = settings.BOSS_DASH_TIME
            self.dash_x, self.dash_y = combat.unit_vector(
                player.x - self.x, player.y - self.y
            )

    def radial(self, room, count, offset):
        step = 360.0 / count
        for index in range(count):
            room.spawn_enemy_tear(self.x, self.y, offset + step * index)

    def animation_state(self):
        if self.hurt_flash > 0.0:
            return "hurt"
        if self.attack_pose > 0.0:
            return "attack"
        if abs(self.vx) + abs(self.vy) > 1.0:
            return "moving"
        return "idle"
