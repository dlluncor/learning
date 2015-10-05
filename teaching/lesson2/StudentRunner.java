
import java.util.List;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.Comparator;

public class StudentRunner {

  // API: Application Programming Interface
  // Expose to the user only what they need to see.
  public static class StudentsComparator implements Comparator<Student> {
    @Override
    public int compare(Student s1, Student s2) {
      float val = s1.getAverageScore() - s2.getAverageScore();
      if (val == 0.0f) {
        return 0;
      } else if (val > 0.0f) {
        return -1;
      }
      return 1;
    }
  }

  public static void main(String[] args) {
    System.out.println("Ranking of students:");
    Student s1 = new Student(
      "David L", new int[]{90, 86, 60, 10});
    Student s2 = new Student(
      "Jovani K", new int[]{92, 84, 83, 12});
    Student s3 = new Student(
      "Alexa O", new int[]{43, 23, 22, 5});

    List<Student> students = Arrays.asList(
      new Student[]{s1, s2, s3});
    Collections.sort(students, new StudentsComparator());

    for (Student student : students) {
      System.out.println(
        String.format("%s \t (%.2f)", 
          student.getName(),
          student.getAverageScore()));
    }
  }
}