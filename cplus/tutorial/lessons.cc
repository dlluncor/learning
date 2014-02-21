#include <iostream>
#include <stdlib.h>
#include "lessons.h"
#include <map>
using namespace std;

int Die::Roll() {
  // Roll a value 1 to 6.
  return 1 + (rand() % 5);
}

// Copy constructors and const pass by reference.

void Craps::Roll() {
  int val0 = die0->Roll();
  int val1 = die1->Roll();
  cout << "Rolled " << val0 << ", " << val1 << "\n";
  
  for (auto& bet : bets) {
    //Process(bet, val0, val1);
  }
}

// Yo (11) or 2 and 1 (3) give 15 to 1 odds when playing the field.
float ScaleHardSumBet(float value) {
  return value * 15;
}

float ScaleFieldBet(float value) {
  return value * 4;
}

float ScaleHardHit(float value, int die) {
  if (die == 1) {
    return value * 30;
  } else if (die == 2) {
    return value * 7;
  } else if (die == 3) {
    return value * 9;
  } else if (die == 4) {
    return value * 9;
  } else if (die == 5) {
    return value * 7;
  } else if (die == 6) {
    return value * 30;
  }
  return -1; // Should never get here.
}

bool InField(float sum) {
  return sum == 2 || sum == 3 || sum == 4 || sum == 9 || sum == 10 || sum == 11 || sum == 12;
}

// Bet has the following components:
// Name: "yo"
// Predicate to determine whether you win or not (takes both die into account and ON or OFF position).
//  special case is the pass, don't pass bets.
// Odds of winning
// Payout based on what you bet.
// Next state of your position given the roll (COME bets will move to the dice rolled).

// Next states can go to the dealer "lose", "" (dont move), a different bet BetName,
// the player "win" which means pay and take off, or "winStay" which means pay but keep bet on table.

// How to represent a push on the current bet?

void Craps::Pay(int player_num, float amount) {
  cout << "Paying player " << player_num << " $" << amount << "\n";
}

// Utils.
float RolledToOdds(int on_num) {
  if (on_num == 6 || on_num == 8) {
    return 7 / 6;
  }
  if (on_num ==  5 || on_num == 9) {
    return 7 / 5;
  }
  if (on_num = 4 || on_num == 10) {
    return 9 / 5;
  }
}

// Win predicates.

// Three types of bets need to organize them!

string HardTwoNext(int die0, int die1, bool is_on) {
  if ((die0 + die1) == 2) {
    return "win"; // always give back money for middle bets...I think.
  }
  return "lose";
}

string PassNext(int on_num, int die0, int die1, bool is_on) {
  int sum = die0 + die1;
  if (is_on && sum == on_num) {
    return "win";
  } else if (is_on && sum == 7) {
    return "lose";
  } else if (!is_on && (sum == 7 || sum == 11)) {
    return "win";
  } else if (!is_on && (sum == 2 || sum == 3 || sum == 12)) {
    return "lose";
  }
  return "";
}

float PassOdds(int on_num) {
  return RolledToOdds(on_num);
}

void Craps::Init() {
  // Odds predicates (for payout). I think they get more complicated than this....
  name_to_odds = {
    {"hardTwo", 30.0}
  };
  name_to_odds_pass = {
    {"pass", *PassOdds},
  };

  // Next state predicates (only ones that matter), they determine whether you win as well.
  name_to_next = {
    {"hardTwo", *HardTwoNext}
  };

  name_to_next_pass = {
    {"pass", *PassNext},
  };
}

Craps::Craps() {
  is_on = false; 
  srand(time(NULL));
  die0 = new Die();
  die1 = new Die();
  // Initialize betting maps with rules.
}

Craps::~Craps() {
  //cout << "Destroy craps\n";
  delete die0;
  delete die1;
}

// Players can instigate this.
void Craps::AddBet(Bet bet) {
  cout << "Added bet " << bet.name << "\n";
  char* str;
  sprintf(str, "%s**%d", bet.name.c_str(), bet.player);
  string key(str);
  bets[key] = bet;
}

// Game state.

// Concepts I don't know:
// #define
// template
// generics
// const references
// macros

// Learning
// #define. Macros have names.

namespace {

void description() {
  cout << "Line " << __LINE__;
  cout << " of file: " << __FILE__ << "\n";
  cout << " Compilation at " << __DATE__ << " and " << __TIME__ << "\n";
  cout << "Compiler version: " << __cplusplus << "\n";
}

void Lessons() {
  Game* game = new Craps();
  // Virtual destructors.
  // Will only destroy game.
  delete game;
  // Now when Game has a virtual destructor, it will call
  // the actual type's destructor of craps.
}

}

int main() {
  //description();
  //Lessons();
  auto* craps = new Craps();
    craps->AddBet(Bet{"pass", 0, 10.0});
  string resp;
  while (true) {
    cout << "Type r (roll): ";
    cin >> resp;
    if (resp == "r") {
      craps->Roll();
    } else {
      break;
    }
  }
  delete craps;
  return 0;
}