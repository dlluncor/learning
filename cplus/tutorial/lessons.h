#ifndef _LESSONS_H
#define _LESSONS_H

#include <stdio.h>
#include <string.h>
#include <vector>
#include <map>

using namespace std;

class Game {
  public:
    virtual ~Game(){
      //cout << "Destroy games\n";
    };
    void Name(){ cout << "I am a game" << "\n"; };
  private:
  	string game_;
};

class Die {
 public:
  int Roll();
};

struct Bet {
  string name;
  int player;
  float value;
};

typedef string (*BetNext)(int die0, int die1, bool is_on);
// Bets that depend on the "ON" position.
typedef string (*BetNextPass)(int on_num, int die0, int die1, bool is_on);
typedef float (*BetOddsPass) (int on_num);
typedef string BetName;

class Craps : public Game {
 public:
   Craps();
   ~Craps();  // Only use virtual destructors when it has ANY virtual methods.
   void Roll();
   void AddBet(Bet bet);
 private:
  void Init();
  void Pay(int player_num, float amount);
 	Die* die0;
 	Die* die1;
 	map<string, Bet> bets;

  // Internal state to game.
  bool is_on; // Game starts off, then ON given certain rules.
  int on_value; // Value when table is "ON"

  map<BetName, BetNext> name_to_next;
  map<BetName, BetNextPass> name_to_next_pass;
  map<BetName, float> name_to_odds;
  map<BetName, BetOddsPass> name_to_odds_pass;
};
#endif // _LESSONS