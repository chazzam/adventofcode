#!/usr/bin/env python
import argparse
import os.path
import sys
import collections

def get_options(argv=None):
  """parse the commandline options.

  Check for all supported flags and do any available pre-processing
  """
  opts = argparse.ArgumentParser(
      description='http://adventofcode.com/2016/day/4')

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

# Re-order the value so the more important character is first <0-9>-<a-z>
def sort_room(x):
  res = '{1}-{0}'.format(*x)
  return res

def cmp_room(x,y):
  res = cmp(x.split('-')[0], y.split('-')[0])
  # if the numbers are not equal, we're done
  if res != 0:
    return res
  # Sort in the opposite direction for the letters
  return (cmp(x.split('-')[1], y.split('-')[1]) * -1)

# Generate the checksum from a list, using reduce
def room_sum(x,y):
  #~ if type(x) is not tuple:
  if type(x) is str:
    return x + y[0]
  # work differently for first reduction
  return x[0] + y[0]

def rotate_name(fields, r):
  enc_name = '-'.join(fields)
  name = ""
  for i in enc_name:
    if i == '-':
      name += i
      continue
    # get the 0 adjusted and shifted letter id
    l = ord(i) - ord('a') + r
    # normalize it back to 0-25
    l = l % 26
    # Convert it back to ASCII
    name += chr(l + ord('a'))
  print("{} : {}".format(name, r))
  return name

def test_line(line):
  # get the sector id and checksum as last field
  fields = line.strip(']').split('-')
  # count the letters in room name fields
  x = collections.Counter(''.join(fields[:-1]))
  # Get the most common 5 characters, sorted as: ('char', <count>)
  y = sorted(
    x.items(),
    key=sort_room,
    cmp=cmp_room,
    reverse=True
  )[:5]
  # split out the sector ID and checksum
  data = fields[-1].split('[')
  # If our checksum doesn't match, return 0
  if data[1] != reduce(room_sum, y):
    return 0
  # Otherwise, return the sector ID and print the name + sector id
  rotate_name(fields[:-1], int(data[0]))
  return int(data[0])

def test_lines(a):
  return test_line(a)

def main(argv=None):
  if argv is None:
    argv = sys.argv
  args = get_options(argv[1:])

  if (
    ("input" not in args or args.input is None) and
    ("alt_input" not in args or args.alt_input is None)
  ):
    return 1

  sector_sum = 0
  my_f = test_line
  if args.part == '2':
    my_f = test_lines
  if args.input is not None and os.path.isfile(args.input):
    with open(args.input) as f:
      for line in f:
        sector_sum += my_f(line.strip())
  elif args.alt_input is not None and len(args.alt_input) > 0:
    for line in args.alt_input:
        sector_sum += my_f(line.strip())
  print("Sector ID Sum is {0}".format(sector_sum))

if __name__ == '__main__':
  if sys.hexversion < 0x02070000:
    print("\n\nERROR: Requires Python 2.7.0 or newer\n")
    sys.exit(1)
  sys.exit(main())
