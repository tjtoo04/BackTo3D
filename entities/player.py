"""The hero."""

import math

import combat
import items
import settings
from animation import AnimationSet
from entities.entity import Entity
from entities.tear import Tear

PLAYER_ANIMATIONS = AnimationSet(
    "player",
    {
        "idle": ["idle_1", "idle_2", "idle_3", "idle_4"],
        "moving": ["moving_1", "moving_2", "moving_3", "moving_4"],
        "attack": ["attack_1", "attack_2", "attack_3"],
        "hurt": ["hurt_1", "hurt_2"],
        "dodge": [
            "dodge_1",
            "dodge_2",
            "dodge_3",
            "dodge_4",
            "dodge_5",
            "dodge_6",
            "dodge_7",
            "dodge_8",
        ],
    },
    rates={"dodge": 30, "attack": 16},
)


class Player(Entity):
    """The hero. Owns health, the attack numbers and the dodge."""

    def __init__(self, x, y):
        super().__init__(PLAYER_ANIMATIONS, x, y, settings.PLAYER_RADIUS)
        self.hp = settings.PLAYER_MAX_HP
        self.max_hp = settings.PLAYER_MAX_HP
        self.attack = combat.base_attack()
        self.item = None
        self.cooldown = 0.0
        self.invulnerable = 0.0
        self.hurt_flash = 0.0
        self.attack_pose = 0.0
        self.dodge_timer = 0.0
        self.dodge_cooldown = 0.0
        self.facing = 90.0
        self.moving = False
        self.knock_vx = 0.0
        self.knock_vy = 0.0

    # state

    def is_dodging(self):
        return self.dodge_timer > 0.0

    def is_alive(self):
        return self.hp > 0

    def visible(self):
        """The hero blinks while invulnerable."""
        if self.invulnerable <= 0.0:
            return True
        return math.floor(self.invulnerable * 16) % 2 == 0

    # actions

    def start_dodge(self, move_x, move_y):
        """Begin a dodge. Returns True when the dodge started."""
        if self.dodge_cooldown > 0.0 or self.dodge_timer > 0.0:
            return False
        dx, dy = move_x, move_y
        if dx == 0 and dy == 0:
            dx, dy = combat.direction_from_angle(self.facing)
        self.vx, self.vy = combat.scaled_velocity(dx, dy, settings.PLAYER_DODGE_SPEED)
        self.dodge_timer = settings.PLAYER_DODGE_TIME
        self.dodge_cooldown = (
            settings.PLAYER_DODGE_TIME + settings.PLAYER_DODGE_COOLDOWN
        )
        self.invulnerable = max(self.invulnerable, settings.PLAYER_DODGE_TIME)
        return True

    def shoot(self):
        """Fire if ready. Returns the new tears, which may be an empty list."""
        if self.dodge_timer > 0.0 or self.cooldown > 0.0:
            return []
        self.cooldown = self.attack.cooldown
        self.attack_pose = settings.PLAYER_ATTACK_POSE_TIME
        tears = []
        for angle in combat.spread_angles(
            self.facing, self.attack.projectiles, self.attack.spread
        ):
            dx, dy = combat.direction_from_angle(angle)
            tears.append(
                Tear(
                    self.x + dx * settings.TEAR_SPAWN_OFFSET,
                    self.y + dy * settings.TEAR_SPAWN_OFFSET,
                    angle,
                    self.attack,
                )
            )
        return tears

    def take_damage(self, amount, source_x, source_y):
        """Apply a hit. Returns False when the hit was ignored."""
        if self.invulnerable > 0.0 or self.dodge_timer > 0.0:
            return False
        self.hp = max(0, self.hp - amount)
        self.invulnerable = settings.PLAYER_INVULNERABLE_TIME
        self.hurt_flash = settings.PLAYER_HURT_FLASH_TIME
        self.knock_vx, self.knock_vy = combat.scaled_velocity(
            self.x - source_x, self.y - source_y, settings.PLAYER_HIT_KNOCKBACK
        )
        return True

    def equip(self, item):
        """Apply an item to the current attack numbers."""
        self.attack = items.apply_item(self.attack, item)
        self.item = item

    # frame

    def update(self, dt, room, move_x, move_y):
        self.cooldown = combat.step_timer(self.cooldown, dt)
        self.invulnerable = combat.step_timer(self.invulnerable, dt)
        self.hurt_flash = combat.step_timer(self.hurt_flash, dt)
        self.attack_pose = combat.step_timer(self.attack_pose, dt)
        self.dodge_cooldown = combat.step_timer(self.dodge_cooldown, dt)

        if self.dodge_timer > 0.0:
            self.dodge_timer = combat.step_timer(self.dodge_timer, dt)
        else:
            self.vx, self.vy = combat.scaled_velocity(
                move_x, move_y, settings.PLAYER_SPEED
            )
            self.moving = bool(move_x or move_y)
            if self.moving:
                self.facing = combat.angle_from_direction(move_x, move_y)

        self.actor.x += (self.vx + self.knock_vx) * dt
        self.actor.y += (self.vy + self.knock_vy) * dt
        decay = max(0.0, 1.0 - settings.PLAYER_KNOCKBACK_DECAY * dt)
        self.knock_vx *= decay
        self.knock_vy *= decay
        self.clamp(room)

        self.animator.play(self.animation_state())
        self.animator.update(dt)
        self.sync_sprite()

    def animation_state(self):
        if self.dodge_timer > 0.0:
            return "dodge"
        if self.hurt_flash > 0.0:
            return "hurt"
        if self.attack_pose > 0.0:
            return "attack"
        if self.moving:
            return "moving"
        return "idle"

    def draw(self, screen):
        if self.visible():
            screen.blit(self._sprite, self.actor.topleft)
