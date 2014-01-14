#include <stdio.h>
#include <iostream>

using namespace std;

class Frank {
 public:
   Frank(){
     internal_ = 2;
   };
   ~Frank(){};
   const int answer(const int* i) const;
 private:
    int internal_;
};

// Interesting. Seems like the last const means nothing here...(1st const)
// is for instructional purposes and is not actually honored by the compiler.
const int Frank::answer(const int* const i) const {
  //*i = 3; // 2nd const applies. Cannot change value the pointer points to.

  int j = 3;
  i = &j; // 3rd const applies. Cannot change the value of the pointer.

  //internal_++; // 4th const applies. Cannot change internal state because
  // this object is in a read only state.
  return *i + 1;
}

int main() {
  cout << "Yoo\n";
  Frank* f = new Frank();
  int num = 2;
  int newAnswer = f->answer(&num);
  newAnswer = 4;  // Shouldn't this be a compiler error?
  cout << newAnswer << "\n";
  return 0;
}
