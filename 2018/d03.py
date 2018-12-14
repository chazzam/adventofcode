part = 1

if part == 1:
  total_space = set()

  with open("completed/input_c3.txt", "r") as f:
    while True:
      line = f.readline()
      if not line:
        break
      # add all the ranges to a set: 704x926, 704x927... 704x930 ... 709x930
