#ifndef _LESSONS_H
#define _LESSONS_H

#include <stdio.h>
#include "lib.h"
#include <string>
#include <vector>
#include <map>

namespace craps {

class Die {
 public:
  virtual int Roll() = 0;
};

class RandomDie: public Die {
 public:
  int Roll();
};

typedef std::string BetName;
typedef int PlayerId;

// Info needed about the board bet for the player to know how to bet next.
struct BetInfo{
  BetInfo(){}
  BetInfo(std::string prev_state_, std::string next_state_, float prev_val_, float next_val_):
    prev_state(prev_state_), next_state(next_state_), prev_value(prev_val_),
    next_value(next_val_){}
  std::string prev_state; // previous state of the bet.
  std::string next_state; // next state of the bet.
  float prev_value;
  float next_value;
  // For tests.
  int id_;  // Id of the original bet. 
};

struct Bet {
  BetName name;
  PlayerId player;
  float value;
  // Internal for test. As the game moves on, ids for bets monotonically increase.
  int id_;

  Bet(BetName name_, float value_): name(name_), value(value_){};
  Bet(){};
};

typedef std::string (*BetNext)(int die0, int die1, bool is_on);
// Bets that depend on the "ON" position.
typedef std::string (*BetNextPass)(int on_num, int die0, int die1, bool is_on);
typedef float (*BetOddsPass) (int on_num, int sum);

class Game {
  public:
    virtual ~Game(){
      //cout << "Destroy games\n";
    };
    void Name(){ printf("I am a game\n"); };
    virtual void AddBet(Bet bet) = 0;
    virtual void Buyin(PlayerId id, float amount) = 0;
  private:
    std::string game_;
};

// Visible state of the game needed for a player to decide how to bet next.
struct GameState {
  bool is_on;
  int on_num;
};

// Info needed for a player to make a decision.
struct PlayerDecision {
  GameState game_state;
  std::vector<BetInfo> bet_infos;
  float amount;  // amount this player has.
  float paid; // how much the player has paid.
  PlayerDecision(const GameState& game_state_, const std::vector<BetInfo>& bet_infos_,
    float amount_, float paid_):
    game_state(game_state_), bet_infos(bet_infos_), amount(amount_), paid(paid_){};
};

class Player {
  public:
    Player(Game* game, std::string name, std::string strategy);
    void set_id(PlayerId id);
    void NextActions(const PlayerDecision& decision);
    std::string str();
  private:
    Game* game;
    std::string name;
    std::string strategy;
    PlayerId id;
};

class Craps : public Game {
 public:
   Craps();
   ~Craps();  // Only use virtual destructors when it has ANY virtual methods.
   void Roll();
   void InspectState();
   PlayerId Register(Player* player);
   void Decide(PlayerId player);  // inspect what the player should do next.
   void Buyin(PlayerId player, float amount);
   void AddBet(Bet bet);
   // Clears things like the last set of relevant bets for a player that changed.
   void ClearPrevState();

   // Runs craps where all the players are automated robots.
   void RunStrategies();
   // For debug and tests.
   Craps(Die* die0_, Die* die1_);
   void Summary();
   PlayerDecision Decision(PlayerId player);  // Info about the game state for a player.
 private:
  void Init();
  void Pay(float amount, PlayerId player_num);
 	Die* die0;
 	Die* die1;
 	std::map<std::string, Bet> bets;
  std::map<PlayerId, float> paid;  // How much each player has paid.
  std::map<PlayerId, float> bankrolls; // How much each player currently has.
  int bet_id_; // increment how many bets we have, increases from 0 to n.

  // Internal state to game.
  bool is_on; // Game starts off, then ON given certain rules.
  int on_num; // Value when table is "ON"
  PlayerId next_player_id;
  std::map<PlayerId, Player*> cur_players;
  lib::Counter* cnt;

  // To determine what happens to each bet next. The rules.
  std::map<BetName, BetNext> name_to_next;
  std::map<BetName, BetNextPass> name_to_next_pass;
  std::map<BetName, float> name_to_odds;
  std::map<BetName, BetOddsPass> name_to_odds_pass;
  // To help each player decide what bet to make next.
  std::map<PlayerId, std::vector<BetInfo> > last_changed_bets;
  bool IsPassBet(BetName name);
  bool IsPassBetOdds(BetName name); 
};

 void Round(Craps* craps);
 void TestStrategyMain();
}
#endif // _LESSONS