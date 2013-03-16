import math
import itertools

def assertSameElements(els, els1):
  assert len(els) == len(els1)
  els1copy = els1[:]
  for el in els:
    els1copy.remove(el)
  assert len(els1copy) == 0

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

def testPowerSet():
  power_set = powerSet([1, 2 ,3])
  print power_set
  expected_set = [[], [1], [2], [3], [1, 2], [2, 3], [1, 3], [1, 2, 3]]
  assertSameElements(expected_set, power_set)

testPowerSet()
