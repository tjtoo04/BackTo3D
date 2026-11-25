"""Room order and the rules that unlock the next door.

Pure logic: no window, no Pygame Zero.
"""

ROOM_TUTORIAL = "tutorial"
ROOM_MOB_ONE = "mob_one"
ROOM_ITEM = "item"
ROOM_MOB_TWO = "mob_two"
ROOM_BOSS = "boss"

ROOM_ORDER = (
    ROOM_TUTORIAL,
    ROOM_MOB_ONE,
    ROOM_ITEM,
    ROOM_MOB_TWO,
    ROOM_BOSS,
)

ROOM_LABELS = {
    ROOM_TUTORIAL: "TUTORIAL",
    ROOM_MOB_ONE: "MOB ROOM",
    ROOM_ITEM: "ITEM ROOM",
    ROOM_MOB_TWO: "MOB ROOM",
    ROOM_BOSS: "BOSS",
}


def total_rooms():
    return len(ROOM_ORDER)


def room_number(room_id):
    """One-based position of a room in the gauntlet."""
    return ROOM_ORDER.index(room_id) + 1


def room_label(room_id):
    return ROOM_LABELS[room_id]


def next_room(room_id):
    """The room after `room_id`, or None after the boss."""
    position = ROOM_ORDER.index(room_id) + 1
    if position >= len(ROOM_ORDER):
        return None
    return ROOM_ORDER[position]


def door_is_open(room_id, enemies_remaining, item_taken):
    """True when the top door of a room may be used."""
    if room_id == ROOM_TUTORIAL:
        return True
    if room_id == ROOM_ITEM:
        return item_taken
    return enemies_remaining == 0


def boss_phase(health_ratio_value):
    """Behaviour phase of the boss for a remaining-health fraction."""
    if health_ratio_value > 0.60:
        return 1
    if health_ratio_value > 0.30:
        return 2
    return 3
