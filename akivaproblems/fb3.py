# Binary search through an array.
num_comp = 0

def bSearch(arr, left, right, val):
  global num_comp
  n = right - left
  if n == 0:
    return None
  num_comp += 1
  if n == 1:
    if arr[left] == val:
      return left
    else:
      return None
  half = n / 2
  halfval = arr[half]
  if val == halfval:
    return half
  elif val < halfval: 
    return bSearch(arr, left, half, val)
  else:
    return bSearch(arr, half, right, val)


def findWord(board, wordOrig):
  allowedPlacesOrig = []
  numRows = len(board)
  numCols = len(board[0])
  for i in xrange(numRows):
    for j in xrange(numCols):
      allowedPlacesOrig.append([i, j])
  visitedOrig = []

  def findWordR(word, allowedPlaces, visited):
    #print word
    #print allowedPlaces
    if not word:
      return True

    match = word[0]
    valid_places = []

    for place in allowedPlaces:
      rowI = place[0]
      colI = place[1]
      letter = board[rowI][colI]
      if letter == match:
        valid_places.append(place)

    if not valid_places:
      #print 'no match in place'
      return False

    rest = word[1:]
    for valid_place in valid_places:
      visited.append(valid_place)
      # Find all valid places. 
      valid_neighs = []
      for place in allowedPlacesOrig:
        if place in visited:
          continue
        rowI = valid_place[0]
        colI = valid_place[1]
        if place[0] >= (rowI - 1) and place[0] <= (rowI + 1):
          if place[1] >= (colI -1) and place[1] <= (colI + 1):
            valid_neighs.append(place)
      #print valid_neighs
      # Only neighbors are allowed. 
      if findWordR(rest, valid_neighs, visited):
        return True
      visited.remove(valid_place)
    return False
 
  return findWordR(wordOrig[:], allowedPlacesOrig, visitedOrig[:]) 

def testBsearch():
  arr = [1, 2, 10, 14, 100, 120, 135, 150, 200] 
  print bSearch(arr, 0, len(arr) -1, 2)
  print num_comp

def makeBoard(string):
  board = []
  for line in string.split('\n'):
    row = []
    for char in line:
      row.append(char)
    board.append(row)
  return board

def testBoggle():
  boardstr = 'SMEF\nRATD\nLONI\nKAFB'
  board = makeBoard(boardstr)
  print board
  assert False == findWord(board, 'STAR')
  assert False == findWord(board, 'TONE')
  assert findWord(board, 'NOTE')
  assert findWord(board, 'SAND')

  boardDiff = 'SAAA\nFFFA\nAZZB\nDDDA'
  board2 = makeBoard(boardDiff)
  print board2
  assert findWord(board2, 'AB')
  assert findWord(board2, 'DDD')
  assert False == findWord(board2, 'AAAAA')


maxc = 0

# Crappy way no dynamic programming solution.
def costJobs(jobs):
  global maxc
  jobs = sorted(jobs)
  path = []
  # Sort by start time.
  def jobsR(startInd, cur_end, total_cost, cur_path):
    global maxc
    rest = jobs[startInd:]
    if not rest:
      return total_cost

    for ind, job in enumerate(rest):
      if job[0] >= cur_end:
        next_cur_path = cur_path + [ind]
        next_cost = total_cost + job[2]
        next_end = job[1]
        cur_max_cost = jobsR(ind + 1, next_end, next_cost, next_cur_path)
        if cur_max_cost > maxc:
          maxc = cur_max_cost
    return total_cost

  jobsR(0, 0, 0, path)
  actual_max = maxc
  maxc = 0
  return actual_max 


# Good linear programming solution.
def costJobs2(jobs):
  seen = {}  # map of original time to index in cost table.
  for job in jobs:
    seen[job[0]] = True
    seen[job[1]] = True

  costs = {}
  for curTime in seen:
    costs[curTime] = 0 

  sorted(jobs, key=lambda job: job[1])
  for ind, job in enumerate(jobs):
    nowStart = job[0]
    nowEnd = job[1]
    nowCost = job[2]
    bestCurCost = costs[nowEnd]
    bestUpToStart = costs[nowStart]
    if (nowCost + bestUpToStart) > bestCurCost:
      costs[nowEnd] = nowCost + bestUpToStart

  maxCost = -1
  for curTime in costs:
    if costs[curTime] > maxCost:
      maxCost = costs[curTime]
  return maxCost


def getMaxSpiral(board):
  # Compute horiz sums.
  print board
  horizs = []
  for rowI, row in enumerate(board):
    horiz = []
    for colI, col in enumerate(row):
      if not horiz:
        horiz.append(col)
      else:
        horiz.append(col + horiz[-1])
    horizs.append(horiz)

  # Vertical sums.
  verts = []
  for rowI, row in enumerate(board):
    vert = [] 
    for colI, col in enumerate(row):
      if rowI == 0:
        vert.append(col)
      else:
        vert.append(col + verts[rowI - 1][colI])
    verts.append(vert)

  nRows = len(board)
  nCols = len(board[0])
  maxN = min(nRows, nCols)
  curSize = 1
  while curSize < maxN:
    # Find all spirals of that size.
    for rowI, row in enumerate(board):
      for colI, _ in enumerate(row):
        if (curSize - 1 + rowI) < nRows and (curSize - 1 + colI) < nCols:
          # Make sure I fit.
          val0 =  
    curSize += 2 



def makeSpiralBoard(lines):
  rows = []
  for line in lines:
    row = []
    for col in line.split(','):
      row.append(int(col))
    rows.append(row)
  return rows

def testSpirals():
  spirals = ['1,1,1', '-1,7,10', '10,8,10']
  board = makeSpiralBoard(spirals)
  print getMaxSpiral(board)

def testSortJobs():
  #jobs = [(1, 2, 3), (3, 5, 10), (3, 7, 15)]
  #jobs = [(0,2,3), (1,3,5)]
  #jobs = [(0,2,3), (1,3,5), (0,100000,3), (1,3,5)]
  #jobs = [(0,10,1),(0,2,3), (1,3,5), (2,5,9)] 
  m2 = [(0,10,1),(0,2,3), (1,3,5), (6,9,2),(2,5,9),(2,10000000000000000,8)]
  m = []
  for i in xrange(102):
    m.append((i, i+1, 1))
  m.append((2,101,95))
  print costJobs2(m2)

def tests():
  #testBsearch()
  #testBoggle()
  #testSortJobs()
  testSpirals()

tests()
