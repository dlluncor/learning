require "./common"
require "./other"

class Student
  include Common

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

def compareM(x, y)
 return y.getAverageScore <=> x.getAverageScore
end 

def main()
puts "Ranking of students:"
s0 = Student.new("David L", [90, 86, 60, 10])
s1 = Student.new("Jovani K", [92, 84, 83, 12])
s2 = Student.new("Alexa O", [43, 23, 22, 5])
students = [s0, s1, s2]
students.sort! {|x, y| compareM(x, y)}
symbol = :hello
d = {:hello => "name = #{s0.getName}"}
p d[:hello]
students.each {
  |s|
  puts "%s \t (%.2f)\n" % [s.getName, s.getAverageScore]
  d[s.getName] = s
}

puts d["David L"].getName
s0.greeting
Other::hello
puts match("$hello", "hello there")
end

main()


