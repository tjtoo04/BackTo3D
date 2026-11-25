BackTo3d
========

A short twin-stick roguelite in the style of The Binding of Isaac, built with
Pygame Zero.

A 3D hero falls into a hand-drawn 2D world. He must fight through five rooms and
leave through the door at the end.


LIBRARIES
---------

The game imports only these:

  Pygame Zero (pgzero)   Window, game loop, images, text, music and sound
  math                   Angles, distances, sine waves
  random                 Enemy start positions and timers
  pygame.Rect            The one Pygame class the drawing API needs

No other library is used. pygame itself is imported for Rect only.

The files in tools/ and tests/ are developer tools. The game never loads them,
so they may use other standard modules.


HOW TO RUN
----------

0. Install into a virtual environment:

     python -m venv .venv
     source .venv/bin/activate      (Linux and macOS)
     .venv\Scripts\activate         (Windows)

1. Install pygame-ce (pygame is no longer maintained and is deprecated), then Pygame Zero:
   Note: default pgzero installation still installs pygame.

     pip install pygame-ce
     pip install --no-deps pgzero

   --no-deps stops pip from also installing the plain pygame package, which
   would overwrite pygame-ce. pygame-ce ships SDL_image and SDL_mixer inside the
   wheel, so the game gets both image and audio support.

2. Start the game from the project folder:

     pgzrun game.py

Keep the images/, sounds/ and music/ folders next to game.py. Pygame Zero loads
them by name.


CONTROLS
--------

  W A S D            Move
  Arrow keys         Shoot a tear
  Shift              Dodge, with a short invulnerability window
  E                  Take the item under the hero
  Esc                Pause, or leave the pause screen
  Up Down Enter      Move and confirm in the menus


THE GAUNTLET
------------

  Room 1   Tutorial. A control card and an open door.
  Room 2   First mob room. Three blobs chase the hero.
  Room 3   Item room. Three pedestals, one choice.
  Room 4   Second mob room. Two chomper cubes and three paperclip spiders.
  Room 5   Boss room. The Glitch Master fires bursts and dashes.

The door at the top of a room opens when the room is cleared. Walk into it to
move on. After the boss dies, the same door wins the run.


ITEMS
-----

The item room offers one item from three. The choice is final.

  Gauntlet     Doubles damage, doubles the cooldown
  Laser        Pierces every enemy, halves the damage
  Triplegun    Fires three tears, cooldown 65%, each tear 60% damage


PROJECT LAYOUT
--------------

  game.py               Entry point, window size and the Pygame Zero hooks
  settings.py           Every tuning number and colour, in one place
  combat.py             Combat maths. Pure: no window
  items.py              The three items and the rule that applies them
  progression.py        Room order, door rules and boss phases
  animation.py          Frame cycling for the sprites
  entities/             One file per entity, listed below
  rooms/                One file per room type, listed below
  scenes.py             Menu, run, pause, win and game over
  hud.py                Hearts, dodge meter, held item and room label
  icons.py              The three item icons, drawn from the scaled item art
  drawing.py            Shared drawing helpers
  audio.py              Music and sound behind the two on/off switches
  keymap.py             The Pygame Zero key constants
  tools/build_assets.py Builds images/, sounds/ and music/ from sprites/
  tools/smoke_test.py   Runs the real game headlessly and checks the flow
  tests/test_logic.py   Tests for the pure rules


ENTITIES
--------

Each entity has its own file under entities/. A base class lives beside the
entities that use it.

  entity.py             Entity, the base: position, radius, sprite, floor clamp
  player.py             Player and its animation set
  enemy.py              Enemy, the base: health, knockback, hurt flash, death
  blob.py               Blob
  chomper_cube.py       ChomperCube
  paperclip_spider.py   PaperclipSpider
  glitch_master.py      GlitchMaster, the boss
  projectile.py         Projectile, the shared flight for both shot types
  tear.py               Tear, the hero's shot
  enemy_tear.py         EnemyTear, an enemy shot
  __init__.py           Re-exports the names and holds the ENEMY_TYPES table


ROOMS
-----

Each room type has its own file under rooms/. A base class lives beside the
rooms that use it.

  room.py               Room, the base: geometry, floor, door, collision, order
  tutorial_room.py      TutorialRoom, the control card
  mob_room.py           MobRoom and the two wave tables
  pedestal.py           Pedestal, one stand holding one item
  item_room.py          ItemRoom and the pedestal positions
  boss_room.py          BossRoom and its health bar
  __init__.py           Re-exports the names


