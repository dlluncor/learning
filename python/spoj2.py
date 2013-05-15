
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

def Pizza():
  p = Pizzaer()
  n_friends = int(raw_input())
  for _ in xrange(n_friends):
    amount = raw_input()
    p.Process(amount)

  print p.Answer()

def main():
  Pizza()

main()
