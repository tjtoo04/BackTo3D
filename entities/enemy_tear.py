"""A projectile fired by an enemy."""

import settings
from entities.projectile import Projectile


class EnemyTear(Projectile):
    def __init__(self, x, y, angle, speed=None, damage=None):
        super().__init__(
            x,
            y,
            angle,
            settings.ENEMY_TEAR_SPEED if speed is None else speed,
            settings.ENEMY_TEAR_RADIUS,
            settings.ENEMY_TEAR_LIFETIME,
        )
        self.damage = settings.ENEMY_TEAR_DAMAGE if damage is None else damage

    def draw(self, screen):
        screen.draw.filled_circle(
            (self.x, self.y), self.radius + 2.0, settings.ENEMY_TEAR_EDGE
        )
        screen.draw.filled_circle(
            (self.x, self.y), self.radius, settings.ENEMY_TEAR_CORE
        )
