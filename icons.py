"""The item icons, drawn from the scaled art in images/items/."""

from pgzero.builtins import Actor

_actors = {}


def icon_actor(item):
    """The cached sprite for an item, loaded on first use."""
    actor = _actors.get(item.key)
    if actor is None:
        actor = Actor(item.icon)
        _actors[item.key] = actor
    return actor


def draw_item_icon(screen, item, centre_x, bottom_y):
    """Draw an item icon with its bottom centre on a point."""
    actor = icon_actor(item)
    screen.blit(
        actor.image,
        (int(centre_x - actor.width / 2), int(bottom_y - actor.height)),
    )
