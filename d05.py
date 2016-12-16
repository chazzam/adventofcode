#!/usr/bin/env python
import argparse
import os.path
import sys
import hashlib

def get_options(argv=None):
  """parse the commandline options.

  Check for all supported flags and do any available pre-processing
  """
  opts = argparse.ArgumentParser(
      description='http://adventofcode.com/2016/day/5')

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

def forever_quest(door):
  i = 0
  pass_len = 8
  # allowed position list
  pass_pos = ''.join(map(str,range(pass_len)))
  password1 = ""
  password2 = [' ' for x in pass_pos]
  # Base hash object
  md5_base = hashlib.md5()
  md5_base.update(door)
  while True:
    # Copy the hash object, add the index, and get the hexdigest
    md5 = md5_base.copy()
    md5.update(str(i))
    code = md5.hexdigest()[:7]
    i += 1
    # move on if this isn't a valid result
    if "00000" != code[:5]:
      continue
    # always update part 1 password
    x = code[5:6]
    password1 += x
    # update part 2 password iff a position is valid and blank
    if x not in pass_pos:
      continue
    x = int(x)
    if password2[x] != " ":
      continue
    password2[x] = code[6:7]
    # verify password1 is at least our length, and all slots in password 2 are filled
    if (len(password1) >= pass_len) and (' ' not in ''.join(password2)):
      break
  # Trim password1 back down to 8 characters, stringify password2
  return (password1[:pass_len], ''.join(password2))

def test_lines(a):
  return forever_quest(a)

def main(argv=None):
  if argv is None:
    argv = sys.argv
  args = get_options(argv[1:])

  if (
    ("input" not in args or args.input is None) and
    ("alt_input" not in args or args.alt_input is None)
  ):
    return 1

  data = 0
  my_f = forever_quest
  if args.part == '2':
    my_f = test_lines
  if args.input is not None and os.path.isfile(args.input):
    with open(args.input) as f:
      for line in f:
        data = my_f(line.strip())
  elif args.alt_input is not None and len(args.alt_input) > 0:
    for line in args.alt_input:
        data = my_f(line.strip())
  print("Part1 Password is {0}, Part 2 is {1}".format(*data))

if __name__ == '__main__':
  if sys.hexversion < 0x02070000:
    print("\n\nERROR: Requires Python 2.7.0 or newer\n")
    sys.exit(1)
  sys.exit(main())
