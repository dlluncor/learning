#include "lessons.h"
#include "lessons_test.h"

int main() {
  if (craps::VerifyTests()) {
    craps::TestStrategyMain();
  }
  return 0;
}