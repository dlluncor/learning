import re
import math

# ADDREV
def _OutputRevSum(nums):
  def _RevNum(num_str):
    new_str = re.sub('0+$', '', num_str)
    new_str = new_str[::-1]
    if not new_str:
      return 0
    return int(new_str)
  num0 = _RevNum(nums[0])
  num1 = _RevNum(nums[1])
  print _RevNum(str(num0 + num1))

def _RevNumbers():
  N = int(raw_input())
  for i in xrange(N):
    line = raw_input()
    nums = [el for el in line.split(' ')]
    _OutputRevSum(nums)

# TEST
def _MeanLife():
  while True:
    num = raw_input()
    if num == '42':
      break
    print num


# Not correct yet :<
def _CheckMersennePrimality(mersenne, n):
  # Check for numbers no larger than this.
  largest = pow(mersenne, 0.5)

  # Factors will be of form 2kn + 1
  k = 1
  while True:
    factor = (2 * k * n) + 1
    if factor > largest:
      return True
    
    if (mersenne % factor) == 0:
      return False
    k += 1

  return True

def _GetPrimes(primes, lower, upper):
  valids = set([])
  for prime in primes:
    # Go through prime numbers, check if they are in range, and also
    # if 2 ^ n is in range, then check if its prime as well.
    n = prime
    if n < lower or n > upper:
      continue
    valids.add(n)
    mersenne = pow(2, n) - 1
    if mersenne < lower or mersenne > upper:
      continue
    # Check mersenne number for primality.
    if _CheckMersennePrimality(mersenne, n):
      valids.add(mersenne)

  for valid in valids:
    print valid
  print ''

def _FirstPrimes():
  FIRST_PRIMES = '2 3 5 7 11 13 17 19 23 29 31 37 41 43 47 53 59 61 67 71 73 79 83 89 97 101 103 107 109 113 127 131 137 139 149 151 157 163 167 173 179 181 191 193 197 199 211 223 227 229 233 239 241 251 257 263 269 271 277 281 283 293 307 311 313 317 331 337 347 349 353 359 367 373 379 383 389 397 401 409 419 421 431 433 439 443 449 457 461 463 467 479 487 491 499 503 509 521 523 541 547 557 563 569 571 577 587 593 599 601 607 613 617 619 631 641 643 647 653 659 661 673 677 683 691 701 709 719 727 733 739 743 751 757 761 769 773 787 797 809 811 821 823 827 829 839 853 857 859 863 877 881 883 887 907 911 919 929 937 941 947 953 967 971 977 983 991 997'
  primes = [int(el) for el in FIRST_PRIMES.split(' ')]

  T = int(raw_input())
  for i in xrange(T):
    line = raw_input()
    nums = [int(el) for el in line.split(' ')]
    _GetPrimes(primes, nums[0], nums[1])


def _MakePolishExpr(expr):
  # Expression could be terminal.
  digit_match = re.search('^\d$', expr)
  if digit_match:
    return expr

  # Matching parens is tricky.
  # or have parens.
  if '(' == expr[0] and ')' == expr[-1]:
    return _MakePolishExpr(expr[1:-1])

  # We have a binary operator.
  m = re.search('\+\-\*\/\^', expr)
  if not m:
    print expr
  char = m.group(0)
  [left, right] = expr.split(char)
  ans = ''
  ans += _MakePolishExpr(left)
  ans += _MakePolishExpr(right)
  ans += char
  return ans

def _MakePol(expr, start, open_inds):
  if expr[0] == '(':
    open_inds.add()


def _HasLowerOrEqualPrecedence(cur_token, comparison):
  """Does cur_token have less precedence than comparison?"""
  if cur_token == '+':
    return comparison in '+-*/^'
  elif cur_token == '-':
    return comparison in '-*/^'
  elif cur_token == '*':
    return comparison in '*/^'
  elif cur_token == '/':
    return comparison in '/^'
  elif cur_token == '^':
    return comparison in '^'


def _MakePolishExprDijk(expr):
  output = ''
  op_stack = []
  for token in expr:
    if token in 'abcdefghijklmnopqrstuvwxyz':
      output += token
    elif token in '+-*/^':
      # Peek at the last element
      if op_stack:
        top_token = op_stack[-1]
        if _HasLowerOrEqualPrecedence(token, top_token):
          output += op_stack.pop()
      op_stack.append(token)
    elif token in '(':
      op_stack.append(token)
    elif token in ')':
      cur_token = op_stack.pop()
      while cur_token != '(':
        output += cur_token
        cur_token = op_stack.pop()
    
  while op_stack:
    output += op_stack.pop()

  return output

# ONP
def _ReversePolish():
  #expr = '(a+(b*c))'
  #expr = '((a+b)*(z+x))'
  #expr = '((a+t)*((b+(a+c))^(c+d)))'
  #expr = '3+4'
  T = int(raw_input())
  for _ in xrange(T):
    expr = raw_input()
    print _MakePolishExprDijk(expr)

def main():
  #_RevNumbers()
  #_MeanLife()
  #_FirstPrimes()
  _ReversePolish()


main()
