#include <iostream>
#include <stdlib.h>
#include <assert.h>
#include "lessons.h"
#include <map>
#include <sstream>
using namespace std;

// Stack traces.
#include <stdio.h>
#include <execinfo.h>
#include <signal.h>
//#include <unistd.h>

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
*/

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

// Utils.
float RolledToOdds(int on_num) {
  if (on_num == 6 || on_num == 8) {
    return 7 / 6.0;
  }
  if (on_num ==  5 || on_num == 9) {
    return 7 / 5.0;
  }
  if (on_num = 4 || on_num == 10) {
    return 9 / 5.0;
  }
}

// Win predicates.

// Three types of bets need to organize them!

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

string HardTwoNext(int die0, int die1, bool is_on) {
  if ((die0 + die1) == 2) {
    return "win"; // always give back money for middle bets...I think.
  }
  return "lose";
}

string FieldNext(int die0, int die1, bool is_on) {
  if (InField(die0 + die1)) {
    return "win";
  }
  return "lose";
}

string FiveNext(int on_num, int die0, int die1, bool is_on) {
  if ((die0 + die1) == 5) {
    return "win_stay";  // You win but can't remove the bet itself.
  }
  if (PassNext(on_num, die0, die1, is_on) == "lose") {
    return "lose"; // If we dont lose, we stay around.
  }
  return "";  // We didn't win, and we didn't lose, stick around.
}

string SixNext(int on_num, int die0, int die1, bool is_on) {
  if ((die0 + die1) == 6) {
    return "win_stay";  // You win but can't remove the bet itself.
  }
  if (PassNext(on_num, die0, die1, is_on) == "lose") {
    return "lose"; // If we dont lose, we stay around.
  }
  return "";  // We didn't win, and we didn't lose, stick around.
}

string EightNext(int on_num, int die0, int die1, bool is_on) {
  if ((die0 + die1) == 8) {
    return "win_stay";  // You win but can't remove the bet itself.
  }
  if (PassNext(on_num, die0, die1, is_on) == "lose") {
    return "lose"; // If we dont lose, we stay around.
  }
  return "";  // We didn't win, and we didn't lose, stick around.
}

float PassOdds(int on_num, int sum) {
  return RolledToOdds(on_num);
}

float FieldOdds(int on_num, int sum) {
  if (sum == 2 || sum == 12) {
    return 2.0;
  }
  return 1.0;
}

bool Craps::IsPassBet(string bet_name) {
  return name_to_next_pass.find(bet_name) != name_to_next_pass.end();
}

bool Craps::IsPassBetOdds(string bet_name) {
  return name_to_odds_pass.find(bet_name) != name_to_odds_pass.end();
}


void Craps::ClearPrevState() {
  for (auto& last_bets_kv: last_changed_bets) {
    // Clear the set of bets associated with each player.
    last_bets_kv.second.clear();
  }
}

void Craps::Roll() {
  ClearPrevState();
  int val0 = die0->Roll();
  int val1 = die1->Roll();
  cout << "Rolled " << val0 << ", " << val1 << "\n";
  vector<string> remove_bets;  // list of keys for bets to remove if win or lose.
  for (auto& bet_tup : bets) {
    BetInfo bet_info;
    auto& bet = bet_tup.second;
    auto& bet_key = bet_tup.first;
    string name = bet.name;
    bet_info.prev_state = name;
    bet_info.prev_value = bet.value;
    // Determine the next state for each bet.
    string next_state;
    float next_value;
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
      if (IsPassBetOdds(name)) {
        payout_multiplier = name_to_odds_pass[name](on_num, val0 + val1);
      } else {
        payout_multiplier = name_to_odds[name];
      }
      if (next_state == "win") {
        // Pay odds + original bet, as well as remove bet, require the player to place a bet
        // again.
        next_value = (payout_multiplier*bet.value) + bet.value;
        Pay(next_value, bet.player);
        remove_bets.push_back(bet_key);
      } else {
        // Pay the player their winnings but don't remove their bet.
        next_value = (payout_multiplier*bet.value);
        Pay(next_value, bet.player);
      }
    } else if (next_state == "lose") {
      // Remove the bet!
      next_value = 0;
      remove_bets.push_back(bet_key);
      //bets.erase(bet_key);
    } else if (next_state != "") {
      // Then we need to transition the money to another bet (COME) bet.
      bet.name = next_state;  // TODO: Will this actually work?? Or a bug??
      next_value = bet.value;
    } else {
      // Or don't do anything, so the next state is the prev state.
      next_state = name;
      next_value = bet.value;
    }
    bet_info.next_state = next_state;
    bet_info.next_value = next_value;
    last_changed_bets[bet.player].push_back(bet_info);
  }
  for (auto& bet_name: remove_bets) {
    bets.erase(bet_name);
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
  //cout << "Paying player " << player << ": $" << amount << "\n";
  bankrolls[player] += amount;
}

void Craps::Init() {
  // Odds predicates (for payout). I think they get more complicated than this....
  // TODO(dlluncor): Fill in more next states and odds.
  name_to_odds = {
    {"hardTwo", 30.0},
    {"Five", 7/5.0},
    {"Six", 7/6.0},
    {"Eight", 7/6.0}
  };
  name_to_odds_pass = {
    {"pass", *PassOdds},
    {"Field", *FieldOdds},
  };

  // Next state predicates (only ones that matter), they determine whether you win as well.
  name_to_next = {
    {"hardTwo", *HardTwoNext},
    {"Field", *FieldNext}
  };

  name_to_next_pass = {
    {"pass", *PassNext},
    {"Five", *FiveNext},
    {"Six", *SixNext},
    {"Eight", *EightNext}
  };
}

Craps::Craps() {
  is_on = false; 
  srand(time(NULL));
  die0 = new Die();
  die1 = new Die();
  next_player_id = 0;
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
    auto& player_id = paid_tup.first;
    Player* player = cur_players[player_id];
    printf("  Player %s put in $%.1f and has $%.1f\n", player->str().c_str(), paid_tup.second, bankrolls[player_id]);
  }
}

void Craps::Decide(PlayerId player) {
  // Tell each player the state of the game to help them decide what bet to make next.
  // Give them each of their bets and the previous and current state of their bet, and how much
  // the bet is valued to them.
  auto& bet_infos = last_changed_bets[player];
  printf("Player %d had these bets changed: \n", player);
  for (auto& bet_info: bet_infos) {
    printf("  Prev: ($%.1f, %s). Current: ($%.1f, %s)\n", bet_info.prev_value, 
      bet_info.prev_state.c_str(), bet_info.next_value, bet_info.next_state.c_str());
  }
}

PlayerId Craps::Register(Player* player) {
  // This is the only place where we "initialize a player".
  next_player_id++;
  paid[next_player_id] = 0;
  bankrolls[next_player_id] = 0;
  last_changed_bets[next_player_id] = {};
  cur_players[next_player_id] = player;
  return next_player_id;
}

void Craps::Buyin(PlayerId player, float amount) {
  //bool new_player = paid.find(player) == paid.end();
  paid[player] = paid[player] + amount;
  bankrolls[player] = bankrolls[player] + amount;
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
  printf("Player %d added bet: %s\n", bet.player, bet.name.c_str());
  bets[key.str()] = bet;
  // Deduct from player's bankroll.
  bankrolls[bet.player] -= bet.value;
}

void Craps::RunStrategies() {
  GameState game_state;
  game_state.is_on = is_on;
  game_state.on_num = on_num;
  for (auto& player_kv: cur_players) {
    Player* player = player_kv.second;
    PlayerId player_id = player_kv.first;
    PlayerDecision decision(game_state, last_changed_bets[player_id],
      bankrolls[player_id]);
    player->NextActions(decision);
    // Need to export the game state and set of bets relevant to this player for them
    // to decide what to do next.
  }
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
  // the actual type's destructor of Craps.
}

}

// List of strategies. They all take decision info for a player and then make the appropriate
// named bet with the right amount of dollars.

vector<Bet> PassOnly(const PlayerDecision& decision) {
  vector<Bet> bets;
  bool is_off = !decision.game_state.is_on;
  if (is_off) {
    // When the die roll is off, we want to simply put 10 on the pass line. Our money
    // is not still on the table.
    Bet bet("pass", 10.0);
    bets.push_back(bet);
  }
  return bets;
}

vector<Bet> IronCross(const PlayerDecision& decision) {
  float default_bet = 10.0;
  vector<Bet> bets;
  map<BetName, bool> cur_bets_map;
  for (auto& bet_info: decision.bet_infos) {
    if (bet_info.next_value > 0) {
       cur_bets_map[bet_info.next_state] = true;
    }
  }

  bool is_off = !decision.game_state.is_on;
  int on_num = decision.game_state.on_num;
  if (is_off) {
    // When the die roll is off, we want to simply put 10 on the pass line. Our money
    // is not still on the table.
    Bet bet("pass", default_bet);
    bets.push_back(bet);
  } else {
    // We are on, we need to look at the button and our bets.
    if (on_num != 5 && (cur_bets_map.find("Five") == cur_bets_map.end())) {
      // Make a bet on 5 if we don't have a bet down already.
      Bet bet("Five", default_bet);
      bets.push_back(bet);
    }
    if (on_num != 6 && (cur_bets_map.find("Six") == cur_bets_map.end())) {
      // Make a bet on 6 if we don't have a bet down already.
      Bet bet("Six", default_bet);
      bets.push_back(bet);
    }
    if (on_num != 8 && (cur_bets_map.find("Eight") == cur_bets_map.end())) {
      // Make a bet on 8 if we don't have a bet down already.
      Bet bet("Eight", default_bet);
      bets.push_back(bet);
    }
    if(cur_bets_map.find("Field") == cur_bets_map.end()) {
      // Make a bet on the field if we don't have a bet down already.
      Bet bet("Field", default_bet);
      bets.push_back(bet); 
    }
  }
  return bets;
}

Player::Player(Game* game_, string name_, string strategy_) {
  game = game_;
  name = name_;
  strategy = strategy_;
}

void Player::NextActions(
  const PlayerDecision& decision) {
  vector<Bet> bets;
  if (strategy == "iron_cross") {
    bets = IronCross(decision);
  } else if (strategy == "pass_only") {
    bets = PassOnly(decision);
  } else {
    printf("Unrecognized strategy %s\n", strategy.c_str());
    assert(0 == 1);
  }
  // Make sure the player has enough money for the bets, if not pay for more.
  float total = 0;
  for (auto& bet : bets) {
    total += bet.value;
  }
  if (decision.amount < total) {
    game->Buyin(id, (total - decision.amount) + 10);
  }
  // Add bets that your strategy told you to do.
  for (auto& bet : bets) {
    bet.player = id;  // Need to set which player this bet belongs to.
    game->AddBet(bet);
  }
}

void Player::set_id(PlayerId id_) {
  id = id_;
}

string Player::str() {
  string s;
  s += name + " (" + strategy + ")";
  return s;
}

/*
  Person has an id associated with a game. When they get their id they can.
  NextAction(prev_actions) // notification to do something about what just happened. Next round.
  Lose()  // notification that they lost all money. Won't call NextAction here.
*/

void TestStrategyMain() {
  Craps craps;
  Player player0(&craps, "Ben", "iron_cross");
  player0.set_id(craps.Register(&player0));
  Player player1(&craps, "David", "pass_only");
  player1.set_id(craps.Register(&player1));
  for (int i = 0; i < 100; i++) {
    craps.Roll();
    craps.RunStrategies();
  }
  craps.InspectState();
}

void CommandLineMain() {
  Craps craps;
  PlayerId id = 0;
  craps.Buyin(id, 200);
  Bet bet("pass", 10.0);
  bet.player = id;
  craps.AddBet(bet);
  string resp;
  while (true) {
    cout << "Type r (roll): ";
    cin >> resp;
    if (resp == "r") {
      craps.Roll();
    } else if (resp == "i") {
      craps.InspectState();
    } else if (resp == "d") {
      craps.Decide(0);
    } else {
      break;
    }
  }
}

int main() {
  //CommandLineMain();
  TestStrategyMain();
  return 0;
}