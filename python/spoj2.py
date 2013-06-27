
import math

class Pizzaer(object):

  def __init__(self):
    self.fourths = 0
    self.halves = 0
    self.threeqs = 0
    self.total = 1  # For myself first.

  def Process(self, amount):
    if amount == '1/4':
      # Use up 3/4ths if possible otherwise save.
      if self.threeqs > 0:
        self.threeqs -= 1
        self.total += 1
      else:
        self.fourths += 1

    elif amount == '1/2':
      if self.halves > 0:
        self.halves -= 1
        self.total += 1
      else:
        self.halves += 1
    else:
      if self.fourths > 0:
        self.fourths -= 1
        self.total += 1
      else:
        self.threeqs += 1
 
  def Answer(self):
    self.total += self.threeqs  # If we have any 3/4 left, they take up a whole pizza.
    if self.halves > 0:
      # There is only 1 1/2 at this point.
      # Use up all the 1/4 values that you can.
      if self.fourths >= 2:
        self.fourths -= 2
        self.total += 1
      elif self.fourths >= 1:
        self.fourths -= 1
        self.total += 1
      else:
        self.total += 1

    # Deal with remaining 1/4ths. The amount of pizzas you have left is
    # num4s / 4 rounded up.
    self.total += math.ceil(self.fourths / 4.0)
    return int(self.total)

#EGYPIZZA
def Pizza():
  p = Pizzaer()
  n_friends = int(raw_input())
  for _ in xrange(n_friends):
    amount = raw_input()
    p.Process(amount)

  print p.Answer()

START = 's'
STOP = 'e'

class GBaller(object):

  def __init__(self):
    self.Reset()

  def Reset(self):
    self.inds = {}

  def Process(self, start, stop):
    self.inds[start] = START
    self.inds[stop] = STOP

  def Answer(self):
    maxPeople = 0
    curPeople = 0
    for key, val in sorted(self.inds.iteritems()):
      if val == START:
        curPeople += 1
        if curPeople > maxPeople:
          maxPeople = curPeople
      else:
        curPeople -= 1

    return maxPeople

#BYTESE2
def GreatBall():
  T = int(raw_input())
  b = GBaller()
  for _ in xrange(T):
    b.Reset()
    N = int(raw_input())
    for _ in xrange(N):
      nums = [int(el) for el in raw_input().split(' ')]
      b.Process(nums[0], nums[1])
      
    print b.Answer()

def invTri(n):
  if n <= 1:
    return 0
  elif n == 2:
    return 1

  return 2 + (n - 3) * (n - 2) / 2

def InvTriangle():
  T = int(raw_input())

  for _ in xrange(T):
    N = int(raw_input())
    print invTri(N)

def _findMin(nums):
  mel = nums[0]
  if nums[1] < mel:
    if nums[2] < nums[1]:
      return nums[2]
    else:
      return nums[1]
  elif nums[2] < mel:
    return nums[2]
  return mel

def countTri(rows):
  cost0 = int(raw_input().split(' ')[1])
  vals = [int(el) for el in raw_input().split(' ')]
  min1 = _findMin(vals)
  vals = [int(el) for el in raw_input().split(' ')]
  min2 = _findMin(vals)
  cost3 = int(raw_input().split(' ')[1])
  return cost0 + min1 + min2 + cost3

def Trigraph():
  i = 1
  while True:
    rows = int(raw_input())
    if rows == 0:
      break
    print '%d. %d' % (i, countTri(rows))
    i += 1

def Tour():
  T = int(raw_input())
  for _ in xrange(T):
    can_be_beaten = {} # integer to True if i can be beaten
    udders = {}
    N = int(raw_input())
    for i in xrange(N):
      peeps = raw_input().split(' ')
      udders[i] = peeps[1:]
      if peeps[0] != '0':
        can_be_beaten['%d' % (i+1)] = True

    invincibles = 0
    for _, peeps in udders.iteritems():
      count_stacked = True
      for peep in peeps:
        if peep not in can_be_beaten:
          count_stacked = False
          break
      if count_stacked:
        invincibles += 1
    print invincibles

# T Interview.
# Given n homes that can each donate D(i) amount, but you can't get from neighbors, what is the max
# donations I can choose from?

answers = {}

def _MaxDonations(nums):
  """nums - donations from each of the houses."""

  T = {}
  # Most donations you can get from just your range is yourself.
  for index, num in enumerate(nums):
    T[(index, index)] = num

  N = len(nums)

  def _MaxDon(orig_nums, cur_index, T, called):
    if (cur_index, N-1) in T:
      return T[(cur_index, N-1)]

    if cur_index >= N:
      return 0

    called[0] += 1
    # Missing key?
    including_me = orig_nums[cur_index] + _MaxDon(orig_nums, cur_index+2, T, called)
    not_including_me = _MaxDon(orig_nums, cur_index + 1, T, called)
    return max(including_me, not_including_me)
  
  invocations = [0]  
  max_val = _MaxDon(nums, 0, T, invocations)
  print 'Called:\t %s' % str(invocations)
  print 'N:\t %s' % str(N)
  return max_val

def HouseDonations():
  T = int(raw_input())
  for _ in xrange(T):
    nums = [int(el) for el in raw_input().split(' ')]
    print _MaxDonations(nums)


def main():
  #Pizza()
  #GreatBall()
  #InvTriangle()
  #Trigraph()
  #Tour()
  HouseDonations()

main()
