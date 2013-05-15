

#ACPC10A
def _Progress(ns):
  diff = ns[1] - ns[0]
  diff2 = ns[2] - ns[1]
  if diff2 == diff:
    return 'AP %d' % (ns[2] + diff)

  factor = ns[2] / ns[1]
  return 'GP %d' % (int(factor * ns[2]))

def progression():
  line = raw_input()
  while line:
    nums = line.split(' ')
    nums = [int(num) for num in nums]
    print _Progress(nums)
    line = raw_input()
    if line == '0 0 0':
      break


import bisect

class Inv(object):

  def __init__(self, N):
    self.N = N
    self.a = []
    self.size = 0
    self.inversions = []

  def Add(self, num):
    pos = _InsertSorted(self.a, num)
    num_inversions = self.size - pos
    self.inversions.append(num_inversions)
    self.size += 1

  def Answer(self):
    ans = 0
    for inversion in self.inversions:
      ans += inversion
    return ans


def _InsertSorted(a, el):
  pos = bisect.bisect_right(a, el)
  a.insert(pos, el)
  return pos


class Node(object):
  def __init__(self, data):
    self.left = None
    self.right = None
    self.d = data


class BST(object):

  def __init__(self):
    self.root = None

  def _AddRec(self, curNode, insertNode):
    goLeft = insertNode.d < curNode.d
    if goLeft:
      if not curNode.left:
        curNode.left = insertNode
        return
      self._AddRec(curNode.left, insertNode)
    else:
      if not curNode.right:
        curNode.right = insertNode
        return
      self._AddRec(curNode.right, insertNode)

  def Add(self, el):
    node = Node(el)
    if not self.root:
      self.root = node
      return
    self._AddRec(self.root, node)

  def Print(self):
    output = []
    def _PrintRec(node):
      if not node:
        return
      if node.left:
        _PrintRec(node.left)
      output.append('%d' % node.d)
      if node.right:
        _PrintRec(node.right)

    _PrintRec(self.root)
   
    print ' '.join(output)

  def SpecialAnswer(self):
    def _PrintRec(node, numLeft, myvals):
      if not node:
        return
      if node.left:
        _PrintRec(node.left, numLeft + 1, myvals)
      myvals[0] += numLeft
      if node.right:
        _PrintRec(node.right, numLeft, myvals)
    vals = [0]
    _PrintRec(self.root, 0, vals)
    return vals[0]

class Inv2(object):

  def __init__(self, N):
    self.N = N
    self.bst = BST()

  def Add(self, num):
    self.bst.Add(num)

  def Answer(self):
    return self.bst.SpecialAnswer() 


def Inversions():
  T = int(raw_input())
  raw_input()
  for _ in xrange(T):
    N = int(raw_input())
    inv = Inv2(N)
    for _ in xrange(N):
      num = int(raw_input())
      inv.Add(num)

    print inv.Answer()
    raw_input()

import math

def _GetMaxDivers(G, B):
  big = G
  little = B
  if B > G:
    big = B
    little = G
  if big == 0 and little == 0:
    return 0

  left = big - 1 - little
  if left <= 0:
    return 1
  extra = int(math.ceil(left / (little + 1.0)))
  return extra + 1

# GIRLSNBS
def GirlBoys():
  while True:
    line = raw_input()
    if line == '-1 -1':
      break
    nums = [int(el) for el in line.split(' ')]
    print _GetMaxDivers(nums[0], nums[1])


from collections import deque

class Bitmapper(object):

  def __init__(self, numRows, numCols):
    self.numRows = numRows 
    self.numCols = numCols

  def ReadMap(self):
    self.valueMap = {}
    self.q = deque()
    for rowInd in xrange(self.numRows):
      line = raw_input()
      for colInd in xrange(self.numCols):
        val = int(line[colInd])
        inds = (rowInd, colInd)
        if val == 1:
          self.valueMap[inds] = {'seen': True, 'distance': 0}
          self.q.append(inds)
        else:
          self.valueMap[inds] = {'seen': False, 'distance': -1} 
    return

  def Solve(self):
    # Find all ones and put them onto the queue.
    q = self.q
    valueMap = self.valueMap
    while q:
      inds = q.pop()
      # Find neighbors.
      # Put them on queue if any neighbor is not seen yet.
      up = (inds[0] -1, inds[1])
      down = (inds[0] + 1, inds[1])
      left = (inds[0], inds[1] - 1)
      right = (inds[0], inds[1] + 1)
      myObj = valueMap[inds]
      for neigh in [up, down, left, right]:
        if neigh not in valueMap:
          continue
        valueObj = valueMap[neigh]
        # We haven't seen it yet add to its distance, and add to queue.
        curDist = valueObj['distance']
        if curDist == -1:
          valueObj['distance'] = myObj['distance'] + 1
        else:
          # Check if it is a more optimal distance, and then update.
          myNewDist = myObj['distance'] + 1
          if myNewDist < curDist:
            valueObj['distance'] = myNewDist
            # Add it back to the queue this has been updated.
            valueObj['seen'] = False
            #q.append(neigh)

        # Add to queue only if it has not been explored yet.
        if not valueObj['seen']:
          q.append(neigh)
      myObj['seen'] = True
    # Iterate through valueMap getting the distances.
    output = []
    for rowInd in xrange(self.numRows):
      line = []
      for colInd in xrange(self.numCols):
        valueObj = valueMap[(rowInd, colInd)]
        line.append('%d' % valueObj['distance'])
      output.append(' '.join(line))

    print '\n'.join(output)
    return 

# BITMAP
def Bitmap():
  T = int(raw_input())
  for _ in xrange(T):
    try:
      line = raw_input()
      nums = [int(el) for el in line.split(' ')]
      bp = Bitmapper(nums[0], nums[1])
      bp.ReadMap()
      bp.Solve()
    except:
      pass

def partySolver(budget, numParties):
  costs = []
  for i in xrange(budget + 1):
    costs.append(0)
  maxFun = 0
  maxDollars = 0
  for i in xrange(numParties):
    line = raw_input()
    els = line.split(" ")
    nums = [int(el) for el in els]
    cost = nums[0]
    fun = nums[1]
    maxBudgetToCheck = budget - cost
    for k in xrange(maxBudgetToCheck, -1, -1):
      curFun = costs[k]
      if k != 0 and curFun == 0:
        continue
      newBudget = cost + k
      possNewFun = curFun + fun
      if costs[newBudget] < possNewFun:
        costs[newBudget] = possNewFun
        if possNewFun > maxFun:
          maxFun = possNewFun
          maxDollars = newBudget
  
  raw_input()
  return '%d %d' % (maxDollars, maxFun)

def Party():
  while True:
    line = raw_input()
    if line == "0 0":
      break
    els = line.split(" ")
    nums = [int(el) for el in els]
    print partySolver(nums[0], nums[1])

def main():
  #progression()
  #Inversions()
  #GirlBoys()
  #Bitmap()
  Party()

main()
