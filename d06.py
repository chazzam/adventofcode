#!/usr/bin/env python
import argparse
import os.path
import sys
import collections

class RepeatedMessage:
  """Repeated Message"""
  def __init__(self):
    self.message = list()

  def text(self):
    message = ""
    for x in self.message:
      # x.most_common always returns a list of tuples
      # so we need to get the first element twice
      message += x.most_common(1)[0][0]
    return message

  def uncommon(self):
    message = ""
    for x in self.message:
      # neither reversed() nor list.reverse() were happy as a one-liner
      r = x.most_common()
      r.reverse()
      # x.most_common always returns a list of tuples
      # so we need to get the first element twice
      message += r[0][0]
    return message

  def update(self, line):
    """Update with the new line"""
    if line is None or line == "":
      return
    # store each column in its own Counter in the message list
    for i,v in enumerate(line):
      # this is apparently the pythonic way of doing this
      # try it, if it fails do it different
      # but hey, we don't care if a line changes length in the middle!
      #   but is that good or bad?
      try:
        self.message[i].update(v)
      except IndexError:
        self.message.append(collections.Counter(v))

def get_options(argv=None):
  """parse the commandline options.

  Check for all supported flags and do any available pre-processing
  """
  opts = argparse.ArgumentParser(
      description='http://adventofcode.com/2016/day/6')

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

def main(argv=None):
  if argv is None:
    argv = sys.argv
  args = get_options(argv[1:])

  if (
    ("input" not in args or args.input is None) and
    ("alt_input" not in args or args.alt_input is None)
  ):
    return 1

  message = RepeatedMessage()
  if args.input is not None and os.path.isfile(args.input):
    with open(args.input) as f:
      for line in f:
        message.update(line.strip())
  elif args.alt_input is not None and len(args.alt_input) > 0:
    for line in args.alt_input:
        message.update(line.strip())
  print("Part 1 is {}, Part 2 is {}".format(message.text(), message.uncommon()))

if __name__ == '__main__':
  if sys.hexversion < 0x02070000:
    print("\n\nERROR: Requires Python 2.7.0 or newer\n")
    sys.exit(1)
  sys.exit(main())
