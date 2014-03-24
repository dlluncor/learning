#include "lessons_test.h"
#include "lessons.h"
#include "lib.h"
#include <iostream>
#include <stdlib.h>
#include <assert.h>
#include <algorithm>

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

string AssertEquals(bool v0, bool v1) {
  if (v0 != v1) {
  	sprintf(lib::OUT, "Expected: %d. Got: %d", v0, v1);
  	return lib::OUT;
  }
  return "";
}

string AssertEquals(float v0, float v1) {
  if (v0 != v1) {
  	sprintf(lib::OUT, "Expected: %f. Got: %f", v0, v1);
  	return lib::OUT;
  }
  return "";
}

string AssertEquals(string v0, string v1) {
  if (v0 != v1) {
  	sprintf(lib::OUT, "Expected: %s. Got: %s", v0.c_str(), v1.c_str());
  	return lib::OUT;
  }
  return "";
}


string AssertEquals(const BetInfo v0, const BetInfo v1) {
  string str = "";
  str += AssertEquals(v0.next_state, v1.next_state);
  str += AssertEquals(v0.prev_state, v1.prev_state);
  str += AssertEquals(v0.next_value, v1.next_value);
  str += AssertEquals(v0.prev_value, v1.prev_value);
  return str;
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

struct bets_by_id {
  bool operator()(const BetInfo& b0, const BetInfo& b1) {
  	return b0.id_ < b1.id_;
  }
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
  res += AssertEquals(20.0, d.paid);  // Bets 10, then always buys in for 10 more.
  res += AssertEquals(30.0, d.amount);  // Won 10 dollar bet.
  res += AssertEquals(false, d.game_state.is_on);
  res += AssertEquals(0, d.game_state.on_num);
  std::sort(d.bet_infos.begin(), d.bet_infos.end(), bets_by_id());
  res += AssertEquals(BetInfo("pass", "win", 10.0, 20.0), d.bet_infos[0]);
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