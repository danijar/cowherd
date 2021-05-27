import numpy as np

from . import constants


class Object:

  def __init__(self, world, pos):
    self.world = world
    self.pos = np.array(pos)
    self.random = world.random
    self.health = 0

  @property
  def texture(self):
    raise 'unknown'

  @property
  def walkable(self):
    return constants.walkable

  def move(self, direction):
    direction = np.array(direction)
    target = self.pos + direction
    if self.is_free(target):
      self.world.move(self, target)
      return True
    return False

  def is_free(self, target, materials=None):
    materials = self.walkable if materials is None else materials
    material, obj = self.world[target]
    return obj is None and material in materials

  def distance(self, target):
    if hasattr(target, 'pos'):
      target = target.pos
    return np.abs(target - self.pos).sum()

  def toward(self, target, long_axis=True):
    if hasattr(target, 'pos'):
      target = target.pos
    offset = target - self.pos
    dists = np.abs(offset)
    if (dists[0] > dists[1] if long_axis else dists[0] <= dists[1]):
      return np.array((np.sign(offset[0]), 0))
    else:
      return np.array((0, np.sign(offset[1])))

  def random_dir(self):
    dirs = ((-1, 0), (+1, 0), (0, -1), (0, +1))
    return dirs[self.random.randint(0, len(dirs))]


class Player(Object):

  def __init__(self, world, pos):
    super().__init__(world, pos)
    self.facing = (0, 1)
    self.inventory = {item: 0 for item in constants.items}
    self.achievements = {name: 0 for name in constants.achievements}

  @property
  def texture(self):
    return {
        (-1, 0): 'player-left',
        (+1, 0): 'player-right',
        (0, -1): 'player-up',
        (0, +1): 'player-down',
    }[tuple(self.facing)]

  @property
  def walkable(self):
    return constants.walkable + ['lava']

  def update(self, action):
    target = (self.pos[0] + self.facing[0], self.pos[1] + self.facing[1])
    material, obj = self.world[target]
    action = constants.actions[action]
    if action == 'noop':
      pass
    elif action.startswith('move_'):
      self._move(action[len('move_'):])
    elif action == 'do' and obj:
      self._interact(obj)
    elif action == 'do':
      self._collect(target, material)
    elif action.startswith('place_'):
      self._place(action[len('place_'):], target, material)

  def _move(self, direction):
    dirs = dict(left=(-1, 0), right=(+1, 0), up=(0, -1), down=(0, +1))
    self.facing = dirs[direction]
    self.move(self.facing)
    if self.world[self.pos][0] == 'lava':
      self.health = 0

  def _interact(self, obj):
    if isinstance(obj, Cow) and not obj.molken:
      self.inventory['milk'] += 1
      self.achievements['milk_cow'] += 1
      obj.molken = True

  def _collect(self, target, material):
    info = constants.collect.get(material)
    if not info:
      return
    for name, amount in info['require'].items():
      if self.inventory[name] < amount:
        return
    self.world[target] = info['leaves']
    for name, amount in info['receive'].items():
      self.inventory[name] += 1
    self.achievements[f'collect_{material}'] += 1

  def _place(self, name, target, material):
    if not self.is_free(target):
      return
    info = constants.place[name]
    if material not in info['where']:
      return
    if any(self.inventory[k] < v for k, v in info['uses'].items()):
      return
    for item, amount in info['uses'].items():
      self.inventory[item] -= amount
    self.world[target] = name
    self.achievements[f'place_{name}'] += 1

  def _make(self, name):
    nearby = self.world.nearby(self.pos, 2)
    info = constants.make[name]
    if not all(util in nearby for util in info['nearby']):
      return
    if any(self.inventory[k] < v for k, v in info['uses'].items()):
      return
    for item, amount in info['uses'].items():
      self.inventory[item] -= amount
    self.inventory[name] += 1
    self.achievements[f'make_{name}'] += 1


class Cow(Object):

  def __init__(self, world, pos, player):
    super().__init__(world, pos)
    self.health = 3
    self.player = player
    self.molken = False

  @property
  def texture(self):
    if self.molken:
      return 'cow-molken'
    else:
      return 'cow'

  def update(self):
    near = self.distance(self.player) < 3
    if near and self.random.uniform() < 0.8:
      away = -self.toward(self.player, self.random.uniform() < 0.6)
      if self.is_free(self.pos + away):
        self.move(away)
        return
      dirs = [(-1, 0), (+1, 0), (0, -1), (0, +1)]
      dirs = [np.array(x) for x in dirs]
      dirs = [x for x in dirs if self.is_free(self.pos + x)]
      dirs = [x for x in dirs if self.player.distance(self.pos + x) > 1]
      dirs = dirs if dirs else [self.random_dir()]
      self.move(dirs[self.random.randint(0, len(dirs))])
    elif near or self.random.uniform() < 0.3:
      self.move(self.random_dir())
