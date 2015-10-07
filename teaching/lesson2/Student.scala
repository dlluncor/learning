class Student(var name: String, var scores:Array[Int]) {

  def averageScore: Double = {
    var sum = 0.0
    for (v <- this.scores) {
      sum += v
    }
    return sum / this.scores.length;
  }
}

def main() = {
var s0 = new Student("David L", Array(90, 86, 60, 10))
var s1 = new Student("Jovani K", Array(92, 84, 83, 12))
var s2 = new Student("Alexa O", Array(43, 23, 22, 5))

var students = List(s0, s1, s2)
students = students.sortBy(- _.averageScore)
//students.sort((e1, e2) => (e1.averageScore < e2.averageScore))

System.out.println("Ranking of students:")
for (s <- students) {
  var name = s.name
  var score = s.averageScore
  System.out.println(f"$name%s \t($score%.2f)")
}

}

main()
