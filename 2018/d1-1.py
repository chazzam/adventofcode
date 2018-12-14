with open("completed/input_c1-1.txt", "r") as f:
  line = "0"
  sum = 0
  while line:
    sum += int(line)
    line = f.readline()
  print("Final Frequency: {}", sum)
