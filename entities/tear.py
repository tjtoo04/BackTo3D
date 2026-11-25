"""The hero's projectile."""

import combat
import settings
from entities.projectile import Projectile


class Tear(Projectile):
    """A tear. Drawn with primitives, so it needs no art."""

    def __init__(self, x, y, angle, attack):
        super().__init__(
            x, y, angle, attack.speed, settings.TEAR_RADIUS, settings.TEAR_LIFETIME
        )
        self.damage = attack.damage
        self.pierce = attack.pierce

    def is_laser(self):
        return self.pierce == combat.INFINITE_PIERCE

    def hit(self, enemy):
        """Register a hit and report whether the hit killed the enemy."""
        killed = enemy.take_damage(self.damage, self.x, self.y)
        self.pierce = combat.consume_pierce(self.pierce)
        if combat.is_spent(self.pierce):
            self.dead = True
        return killed

    def draw(self, screen):
        if self.is_laser():
            for step in range(6):
                fade = step / 5.0
                centre = (
                    self.x - self.dx * 34.0 * fade,
                    self.y - self.dy * 34.0 * fade,
                )
                screen.draw.filled_circle(
                    centre, self.radius * (1.0 - 0.45 * fade), settings.LASER_EDGE
                )
            screen.draw.filled_circle(
                (self.x, self.y), self.radius * 0.55, settings.LASER_CORE
            )
            return
        screen.draw.filled_circle(
            (self.x, self.y), self.radius + 1.5, settings.TEAR_EDGE
        )
        screen.draw.filled_circle(
            (self.x, self.y), self.radius - 2.0, settings.TEAR_CORE
        )
