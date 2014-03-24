#ifndef _LIB_H
#define _LIB_H

#include <string>
#include <map>

// Common code.
namespace lib {
  typedef int Level;
  extern char OUT[1000];
  extern int INFO;
  extern int WARN;
  extern int ERROR;
  extern int DEBUG_LEVEL;
  void Log(std::string info, Level level);

  class Counter {
   public:
    virtual int Int(std::string name) = 0;
    virtual void Inc(std::string name) = 0;
    virtual void Inc(std::string name, int amount) = 0;
  };

  class MemCounter: public Counter {
   public:
    int Int(std::string name);
    void Inc(std::string name);
    void Inc(std::string name, int amount);
   private:
    std::map<std::string, int> int_counts;
  };
}
// End common code.

#endif