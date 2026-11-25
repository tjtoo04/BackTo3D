"""The Pygame Zero key constants.

Pygame Zero builds `keys` with exec, so static analysers cannot see it. Reading
it out of the module namespace keeps the import checkable.
"""

from pgzero import constants

keys = vars(constants)["keys"]
