"""Room three: the pedestals and the item choice."""

from pygame import Rect

import combat
import drawing
import icons
import progression
import settings
from items import ITEM_ORDER
from rooms.pedestal import Pedestal
from rooms.room import Room

# Where the three pedestals stand, as fractions of the walkable floor.
PEDESTAL_POSITIONS = (0.26, 0.50, 0.74)


class ItemRoom(Room):
    """Three pedestals. Taking one opens the door."""

    def __init__(self, audio):
        super().__init__(progression.ROOM_ITEM,
                         settings.ROOM_MOB_IMAGE, audio)
        self.pedestals = self.build_pedestals()
        self.chosen = None

    def build_pedestals(self):
        left, top, right, bottom = self.floor
        width = right - left
        height = bottom - top
        pedestals = []
        for item, fraction in zip(ITEM_ORDER, PEDESTAL_POSITIONS,
                                  strict=True):
            pedestals.append(Pedestal(
                item, left + width * fraction, top + height * 0.42))
        return pedestals

    def nearest_pedestal(self, player):
        """The pedestal under the hero, or None once the choice is made."""
        if self.chosen is not None:
            return None
        for pedestal in self.pedestals:
            if combat.circle_overlap(player.x, player.y, player.radius + 22.0,
                                     pedestal.x, pedestal.y, 34.0):
                return pedestal
        return None

    def try_take(self, player):
        pedestal = self.nearest_pedestal(player)
        if pedestal is None:
            return None
        self.chosen = pedestal.item
        self.item_taken = True
        player.equip(pedestal.item)
        self.audio.play_sound("pickup")
        return pedestal.item

    def draw_props(self, screen):
        """The pedestals leave the screen once the hero takes one."""
        if self.chosen is not None:
            return
        for pedestal in self.pedestals:
            self.draw_pedestal(screen, pedestal)

    def draw_pedestal(self, screen, pedestal):
        x, y = pedestal.x, pedestal.y
        screen.draw.filled_rect(Rect(x - 32, y + 4, 64, 26), (84, 76, 68))
        screen.draw.filled_rect(Rect(x - 38, y - 2, 76, 10), (122, 112, 100))
        screen.draw.rect(Rect(x - 38, y - 2, 76, 32), (44, 38, 34))
        icons.draw_item_icon(screen, pedestal.item, x, y - 8)
        drawing.draw_text(screen, pedestal.item.name, (x, y + 44), 16,
                          settings.GOLD, anchor="center",
                          outline=settings.BLACK)
        drawing.draw_wrapped_text(
            screen, pedestal.item.summary, x, y + 66, 12,
            settings.HUD_TEXT, line_gap=16, outline=settings.BLACK)

    def draw(self, screen, player):
        super().draw(screen, player)
        pedestal = self.nearest_pedestal(player)
        if pedestal is not None:
            drawing.draw_text(
                screen, "PRESS  E", (pedestal.x, pedestal.y + 108), 14,
                settings.WHITE, anchor="center", outline=settings.BLACK)
