
# Definition: define what something does.
# Invocation: you do what was defined.

# Data structure: container that helps you organize information.

"""
  # Don't do this! Use objects!
  print 'Start of program:'
  student1_name = 'David Lluncor'
  student1 = [90, 86, 60, 10]
  student2_name = 'Jovani'
  student2 = [92, 84, 63, 12]
  for grade in student1:
    print grade
"""
"""
# Ownership: what does the object maintain control of.
class Student(object):

  def __init__(self, name, grades):
    self.name = name
    self.grades = grades

  def average_score(self):
    N = len(self.grades)
    return sum(self.grades) / N

def main():
  print 'Start of program:'
  student1 = Student('David L', [90, 86, 60, 10])
  student2 = Student('Jovani K', [92, 84, 83, 12])
  students = [student1, student2]
  for student in students:
    student.average_score()
"""

class Board(object):
  """This is a tic-tac-toe board."""

  def __init__(self):
    self.p1 = 'X'  # player 1s char.
    self.p2 = 'O'  # player 2s char.
    self.cur_player = self.p1  # Whose turn is it.
    self.b = ['[]' for i in xrange(9)]  # Board state.

  def board_as_str(self):
    # Print the board
    lines = []  # All the lines.
    i = 0
    for row in xrange(3):
      line = []
      for col in xrange(3):
        c = self.b[i]
        if c == '[]':
          c = '[%d]' % (i + 1)
        else:
          c = '[%s]' % (c)
        line.append(c)
        i = i + 1
      lines.append(' '.join(line)) # Separates each element in list by a space.

    # Join combines all elements in a list into a string
    # separated by the \n newline character.
    return '\n'.join(lines)

  def finished(self):
    """Are all the pieces filled out in the game."""
    # Did a player win already?
    w = self.won_player()
    if w == 'X' or w == 'O':
      return True

    # If not, is there a spot open?
    for board_pos in self.b:
      if board_pos == '[]':
        return False
    return True

  def ask_player(self):
    # Set up of the method.
    print 'Player %s choose a location:' % (self.cur_player)
    err_msg = 'Input a number 1-9 biatch.'
    pos = -1

    # Make sure the person enters a number 1 - 9.
    try:
      pos = int(raw_input())
      if pos < 1 or pos > 9:
        print err_msg
        self.ask_player()
        return
    except Exception as e:
      print err_msg
      self.ask_player()
      return


    # A position 1-9 has been entered at this point.
    #print pos

    # Determine whether the person entered a position which
    # has not been chosen yet (is open.)
    real_pos = pos-1  # User typed 1. For me that means 0.
    board_el = self.b[real_pos]
    if board_el != '[]':
      print 'Position %d is already filled in. Choose another.' % (pos)
      self.ask_player()
      return

    # I need to fill in the board state with that location.
    self.b[real_pos] = self.cur_player

    # Switch players.
    if self.cur_player == 'X':
      self.cur_player = 'O'
    elif self.cur_player == 'O':
      self.cur_player = 'X'


  def won_player(self):
    """Returns if player 1 or player 2 has won, or a tie."""
    winning_combos = [
    [1,2,3],[4,5,6],[7,8,9],
    [1,4,7],[2,5,8],[3,6,9],
    [1,5,9],[3,5,7]]
    for p in winning_combos:
      if self.b[p[0]-1] == self.b[p[1]-1] and self.b[p[1]-1] == self.b[p[2]-1]:
        return self.b[p[0]-1]
    return 'tie'

def main():
  # Start of the program.
  b = Board()
  i = 0
  # Constantly run program until game is over.
  while not b.finished():
    #if i == 2:
    #  break
    print b.board_as_str()  # To see what the board looks like.
    b.ask_player()  # Ok, next player take a turn and enter input.
    #i += 1  # Debug purposes.

  print 'Final board:'
  print b.board_as_str()
  print ''
  print 'Game over player %s won.' % (b.won_player())
#main()

import pdb

def have_happiness(money, friends):
  if money <= 0 and friends <= 0:
    pdb.set_trace()
    return "unhappy"
  else:
    if money > 0:
      if friends <= 0:
        pdb.set_trace()
        return "happy"
      return "unhappy"
  return "indifferent"

have_happiness(0, 0)
have_happiness(300000, 2)