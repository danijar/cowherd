import numpy as np

from . import objects


MAP = """
SSSSSSSSSSSSSS
SWWWW   T    S
SWW          S
S         T  S
S         T  S
S            S
S            S
S   T        S
S            S
S            S
S         T  S
S   WW       S
S  WWWWWWW   S
SSSSSSSSSSSSSS
"""


def generate_world(world, player, num_cows):
  lines = MAP.split('\n')
  lines = [line.strip() for line in lines if line]
  for y, line in enumerate(lines):
    for x, char in enumerate(line):
      world[x, y] = {
          ' ': 'grass',
          'T': 'tree',
          'S': 'stone',
          'W': 'water',
      }[char]
  empties = []
  for x in range(world.area[0]):
    for y in range(world.area[1]):
      dist = np.abs(player.pos - np.array([x, y])).sum()
      if world[x, y][0] == 'grass' and dist > 5:
        empties.append((x, y))
  for _ in range(num_cows):
    index = world.random.randint(0, len(empties))
    pos = empties[index]
    del empties[index]
    world.add(objects.Cow(world, pos, player))
