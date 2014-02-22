#include <iostream>
#include <stdlib.h>
#include "lessons.h"
#include <map>
#include <sstream>
using namespace std;

int Die::Roll() {
  // Roll a value 1 to 6.
  return 1 + (rand() % 5);
}

/*
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
*/

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

bool IsPassBet(string bet_name) {
  return bet_name == "pass";  // TODO(dlluncor): Update.
}

void Craps::Roll() {
  int val0 = die0->Roll();
  int val1 = die1->Roll();
  cout << "Rolled " << val0 << ", " << val1 << "\n";
  
  for (auto& bet_tup : bets) {
    auto& bet = bet_tup.second;
    auto& bet_key = bet_tup.first;
    string name = bet.name;
    // Determine the next state for each bet.
    string next_state;
    if (IsPassBet(name)) {
      // Or other pass bets process here...
      next_state = name_to_next_pass[name](on_num, val0, val1, is_on);
    } else {
      next_state = name_to_next[name](val0, val1, is_on);
    }
    printf("Bet: %s Next state: %s\n", bet.name.c_str(), next_state.c_str());
    
    // Determine what to do with money.
    if (next_state == "win" || next_state == "win_stay") {
      float payout_multiplier;
      if (IsPassBet(name)) {
        payout_multiplier = name_to_odds_pass[name](on_num);
      } else {
        payout_multiplier = name_to_odds[name];
      }
      if (next_state == "win") {
        // Pay odds + original bet, as well as remove bet, require the player to place a bet
        // again.
        Pay((payout_multiplier*bet.value) + bet.value, bet.player);
        bets.erase(bet_key);
      } else {
        // Pay the player their winnings but don't remove their bet.
        Pay((payout_multiplier*bet.value), bet.player);
      }
    } else if (next_state == "lose") {
      // Remove the bet!
      bets.erase(bet_key);
    } else if (next_state != "") {
      // Then we need to transition the money to another bet (COME) bet.
      bet.name = next_state;  // TODO: Will this actually work?? Or a bug??
    }
    // Or don't do anything.
  }

  string next_button_state = PassNext(on_num, val0, val1, is_on);
  if (next_button_state == "win" || next_button_state == "lose") {
    on_num = 0;
    if (is_on) {
      is_on = false;
    }
    // If you were off you stay off.
  } else {
    // If you were on do nothing.
    if (!is_on) {
      is_on = true;  // Didn't craps or hit a bingo.
      on_num = val0 + val1;
    }
  }
}

void Craps::Pay(float amount, PlayerId player) {
  cout << "Paying player " << player << ": $" << amount << "\n";
  bankrolls[player] += amount;
}

void Craps::Init() {
  // Odds predicates (for payout). I think they get more complicated than this....
  // TODO(dlluncor): Fill in more next states and odds.
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
  Init();
}

Craps::~Craps() {
  //cout << "Destroy craps\n";
  delete die0;
  delete die1;
}

void Craps::InspectState() {
  printf("is_on:%d on_num:%d\n", is_on, on_num);
  printf("Bets:\n");
  for (auto& bet_tup: bets) {
    auto& bet = bet_tup.second;
    printf("  Bet %s by player %d for $%.1f\n", bet.name.c_str(), bet.player, bet.value);
  }
  printf("Players:\n");
  for (auto& paid_tup: paid) {
    auto& player = paid_tup.first;
    printf("  Player %d put in $%.1f and has %.1f\n", player, paid_tup.second, bankrolls[player]);
  }
}

void Craps::Decide() {
  // Tell each player the state of the game to help them decide what bet to make next.
  // Give them each of their bets and the previous and current state of their bet, and how much
  // the bet is valued to them.
}

void Craps::Buyin(PlayerId player, float amount) {
  bool new_player = paid.find(player) == paid.end();
  if (new_player) {
    paid[player] = amount;
    bankrolls[player] = amount;
  } else {
    paid[player] = paid[player] + amount;
    bankrolls[player] = bankrolls[player] + amount;
  }
}

/*string Sprintf(const char* format, ...) {
  char* str;
  va_list args;
  sprintf(str, format, args);
  string key(str);
  return key;
}*/

// Players can instigate this.
void Craps::AddBet(Bet bet) {
  char* str;
  stringstream key;
  key << bet.name << "**" << bet.player;
  bets[key.str()] = bet;
  // Deduct from player's bankroll.
  bankrolls[bet.player] -= bet.value;
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
  auto* craps = new Craps();
  craps->Buyin(0, 200);
  craps->AddBet(Bet{"pass", 0, 10.0});
  string resp;
  while (true) {
    cout << "Type r (roll): ";
    cin >> resp;
    if (resp == "r") {
      craps->Roll();
    } else if (resp == "i") {
      craps->InspectState();
    } else if (resp == "d") {
      craps->Decide();
    } else {
      break;
    }
  }
  delete craps;
  return 0;
}