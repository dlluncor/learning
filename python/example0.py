
def checker(func):

  def runme(a):
    if a < 0:
      return 0
    out = func(a)
    if out < 0:
      return 0 
    return out

  return runme

# @checker really just means checker(minus10)(a)
@checker
def minus10(a):
  return a - 10

def charge0(a, *args, **kwargs):
  print a
  print args
  print kwargs

def main():
  # checker runs on minus10 because we used the decorator to run it every single
  # time this function is called.
  ## print minus10(-3)
  print charge0(1, 2, 3, d=10,e=15)


if __name__ == '__main__':
  main()
