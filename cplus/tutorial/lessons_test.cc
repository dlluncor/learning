#include "lessons_test.h"
#include "lessons.h"
#include "lib.h"
#include <iostream>
#include <stdlib.h>
#include <assert.h>

using namespace std;

namespace craps {

// lib
string AssertEquals(int v0, int v1) {
  if (v0 != v1) {
  	sprintf(lib::OUT, "Expected: %d. Got: %d", v0, v1);
  	return lib::OUT;
  }
  return "";
}

class FakeDie: public Die {
  public:
  	FakeDie(vector<int> rolls): next_roll_(rolls), ind_(0){};
  	int Roll() {
  	  int val = next_roll_[ind_];
  	  ind_++;
  	  return val;
  	}
  private:
  	vector<int> next_roll_;
  	int ind_; // current roll.
};

string Test1() {
  string res = "";
  // Create Craps game.
  // Need two deterministic die.
  // Want to verify that when players place certain bets they end up with that
  // amount after each roll.
  // Sort of like list of bets, list of die rolls, list of dollar amounts after
  // each event.
  Craps craps(new FakeDie({4}), new FakeDie({3}));
  Player player1(&craps, "David", "pass_only");
  int pid1 = craps.Register(&player1);
  player1.set_id(pid1);
  Round(&craps);
  PlayerDecision d = craps.Decision(pid1);
  res += AssertEquals(20, d.paid);  // Bets 10, then always buys in for 10 more.
  res += AssertEquals(30, d.amount);  // Won 10 dollar bet.
  // TODO(dlluncor): Make it so we can inspect what bets are on the table easier
  // based on the PlayerDecision.
  return res;
}

string RunTests() {
  string res = "";
  res += Test1();
  return res;
};

using namespace lib;
bool VerifyTests() {
  lib::DEBUG_LEVEL = lib::INFO;
  string result = craps::RunTests();
  lib::DEBUG_LEVEL = lib::ERROR;
  if (result != "") {
    sprintf(OUT, "--FAILS TEST--\n%s", result.c_str());
    Log(OUT, lib::ERROR);
    return false;
  } else {
    Log("--PASSES--", ERROR);
    return true;
  }
}  // namespace craps

}