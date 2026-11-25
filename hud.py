"""The heads-up display, drawn in the two side margins."""

from pygame import Rect

import drawing
import icons
import progression
import settings

HEART_PATTERN = (
    ".FF..FF.",
    "FFFFFFFF",
    "FFFFFFFF",
    "FFFFFFFF",
    ".FFFFFF.",
    "..FFFF..",
    "...FF...",
    "........",
)

HEART_CELL = 4
HEART_GAP = 6
HEART_COUNT = settings.PLAYER_MAX_HP // 2
HEART_COLUMNS = len(HEART_PATTERN[0])


class HUD:
    """Draws hearts, the dodge meter, the held item and the room label."""

    def draw(self, screen, player, room):
        self.draw_hearts(screen, player, room)
        self.draw_dodge_meter(screen, player, room)
        self.draw_item(screen, player, room)
        self.draw_room_label(screen, room)
        self.draw_pause_hint(screen, room)

    # ------------------------------------------------------------ hearts

    def draw_hearts(self, screen, player, room):
        full = player.hp // 2
        half = player.hp % 2
        width = self.heart_row_width()
        left = room.left // 2 - width // 2
        palette = {
            "F": settings.HEART_FULL,
            "E": settings.HEART_EMPTY,
        }
        for index in range(HEART_COUNT):
            if index < full:
                pattern = HEART_PATTERN
            elif index == full and half:
                pattern = self.drained(HEART_COLUMNS // 2)
            else:
                pattern = self.drained(0)
            drawing.draw_pixel_icon(
                screen, pattern, palette,
                left + index * (HEART_COLUMNS * HEART_CELL + HEART_GAP),
                48, HEART_CELL)

    def heart_row_width(self):
        return (HEART_COUNT * HEART_COLUMNS * HEART_CELL
                + (HEART_COUNT - 1) * HEART_GAP)

    def drained(self, first_empty_column):
        """The heart pattern with columns from `first_empty_column` drained."""
        return tuple(
            "".join("E" if column >= first_empty_column else cell
                    for column, cell in enumerate(row))
            for row in HEART_PATTERN
        )

    # ------------------------------------------------------------ dodge

    def draw_dodge_meter(self, screen, player, room):
        width = 92
        left = room.left // 2 - width // 2
        top = 104
        total = settings.PLAYER_DODGE_TIME + settings.PLAYER_DODGE_COOLDOWN
        ready = 1.0 - min(1.0, player.dodge_cooldown / total)
        drawing.draw_text(screen, "DODGE", (left, top - 18), 13,
                          settings.HUD_DIM, anchor="topleft")
        screen.draw.filled_rect(Rect(left, top, width, 9), settings.PANEL)
        screen.draw.filled_rect(
            Rect(left, top, int(width * ready), 9),
            drawing.blend(settings.HUD_DIM, settings.GOLD, ready))
        screen.draw.rect(Rect(left, top, width, 9), settings.HUD_DIM)

    # ------------------------------------------------------------ item

    def draw_item(self, screen, player, room):
        centre = room.right + (settings.WIDTH - room.right) // 2
        if player.item is None:
            drawing.draw_text(screen, "NO ITEM", (centre, 66), 14,
                              settings.HUD_DIM, anchor="center")
            return

        icons.draw_item_icon(screen, player.item, centre, 118)
        drawing.draw_text(screen, player.item.name, (centre, 138), 17,
                          settings.GOLD, anchor="center",
                          outline=settings.BLACK)
        drawing.draw_wrapped_text(
            screen, player.item.summary, centre, 162, 13, settings.HUD_DIM)

    # ------------------------------------------------------------ labels

    def draw_room_label(self, screen, room):
        centre = room.left // 2
        drawing.draw_text(
            screen, f"ROOM {progression.room_number(room.room_id)}"
                    f"/{progression.total_rooms()}",
            (centre, settings.HEIGHT - 96), 15, settings.HUD_TEXT,
            anchor="center")
        drawing.draw_text(
            screen, progression.room_label(room.room_id),
            (centre, settings.HEIGHT - 76), 12, settings.HUD_DIM,
            anchor="center")

    def draw_pause_hint(self, screen, room):
        centre = room.right + (settings.WIDTH - room.right) // 2
        drawing.draw_text(screen, "ESC  PAUSE", (centre, settings.HEIGHT - 86),
                          12, settings.HUD_DIM, anchor="center")
