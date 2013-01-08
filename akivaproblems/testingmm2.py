import mm2

def AssertIn(obj, item):
  if obj not in item:
    raise AssertionError('%s not in %s' % (obj, item))

def AssertEqual(obj, item, msg=None):
  if obj is not item:
    raise AssertionError('%s not in %s. %s' % (obj, item, msg))

(black, white) = mm2._DetermineWhiteBlack([0, 6, 1, 4, 1], [0, 6, 4, 1, 0])
AssertEqual(2, black, 'Black pegs.')
AssertEqual(2, white, 'White pegs.')

print 'Go ahead make my day'
