"""Scenes: the menu, the run, the pause overlay and the two endings.

A scene owns one full-screen mode.
"""

from pgzero.builtins import keyboard
from pygame import Rect

import combat
import drawing
import progression
import settings
from entities import PLAYER_ANIMATIONS, Entity, Player
from keymap import keys
from rooms import (
    WAVE_MOB_ONE,
    WAVE_MOB_TWO,
    BossRoom,
    ItemRoom,
    MobRoom,
    TutorialRoom,
)

MENU_ENTRIES = ("play", "music", "sound", "quit")
PAUSE_ENTRIES = ("resume", "music", "sound", "menu")


class Scene:
    """One full-screen mode."""

    def __init__(self, game):
        self.game = game

    @property
    def audio(self):
        return self.game.audio

    def handle_key(self, key):
        """React to a key press."""

    def handle_key_up(self, key):
        """React to a key release."""

    def update(self, dt):
        """Advance the scene."""

    def draw(self, screen):
        """Draw the scene."""


class MenuScene(Scene):
    """The title screen: play, music, sound and quit."""

    def __init__(self, game):
        super().__init__(game)
        self.index = 0
        self.elapsed = 0.0
        self.figure = Entity(PLAYER_ANIMATIONS, settings.WIDTH // 2, 612, 0.0)
        self.audio.play_music("menu")

    def labels(self):
        return [
            "PLAY",
            self.audio.music_label(),
            self.audio.sound_label(),
            "QUIT",
        ]

    def handle_key(self, key):
        if key == keys.UP:
            self.move(-1)
        elif key == keys.DOWN:
            self.move(1)
        elif key in (keys.RETURN, keys.KP_ENTER, keys.SPACE):
            self.activate()

    def move(self, step):
        self.index = (self.index + step) % len(MENU_ENTRIES)
        self.audio.play_sound("select")

    def activate(self):
        entry = MENU_ENTRIES[self.index]
        if entry == "play":
            self.game.start_run()
        elif entry == "music":
            self.audio.toggle_music()
            self.audio.play_sound("select")
        elif entry == "sound":
            self.audio.toggle_sound()
            self.audio.play_sound("select")
        else:
            self.game.quit()

    def update(self, dt):
        self.elapsed += dt
        self.figure.animator.update(dt)
        self.figure.sync_sprite()

    def draw(self, screen):
        self.draw_background(screen)
        self.draw_title(screen)
        self.draw_entries(screen)
        self.figure.draw(screen)
        drawing.draw_text(
            screen, "UP / DOWN   ENTER", (settings.WIDTH // 2, 700), 15,
            settings.HUD_DIM, anchor="center")

    def draw_background(self, screen):
        bands = 24
        height = settings.HEIGHT / bands
        for index in range(bands):
            amount = index / (bands - 1)
            colour = drawing.blend((15, 13, 21), (46, 35, 54), amount)
            screen.draw.filled_rect(
                Rect(0, index * height, settings.WIDTH, height + 1), colour)

        for index in range(9):
            travel = self.elapsed * (20 + index * 6) + index * 130
            x = travel % (settings.WIDTH + 120) - 60
            y = 90 + (index * 71) % (settings.HEIGHT - 170)
            radius = 4 + index % 3
            screen.draw.filled_circle((x, y), radius + 2, settings.TEAR_EDGE)
            screen.draw.filled_circle((x, y), radius, settings.TEAR_CORE)

    def draw_title(self, screen):
        drawing.draw_text(
            screen, "BACK TO 3D", (settings.WIDTH // 2, 78), 68,
            settings.GOLD, anchor="midtop", outline=settings.BLACK)
        drawing.draw_text(
            screen, "a 3D hero lost in a 2D world",
            (settings.WIDTH // 2, 164), 21, settings.HUD_TEXT,
            anchor="midtop", outline=settings.BLACK)

    def draw_entries(self, screen):
        labels = self.labels()
        top = 300
        spacing = 56
        for index, label in enumerate(labels):
            selected = index == self.index
            y = top + index * spacing
            if selected:
                screen.draw.filled_rect(
                    Rect(settings.WIDTH // 2 - 195, y - 23, 390, 46),
                    settings.PANEL)
                screen.draw.rect(
                    Rect(settings.WIDTH // 2 - 195, y - 23, 390, 46),
                    settings.GOLD)
                screen.draw.filled_circle(
                    (settings.WIDTH // 2 - 172, y), 6, settings.TEAR_EDGE)
            drawing.draw_text(
                screen, label, (settings.WIDTH // 2, y),
                31 if selected else 26,
                settings.GOLD if selected else settings.HUD_TEXT,
                anchor="center", outline=settings.BLACK)


class PlayScene(Scene):
    """A run: one room at a time, from the tutorial to the boss."""

    def __init__(self, game):
        super().__init__(game)
        self.player = Player(0.0, 0.0)
        self.curtain = 1.0
        self.room = self.build_room(progression.ROOM_TUTORIAL)
        self.prepare_room()

    # ------------------------------------------------------------ rooms

    def build_room(self, room_id):
        if room_id == progression.ROOM_TUTORIAL:
            return TutorialRoom(self.audio)
        if room_id == progression.ROOM_MOB_ONE:
            return MobRoom(room_id, self.audio, WAVE_MOB_ONE)
        if room_id == progression.ROOM_ITEM:
            return ItemRoom(self.audio)
        if room_id == progression.ROOM_MOB_TWO:
            return MobRoom(room_id, self.audio, WAVE_MOB_TWO)
        return BossRoom(self.audio)

    def load_room(self, room_id):
        self.room = self.build_room(room_id)
        self.prepare_room()

    def prepare_room(self):
        self.room.spawn_player(self.player)
        self.curtain = 1.0
        self.audio.play_music(self.room.music())

    def leave_room(self):
        following = progression.next_room(self.room.room_id)
        if following is None:
            self.game.end_run(won=True)
            return
        self.audio.play_sound("door")
        self.load_room(following)

    # ------------------------------------------------------------ input

    def handle_key(self, key):
        if key == keys.ESCAPE:
            self.game.pause()
        elif key in (keys.LSHIFT, keys.RSHIFT):
            self.try_dodge()
        elif key == keys.E:
            self.room.try_take(self.player)

    def move_input(self):
        """WASD, as a direction that may be diagonal."""
        horizontal = 0.0
        vertical = 0.0
        if keyboard.a:
            horizontal -= 1.0
        if keyboard.d:
            horizontal += 1.0
        if keyboard.w:
            vertical -= 1.0
        if keyboard.s:
            vertical += 1.0
        return horizontal, vertical

    def aim_input(self):
        """Arrow keys, as a shooting direction."""
        horizontal = 0.0
        vertical = 0.0
        if keyboard.left:
            horizontal -= 1.0
        if keyboard.right:
            horizontal += 1.0
        if keyboard.up:
            vertical -= 1.0
        if keyboard.down:
            vertical += 1.0
        return horizontal, vertical

    def try_dodge(self):
        horizontal, vertical = self.move_input()
        if self.player.start_dodge(horizontal, vertical):
            self.audio.play_sound("dodge")

    # ------------------------------------------------------------ frame

    def update(self, dt):
        self.curtain = combat.step_timer(self.curtain, dt * 2.4)
        horizontal, vertical = self.move_input()
        self.player.update(dt, self.room, horizontal, vertical)
        self.handle_shooting()
        self.room.update(dt, self.player)

        if not self.player.is_alive():
            self.game.end_run(won=False)
        elif self.room.door_open() and self.room.player_at_exit(self.player):
            self.leave_room()

    def handle_shooting(self):
        aim_x, aim_y = self.aim_input()
        if aim_x == 0.0 and aim_y == 0.0:
            return
        self.player.facing = combat.angle_from_direction(aim_x, aim_y)
        tears = self.player.shoot()
        if tears:
            self.room.tears.extend(tears)
            self.audio.play_sound("shoot")

    def draw(self, screen):
        self.room.draw(screen, self.player)
        self.game.hud.draw(screen, self.player, self.room)
        self.draw_curtain(screen)

    def draw_curtain(self, screen):
        """A letterbox shutter that opens as a room loads."""
        if self.curtain <= 0.0:
            return
        half = int(settings.HEIGHT * self.curtain / 2)
        if half <= 0:
            return
        screen.draw.filled_rect(
            Rect(0, 0, settings.WIDTH, half), settings.BLACK)
        screen.draw.filled_rect(
            Rect(0, settings.HEIGHT - half, settings.WIDTH, half),
            settings.BLACK)


class PauseScene(Scene):
    """The pause overlay, drawn over a frozen run."""

    def __init__(self, game, play_scene):
        super().__init__(game)
        self.play_scene = play_scene
        self.index = 0

    def labels(self):
        return [
            "RESUME",
            self.audio.music_label(),
            self.audio.sound_label(),
            "QUIT TO MENU",
        ]

    def handle_key(self, key):
        if key == keys.ESCAPE:
            self.game.resume()
        elif key == keys.UP:
            self.move(-1)
        elif key == keys.DOWN:
            self.move(1)
        elif key in (keys.RETURN, keys.KP_ENTER, keys.SPACE):
            self.activate()

    def move(self, step):
        self.index = (self.index + step) % len(PAUSE_ENTRIES)
        self.audio.play_sound("select")

    def activate(self):
        entry = PAUSE_ENTRIES[self.index]
        if entry == "resume":
            self.game.resume()
        elif entry == "music":
            self.audio.toggle_music()
            self.audio.play_sound("select")
        elif entry == "sound":
            self.audio.toggle_sound()
            self.audio.play_sound("select")
        else:
            self.game.show_menu()

    def draw(self, screen):
        self.play_scene.draw(screen)
        band_top = settings.HEIGHT // 2 - 170
        screen.draw.filled_rect(
            Rect(0, band_top, settings.WIDTH, 340), settings.BLACK)
        drawing.draw_text(
            screen, "PAUSED", (settings.WIDTH // 2, band_top + 26), 34,
            settings.GOLD, anchor="midtop")

        labels = self.labels()
        for index, label in enumerate(labels):
            selected = index == self.index
            y = band_top + 96 + index * 44
            drawing.draw_text(
                screen, label, (settings.WIDTH // 2, y),
                25 if selected else 21,
                settings.GOLD if selected else settings.HUD_TEXT,
                anchor="center")
            if selected:
                screen.draw.filled_circle(
                    (settings.WIDTH // 2 - 150, y), 5, settings.TEAR_EDGE)


class EndScene(Scene):
    """Shared ending screen: a title, a line and two choices."""

    title = "THE END"
    subtitle = ""
    sting = None
    entry_labels = ("PLAY AGAIN", "MAIN MENU")
    entry_keys = ("again", "menu")

    def __init__(self, game):
        super().__init__(game)
        self.index = 0
        self.audio.stop_music()
        if self.sting is not None:
            self.audio.play_sound(self.sting)

    def handle_key(self, key):
        if key == keys.UP:
            self.move(-1)
        elif key == keys.DOWN:
            self.move(1)
        elif key in (keys.RETURN, keys.KP_ENTER, keys.SPACE):
            self.activate()

    def move(self, step):
        self.index = (self.index + step) % len(self.entry_keys)
        self.audio.play_sound("select")

    def activate(self):
        if self.entry_keys[self.index] == "again":
            self.game.start_run()
        else:
            self.game.show_menu()

    def draw(self, screen):
        screen.draw.filled_rect(
            Rect(0, 0, settings.WIDTH, settings.HEIGHT), settings.BLACK)
        drawing.draw_text(
            screen, self.title, (settings.WIDTH // 2, 210), 62,
            settings.GOLD, anchor="midtop")
        drawing.draw_text(
            screen, self.subtitle, (settings.WIDTH // 2, 292), 22,
            settings.HUD_TEXT, anchor="midtop")

        for index, label in enumerate(self.entry_labels):
            selected = index == self.index
            y = 420 + index * 58
            drawing.draw_text(
                screen, label, (settings.WIDTH // 2, y),
                30 if selected else 25,
                settings.GOLD if selected else settings.HUD_DIM,
                anchor="center")
            if selected:
                screen.draw.filled_circle(
                    (settings.WIDTH // 2 - 150, y), 6, settings.TEAR_EDGE)


class WinScene(EndScene):
    title = "YOU ESCAPED"
    subtitle = "the door closes on the 2D world"
    sting = "win"


class GameOverScene(EndScene):
    title = "GAME OVER"
    subtitle = "the 2D world keeps you"
    sting = "lose"
