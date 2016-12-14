#!/usr/bin/env python
import argparse
import os.path
import sys

def get_options(argv=None):
  """parse the commandline options.

  Check for all supported flags and do any available pre-processing
  """
  opts = argparse.ArgumentParser(
      description='http://adventofcode.com/2016/day/2')

  opts.add_argument(
    "-input", "-i",
    help="Specify input file")
  opts.add_argument(
    "-alt_input", "-a", nargs="*",
    help="Specify inputs on command line"
  )
  opts.add_argument(
    "-part", "-p", default='1',
    choices=['1', '2'],
    help="Solve for part")
  args = opts.parse_args(argv)
  return args

def code_position2(loc):
  codes = {
    (4,2) : '1',
    (3,1) : '2',
    (3,2) : '3',
    (3,3) : '4',
    (2,0) : '5',
    (2,1) : '6',
    (2,2) : '7',
    (2,3) : '8',
    (2,4) : '9',
    (1,1) : 'A',
    (1,2) : 'B',
    (1,3) : 'C',
    (0,2) : 'D',
  }
  res = None
  if tuple(loc) in codes:
    res = codes[tuple(loc)] 
  return res

def code_position1(loc):
  codes = {
    (2,0) : '1',
    (2,1) : '2',
    (2,2) : '3',
    (1,0) : '4',
    (1,1) : '5',
    (1,2) : '6',
    (0,0) : '7',
    (0,1) : '8',
    (0,2) : '9'
  }
  res = None
  if tuple(loc) in codes:
    res = codes[tuple(loc)] 
  return res

def field(move):
  moves = {
    'U': 0,
    'R': 1,
    'D': 2,
    'L': 3,
  }
  res = None
  if move.upper() in moves:
    res = moves[move.upper()]
  return res

def walk_line(line, position=[1,1], p='1'):
  stop = 2
  cp = code_position1
  if p != '1':
    stop = 4
    cp = code_position2
  
  for i in line:
    f = field(i)
    if f is None:
      continue
    x = 1
    if f >= 2:
      x = -1
    f = f % 2
    trial = position[:]
    trial[f] = max(min(position[f] + x, stop), 0)
    if cp(trial) is None:
      continue
    position[f] = trial[f]
  return cp(position)

def main(argv=None):
  if argv is None:
    argv = sys.argv
  args = get_options(argv[1:])

  if (
    ("input" not in args or args.input is None) and
    ("alt_input" not in args or args.alt_input is None)
  ):
    return 1

  code=""
  position = [1, 1]
  if args.part == '2':
    position = [2, 0]
  if args.input is not None and os.path.isfile(args.input):
    with open(args.input) as f:
      for line in f:
        code += walk_line(line.strip(), position, args.part)
  elif args.alt_input is not None and len(args.alt_input) > 0:
    for line in args.alt_input:
      code += walk_line(line.strip(), position, args.part)
  print("code is {0}".format(code))

if __name__ == '__main__':
  if sys.hexversion < 0x02070000:
    print("\n\nERROR: Requires Python 2.7.0 or newer\n")
    sys.exit(1)
  sys.exit(main())
