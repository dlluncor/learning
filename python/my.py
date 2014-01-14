# My qs.

def Assert(el0, el1):
  if el0 != el1:
    print 'Failed! %s != %s' % (str(el0), str(el1))

class Node(object):

  def __init__(self, val):
    self.to = None # pointer to next.
    self.val = val # value I store.

  def Print(self):
    arr = ['%d' % self.val]
    cur = self.to
    while cur:
      arr.append('%d' % cur.val)
      cur = cur.to
      if cur == self:
        break
    print ', '.join(arr)

def InsertHelp(prev, cur):
  # Insert cur ahead of prev.
  temp = prev.to
  cur.to = temp
  prev.to = cur

def InsertF(node, el):
  insertEl = Node(el)
  
  # Cover base cases when there is only one element or none.
  if not node:
    return insertEl
  if not node.to:
    # Only one element, insert anywhere!
    InsertHelp(node, el)
    return insertEl

  start = node # Keep track of where I've started.
  p = node
  n = node.to
  while True:
    # Solve for smaller and greater.
    if p.val < n.val:
      # Increasing in the list.
      if el >= p.val and el <= n.val:
        # Insert ahead of p
        InsertHelp(p, insertEl)
        break
    elif p.val > n.val:
      # Hit the end of the list.
      if el > p.val:
        # Insert ahead of p.
        InsertHelp(p, insertEl)
        break
      elif el < n.val:
        # Smallest element in the list.
        InsertHelp(p, insertEl)
        break
    elif p.val == n.val:
      # Only insert if we insert the same element.
      if el == p.val:
        InsertHelp(p, insertEl)
        break
   
    # Are we about to do a full loop around.
    if n == start:
      # Decide our insert now.
      InsertHelp(p, insertEl)
      break
 
    p = n
    n = n.to
  return insertEl

def Insert(indexToPullFromNodeArr, arr, insertEl):
  # Tests the method.
  keepNode = None
  nodesList = [Node(el) for el in arr]
  lastInd = len(arr) - 1
  for index, el in enumerate(arr):
    node = nodesList[index]
    if index == lastInd:
      node.to = nodesList[0]
    else:
      node.to = nodesList[index+1]
    if index == indexToPullFromNodeArr:
      keepNode = node
  inserted = InsertF(keepNode, insertEl)
  inserted.Print()
 
def TestInsert():
  # Arbitrary pointer into a list, insert the element.
  Insert(1, [1, 2, 5], 4) # In the middle.
  Insert(1, [3, 3, 3], 3) # all same elements.
  Insert(1, [3, 3, 3], 1) # All same elements.
  Insert(1, [3, 3, 3], 5)
  Insert(1, [1, 5, 7], 9) # biggest num.
  Insert(3, [3, 4, 5, 6], 7)
  Insert(0, [1, 5, 7], -1) # smallest num.
  Insert(3, [3, 4, 5, 6], -1)
  Insert(0, [], 2) # Into an empty list.
  Insert(0, [1], 2) # Into a list with one element.
  Insert(1, [3, 3, 3, 3, 3, 5], 4)

'''
1 byte rune -- 0xxxxxxx
continuation byte -- 10xxxxxx
2 byte rune -- 110xxxxx 10xxxxxx
3 byte rune -- 1110xxxx 10xxxxxx 10xxxxxx
4 byte rune -- 11110xxx 10xxxxxx 10xxxxxx 10xxxxxx
5 byte rune -- 111110xx 10xxxxxx 10xxxxxx 10xxxxxx 10xxxxxx
6 byte rune -- 1111110x 10xxxxxx 10xxxxxx 10xxxxxx 10xxxxxx 10xxxxxx
7 byte rune -- 11111110 10xxxxxx 10xxxxxx 10xxxxxx 10xxxxxx 10xxxxxx 10xxxxxx
8 byte rune -- 11111111 10xxxxxx 10xxxxxx 10xxxxxx 10xxxxxx 10xxxxxx 10xxxxxx 10xxxxxx


0xxxxxxx 11111111 10xxxxxx 10xxxxxx 10xxxxxx 10xxxxxx 10xxxxxx 10xxxxxx 10xxxxxx 1110xxxx 10xxxxxx 10xxxxxx
'''

# 34

def leading(abyte):
  l = 0
  for i in xrange(8):
    isOne = abyte >> i & 0x1
    if isOne == 0:
      l = 0
    else:
      l += 1
  return l

def Utf8Valid(arr, nextInd, contBytes):
  # print '%d %d' % (nextInd, contBytes)
  if len(arr) == nextInd:
    return contBytes == 0
  nextByte = arr[nextInd]
  nextNumOnes = leading(nextByte)
  nextContBytes = continuationBytes(nextNumOnes)
  if contBytes == 0:
    # Needs to not be a continuation byte.
    if nextContBytes is None:
      return False
    return Utf8Valid(arr, nextInd + 1, nextContBytes)
  else:
    # Needs to be a continuation byte.
    if nextContBytes is not None:
      return False
    # keep going
    return Utf8Valid(arr, nextInd + 1, contBytes - 1) 

def continuationBytes(numOnes):
  contBytes = 0
  if numOnes == 1:
    return None
  if numOnes > 0:
    contBytes = numOnes - 1
  return contBytes  

def Utf8Parser(arr):
  return Utf8Valid(arr, 0, 0)


def toBinArr(charStr):
  els = charStr.split(' ')
  return [int(el, 2) for el in els]

def TestUtf8():
  zero = int('00000000', 2)
  cont = int('10000000', 2)
  two = int('11000000', 2)
  three = int('11100000', 2)
  four = int('11110000', 2)
  five = int('11111000', 2)
  six = int('11111100', 2)
  seven = int('11111110', 2)
  eight = int('11111111', 2)
  Assert(True, Utf8Parser([zero]))
  Assert(False, Utf8Parser([cont]))
  Assert(True, Utf8Parser([two, cont, two, cont, three, cont, cont]))
  print 'Done' 

from copy import copy

def distance(charsToInd):
  vals = []
  for _, val in charsToInd.iteritems():
    vals.append(val)
  vals = sorted(vals)
  if len(vals) == 0:
    return 0
  return vals[len(vals)-1] - vals[0] + 1

class Info(object):

  def __init__(self):
    self.total = 0
    self.chars = {}  

  def closestNotMe(self, word, index):
    # There could be no biggest as well, in case just add me.
    if word in self.chars:
      # Only add me if I decrease the overall size.
      old = distance(self.chars)
      newchars = copy(self.chars)
      newchars[word] = index
      new = distance(newchars)
      if new < old:
        self.chars = newchars      
    else:
      # Have to add me.
      self.chars[word] = index
      #print 'Char map: %s' % str(self.chars)


def Dist(arr, chars):
  charMap = {}
  for char in chars:
    charMap[char] = True

  info = Info()
  
  for index, word in enumerate(arr):
    if word in charMap:
      #print 'Word: %s' % word
      # Find closest that is not me.
      info.closestNotMe(word, index) 

  # Find the shortest one that has all the characters.
  numChars = len(chars)
  smallestDist = -1
  if numChars == len(info.chars.keys()):
    print 'Found a candidate'
    print 'Final: %s' % str(info.chars)
    candidate = distance(info.chars)
    if smallestDist == -1:
      smallestDist = candidate
    elif candidate < smallestDist:
      smallestDist = candidate

  if smallestDist == -1:
    return None
  return smallestDist


def TestDistanceInWords():
  # 11:42 to 12:08. 25 minutes.
  """
  a x x b c
  xx a b c
  x x a b
  
  a xxxxxxxxxx bca
  a xxxxxcxxxxxxx b c d xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxa
  """
  # Find distances between words.
  # Find the minimum sum amongst all the distances.
  # Lots of occurrences this is bad...
 
  # If you find a character, find the distance between that
  # and the last character that you saw that is in the set of
  # words you are looking for.
  # If that sum is less than the current sum you see, add that
  # character to this position's best character set.

  # Then iterate through the array again and find the minimum
  # val that contains all characters in the set.

  input1 = 'axxcxxbdcxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxa'
  print Dist(input1, ['a', 'b', 'd', 'c'])
  print Dist('ab', ['a', 'b', 'd', 'c'])
  print Dist('abccccddddd', ['a', 'b', 'd', 'c'])
  arr = 'a b c c c c d c a b d'
  # a - 0 8
  # b - 1 9
  # c - 2 3 4 5 7
  # d - 6 10
  arr = arr.replace(' ', '')
  print Dist(arr, ['a', 'b', 'd', 'c'])

def main():
  #TestInsert()
  #TestUtf8()
  TestDistanceInWords()

main()
