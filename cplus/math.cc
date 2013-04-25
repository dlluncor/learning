#include <iostream>
#include <sstream>

using namespace std;

const float EPSILON = 0.0000001;

float sqrt(float n) {
  if (n == 1.0) {
    return 1.0;
  }
  float x = n;
  while (true) {
    float err = x * x - n;
    if (err > EPSILON) {
      x = x - (x * x - n) / (2 * x);
    } else {
      break;
    }
  }
  return x;
}

int main() {
  cout << sqrt(4) << "\n";
  cout << sqrt(2) << "\n";
  return 0;
}
