#!/usr/bin/env python
import argparse
import sys
import hashlib

# -i ihgpwlah
# -i kglvqrro
# -i ulqzkmiv

def get_options(argv=None):
  """parse the commandline options.

  Check for all supported flags and do any available pre-processing
  """
  opts = argparse.ArgumentParser(
      description='http://adventofcode.com/2016/day/17')

  opts.add_argument(
    "--input_state", "-i", required=True,
    help="Specify input state")
  args = opts.parse_args(argv)
  return args

# walk
def forever_quest(code, paths=list(), path="", pos=[0,0]):
  # Copy the hash object, add the index, and get the hexdigest
  locks = code.copy()
  locks.update(path)
  locks = locks.hexdigest()[:4]
  for i,x in enumerate(locks):
    # move along if this direction isn't open
    if x <= 'a':
      continue
    inner_pos = pos[:]
    # track our location
    m = 1
    if i % 2 == 0:
      m = -1
    # only allow valid moves
    if inner_pos[int(i/2)] + m < 0:
      continue
    if inner_pos[int(i/2)] + m > 3:
      continue
    inner_pos[int(i/2)] += m
    # update our path
    inner_path = path + dict(enumerate('UDLR'))[i]
    if inner_pos[0] == 3 and inner_pos[1] == 3:
      # we made it to the vault on this path!
      return inner_path
    # not at vault yet, recurse this path
    inner_path = forever_quest(code, inner_path, inner_pos, paths)
    if inner_path != "":
      paths.append(inner_path)
  # found nothing, return nothing
  return ""

def main(argv=None):
  if argv is None:
    argv = sys.argv
  args = get_options(argv[1:])

  if "input_state" not in args or args.input_state is None:
    return 1
  md5_base = hashlib.md5()
  md5_base.update(args.input_state)

  all_paths = list()
  # all_paths should be copied by reference throughout
  forever_quest(md5_base, all_paths)
  if len(all_paths) == 0:
    print("No Valid Path Found")
    return 1
  # identify the shortest & longest path returned
  minpath = all_paths[0]
  maxpath = all_paths[0]
  for x in all_paths:
    if len(x) < len(minpath):
      minpath = x
    elif len(x) > len(maxpath):
      maxpath = x
  print("Shortest Path is {}, Longest is {} steps".
    format(minpath, len(maxpath))
  )

if __name__ == '__main__':
  if sys.hexversion < 0x02070000:
    print("\n\nERROR: Requires Python 2.7.0 or newer\n")
    sys.exit(1)
  sys.exit(main())
