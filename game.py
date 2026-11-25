"""Entry point of the game

Run with `pgzrun game.py` from this folder.
"""

from pgzero.builtins import exit as pgz_exit
from pgzero.screen import Screen

import audio
import hud
import settings
from scenes import GameOverScene, MenuScene, PauseScene, PlayScene, WinScene

WIDTH = settings.WIDTH
HEIGHT = settings.HEIGHT


class Game:
    """Holds the shared services and the current scene."""

    def __init__(self):
        self.audio = audio.AudioManager()
        self.hud = hud.HUD()
        self.scene = MenuScene(self)

    def start_run(self):
        self.scene = PlayScene(self)

    def pause(self):
        if isinstance(self.scene, PlayScene):
            self.scene = PauseScene(self, self.scene)

    def resume(self):
        if isinstance(self.scene, PauseScene):
            self.scene = self.scene.play_scene

    def show_menu(self):
        self.scene = MenuScene(self)

    def end_run(self, won):
        self.scene = WinScene(self) if won else GameOverScene(self)

    def quit(self):
        self.audio.stop_music()
        pgz_exit()


_game = Game()


def update(dt):
    _game.scene.update(min(dt, 0.05))


def draw():
    surface: Screen = globals()["screen"]
    surface.clear()
    _game.scene.draw(surface)


def on_key_down(key):
    _game.scene.handle_key(key)


def on_key_up(key):
    _game.scene.handle_key_up(key)
