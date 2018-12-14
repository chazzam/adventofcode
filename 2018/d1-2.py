foundRepeatedFrequency = False

sum = 0
frequencies = set()
while not foundRepeatedFrequency:
  with open("completed/input_c1-1.txt", "r") as f:
    #line = "0"
    while True:
      line = f.readline()
      if not line:
        break
      sum += int(line)
      if sum in frequencies:
        foundRepeatedFrequency = True
        print("Repeated Frequency: {}", sum)
        break
      frequencies.add(sum)
    #print("final Frequency: {}", sum)
    print(".", end="")
