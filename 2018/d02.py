import collections

part = 1

if part == 1:
  has2 = set()
  has3 = set()

  with open("completed/input_c2-1.txt", "r") as f:
    while True:
      line = f.readline()
      if not line:
        break
      counts = collections.Counter(line)
      for n in counts.values():
        if n == 2:
          has2.add(line)
        elif n == 3:
          has3.add(line)
  my_checksum = len(has2) * len(has3)
  print("has2: {}, has3: {}, Checksum: {}".format(len(has2), len(has3), my_checksum))
else:
  permutations = set()
  foundPermutation = False

  with open("completed/input_c2-1.txt", "r") as f:
    while not foundPermutation:
      line = f.readline()
      if not line:
        break
      # work through each line, removing one character at each position and adding it to the set
      line_perms = set()
      for m in range(1, len(line), 1):
        n = m + 1
        perm = "{}{}".format(line[:m], line[n:])
        if perm in permutations:
          print("Found perm:'{}'\n from line:'{}'".format(perm.strip(), line.strip()))
          foundPermutation = True
          break
        line_perms.add(perm)
      permutations.update(line_perms)
