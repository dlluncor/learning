class Student(object):

  def __init__(self, name, grades):
    self.name = name
    self.grades = grades

  def get_name(self):
    return self.name

  def average_score(self):
    N = len(self.grades)
    return sum(self.grades) / float(N)

def main():
  print 'Ranking of students:'
  student1 = Student('David L', [90, 86, 60, 10])
  student2 = Student('Jovani K', [92, 84, 83, 12])
  student3 = Student('Alexa O', [43, 23, 22, 5])
  students = [student1, student2, student3]
  students = sorted(
    students, key=lambda s: s.average_score(), 
    reverse=True)
  for student in students:
    print '%s \t(%.2f)' % (
      student.get_name(), student.average_score())


if __name__ == '__main__':
  main()
