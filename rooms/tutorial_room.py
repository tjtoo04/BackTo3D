"""Room one: the control card and the hero's first words."""

from pygame import Rect

import drawing
import progression
import settings
from rooms.room import Room

SPEECH = "I must escape this 2D world!"
SPEECH_SIZE = 18
SPEECH_WIDTH = 250.0
SPEECH_HEIGHT = 48.0
SPEECH_GAP = 58.0


class TutorialRoom(Room):
    """No enemies. The door is open from the start."""

    def __init__(self, audio):
        super().__init__(progression.ROOM_TUTORIAL,
                         settings.ROOM_MOB_IMAGE, audio)
        self.speech_timer = 0.0

    def spawn_player(self, player):
        super().spawn_player(player)
        self.speech_timer = settings.SPEECH_TIME

    def update(self, dt, player):
        super().update(dt, player)
        # The hero stops talking the moment the player takes control.
        if player.moving:
            self.speech_timer = 0.0
            return
        self.speech_timer = max(0.0, self.speech_timer - dt)

    def draw(self, screen, player):
        super().draw(screen, player)
        if self.speech_timer > 0.0:
            self.draw_speech(screen, player)

    def draw_speech(self, screen, player):
        """A bubble over the hero's head, kept inside the room."""
        left, top, right, bottom = self.floor
        half = SPEECH_WIDTH / 2.0
        centre_x = max(left + half, min(right - half, player.x))
        bubble_bottom = player.y - SPEECH_GAP
        bubble_top = bubble_bottom - SPEECH_HEIGHT

        screen.draw.filled_rect(
            Rect(centre_x - half, bubble_top, SPEECH_WIDTH, SPEECH_HEIGHT),
            settings.PANEL)
        screen.draw.rect(
            Rect(centre_x - half, bubble_top, SPEECH_WIDTH, SPEECH_HEIGHT),
            settings.GOLD)
        drawing.draw_text(
            screen, SPEECH, (centre_x, bubble_top + SPEECH_HEIGHT / 2.0),
            SPEECH_SIZE, settings.WHITE, anchor="center",
            outline=settings.BLACK)

        for index, radius in enumerate((6, 3)):
            tail_y = bubble_bottom + 5.0 + index * 11.0
            screen.draw.filled_circle((centre_x, tail_y), radius,
                                      settings.PANEL)
            screen.draw.circle((centre_x, tail_y), radius, settings.GOLD)

    def draw_props(self, screen):
        left, top, right, bottom = self.floor
        width = 430
        height = 172
        panel_left = self.door_x - width / 2.0
        panel_top = top + (bottom - top) * 0.30

        screen.draw.filled_rect(
            Rect(panel_left, panel_top, width, height), settings.PANEL)
        screen.draw.rect(
            Rect(panel_left, panel_top, width, height), settings.GOLD)

        drawing.draw_text(
            screen, "A 3D HERO IN A 2D WORLD", (self.door_x, panel_top + 18),
            19, settings.GOLD, anchor="midtop", outline=settings.BLACK)

        rows = (
            ("WASD", "move"),
            ("ARROW KEYS", "shoot"),
            ("SHIFT", "dodge"),
            ("ESC", "pause"),
        )
        for index, (key_name, action) in enumerate(rows):
            row_y = panel_top + 58 + index * 27
            drawing.draw_text(screen, key_name, (panel_left + 34, row_y), 16,
                              settings.TEAR_EDGE, anchor="midleft")
            drawing.draw_text(screen, action, (panel_left + 190, row_y), 16,
                              settings.HUD_TEXT, anchor="midleft")

        drawing.draw_text(
            screen, "GO UP", (self.door_x, bottom - 26), 15,
            settings.DOOR_GLOW, anchor="center")
