import urllib2

# n > 2
# Fib(n) = Fib(n-1) + Fib(n-2)
# Fib(1) = 1
# Fib(2) = 1 
	
class Player(object):
  
  def __init__(self, name, fg, fg_percent):
	self.name = name
	self.fg = fg
	self.fg_percent = fg_percent

  def fga(self):
    return self.fg / self.fg_percent

def l(player): 
  return player.fga()

def main3():
  players = [
    Player('Kobe', 225, 0.372),
    Player('Lebron', 224, 0.493),
    Player('Dwyane', 179, 0.517)
  ]
  sorted(players, key=lambda player: player.fga())
  for player in players:
	print ('%s shot %d times.' % (player.name, player.fga()))


def fib(n):
  if n<2:
    return 1
  return fib(n-1)+fib(n-2)
   

def main2():
  print fib(10)


def routine1(i):
  if i < 10:
	print 'routine1done'
	return
  print ('r%d' % i)	
  routine1(i-1)
	
def main():
  print 'main1'
  routine1(12)
  print 'main2'

main3()
