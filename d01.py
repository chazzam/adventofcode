#!/usr/bin/env python
#~ direction
#~ R = +1
#~ L = -1
#~ initial direction = 0
#~ resulting direction = current direction % 4
#~ collapse even directions and odd directions together
import argparse
import os.path
import sys

def get_options(argv=None):
  """parse the commandline options.

  Check for all supported flags and do any available pre-processing
  """
  opts = argparse.ArgumentParser(
      description='http://adventofcode.com/2016/day/1')

  opts.add_argument(
    "-input", "-i",
    help="Specify input file")
  opts.add_argument(
    "-alt_input", "-a",
    help="Specify inputs on command line"
  )
  args = opts.parse_args(argv)
  return args

def walk_path(steps):
  direction = 0
  distance = [0, 0]
  cross_distance = 0
  all_coords=set()
  last = [0, 0]

  # We're going to loop through all the direction steps
  for step in steps[:]:
    # Determine our direction increment
    if 'R' in step.upper():
      direction += 1
    else:
      direction -= 1
    # normalize the direction to 0-3
    direction = direction % 4
    # determine the distance field between evens and odds
    field = direction % 2
    # get the actual change in steps, corrected for direction
    step = int(step.strip().lstrip('RrLl'))
    if direction >= 2:
      step = 0 - step;
    # Save the previous distance amount
    last = distance[:]
    # update our current distance
    distance[field] += step
    # if we haven't yet found our first intersection
    if all_coords is None:
      continue
    # Get whichever arrangement of distance change actually works
    # the order doesn't matter for what we're doing
    orig = last[field]
    # check for all the intermediate locations
    for d in (
      range(distance[field],last[field] + 1) or
      range(last[field],distance[field] + 1)
    ):
      # Skip our exact last distance amount (current starting position)
      if d == orig:
        continue
      # Update our location
      last[field]=d
      # if we've crossed this location before, then update our intersection and bail
      if tuple(last) in all_coords:
        cross_distance = abs(last[0]) + abs(last[1])
        all_coords = None
        break
      # otherwise, log this location
      all_coords.add(tuple(last))
      
  return (cross_distance, abs(distance[0]) + abs(distance[1]))

def main(argv=None):
  if argv is None:
    argv = sys.argv
  args = get_options(argv[1:])

  if (
    ("input" not in args or args.input is None) and
    ("alt_input" not in args or args.alt_input is None)
  ):
    return 1

  fields=list()
  if args.input is not None and os.path.isfile(args.input):
    with open(args.input) as f:
      for line in f:
        fields.extend(line.strip().split(','))
  elif args.alt_input is not None and args.alt_input != "":
    fields.extend(args.alt_input.strip().split(','))
  distance = walk_path(fields)
  print("crossed at {0} blocks, out of total {1} blocks traversed".format(*distance))

if __name__ == '__main__':
  if sys.hexversion < 0x02070000:
    print("\n\nERROR: Requires Python 2.7.0 or newer\n")
    sys.exit(1)
  sys.exit(main())
