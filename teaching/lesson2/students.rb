
class Student
  def initialize(name, scores)
    @name = name
    @scores = scores
  end
  
  def getName
    return @name
  end

  def getAverageScore
    sum = 0.0
    @scores.each {
      |score|
      sum += score
    }
    return sum / @scores.length
  end
end

puts "Ranking of students:"
s0 = Student.new("David L", [90, 86, 60, 10])
s1 = Student.new("Jovani K", [92, 84, 83, 12])
s2 = Student.new("Alexa O", [43, 23, 22, 5])
students = [s0, s1, s2]
students.sort! {|x, y| y.getAverageScore <=> x.getAverageScore}
students.each {
  |s|
  puts "%s \t (%.2f)\n" % [s.getName, s.getAverageScore]
}

