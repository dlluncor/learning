public class Student {
  String name;
  int[] grades;

  Student(String name, int[] grades) {
    this.name = name;
    this.grades = grades;  
  }

  String getName() {
    return this.name; 
  }
  
  float getAverageScore() {
    int sum = 0;
    for (int grade: this.grades) {
      sum += grade;
    }
    return (float)sum / (float)this.grades.length;
  }
}
