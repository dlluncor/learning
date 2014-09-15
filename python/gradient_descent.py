
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

class Linear:
  """Represents a linear equation.

  The function is the loss function for a linear model:
    Sum-i (y - w*x)^2

    N = number of dimensions of each example
    i = number of examples in regression
    len(points) == len(ys) == # examples in plot

  Args:
    points: each of the sample points plotted messily along an axis.
    ys: the corresponding y for each example.
  Members:
    starts: the weights on each x(i) dimension. x(0) is the bias.
  """
  def __init__(self, points, ys):
    self.points = points
    self.ys = ys
    if not Linear.verify(points, ys):
      raise AssertionError('Each example not same number of coordinates')
    n = len(points[0])
    self.starts = [0 for _ in xrange(n + 1)] # + 1 for bias

  def verify(points, ys):
    if len(ys) != len(points):
      print 'ys != len points'
      return False

    n = len(points[0])
    for p in points:
      if n != len(p):
        print 'One example has wrong number of coors: n = %d, len(p) = %d' % (n, len(p))
        return False
    return True

  def predict(xs, ws):
    # xs = [0.2, 0.3] corresponding to x1 and x2
    # ws = [0.1, 0.4, 0.5] for w0, w1, w2
    val = ws[0]  # bias
    for i in xrange(len(xs)):
      val += x * ws[i+1]
    return val

  def eq(self, ws):
    # ws corresponds to each weight on each dimension x0 ... x(n)
    # eq is calculating the current total loss
    loss = 0.0
    for i in xrange(len(self.points)):
      p = self.points[i]
      yi = Linear.predict(p, ws)
      y = self.ys[i]
      dist = yi - y
      loss += dist**2
    # TODO: 1 / 2m multiply by
    return loss

  def partials(self):
    ps = []
    def pde(iCoor):
      # iCoor == 0, then calculating pde for w(0) or bias
      # iCoor == 1 then pde for w(1) coordinate
      pCoor = iCoor - 1 # w(1) corresponds to x(0) coordinate
      def hypo(weights):
        dist = 0
        for i in xrange(len(self.points)):
          p = self.points[i]
          distForEx = Linear.predict(p, weights) - self.ys[i]
          if iCoor != 0:
            distForEx *= p[pCoor]
          dist += distForEx

      return hypo

    # hypothesis calculation common to all PDEs
    for i in xrange(len(self.starts)):
      fprime = pde(i)
      ps.append(fprime)

    return ps

  def starts(self):
    return self.starts

def testLinearGD():
  # Minimize linear regression datasets
  pts = [[95], [85]]
  ys = [85, 95]
  l = Linear(pts, ys)
  g = GD(l.eq(), l.partials(), l.starts())
  assertApproxEqual([26.768, 0.644], g.minimize())

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
  testLinearGD()

def main():  
  testGD()

main()