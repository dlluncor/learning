#ifndef _LESSONS_H
#define _LESSONS_H

#include <stdio.h>
#include <string.h>
#include <vector>
#include <map>

using namespace std;

class Die {
 public:
  int Roll();
};

typedef string BetName;
typedef int PlayerId;

// Info needed about the board bet for the player to know how to bet next.
struct BetInfo{
  string prev_state; // previous state of the bet.
  string next_state; // next state of the bet.
  float prev_value;
  float next_value;
};

struct Bet {
  BetName name;
  PlayerId player;
  float value;
};

typedef string (*BetNext)(int die0, int die1, bool is_on);
// Bets that depend on the "ON" position.
typedef string (*BetNextPass)(int on_num, int die0, int die1, bool is_on);
typedef float (*BetOddsPass) (int on_num);

class Game {
  public:
    virtual ~Game(){
      //cout << "Destroy games\n";
    };
    void Name(){ cout << "I am a game" << "\n"; };
  private:
    string game_;
};

class Player {
  public:
    Player(Game* game, string name, string strategy);
    void set_id(PlayerId id);
    void NextActions();
  private:
    Game* game;
    string name;
    string strategy;
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
 private:
  void Init();
  void Pay(float amount, PlayerId player_num);
 	Die* die0;
 	Die* die1;
 	map<string, Bet> bets;
  map<PlayerId, float> paid;  // How much each player has paid.
  map<PlayerId, float> bankrolls; // How much each player currently has.

  // Internal state to game.
  bool is_on; // Game starts off, then ON given certain rules.
  int on_num; // Value when table is "ON"
  PlayerId next_player_id;
  map<PlayerId, Player*> cur_players;

  // To determine what happens to each bet next. The rules.
  map<BetName, BetNext> name_to_next;
  map<BetName, BetNextPass> name_to_next_pass;
  map<BetName, float> name_to_odds;
  map<BetName, BetOddsPass> name_to_odds_pass;

  // To help each player decide what bet to make next.
  map<PlayerId, vector<BetInfo>> last_changed_bets;
};
#endif // _LESSONS