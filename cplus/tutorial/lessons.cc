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
    if (bet.removed) {
      continue;
    }
    Process(bet, val0, val1);
  }

  int sum = val0 + val1;
  // Go to next state.
  if (!is_on) {
    if (sum == 2 || sum == 3 || sum == 12) {
      cout << "CRAPS rolled " << sum << "\n";
    }
    if (sum == 7 || sum == 11) {
      cout << "WON roll again! " << sum << "\n";
    }
    is_on = true;  // Now we are on.
    on_value = sum;
    cout << "ON with value " << sum << "\n";
  } else {
    // What is the on value?
    if (on_value == sum) {
      cout << "HIT the mark payout for all! " << sum << "\n";
      is_on = false;
    } else if (sum == 7) {
      cout << "CRAPS rolled " << sum << "\n";
      is_on = false;
    } else {
      cout << "Rolled " << sum << " just paying." << "\n";
    }
  }
}

// Scale the payout value based on what was rolled.
float ScaleOdds(float value, int rolled) {
  if (rolled == 6 || rolled == 8) {
    return value * 7 / 6;
  }
  if (rolled ==  5 || rolled == 9) {
    return value * 7 / 5;
  }
  if (rolled = 4 || rolled == 10) {
    return value * 9 / 5;
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

void Craps::Process(Bet bet, int val0, int val1) {
  cout << "Processing bet: " << bet.name << "\n";
  int sum = val0 + val1;
  if (!is_on) {
    // Start of game, 2, 3, 12 is craps.
    if (sum == 2 || sum == 3 || sum == 12) {
      // TODO(dlluncor): Remove bet.
      bet.removed = true;
      return;
    }
    // 7 or 11 win money.
    if (sum == 7 || sum == 11) {
      // Get your value back, keep bet.
      Pay(bet.player, bet.value);
      bet.removed = true;
      return;
    }
    // 4, 5, 6, 8, 9, 10 ON.
    return;
  } else {
    // The button is "ON"
    if (sum == on_value) {
      // Hit the ON!
      // Pay based on the pass and BEHIND pass line.
      if (bet.name == "pass") {
        Pay(bet.player, bet.value);
        bet.removed = true;
        return;
      } else if (bet.name == "behind") {
        // TODO(dlluncor): implement BEHIND pass line.
        Pay(bet.player, ScaleOdds(bet.value, sum));
        bet.removed = true;
      }
    } else {
      // Process bets on single numbers.
      if (bet.for_num != 0 && sum == bet.for_num) {
        cout << "Hit " << sum << " for player " << bet.player << "\n";
        Pay(bet.player, ScaleOdds(bet.value, sum));
      }
    }
  }

  // Process the field bet.
  if (bet.name == "three" && sum == 3) {
    cout << "Hit hard 3 " << sum << " for player " << bet.player << "\n";
    Pay(bet.player, ScaleHardSumBet(bet.value));
    bet.removed = true;
  }
  if (bet.name == "eleven" && sum == 11) {
    cout << "Hit hard 11 " << sum << " for player " << bet.player << "\n";
    Pay(bet.player, ScaleHardSumBet(bet.value));
    bet.removed = true;  
  }
  if (bet.name == "field" && InField(sum)) {
    cout << "Hit the field " << sum << " for player " << bet.player << "\n";
    Pay(bet.player, ScaleFieldBet(bet.value));
    bet.removed = true;
  }

  // Process the middle bets.
  if (bet.hard_num != 0) {
    // Check to see if they made the bet and ALWAYS revoke their bet.
    if (val0 == bet.hard_num && val1 == bet.hard_num) {
      cout << "HARD hit " << sum << " for player " << bet.player << "\n";
      Pay(bet.player, ScaleHardHit(bet.value, bet.hard_num));
    }
    bet.removed = true;
  }
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

void Craps::Init() {
  // Odds predicates (for payout). I think they get more complicated than this....
  name_to_odds = {
    {"hardTwo", 30.0}
  };
  /*name_to_odds_pass = {
    {},
  };*/

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
  bets.push_back(bet);
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