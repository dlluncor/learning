import math
import itertools
from datetime import datetime

def assertSameElements(els, els1):
  assert len(els) == len(els1)
  els1copy = els1[:]
  for el in els:
    els1copy.remove(el)
  assert len(els1copy) == 0

def assertEquals(el0, el1):
  if el0 != el1:
    raise AssertionError('%s != %s' % (str(el0), str(el1)))

# Timer.

class MyTimer(object):

  def __init__(self):
    self.time = datetime.now()

  def Start(self):
    # Starts the clock and returns time from now and time
    # before it was last called.
    new_time = datetime.now()
    diff_millis = (self.time - new_time).microseconds / 1000
    self.time = new_time
    return diff_millis

import collections
import functools

class memoized(object):
   '''Decorator. Caches a function's return value each time it is called.
   If called later with the same arguments, the cached value is returned
   (not reevaluated).
   '''
   def __init__(self, func):
      self.func = func
      self.cache = {}
   def __call__(self, *args):
      if not isinstance(args, collections.Hashable):
         # uncacheable. a list, for instance.
         # better to not cache than blow up.
         return self.func(*args)
      if args in self.cache:
         return self.cache[args]
      else:
         value = self.func(*args)
         self.cache[args] = value
         return value
   def __repr__(self):
      '''Return the function's docstring.'''
      return self.func.__doc__
   def __get__(self, obj, objtype):
      '''Support instance methods.'''
      return functools.partial(self.__call__, obj)

# Problem 1.
# Set of 2D points, find some integer k that are closest to (0, 0).

def findIndex(closest, apoint):
  for i in xrange(len(closest)):
    # This index is not defined, fill it in.
    if not closest[i]:
      return i
    # Or we need to be less than this distance.
    if apoint.distance < closest[i].distance:
      return i
  return -1

def replaceAndShift(index, closest, apoint):
  # Shifts all elements after the designated index.
  new_list = closest[0:index] + [apoint]
  # Not at the end of the list.
  if index != len(closest) - 1:
    new_list += closest[index:len(closest)-1]
  return new_list

class Point(object):
  def __init__(self, point):
    self.point = point
    self.distance = math.sqrt(math.pow(point[0], 2) + math.pow(point[1], 2))

  def __str__(self):
    return '(%d, %d)' % (self.point[0], self.point[1]) 

def closestPoints(k, list_of_points):
  # Closest will be a list of smallest distance to greatest.
  closest = [None for _ in xrange(k)]
  for point in list_of_points:
    # Compute distance.
    apoint = Point(point)
    # Find element to replace.
    index = findIndex(closest, apoint)
    print ('Index %d' % index)
    if index >= 0:
      # Replace and shift.
      closest = replaceAndShift(index, closest, apoint)

  return closest

def testPoints():
  points = closestPoints(4, [(1, 1), (2, 2), (3, 3), (4, 10), (0, 0), (2, 2)])
  print [str(point) for point in points]
  actual_points = [apoint.point for apoint in points]
  expected_points = [(0, 0), (1, 1), (2, 2), (2, 2)]
  assertSameElements(expected_points, actual_points)

#testPoints()

# Problem 2.

def mycombinations(elements, k):
  """Returns all combinations of elements of length k."""
  return [list(el) for el in itertools.combinations(elements, k)]


def mycombinations2(building, rest, k):
  combos = set([])
  for el in rest:
    # Add the element, then send the rest of the list until we get to
    # k - 1.
    building.append(el)
    rest = rest[:]
    rest.remove(el)
    combo = mycombinations_recurse(building, rest, k-1)
    combos.add(set(combo))

  return [list(el) for el in combos]

def powerSet(elements):
  sets = []
  for length in xrange(len(elements) + 1):
    combos = mycombinations2([], elements, length)
    sets.extend(combos)
  return sets

# Problem 3

# Parse a formula.

class Term(object):
  def __init__(self, val):
    self.val = val

  @staticmethod
  def minus(t0, t1):
    return Term(t0.val - t1.val)

  @staticmethod
  def plus(t0, t1):
    return Term(t0.val + t1.val)

def solve(term, number):
  return number / term.val


def get_binary(expr):
  # If it is a - b, return (a , Term.sub, b)
  els = expr.split('+')
  if len(els) == 2:
    return (els[0].strip(), Term.plus, els[1].strip())
  els = expr.split('-')
  if len(els) == 2:
    return (els[0].strip(), Term.minus, els[1].strip())
  return (None, None, None)

def get_mult(expr):
  # If it is number x then return a Term(number)
  els = expr.split('x')
  if len(els) == 2:
    number = float(els[0])
    return Term(number)
  return None

def get_parens(expr):
  if len(expr) <= 2:
    return None
  # Strip the parens if it matches that.
  if expr[0] == '(' and expr[-1] == ')':
    return expr[1:len(expr)-1]
  return None

# Returns one term.
def simplify(orig_expr):

  def term(expr):
    expr.strip()
    # Check if there are parenthesis first.
    new_expr = get_parens(expr)
    if new_expr:
      return term(new_expr)

    (lhs, op, rhs) = get_binary(expr)
    if lhs:
      return op(term(lhs), term(rhs))
    aterm = get_mult(expr)
    if aterm:
      return aterm

  return term(orig_expr)

def eval_expr(orig_expr):
  els = orig_expr.split('=')
  lhs = els[0].strip()
  rhs = els[1].strip()
  rhs_num = float(rhs)
  final_term = simplify(lhs)
  return solve(final_term, rhs_num)

def testSolveFormula():
  answer = eval_expr('3x + (2x) = 5')
  assertEquals(float(1), answer)
  answer = eval_expr('3x - (2x) = 5')
  print answer
  assertEquals(float(5), answer)

#testSolveFormula()

# Problem use replacements.
def get_strs(S, M):
  strs = []
  
  def add_strs(cur_s, rest):
    if not rest:
      strs.append(cur_s)
      return
    el = rest[0]
    if el in M:
      replacements = M[el]
      all_els = replacements + [el]
      for repl in all_els:
        copys = cur_s[:]
        copys += repl
        add_strs(copys, rest[1:])
    else:
      cur_s += el
      add_strs(cur_s, rest[1:])

  add_strs('', S)
  return strs

def testGetReplacements():
  M = {'f': ['F', '4'], 'b': ['B', '8']}
  S = 'fab'
  all_strs = get_strs(S, M)
  print all_strs
  expected = ['fab', 'Fab', '4ab', 'faB', 'fa8', '4aB', 'Fa8', '4a8', 'FaB']
  assertSameElements(expected, all_strs)

#testGetReplacements()

# Memoization.
# The process of saving results from a function.

factorial_memo = {}
factorial_calculations = 0
def factorial(k):
  global factorial_calculations
  if k < 2:
    return 1
  if k not in factorial_memo:
    factorial_calculations += 1
    factorial_memo[k] = k * factorial(k - 1)
  return factorial_memo[k]

def simple_fact(k):
  if k < 2:
    return 1
  return k * simple_fact(k - 1)

# Encapsulate memoziation into class.

class Memoize(object):
  def __init__(self, f):
    self.f = f
    self.memo = {}
    self.calls = 0

  def __call__(self, *args):
    if not args in self.memo:
      self.calls += 1
      self.memo[args] = self.f(*args)
    return self.memo[args]

@memoized
def simple_fact2(k):
  if k < 2:
    return 1
  return k * simple_fact2(k - 1)

def testFactorial():
  simple_fact2 = Memoize(simple_fact)
  assertEquals(120, simple_fact2(5))
  assertEquals(720, simple_fact2(6))

  timer = MyTimer()

  timer.Start()
  simple_fact2(200)
  simple_fact2(204)
  print timer.Start()

  simple_fact(200)
  simple_fact(205)
  print timer.Start()


#testFactorial()

class Overlap(object):
  def __init__(self):
    # List of elements. Even index start. Odd index end.
    self.arr = []
    self.overlap = 0

  def get_index(self, number):
    # What position does this element belong in.
    # Must be greater than previous and less than next.
    if not self.arr:
      return 0

    index = 0
    n = len(self.arr)
    while index < n:
      cur_number = self.arr[index]
      if number > cur_number:
        index += 1
      else:
        return index
    return index

  def Add(self, els):
    start, stop = els
    start_index = self.get_index(start)
    end_index = self.get_index(stop)
    before = self.arr[0:start_index]
    after = self.arr[end_index:]
    add_in = []

    prev_arr_len = len(self.arr)

    # Startin counting with some overlap.
    overlap_start = start_index
    if (start_index % 2) == 0:
      overlap_start += 1
    # Now go until we have no more pairs up until
    # the end_index or len(n) is reached.

    while overlap_start + 1 < prev_arr_len and overlap_start + 1 < end_index:
      onerange = self.arr[overlap_start + 1] - self.arr[overlap_start]
      overlap_start += 2
      self.overlap += onerange

    # Then add items to the overlap.
    if (start_index % 2) == 0:
      add_in.append(start)
    if (end_index % 2) == 0:
      add_in.append(stop)
    self.arr = before + add_in + after
    print 'New arr: %s' % (str(self.arr))

    if prev_arr_len == 0:
      return 0


    return self.overlap

def testSubsets():
  overlap = Overlap()
  assertEquals(overlap.Add([1, 3]), 0)
  assertEquals(overlap.Add([5, 6]), 0)
  assertEquals(overlap.Add([8, 9]), 0)
  assertEquals(overlap.Add([4, 10]), 2)
  assertEquals(overlap.Add([0, 12]), 10)

testSubsets()


def testPowerSet():
  power_set = powerSet([1, 2 ,3])
  print power_set
  expected_set = [[], [1], [2], [3], [1, 2], [2, 3], [1, 3], [1, 2, 3]]
  assertSameElements(expected_set, power_set)

#testPowerSet()
