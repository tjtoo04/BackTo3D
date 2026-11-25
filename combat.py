"""Combat arithmetic. Collision logic taken from Google. Imports only math and settings."""

import math

import settings

# -1 means the projectile never runs out of pierce.
INFINITE_PIERCE = -1


class AttackStats:
    """One immutable snapshot of the hero's attack numbers."""

    __slots__ = ("damage", "cooldown", "pierce", "projectiles", "spread", "speed")

    def __init__(self, damage, cooldown, pierce, projectiles, spread, speed):
        self.damage = damage
        self.cooldown = cooldown
        self.pierce = pierce
        self.projectiles = projectiles
        self.spread = spread
        self.speed = speed

    def replace(self, **changes):
        """Return a copy with the given fields changed."""
        values = {name: getattr(self, name) for name in self.__slots__}
        values.update(changes)
        return AttackStats(**values)

    def __eq__(self, other):
        if not isinstance(other, AttackStats):
            return NotImplemented
        return all(
            getattr(self, name) == getattr(other, name) for name in self.__slots__
        )

    def __repr__(self):
        fields = ", ".join(f"{name}={getattr(self, name)!r}" for name in self.__slots__)
        return f"AttackStats({fields})"


def base_attack():
    """The attack the hero starts every run with."""
    return AttackStats(
        damage=settings.BASE_DAMAGE,
        cooldown=settings.BASE_COOLDOWN,
        pierce=settings.BASE_PIERCE,
        projectiles=settings.BASE_PROJECTILES,
        spread=settings.BASE_SPREAD,
        speed=settings.TEAR_SPEED,
    )


def spread_angles(base_degrees, count, spread_degrees):
    """Return `count` firing angles fanned around `base_degrees`."""
    if count <= 1:
        return [base_degrees]
    step = spread_degrees / (count - 1)
    first = base_degrees - spread_degrees / 2.0
    return [first + step * index for index in range(count)]


def circle_overlap(ax, ay, ar, bx, by, br):
    """True when two circles touch or overlap."""
    return (ax - bx) ** 2 + (ay - by) ** 2 <= (ar + br) ** 2


def damage_after_armour(damage, armour=0.0):
    """Damage left after armour absorbs part of it. Never negative."""
    return max(0.0, damage - armour)


def clamp_to_rect(x, y, radius, left, top, right, bottom):
    """Keep a circle of `radius` inside a rectangle."""
    low_x, high_x = left + radius, right - radius
    low_y, high_y = top + radius, bottom - radius
    if low_x > high_x:
        low_x = high_x = (left + right) / 2.0
    if low_y > high_y:
        low_y = high_y = (top + bottom) / 2.0
    return min(max(x, low_x), high_x), min(max(y, low_y), high_y)


def step_timer(value, dt):
    """Count a timer down to zero."""
    return max(0.0, value - dt)


def direction_from_angle(degrees):
    """Unit vector for an angle measured counter-clockwise from the right.

    Screen y grows downwards, so an upward angle yields a negative y.
    """
    radians = math.radians(degrees)
    return math.cos(radians), -math.sin(radians)


def angle_from_direction(dx, dy):
    """Angle in degrees for a screen-space direction vector."""
    return math.degrees(math.atan2(-dy, dx))


def unit_vector(dx, dy):
    """Normalised direction, or a zero vector when the input has no length."""
    length = math.hypot(dx, dy)
    if length == 0.0:
        return 0.0, 0.0
    return dx / length, dy / length


def scaled_velocity(dx, dy, speed):
    """Normalised direction multiplied by a speed."""
    ux, uy = unit_vector(dx, dy)
    return ux * speed, uy * speed


def consume_pierce(pierce):
    """Pierce value after hitting one enemy."""
    if pierce == INFINITE_PIERCE:
        return INFINITE_PIERCE
    return max(0, pierce - 1)


def is_spent(pierce):
    """True when a projectile has used up all of its pierce."""
    return pierce == 0


def health_ratio(current, maximum):
    """Current health as a 0..1 fraction, safe when maximum is zero."""
    if maximum <= 0:
        return 0.0
    return max(0.0, min(1.0, current / maximum))
