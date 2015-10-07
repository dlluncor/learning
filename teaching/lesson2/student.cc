//  g++ student.cc -std=gnu++11
// g++ student.cc -std=gnu++11
#include <stdio.h> 
#include <string>
#include <vector>

using namespace std;

class Student {

public:
  string get_name();
  Student(string name, vector<int> grades);
  string name() const;
  float average_score() const;
  ~Student();
private:
  string _name;
  vector<int> _grades;
};

Student::Student(string name, vector<int> grades) {
  _name = name;
  _grades = grades;
}

string Student::name() const {
  return _name;
}

Student::~Student() {

}

string Student::get_name() {
  return _name;
}

float Student::average_score() const {
  float val = 0.0;
  for (int grade: _grades) {
    val += grade;
  }
  return val / _grades.size();
}

bool compFunc(Student s1, Student s2) {
  return s1.average_score() > s2.average_score();
} 

int main() {
  printf("Ranking of students:\n");
  Student s1("David L", {90, 86, 60, 10});
  Student s2("Jovani K", {92, 84, 83, 12});
  Student s3("Alexa O", {43, 23, 22, 5});
  vector<Student> students({s1, s2, s3});
  std::sort(students.begin(), students.end(), compFunc);
  for (const auto s: students) {
    printf("%s \t(%.2f)\n", s.name().c_str(),
           s.average_score());
  }
  return 0;
}