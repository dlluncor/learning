#include <string>
#include "lib.h"

namespace lib {
  char OUT[1000];
  int INFO = 0;
  int WARN = 1;
  int ERROR = 2;
  int NONE = 3;
  int DEBUG_LEVEL = ERROR;

  using namespace std;
  void Log(string info, Level level) {
    if (DEBUG_LEVEL <= level) {
      printf("[%d] %s\n", level, info.c_str());
    }
  }

  int MemCounter::Int(string name) {
      if (int_counts.find(name) == int_counts.end()) {
        sprintf(OUT, "KEY %s DOES NOT EXIST IN COUNTER", name.c_str());
        Log(OUT, WARN);
        return -1;
      }
      return int_counts[name];
   }

  void MemCounter::Inc(string name) {
    Inc(name, 1);
  }

  void MemCounter::Inc(string name, int amount) {
      if (int_counts.find(name) == int_counts.end()) {
        int_counts[name] = 0;
      }
      int_counts[name] += amount;
  }
}