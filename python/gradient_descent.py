
class GD:
  """Finds the local minimum for an equation.
  
  Args:
    eq: f(x) where x is an array of input points
    partials: f'(x) for each x(i)
    starts: initial x(i) guess
  """
  def __init__(self, eq, partials, starts):
    self.eq = eq
    self.partials = partials
    self.starts = starts
    self.rate = 0.001
    self.mindiff = 0.00000000001

  def minimize(self):
    # assert len(self.partials) == len(self.starts)
    n = len(self.partials)
    d = ''
    points = self.starts
    cur = self.eq(points)
    b4 = cur - 1000
    while abs(cur - b4) > self.mindiff:
      # Calculate gradients at each coordinate
      curPartials = []
      for p in self.partials:
        curPartials.append(p(points))
      # Update each coordinate
      for i in xrange(n):
        points[i] = points[i] - self.rate * curPartials[i]
      # Find out how far I moved.
      b4 = cur
      cur = self.eq(points)
    return points

eps = 0.0001

def assertApproxEqual(l0, l1):
  if len(l0) != len(l1):
    print 'Lengths not equal. %d vs %d' % (len(l0), len(l1))    
  for i in xrange(len(l0)):
    if abs(l0[i] - l1[i]) < eps:
      continue
    print 'At pos %d, %.3f != %.3f' % (i, l0[i], l1[i])    

def testGD():
# Wolfphram minimize -5 - 3x + 4y + x^2 - x y + y^2
# Eq, [partials], [starting points]
  def eq(xs):
    return -5 - 3*xs[0]+4*xs[1]+xs[0]**2 - xs[0]*xs[1] + xs[1]**2
  def p0(xs):
    return -3+2*xs[0]-xs[1]
  def p1(xs):
    return 4 -xs[0]+2*xs[1]

  g = GD(eq, [p0, p1], [0, 2])
  assertApproxEqual([0.66666666, -1.666666666], g.minimize())
  #assertThat([.6666666], Approx(Equals(g.minimize())))

def main():  
  testGD()

main()