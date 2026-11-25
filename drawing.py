"""Small drawing helpers shared by the rooms and the HUD."""

from pygame import Rect

# Pygame Zero takes an anchor as a pair of 0..1 fractions, not as a name.
ANCHORS = {
    "topleft": (0.0, 0.0),
    "midtop": (0.5, 0.0),
    "topright": (1.0, 0.0),
    "midleft": (0.0, 0.5),
    "center": (0.5, 0.5),
    "midright": (1.0, 0.5),
    "bottomleft": (0.0, 1.0),
    "midbottom": (0.5, 1.0),
    "bottomright": (1.0, 1.0),
}


def blend(colour_a, colour_b, amount):
    """Mix two colours. `amount` 0 gives colour_a, 1 gives colour_b."""
    amount = max(0.0, min(1.0, amount))
    return tuple(
        int(start + (end - start) * amount)
        for start, end in zip(colour_a, colour_b, strict=True)
    )


def draw_pixel_icon(screen, pattern, palette, left, top, cell):
    """Draw a pixel icon from rows of palette keys. A space or dot is empty."""
    for row_index, row in enumerate(pattern):
        for column_index, key in enumerate(row):
            colour = palette.get(key)
            if colour is None:
                continue
            screen.draw.filled_rect(
                Rect(left + column_index * cell, top + row_index * cell,
                     cell, cell), colour)


def draw_text(screen, text, pos, size, colour, anchor="topleft", outline=None):
    """Draw text with the default font and an optional outline."""
    options = {
        "fontsize": size,
        "color": colour,
        "anchor": ANCHORS.get(anchor, ANCHORS["topleft"]),
    }
    if outline is not None:
        options["owidth"] = max(1, size // 9)
        options["ocolor"] = outline
    screen.draw.text(text, pos, **options)


def icon_size(pattern, cell):
    """Pixel width and height of an icon pattern."""
    return len(pattern[0]) * cell, len(pattern) * cell


def draw_wrapped_text(screen, text, centre, top, size, colour,
                      line_gap=17, outline=None):
    """Draw text on one or two lines, splitting near the middle space."""
    words = text.split(" ")
    if len(words) < 4:
        draw_text(screen, text, (centre, top), size, colour,
                  anchor="center", outline=outline)
        return
    middle = len(words) // 2
    draw_text(screen, " ".join(words[:middle]), (centre, top), size, colour,
              anchor="center", outline=outline)
    draw_text(screen, " ".join(words[middle:]), (centre, top + line_gap),
              size, colour, anchor="center", outline=outline)
