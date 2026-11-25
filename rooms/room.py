"""The room base: the playfield, its contents and its door."""

import math

from pgzero.builtins import Actor
from pygame import Rect

import combat
import drawing
import progression
import settings
from entities import EnemyTear


class Room:
    """One screen of the gauntlet."""

    music_track = "battle"

    def __init__(self, room_id, image_name, audio):
        self.room_id = room_id
        self.audio = audio
        self.image_name = image_name
        self.actor = Actor(image_name)
        self.left = (settings.WIDTH - self.actor.width) // 2
        self.actor.topleft = (self.left, 0)
        self.width = self.actor.width
        self.height = self.actor.height
        self.right = self.left + self.width
        self.enemies = []
        self.tears = []
        self.enemy_tears = []
        self.item_taken = False
        self.elapsed = 0.0

    # ------------------------------------------------------------ geometry

    @property
    def floor(self):
        """The walkable rectangle, as left, top, right, bottom."""
        return (
            self.left + settings.FLOOR_LEFT * self.width,
            settings.FLOOR_TOP * self.height,
            self.left + settings.FLOOR_RIGHT * self.width,
            settings.FLOOR_BOTTOM * self.height,
        )

    @property
    def door_x(self):
        return self.left + settings.DOOR_CENTRE_X * self.width

    def contains(self, x, y):
        left, top, right, bottom = self.floor
        return left <= x <= right and top <= y <= bottom

    def spawn_player(self, player):
        left, top, right, bottom = self.floor
        player.place(self.door_x, bottom - 48.0)

    def player_at_exit(self, player):
        """True when the hero stands in the top doorway."""
        left, top, right, bottom = self.floor
        half = settings.DOOR_HALF_WIDTH * self.width
        return (
            player.y - player.radius <= top + 34.0
            and abs(player.x - self.door_x) <= half + 12.0
        )

    # ------------------------------------------------------------ rules

    def music(self):
        return self.music_track

    def door_open(self):
        return progression.door_is_open(
            self.room_id, len(self.enemies), self.item_taken
        )

    def spawn_enemy_tear(self, x, y, angle, speed=None, damage=1):
        self.enemy_tears.append(EnemyTear(x, y, angle, speed, damage))

    def try_take(self, player):
        """Offer an item to the hero. Only the item room answers."""
        return None

    # ------------------------------------------------------------ frame

    def update(self, dt, player):
        self.elapsed += dt
        for enemy in self.enemies:
            enemy.update(dt, player, self)
        self.enemies = [enemy for enemy in self.enemies if not enemy.dead]
        for tear in self.tears:
            tear.update(dt, self)
        self.tears = [tear for tear in self.tears if not tear.dead]
        for tear in self.enemy_tears:
            tear.update(dt, self)
        self.enemy_tears = [tear for tear in self.enemy_tears if not tear.dead]
        self.resolve_hits(player)

    def resolve_hits(self, player):
        for tear in self.tears:
            if tear.dead:
                continue
            for enemy in self.enemies:
                if tear.dead:
                    break
                if not enemy.alive():
                    continue
                if combat.circle_overlap(
                    tear.x, tear.y, tear.radius, enemy.x, enemy.y, enemy.radius
                ):
                    killed = tear.hit(enemy)
                    self.audio.play_sound("enemy_die" if killed else "hit")

        for tear in self.enemy_tears:
            if tear.dead:
                continue
            if combat.circle_overlap(
                tear.x, tear.y, tear.radius, player.x, player.y, player.radius
            ):
                if player.take_damage(tear.damage, tear.x, tear.y):
                    self.audio.play_sound("hurt")
                tear.dead = True

        for enemy in self.enemies:
            if (
                enemy.alive()
                and combat.circle_overlap(
                    enemy.x, enemy.y, enemy.radius, player.x, player.y, player.radius
                )
                and player.take_damage(enemy.contact_damage, enemy.x, enemy.y)
            ):
                self.audio.play_sound("hurt")

    # ------------------------------------------------------------ drawing

    def draw(self, screen, player):
        screen.blit(self.image_name, self.actor.topleft)
        self.draw_props(screen)
        for tear in self.enemy_tears:
            tear.draw(screen)
        for enemy in self.enemies:
            enemy.draw(screen)
        player.draw(screen)
        for tear in self.tears:
            tear.draw(screen)
        self.draw_door(screen)

    def draw_props(self, screen):
        """Overridden by rooms that draw furniture."""

    def draw_door(self, screen):
        if not self.door_open():
            return
        left, top, right, bottom = self.floor
        half = settings.DOOR_HALF_WIDTH * self.width
        pulse = 0.5 + 0.5 * math.sin(self.elapsed * 5.0)
        glow = drawing.blend(settings.DOOR_GLOW, settings.WHITE, 0.3 * pulse)

        for index in range(3):
            inset = index * 7
            shade = drawing.blend((66, 58, 44), glow, 1.0 - index * 0.28)
            screen.draw.filled_rect(
                Rect(
                    self.door_x - half + inset,
                    top + index * 8,
                    (half - inset) * 2.3,
                    9,
                ),
                shade,
            )

        arrow_y = top + 46.0 + 4.0 * math.sin(self.elapsed * 5.0)
        screen.draw.line(
            (self.door_x - 13.0, arrow_y + 9.0), (self.door_x, arrow_y), glow
        )
        screen.draw.line(
            (self.door_x, arrow_y), (self.door_x + 13.0, arrow_y + 9.0), glow
        )
