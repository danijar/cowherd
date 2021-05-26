import argparse
import time

import imageio
import numpy as np

import cowherd


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--seed', type=int, default=None)
  parser.add_argument('--view', type=int, nargs=2, default=(7, 7))
  parser.add_argument('--num_cows', type=int, default=3)
  parser.add_argument('--size', type=int, nargs=2, default=(64, 64))
  parser.add_argument('--length', type=int, default=1000)
  parser.add_argument('--health', type=int, default=5)
  parser.add_argument('--record', type=str, default=None)
  args = parser.parse_args()

  random = np.random.RandomState(args.seed)
  env = cowherd.Env(
      args.view, args.size, args.length, args.num_cows, args.seed)
  if args.record:
    frames = []

  start = time.time()
  env.reset()
  print(f'Reset time: {1000*(time.time()-start):.2f}ms')

  start = time.time()
  done = False
  while not done:
    action = random.randint(0, env.action_space.n)
    obs, _, done, _ = env.step(action)
    if args.record:
      frames.append(obs['image'])
  duration = time.time() - start
  step = env._step
  print(f'Step time: {1000*duration/step:.2f}ms ({int(step/duration)} FPS)')
  print('Episode length:', step)

  if args.record:
    imageio.mimsave(args.record, frames)
    print('Saved', args.record)


if __name__ == '__main__':
  main()
