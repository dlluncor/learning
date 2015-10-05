
#include <stdio.h> 
#include <string>
#include <vector>

using namespace std;

class Student {

public:
  string get_name();
  Student(string name, vector<int> grades);
  ~Student();
private:
  string _name;
  vector<int> _grades;
};

Student::Student(string name, vector<int> grades) {
  _name = name;
  _grades = grades;
}

Student::~Student() {

}

string Student::get_name() {
  return _name;
}

int main() {
  vector<int> grades1;
  grades1.push_back(90);
  Student s1("David L", grades1);
  printf("hi\n");
  return 0;
}