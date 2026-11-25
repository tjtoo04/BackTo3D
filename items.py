"""The three items and the rule that applies one to the hero's attack."""

import combat


class Item:
    """A permanent attack modifier offered by the item room."""

    __slots__ = (
        "key",
        "name",
        "summary",
        "icon",
        "damage_mult",
        "cooldown_mult",
        "pierce_override",
        "projectiles",
        "spread",
    )

    def __init__(
        self,
        key,
        name,
        summary,
        icon,
        damage_mult,
        cooldown_mult,
        pierce_override=None,
        projectiles=1,
        spread=0.0,
    ):
        self.key = key
        self.name = name
        self.summary = summary
        self.icon = icon
        self.damage_mult = damage_mult
        self.cooldown_mult = cooldown_mult
        self.pierce_override = pierce_override
        self.projectiles = projectiles
        self.spread = spread

    def __repr__(self):
        return f"Item({self.key!r})"


GAUNTLET = Item(
    key="gauntlet",
    name="Gauntlet",
    summary="x2.5 damage, x1.5 cooldown",
    icon="items/gauntlet",
    damage_mult=2.5,
    cooldown_mult=1.5,
)

LASER = Item(
    key="laser",
    name="Laser",
    summary="Pierces all, x0.5 damage",
    icon="items/laser_gun",
    damage_mult=0.5,
    cooldown_mult=1.1,
    pierce_override=combat.INFINITE_PIERCE,
)

TRIPLEGUN = Item(
    key="triplegun",
    name="Triplegun",
    summary="Three tears, x0.65 cooldown",
    icon="items/triple_gun",
    damage_mult=0.6,
    cooldown_mult=0.65,
    projectiles=3,
    spread=18.0,
)

ITEM_ORDER = (GAUNTLET, LASER, TRIPLEGUN)


def apply_item(stats, item):
    """Return a new AttackStats with the item applied to `stats`."""
    pierce = stats.pierce if item.pierce_override is None else item.pierce_override
    return stats.replace(
        damage=stats.damage * item.damage_mult,
        cooldown=stats.cooldown * item.cooldown_mult,
        pierce=pierce,
        projectiles=item.projectiles,
        spread=item.spread,
    )
