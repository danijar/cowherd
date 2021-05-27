import numpy as np

from . import constants
from . import engine
from . import objects
from . import worldgen


class Env:

  def __init__(
      self, view=(7, 7), size=(64, 64), length=1000, num_cows=3, seed=None):
    view = np.array(view if hasattr(view, '__len__') else (view, view))
    size = np.array(size if hasattr(size, '__len__') else (size, size))
    unit = size // view
    self._size = size
    self._length = length
    self._num_cows = num_cows
    self._seed = seed
    self._episode = 0
    self._world = engine.World((14, 14))
    self._textures = engine.Textures(constants.root / 'assets')
    item_rows = int(np.ceil(len(constants.items) / view[0]))
    self._local_view = engine.LocalView(
        self._world, self._textures, unit,
        [view[0], view[1] - item_rows])
    self._item_view = engine.ItemView(
        self._textures, unit, [view[0], item_rows])
    self._border = (size - unit * view) // 2
    self._step = None
    self._player = None
    self._milked = None

  @property
  def observation_space(self):
    return engine.BoxSpace(0, 255, tuple(self._size) + (3,), np.uint8)

  @property
  def action_space(self):
    return engine.DiscreteSpace(len(constants.actions))

  @property
  def action_names(self):
    return constants.actions

  def reset(self):
    center = (self._world.area[0] // 2, self._world.area[1] // 2)
    self._step = 0
    self._episode += 1
    self._world.reset(seed=hash((self._seed, self._episode)) % 2 ** 32)
    self._player = objects.Player(self._world, center)
    self._player.inventory['fence'] = float('inf')
    self._world.add(self._player)
    self._milked = 0
    worldgen.generate_world(self._world, self._player, self._num_cows)
    return self._obs()

  def step(self, action):
    self._step += 1
    # Copy object list so new added objects are not updated right away.
    for obj in list(self._world.objects):
      if obj is self._player:
        obj.update(action)
      else:
        obj.update()
    obs = self._obs()

    trapped = []
    for obj in self._world.objects:
      if isinstance(obj, objects.Cow):
        for dir_ in ((-1, 0), (+1, 0), (0, -1), (0, +1)):
          trapped.append(not obj.is_free(obj.pos + np.array(dir_)))

    if self._milked < self._player.achievements['milk_cow']:
      self._milked = self._player.achievements['milk_cow']
      reward = 1.0
    else:
      reward = 0.0
    done = self._length and self._step >= self._length
    info = {
        'inventory': self._player.inventory.copy(),
        'achievements': self._player.achievements.copy(),
        'trapped': np.mean(trapped),
        'discount': 1.0,
    }
    return obs, reward, done, info

  def render(self):
    canvas = np.zeros(tuple(self._size) + (3,), np.uint8)
    local_view = self._local_view(self._player)
    item_view = self._item_view(self._player.inventory)
    view = local_view
    view = np.concatenate([local_view, item_view], 1)
    (x, y), (w, h) = self._border, view.shape[:2]
    canvas[x: x + w, y: y + h] = view
    return canvas.transpose((1, 0, 2))

  def _obs(self):
    return self.render()
