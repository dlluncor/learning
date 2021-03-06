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
  	sprintf(lib::OUT, "Expected: %d. Got: %d\n", v0, v1);
  	return lib::OUT;
  }
  return "";
}

string AssertEquals(bool v0, bool v1) {
  if (v0 != v1) {
  	sprintf(lib::OUT, "Expected: %d. Got: %d\n", v0, v1);
  	return lib::OUT;
  }
  return "";
}

float EPSILON = 0.00001;
#include <cmath>
string AssertEquals(float v0, float v1) {
  if (v0 != v1) {
    if (std::abs(v0 - v1) > EPSILON) {
  	  sprintf(lib::OUT, "Expected: %f. Got: %f\n", v0, v1);
  	  return lib::OUT;
    }
  }
  return "";
}

string AssertEquals(string v0, string v1) {
  if (v0 != v1) {
  	sprintf(lib::OUT, "Expected: %s. Got: %s\n", v0.c_str(), v1.c_str());
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

struct TestEntry {
  // Each vector represents the game state after each round. A round is a player's move
  // + a roll.
  int rounds;
  vector<int> die_rolls0;
  vector<int> die_rolls1;
  string strategy;
  vector<float> paids;
  vector<float> amounts;
  vector<bool> is_ons;
  vector<int> on_nums;
  vector<vector<BetInfo> > bet_infos;
};

string RunGenericCrapsTest(TestEntry t) {
  string res = "";
  // Create Craps game.
  // Need two deterministic die.
  // Want to verify that when players place certain bets they end up with that
  // amount after each roll.
  // Sort of like list of bets, list of die rolls, list of dollar amounts after
  // each event.
  // All reusable code to test Craps!!!
  Craps craps(new FakeDie(t.die_rolls0), new FakeDie(t.die_rolls1));
  Player player1(&craps, "David", t.strategy);
  int pid1 = craps.Register(&player1);
  player1.set_id(pid1);
  for (int i = 0; i < t.rounds; i++) {
    Round(&craps);
    PlayerDecision d = craps.Decision(pid1);
    res += AssertEquals(t.paids[i], d.paid);  // Bets 10, then always buys in for 10 more.
    res += AssertEquals(t.amounts[i], d.amount);  // Won 10 dollar bet.
    res += AssertEquals(t.is_ons[i], d.game_state.is_on);
    res += AssertEquals(t.on_nums[i], d.game_state.on_num);
    std::sort(d.bet_infos.begin(), d.bet_infos.end(), bets_by_id());
    auto& bets_list = t.bet_infos[i]; 
    int num_bets = bets_list.size();
    res += AssertEquals(d.bet_infos.size(), num_bets);
    for (int b = 0; b < num_bets; b++) {
      res += AssertEquals(bets_list[b], d.bet_infos[b]);
    }
  }
  return res;
}

string TestPassOnly() {
  // Win, lose, on 8, on 9, win
  // Each entry is the result AFTER the roll.
  const TestEntry t = {
    5,
    {4, 1, 5, 6, 4}, {3, 1, 3, 3, 4}, /* die rolls */
    PASS_ONLY,
    {20.0, 20.0, 20.0, 20.0, 20.0}, /* paid */
    {30.0, 20.0, 10.0, 10.0, 30.0}, /* amount */
    {false, false, true, true, false}, /* is_ons */
    {0, 0, 8, 8, 0}, /* on_nums */
    {
      {BetInfo(PASS, WIN, 10.0, 20.0)},
      {BetInfo(PASS, LOSE, 10.0, 0.0)},
      {BetInfo(PASS, PASS, 10.0, 10.0)},
      {BetInfo(PASS, PASS, 10.0, 10.0)},
      {BetInfo(PASS, WIN, 10.0, 20.0)}
    } /* bet_infos */
  };
  string res = RunGenericCrapsTest(t);
  return res;
}

string TestIronCross() {
  // on 5 (add 6, 8, field bet), roll 6
  // Each entry is the result AFTER the roll.
  const TestEntry t = {
    2,
    {1, 3}, {4, 3}, /* die rolls */
    IRON_CROSS,
    {20.0, 50.0}, /* paid */
    {10.0, 31.666666}, /* amount */
    {true, true}, /* is_ons */
    {5, 5}, /* on_nums */
    {
      {BetInfo(PASS, PASS, 10.0, 10.0)},
      {BetInfo(PASS, PASS, 10.0, 10.0),
       BetInfo(SIX, WIN_STAY, 10.0, 21.66666),
       BetInfo(EIGHT, EIGHT, 10.0, 10.0),
       BetInfo(FIELD, LOSE, 10.0, 0.0)}
    } /* bet_infos */
  };
  string res = RunGenericCrapsTest(t);
  return res;
}

string RunTests() {
  string res = "";
  res += TestPassOnly();
  res += TestIronCross();
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