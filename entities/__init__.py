"""The actors of the game: the hero, the enemies and the projectiles.

One entity per file.
"""

from entities.blob import BLOB_ANIMATIONS, Blob
from entities.chomper_cube import CUBE_ANIMATIONS, ChomperCube
from entities.enemy import Enemy
from entities.enemy_tear import EnemyTear
from entities.entity import Entity
from entities.glitch_master import BOSS_ANIMATIONS, GlitchMaster
from entities.paperclip_spider import SPIDER_ANIMATIONS, PaperclipSpider
from entities.player import PLAYER_ANIMATIONS, Player
from entities.projectile import Projectile
from entities.tear import Tear

# the enemy keys the wave data in rooms/ uses
ENEMY_TYPES = {
    "blob": Blob,
    "cube": ChomperCube,
    "spider": PaperclipSpider,
}

__all__ = [
    "BLOB_ANIMATIONS",
    "BOSS_ANIMATIONS",
    "Blob",
    "CUBE_ANIMATIONS",
    "ChomperCube",
    "ENEMY_TYPES",
    "Enemy",
    "EnemyTear",
    "Entity",
    "GlitchMaster",
    "PLAYER_ANIMATIONS",
    "PaperclipSpider",
    "Player",
    "Projectile",
    "SPIDER_ANIMATIONS",
    "Tear",
]
