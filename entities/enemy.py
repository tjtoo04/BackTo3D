"""Shared enemy behaviour: health, knockback, hurt flash and death."""

import combat
import settings
from entities.entity import Entity


class Enemy(Entity):
    """Base class for the four enemy types."""

    contact_damage = settings.ENEMY_CONTACT_DAMAGE

    def __init__(self, animation_set, x, y, radius, hp):
        super().__init__(animation_set, x, y, radius)
        self.hp = hp
        self.max_hp = hp
        self.hurt_flash = 0.0
        self.dying = 0.0
        self.attack_pose = 0.0
        self.knock_vx = 0.0
        self.knock_vy = 0.0

    def alive(self):
        return self.hp > 0 and self.dying <= 0.0

    def think(self, dt, player, room):
        """Set self.vx and self.vy. Overridden by each enemy type."""

    def take_damage(self, amount, source_x, source_y):
        """Apply a hit. Returns True when the hit killed the enemy."""
        if not self.alive():
            return False
        self.hp -= amount
        self.hurt_flash = settings.ENEMY_HURT_FLASH_TIME
        if self.hp <= 0:
            self.hp = 0
            self.dying = settings.ENEMY_DEATH_TIME
            self.vx = self.vy = 0.0
            return True
        self.knock_vx, self.knock_vy = combat.scaled_velocity(
            self.x - source_x, self.y - source_y, settings.ENEMY_KNOCKBACK
        )
        return False

    def update(self, dt, player, room):
        if self.dying > 0.0:
            self.dying = combat.step_timer(self.dying, dt)
            self.animator.play("death")
            self.animator.update(dt)
            self.sync_sprite()
            if self.dying == 0.0:
                self.dead = True
            return

        self.hurt_flash = combat.step_timer(self.hurt_flash, dt)
        self.attack_pose = combat.step_timer(self.attack_pose, dt)
        self.think(dt, player, room)

        self.actor.x += (self.vx + self.knock_vx) * dt
        self.actor.y += (self.vy + self.knock_vy) * dt
        decay = max(0.0, 1.0 - settings.ENEMY_KNOCKBACK_DECAY * dt)
        self.knock_vx *= decay
        self.knock_vy *= decay
        self.clamp(room)

        self.animator.play(self.animation_state())
        self.animator.update(dt)
        self.sync_sprite()

    def animation_state(self) -> str:
        if self.hurt_flash > 0.0:
            return "hurt"
        if abs(self.vx) + abs(self.vy) > 1.0:
            return "moving"
        return "idle"
