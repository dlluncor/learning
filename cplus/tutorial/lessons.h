#ifndef _LESSONS_H
#define _LESSONS_H

#include <stdio.h>
#include <string.h>
#include <vector>
#include <map>

#define TRACE_MSG fprintf(stderr, __FUNCTION__     \
                          "() [%s:%d] here I am\n", \
                          __FILE__, __LINE__)

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

  Bet(BetName name_, float value_): name(name_), value(value_){};
  Bet(){};
};

typedef string (*BetNext)(int die0, int die1, bool is_on);
// Bets that depend on the "ON" position.
typedef string (*BetNextPass)(int on_num, int die0, int die1, bool is_on);
typedef float (*BetOddsPass) (int on_num, int sum);

class Game {
  public:
    virtual ~Game(){
      //cout << "Destroy games\n";
    };
    void Name(){ cout << "I am a game" << "\n"; };
    virtual void AddBet(Bet bet) = 0;
    virtual void Buyin(PlayerId id, float amount) = 0;
  private:
    string game_;
};

// Visible state of the game needed for a player to decide how to bet next.
struct GameState {
  bool is_on;
  int on_num;
};

// Info needed for a player to make a decision.
struct PlayerDecision {
  GameState game_state;
  vector<BetInfo> bet_infos;
  float amount;  // amount this player has.
  PlayerDecision(const GameState& game_state_, const vector<BetInfo>& bet_infos_,
    float amount_):
    game_state(game_state_), bet_infos(bet_infos_), amount(amount_){};
};

class Player {
  public:
    Player(Game* game, string name, string strategy);
    void set_id(PlayerId id);
    void NextActions(const PlayerDecision& decision);
    string str();
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
  bool IsPassBet(BetName name);
  bool IsPassBetOdds(BetName name); 

  // To help each player decide what bet to make next.
  map<PlayerId, vector<BetInfo>> last_changed_bets;
};
#endif // _LESSONS