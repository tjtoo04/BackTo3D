"""Room five: the Glitch Master and its health bar."""

from pygame import Rect

import combat
import drawing
import progression
import settings
from entities import GlitchMaster
from rooms.room import Room


class BossRoom(Room):
    """One Glitch Master. The run ends at its door."""

    music_track = "boss"

    def __init__(self, audio):
        super().__init__(progression.ROOM_BOSS,
                         settings.ROOM_BOSS_IMAGE, audio)
        left, top, right, bottom = self.floor
        self.boss = GlitchMaster(
            (left + right) / 2.0, top + (bottom - top) * 0.32)
        self.enemies.append(self.boss)
        audio.play_sound("boss_roar")

    def draw(self, screen, player):
        super().draw(screen, player)
        self.draw_boss_bar(screen)

    def draw_boss_bar(self, screen):
        if not self.boss.alive():
            return
        ratio = combat.health_ratio(self.boss.hp, self.boss.max_hp)
        width = 430
        left = settings.WIDTH // 2 - width // 2
        top = 12
        screen.draw.filled_rect(Rect(left, top, width, 15), settings.PANEL)
        screen.draw.filled_rect(
            Rect(left, top, int(width * ratio), 15), settings.HEART_FULL)
        screen.draw.rect(Rect(left, top, width, 15), settings.CREAM)
        drawing.draw_text(
            screen, f"GLITCH MASTER  PHASE {self.boss.current_phase()}",
            (settings.WIDTH // 2, top + 22), 13, settings.HUD_TEXT,
            anchor="midtop", outline=settings.BLACK)
