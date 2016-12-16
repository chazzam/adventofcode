#!/usr/bin/env python
import argparse
import os.path
import sys
import collections

# -i 10000 -s 20
# -i 10010000000110000 -s 272
# -i 10010000000110000 -s 35651584

def get_options(argv=None):
  """parse the commandline options.

  Check for all supported flags and do any available pre-processing
  """
  opts = argparse.ArgumentParser(
      description='http://adventofcode.com/2016/day/16')

  opts.add_argument(
    "--input_state", "-i", required=True,
    help="Specify input state")
  opts.add_argument(
    "--size", "-s", required=True,
    help="Specify disk size"
  )
  args = opts.parse_args(argv)
  return args

# the specified modified dragon curve
def dragon_curve(a):
  # reverse and Flip bits
  b = ''.join(
    map(
      lambda i: str(1 - int(i)),
      reversed(a)
    )
  )
  # return the two fields separated by a '0'
  return a + '0' + b

# recursively run dragon curve until we hit our length
def dragon_curve_length(a, x):
  if len(a) >= x:
    return a[:x]
  while len(a) < x:
    a = dragon_curve(a)
  return a[:x]

def our_checksum(a):
  # Split the data into a list of paired bits as tuples
  c = zip(*[iter(a)]*2)
  # cmp each tuple, reducing to just equal|not-equal
  # flip equals result and convert it to a string
  # then combine all of those results into one string and return it
  return ''.join(map(lambda x: str(1 - abs(cmp(*x))), c))

def checksum_odd(a):
  # take our checksum
  a = our_checksum(a)
  # return it once it is odd length
  if len(a) % 2 == 1:
    return a
  # recurse until our checksum is odd length
  return checksum_odd(a)

def fill_disk(state, size):
  return checksum_odd(dragon_curve_length(state, size))

def main(argv=None):
  if argv is None:
    argv = sys.argv
  args = get_options(argv[1:])

  if (
    ("input_state" not in args or args.input_state is None) and
    ("size" not in args or args.size is None)
  ):
    return 1

  part1 = fill_disk(args.input_state, int(args.size))
  print("Checksum is {}".format(part1))

if __name__ == '__main__':
  if sys.hexversion < 0x02070000:
    print("\n\nERROR: Requires Python 2.7.0 or newer\n")
    sys.exit(1)
  sys.exit(main())
