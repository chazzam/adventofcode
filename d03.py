#!/usr/bin/env python
import argparse
import os.path
import sys

def get_options(argv=None):
  """parse the commandline options.

  Check for all supported flags and do any available pre-processing
  """
  opts = argparse.ArgumentParser(
      description='http://adventofcode.com/2016/day/3')

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

def test_list(data):
  if len(data) != 3:
    return 0
  # compare each pair against the third
  tri = True
  for i in range(0, 3):
    tri &= (
      int(data[i]) + int(data[(i + 1) % 3]) 
      > int(data[(i + 2) % 3])
    )
  return 1 if tri else 0

def test_line(line):
  # split the line by double space
  fields = line.strip().split('  ')
  # strip each field and remove empty fields
  fields = [x.strip() for x in filter(None,fields)]
  return test_list(fields)

def static_var(varname, value):
  def decorate(func):
    setattr(func, varname, value)
    return func
  return decorate

@static_var("line_2", None)
@static_var("line_1", None)
def test_lines(line):
  # split the line
  i = line.strip().split(' ')
  # strip each field and remove empty fields
  # Stripping is technically not necessary here...
  i = [x.strip() for x in filter(None,i)]
  count = 0

  # Setups
  if test_lines.line_1 is None:
    test_lines.line_1 = i[:]
    return count
  if test_lines.line_2 is None:
    test_lines.line_2 = test_lines.line_1[:]
    test_lines.line_1 = i[:]
    return count

  # Run a triple check
  fields = zip(i, test_lines.line_1, test_lines.line_2)
  for f in fields:
    count += test_list(f)

  # Reset our lines
  test_lines.line_2 = None
  test_lines.line_1 = None
  return count

def main(argv=None):
  if argv is None:
    argv = sys.argv
  args = get_options(argv[1:])

  if (
    ("input" not in args or args.input is None) and
    ("alt_input" not in args or args.alt_input is None)
  ):
    return 1

  correct = 0
  my_f = test_line
  if args.part == '2':
    my_f = test_lines
  if args.input is not None and os.path.isfile(args.input):
    with open(args.input) as f:
      for line in f:
        correct += my_f(line)
  elif args.alt_input is not None and len(args.alt_input) > 0:
    for line in args.alt_input:
        correct += my_f(line)
  print("There are {0} valid triangles".format(correct))

if __name__ == '__main__':
  if sys.hexversion < 0x02070000:
    print("\n\nERROR: Requires Python 2.7.0 or newer\n")
    sys.exit(1)
  sys.exit(main())
