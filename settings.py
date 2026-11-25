"""Tuning values and shared constants.

Everything a designer would want to change lives here.
"""

# ---------------------------------------------------------------- window

WIDTH = 1024
HEIGHT = 768

# ---------------------------------------------------------------- room art

ROOM_MOB_IMAGE = "rooms/mob"
ROOM_BOSS_IMAGE = "rooms/boss"

# Walkable floor, as a fraction of the room image. The walls of both room
# drawings sit at the same relative place, so one set of numbers serves both.
FLOOR_LEFT = 0.195
FLOOR_RIGHT = 0.8155
FLOOR_TOP = 0.159
FLOOR_BOTTOM = 0.849

# Door openings are centred on the room, top and bottom.
DOOR_CENTRE_X = 0.49
DOOR_HALF_WIDTH = 0.062

# ---------------------------------------------------------------- player

PLAYER_MAX_HP = 6
PLAYER_SPEED = 215.0
PLAYER_RADIUS = 15.0
PLAYER_INVULNERABLE_TIME = 0.9
PLAYER_DODGE_TIME = 0.28
PLAYER_DODGE_SPEED = 560.0
PLAYER_DODGE_COOLDOWN = 0.7
PLAYER_HIT_KNOCKBACK = 210.0
PLAYER_KNOCKBACK_DECAY = 6.0
PLAYER_HURT_FLASH_TIME = 0.45
PLAYER_ATTACK_POSE_TIME = 0.18

# ---------------------------------------------------------------- combat

BASE_DAMAGE = 1.0
BASE_COOLDOWN = 0.26
BASE_PIERCE = 1
BASE_PROJECTILES = 1
BASE_SPREAD = 0.0

TEAR_SPEED = 430.0
TEAR_RADIUS = 7.0
TEAR_LIFETIME = 1.4
TEAR_SPAWN_OFFSET = 22.0
ENEMY_TEAR_SPEED = 190.0
ENEMY_TEAR_RADIUS = 8.0
ENEMY_TEAR_LIFETIME = 3.2
ENEMY_TEAR_DAMAGE = 1
ENEMY_CONTACT_DAMAGE = 1
ENEMY_KNOCKBACK = 150.0
ENEMY_KNOCKBACK_DECAY = 7.0
ENEMY_HURT_FLASH_TIME = 0.14
ENEMY_DEATH_TIME = 0.45

# ---------------------------------------------------------------- enemies

BLOB_HP = 4
BLOB_SPEED = 58.0
BLOB_RADIUS = 26.0

CUBE_HP = 7
CUBE_RADIUS = 27.0
CUBE_IDLE_TIME = 0.9
CUBE_WINDUP_TIME = 0.4
CUBE_CHARGE_SPEED = 430.0
CUBE_CHARGE_TIME = 0.5
CUBE_RECOVER_TIME = 0.6

SPIDER_HP = 3
SPIDER_SPEED = 122.0
SPIDER_RADIUS = 24.0
SPIDER_ORBIT = 155.0
SPIDER_SHOOT_INTERVAL = 2.0

BOSS_HP = 45
BOSS_SPEED = 52.0
BOSS_RADIUS = 58.0
BOSS_BURST_INTERVAL = 2.1
BOSS_DASH_SPEED = 330.0
BOSS_DASH_TIME = 0.45

# ---------------------------------------------------------------- animation

FRAME_RATE = 10
FAST_FRAME_RATE = 14

# ---------------------------------------------------------------- interface

TITLE = "BackTo3d"
MENU_X = WIDTH // 2
FLOOR_COLOUR = (24, 22, 28)

# Seconds the hero keeps a speech bubble after spawning.
SPEECH_TIME = 3.5

# ---------------------------------------------------------------- palette

WHITE = (255, 255, 255)
BLACK = (12, 10, 16)
CREAM = (240, 228, 202)
GOLD = (255, 208, 92)
TEAR_CORE = (255, 252, 214)
TEAR_EDGE = (255, 186, 56)
LASER_CORE = (226, 255, 252)
LASER_EDGE = (86, 224, 240)
ENEMY_TEAR_CORE = (226, 158, 255)
ENEMY_TEAR_EDGE = (120, 48, 190)
HEART_FULL = (222, 46, 62)
HEART_HALF = (222, 46, 62)
HEART_EMPTY = (74, 60, 66)
HEART_SHINE = (255, 168, 168)
HUD_DIM = (150, 140, 146)
HUD_TEXT = (232, 224, 210)
DOOR_GLOW = (255, 214, 120)
PANEL = (18, 16, 22)
