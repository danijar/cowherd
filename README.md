# CowHerd

[![PyPI](https://img.shields.io/pypi/v/cowherd.svg)](https://pypi.python.org/pypi/cowherd/#history)

CowHerd is a partially-observed reinforcement learning environment, where the
player walks around an area and is rewarded for milking cows. The cows try to
escape and the player can place fences to help capture them. The implementation
of CowHerd is based on the [Crafter][crafter] environment.

![Cow Herd Video](https://github.com/danijar/cowherd/raw/main/media/video.gif)

[crafter]: https://github.com/danijar/crafter

## Play Yourself

You can play the game yourself with an interactive window and keyboard input.
The mapping from keys to actions, health level, and inventory state are printed
to the terminal.

```sh
# Install with GUI
pip3 install 'cowherd[gui]'

# Start the game
cowherd

# Alternative way to start the game
python3 -m cowherd.run_gui
```

The following optional command line flags are available:

| Flag | Default | Description |
| :--- | :-----: | :---------- |
| `--window <width> <height>` | 800 800 | Window size in pixels, used as width and height. |
| `--fps <integer>` | 5 | How many times to update the environment per second. |
| `--record <filename>.mp4` | None | Record a video of the trajectory. |
| `--num_cows` | 3 | The number of cows in the environment. |
| `--view <width> <height>` | 7 7 | The layout size in cells; determines view distance. |
| `--length <integer>` | None | Time limit for the episode. |
| `--seed <integer>` | None | Determines world generation and creatures. |

## Training Agents

Installation: `pip3 install -U cowherd`

The environment follows the [OpenAI Gym][gym] interface:

```py
import cowherd

env = cowherd.Env(seed=0)
obs = env.reset()
assert obs.shape == (64, 64, 3)

done = False
while not done:
  action = env.action_space.sample()
  obs, reward, done, info = env.step(action)
```

[gym]: https://github.com/openai/gym

## Environment Details

### Reward

A reward of +1 is given every time the player milks one of the cows.

### Termination

Episodes terminate after 1000 steps.

### Observation Space

Each observation is an RGB image that shows a local view of the world around
the player, as well as the inventory state of the agent.

### Action Space

The action space is categorical. Each action is an integer index representing
one of the possible actions:

| Integer | Name | Description |
| :-----: | :--- | :---------- |
| 0 | `noop` | Do nothing. |
| 1 | `move_left` | Walk to the left. |
| 2 | `move_right` | Walk to the right. |
| 3 | `move_up` | Walk upwards. |
| 4 | `move_down` | Walk downwards. |
| 5 | `do` | Pick up a placed fence or milk a cow. |
| 6 | `place_fence` | Place a fence in front of the player. |

## Questions

Please [open an issue][issues] on Github.

[issues]: https://github.com/danijar/cowherd/issues
