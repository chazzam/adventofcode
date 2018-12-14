"""
cart:
current row, current column, current direction, next track
0,100,r+,-


Direction:
left/right: c-/+
up/down: r-/+
left c-
right c+
up r-
down r+

Track:
| : row +/-
- : column +/-
+ : can do either row or column +/-
/ : process current value, swap row/column indicator, swap +/- ?
\ : process current value, swap row/column indicator ?
' ': empty space, not a track, can not use.
anything else results in collision

collisions: add current position of each cart to a tick_set each tick. if it already exists, then it becomes a collision, return those coordinates.

when do we update cart value, and when do we lookup valid?

lookup next after:
row, col, next update/direction, next track
strt: 0,100,c+,- # add one to column, lookup next track
tick: 0,101,c+,\ # add one to column, replace c with r, lookup next track (accounting for c/r swap)
tick: 0,102,r+,| # add one to row, lookup next
tick: 1,102,r+,+ # add one to row, lookup next
tick: 2,102,r+,| # add one to row, lookup next

# how to handle other curves






lookup current track before moving:
row, col, next update/direction, (last/current track no need to store...)
strt: 0,100,c+ # on a dash, leave dir alone, update row/col from dir
tick: 0,101,c+ # on a dash, leave dir alone, update row/col from dir
tick: 0,102,r+ # on a \ curve, swap dir c/r, update row/col from dir
# validity check?
"""

total_space = set()
board = []
carts = []

def find_carts(carts, line, row):
  # find position of <,>,^,v
  cart_indicators = [
    ("<", "c-"),
    (">", "c+"),
    ("^", "r-"),
    ("v", "r+")]
  for indicator in cart_indicators:
    index = 0
    while True:
      index = line.find(indicator[0], index)
      if index < 0:
        break
      # we have a cart, add it and reset index past it to continue searching
      cart = {"row": row, "col": index, "dir": indicator[1]}
      # Need to idenfity what this board location should be for the track and update it. but we can't without the whole board. Replace the cart with '@' for now
      line = line[:index] + '@' + line[(index + 1):]
      carts.append(cart)
      index += 1
  return line

def replace_cart_location(left, up, right, down):
  # Need to work out what the center of these four bits should be
  # -, |, +, /, \, ' '
  if (
      (# top left corners. if up or left are barred while down and right are available, curve forwardslash
        (up == ' ' or up == '-') 
        and (left == ' ' or left == '|') 
        and (right == '-' or right == '+') 
        and (down == '|' or down == '+'))
      or ( # bottom right corners
        (up == '|' or up == '+') 
              and (left == '-' or left == '+') 
              and (right == ' ' or right == '|') 
              and (down == ' ' or down == '-'))
      ):
    return "/"
  elif (
      (# top right corners. if up or right are barred while down and left are available, curve backslash
        (up == ' ' or up == '-') 
        and (left == '-' or left == '+') 
        and (right == ' ' or right == '|') 
        and (down == '|' or down == '+'))
      or (# bottom left corners.
        (up == '|' or up == '+') 
        and (left == '|' or left == ' ') 
        and (right == '-' or right == '+') 
        and (down == '-' or down == ' '))
      ):
    return "\\"
  elif (
    (# intersection. all sides are valid paths
        (up != '-' and up != ' ') 
        and (left != '|' and left != ' ') 
        and (right != '|' and right != ' ') 
        and (down != '-' and down != ' '))
  ):
    return "+"
  elif (
    (# horizontal path. up and down not valid
        (up == '-' or up == ' ') 
        and (left != '|' and left != ' ') 
        and (right != '|' and right != ' ') 
        and (down == '-' or down == ' '))
  ):
    return "-"
  elif (
    (# vertical path. left and right not valid
        (up != '-' and up != ' ') 
        and (left == '|' or left == ' ') 
        and (right == '|' or right == ' ') 
        and (down != '-' and down != ' '))
  ):
    return "|"
  else:
    # something went very wrong here though....
    print("WARNING: failed to parse a line: l:'{}' u:'{}' r:'{}' d:'{}'".format(left,up,right,down))
    return " "

# First need to read in the board and carts
with open("completed/input_c13.txt", "r") as f:
  first_line = True
  line_len = 0
  max_len = 0
  while True:
    line = f.readline()
    if not line:
      break
    line = line.strip("\n")
    # need to process out carts and update map track
    line = find_carts(carts, line, len(board))
    if first_line:
      # add an empty first line
      line_len = len(line) + 2
      board.append(" " * line_len)
      first_line = False
    # pad left and right edges with empty spaces
    board.append(" " + line + " ")
  # add an empty last line
  board.append(" " * line_len)
#print(board)
# TODO: probably need to do something different to handle two carts starting near each other...

# Now need to fix board to remove carts
# we have especially padded the edges with spaces so we don't have to handle edges especially different
for i in range(1, len(board)):
  index = 1
  while True:
    index = board[i].find('@', index)
    if index < 0:
      break
    #print(index, board[i])
    up    = board[i - 1][index]
    left  = board[i][index - 1]
    right = board[i][index + 1]
    down  = board[i + 1][index]
    loc = replace_cart_location(left, up, right, down)
    if loc == " ":
      print("i:{} ind:{}:: '{},{},{},{}' len:{} lines:'\n{}\n{}\n{}'\n".format(i,index,up,left,right,down, len(board[i]), board[i - 1], board[i], board[i + 1]))
    
    #print(loc)
    board[i] = board[i][:index] + loc + board[i][(index + 1):]

#print(board)
# process tick through carts
#for cart in sorted(carts, key=lambda c: c['row']*10000 + c['col']):
 # pass

 # remember to subtract one each from row and column when reporting collision coordinates
