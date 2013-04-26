import pdb

# 10 checks maximum.

# You can invalidate others for each test case you check.

def _CheckVals(vals):
  if '.' in vals:
    return ''
  count = 4
  if 'T' in vals:
    if 'X' in vals:
      vals = vals.replace('T', 'X')
    elif 'O' in vals:
      vals = vals.replace('T', 'O')

  if ('X' * count) == vals:
    return 'X'
  if ('O' * count) == vals:
    return 'O'
  return ''

def solveTic(board):
  b = board[0]
  across = [0, 4, 8, 12]
  down = [0, 1, 2, 3]
  diag = [0]
  diag_down = [3]

  for ind in across:
    vals = b[ind:ind+4]
    won = _CheckVals(vals)
    if won:
      return won + ' won'

  for ind in down:
    vals = b[ind] + b[ind+4] + b[ind+8] + b[ind+12]
    won = _CheckVals(vals)
    if won:
      return won + ' won'
  
  for ind in diag:
    vals = b[ind] + b[ind+5] + b[ind+10] + b[ind+15]
    won = _CheckVals(vals)
    if won:
      return won + ' won'
  
  for ind in diag_down:
    vals = b[ind] + b[ind+3] + b[ind+6] + b[ind+9]
    #print vals
    won = _CheckVals(vals)
    if won:
      return won + ' won'

  if '.' in b:
    return 'Game has not completed'
  else:
    return 'Draw'
  

# Tic-Tac-Toe-Tomek
def ticTacToe():
  #board = ['XXXT....OO......']
  #board2 = ['XOXTXXOOOXOXXXOO']
  #board3 = ['XXXO..O..O..T...']
  #print solveTic(board)
  #print solveTic(board2)
  #print solveTic(board3)

  fd = open('A-large-practice.in', 'r')
  lines = fd.readlines()
  T = int(lines[0])
  ind = 1
  output = []
  for case in xrange(T):
    board = ''
    for _ in xrange(4):
      line = lines[ind]
      line = line.replace('\n', '')
      board += line
      ind += 1
    #print board
    ans = solveTic([board])
    output.append('Case #%d: %s' % (case+1, ans))
    ind += 1

  fdout = open('smallans.txt', 'w')
  fdout.write('\n'.join(output))
  fdout.close()
    

import math

def _IsPalin(num):
  d = str(num)
  length = len(d)
  upto = length / 2
  for i in xrange(upto):
    if d[i] != d[length-i-1]:
      return False
    
  return True

def isFairSquare(num):
  val = math.sqrt(num)
  if val - int(val) != 0.0:
    return False
  return _IsPalin(int(val)) and _IsPalin(num)  

def fairAndSquare(low, high):
  start = low
  count = 0
  found = False
  sqstart = 0
  while start <= high:
    if not found and isFairSquare(start):
      count += 1
      # This is our first fair square, now we can get its value
      # and only check squares of those values.
      found = True
      sqstart = int(math.sqrt(start))
      sqstart += 1
    if found:
      newstart = int(math.pow(sqstart, 2))
      # Make sure this value is still in range.
      if newstart > high:
        break
      if _IsPalin(newstart) and _IsPalin(sqstart):
        count += 1
      sqstart += 1
    else: 
      start += 1
  return count

def numPalindrome():
  #fd = open('C-small-practice.in', 'r')
  fd = open('C-large-practice-1.in', 'r')
  lines = fd.readlines()
  T = int(lines[0])
  ind = 1
  output = []
  for case in xrange(T):
    print 'test case: %d' % case
    line = lines[ind]
    line = line.replace('\n', '')
    nums = line.split(' ')
    ans = fairAndSquare(int(nums[0]), int(nums[1]))
    output.append('Case #%d: %d' % (case+1, ans))
    ind += 1

  fdout = open('smallans.txt', 'w')
  fdout.write('\n'.join(output))
  fdout.close() 

def main():
  #ticTacToe()
  numPalindrome()
  pass

main()
