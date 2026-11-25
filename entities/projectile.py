"""A shot in flight: a direction, a speed and a lifetime."""

import combat


class Projectile:
    """Shared flight for the hero's tears and the enemies' shots."""

    def __init__(self, x, y, angle, speed, radius, life):
        self.x = x
        self.y = y
        self.dx, self.dy = combat.direction_from_angle(angle)
        self.speed = speed
        self.radius = radius
        self.life = life
        self.dead = False

    def update(self, dt, room):
        """Advance one frame. The shot dies on its timer or at the wall."""
        self.life -= dt
        self.x += self.dx * self.speed * dt
        self.y += self.dy * self.speed * dt
        if self.life <= 0.0 or not room.contains(self.x, self.y):
            self.dead = True
