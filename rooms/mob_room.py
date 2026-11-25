"""The fight rooms, and the wave tables they spawn from."""

import settings
from entities import ENEMY_TYPES
from rooms.room import Room

# Enemy placements, as fractions of the walkable floor.
WAVE_MOB_ONE = (
    ("blob", 0.28, 0.26),
    ("blob", 0.72, 0.24),
    ("blob", 0.50, 0.52),
)

WAVE_MOB_TWO = (
    ("cube", 0.24, 0.22),
    ("cube", 0.76, 0.22),
    ("spider", 0.28, 0.64),
    ("spider", 0.72, 0.64),
    ("spider", 0.50, 0.40),
)


class MobRoom(Room):
    """A fight room. The wave is a list of enemy type and floor fractions."""

    def __init__(self, room_id, audio, wave):
        super().__init__(room_id, settings.ROOM_MOB_IMAGE, audio)
        self.wave = wave
        self.spawn_wave()

    def spawn_wave(self):
        left, top, right, bottom = self.floor
        width = right - left
        height = bottom - top
        for enemy_key, fraction_x, fraction_y in self.wave:
            enemy_type = ENEMY_TYPES[enemy_key]
            self.enemies.append(enemy_type(
                left + width * fraction_x,
                top + height * fraction_y))
