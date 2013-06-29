#include <iostream>
#include <stdlib.h>
#include <string.h> // memcpy
#include <string>
#include <sstream>
#include <iterator>
#include <vector>

// Frontier.
#include <algorithm>    // make_heap, pop_heap, push_heap, sort_heap
// Frontier and searched.
#include <map>

// Tests.
#include <assert.h>

using namespace std;

bool DEBUG = 0;
int CYCLE = 1000;
int STOP = 0;

class Reader{
  public:
  	Reader();
  	string Read();
};

Reader::Reader() {}

string Reader::Read() {
	string name;
	getline(cin, name);
	return name;
}

vector<string> Split(const string &input, char delim, vector<string> &tokens) {
	stringstream ss(input);
	string token;
	while(getline(ss, token, delim)) {
		tokens.push_back(token);
	}
	return tokens;
}

// Utilities.

string FromBoard(int* arr) {
	ostringstream s;
	string space = " ";
	for (int i = 0; i < 16; i++) {
		if (i == 0) {
			space = "";
		} else {
			space = " ";
		}
		s << space << arr[i];
	}
	return s.str();
};

int* ToBoard(string board) {
	vector<string> tokens;
	Split(board, ' ', tokens);
	int* arr = new int[16];
	for (int i=0; i < 16; i++) {
		arr[i] = atoi(tokens[i].c_str());
	}
	return arr;
}

// Crappy heuristic, how many pieces are misplaced.
int H1Dist(string board) {
  int* els = ToBoard(board);
  int missing = 0;
  for (int i = 0; i < 4; ++i) {
  	for (int j = 0; j < 4; ++j) {
  		int k = i * 4 + j;
  		if (els[k] != k + 1) {
  			missing++;
  		}
  	}
  }
  return missing;
}

/*
map<int, pair<int, int>> TILE_TO_LOC ({
  make_pair(1, make_pair(0, 0))
});
  2: {0, 1},
  3: {0, 2},
  4: {0, 3},
  5: {1, 0},
  6: {1, 1},
  7: {1, 2},
  8: {1, 3},
  9: {2, 0},
  10: {2, 1},
  11: {2, 2},
  12: {2, 3},
  13: {3, 0},
  14: {3, 1},
  15: {3, 2},
  16: {3, 3},
 */

// Better distance counts the number of steps to get a tile to a location.
int H2Dist(string board) {
  int* els = ToBoard(board);
  int missing = 0;
  for (int i = 0; i < 4; ++i) {
  	for (int j = 0; j < 4; ++j) {
  		int k = i * 4 + j;
  		int val = els[k];
  		int shouldBeRow = (val - 1) / 4;
  		int shouldBeCol = (val - 1) % 4;
  		missing = missing + abs(shouldBeRow - i) + abs(shouldBeCol - j);
  		}
  }
  return missing;
}

int Heuristic(string board) {
	return H1Dist(board);
}


// A*, graph utility functions.

class Node {
  public:
  	Node(string state);
  	int f; // how many steps to get here.
  	int g; // heuristic component.
  	int h; // sum of f and g.
  	string state;
  	Node* parent; // who I came from.
  	string str();
};

Node::Node(string stateI) {
  state = stateI;
  f = 0;
  g = 0;
  h = 0;
  parent = NULL;
}

string Node::str() {
	ostringstream s;
	s << " f: " << f << " g: " << g << " h: " << h << " state: " << state;
	return s.str();
}

class ExploredI {
  public:
    virtual void Add(Node* n)=0;
    virtual bool Contains(Node* n)=0;
};

class FrontierI {
  public:
  	virtual void Add(Node* n)=0;
  	virtual bool Contains(Node* n)=0;
  	virtual bool IsEmpty()=0;
  	virtual Node* Pop()=0;
};

class SolverI {
  public:
  	virtual bool IsGoal(Node* n)=0;
  	virtual vector<Node*> GetCandidates(Node* n)=0;
};

Node* GraphSearch(ExploredI* explored, FrontierI* frontier, SolverI* solver) {
  int count = 0;
  while (!frontier->IsEmpty()) {
  	count++;
  	Node* cur = frontier->Pop();
  	if (STOP != 0 && STOP == count) {
  		break;
  	}
  	if (DEBUG) {
  	  if (count % CYCLE == 0) {
  		  cout << cur->str() << '\n';
  	  }
  	}
  	if (solver->IsGoal(cur)) {
  		return cur;
  	}
  	vector<Node*> candidates = solver->GetCandidates(cur);
  	explored->Add(cur);
  	for (int i = 0; i < candidates.size(); ++i) {
  		Node* cand = candidates[i];
  		if (!frontier->Contains(cand) && !explored->Contains(cand)) {
  			frontier->Add(cand);
  		}
  	}
  }
  return NULL;
}

// An item to allow for comparisons across a heuristic while still maintaining
// the board (obj).
class Item {
  public:
    string obj;
    int val;
    Item();
    Item(string obj, int val);
};

Item::Item() {}

Item::Item(string objIn, int valIn) {
  obj = objIn;
  val = valIn;
}

class CompareItem {
  public:
    bool operator() (const Item& x, const Item& y) const {
      return x.val > y.val;
    }
};

// Implementation of the frontier, explored, and solver interfaces.

class Frontier: public FrontierI {
  public:
  	Frontier();
  	void Add(Node* n);
  	bool Contains(Node* n);
  	bool IsEmpty();
  	Node* Pop();
  	int size();
  	int guesses();
  private:
  	vector<Item> items;
  	map<string, Node*>stateToNode;
  	int dbgCounter; 
};

Frontier::Frontier() {
  vector<Item> items;
  map<string, Node*>stateToNode;
  dbgCounter = 0;
}

// Frontier.
void Frontier::Add(Node* n) {
  // Calculate heuristic values for the node when adding it.
  // and save it into the node.
  if (n->parent != NULL) {
  	n->f = n->parent->f + 1;
  	n->g = Heuristic(n->state);
  	n->h = n->f + n->g; // Combine the costs linearly.
  }

  Item i0(n->state, n->h);

  items.push_back(i0);
  stateToNode[n->state] = n;
  if (items.size() == 0) {
  	// Make the heap the first time.
  	make_heap(items.begin(), items.end(), CompareItem());
  } else {
  	push_heap(items.begin(), items.end(), CompareItem());
  }
}

bool Frontier::Contains(Node* n) {
	return stateToNode.find(n->state) != stateToNode.end();
}

bool Frontier::IsEmpty() {
	dbgCounter++;
	if (DEBUG && dbgCounter % CYCLE == 0) {
		cout << "Frontier states: " << items.size() << '\n';
	}
	return items.size() == 0;
}

Node* Frontier::Pop() {
	Item ret = items.front();
	pop_heap(items.begin(), items.end(), CompareItem());
	items.pop_back();
	return stateToNode[ret.obj];
}

int Frontier::size() {
  return items.size();
}

int Frontier::guesses() {
  return dbgCounter;
}

// Explored set.
class Explored: public ExploredI {
  public:
    void Add(Node* n);
    bool Contains(Node* n);
    Explored();
  private:
  	map<string, bool> stateMap;
};

Explored::Explored() {
	map<string, bool> stateMap;
}

void Explored::Add(Node* n) {
	stateMap[n->state] = true;
}

bool Explored::Contains(Node* n) {
	return stateMap.find(n->state) != stateMap.end();
}

// Solver.
class Solver: public SolverI {
  public:
  	bool IsGoal(Node* n);
  	vector<Node*> GetCandidates(Node* n);
};

bool Solver::IsGoal(Node* n) {
	return Heuristic(n->state) == 0;
}

// Returns a new board with the two integers swapped.
int* SwapThem(int* board, int blankInd, int switchInd) {
  int* newBoard = new int[16];
  memcpy(newBoard, board, sizeof(int) * 16);
  int b4Val = board[switchInd];
  newBoard[switchInd] = 16;
  newBoard[blankInd] = b4Val;
  return newBoard;
}

vector<Node*> Solver::GetCandidates(Node* n) {
	int* board = ToBoard(n->state);
	// Find the blank board.
	int blankInd = -1;
    for (int i = 0; i < 16; ++i) {
    	if (board[i] == 16) {
    		blankInd = i;
    		break;
    	}
    }
	vector<Node*> cands;
	// Fill in the candidates with just their state values and who their
	// parent is.

    int adjStates[4] = {blankInd+1, blankInd-1, blankInd-4, blankInd+4};
    for (int j = 0; j < 4; ++j) {
      int ind = adjStates[j];
      if (ind > 0 && ind < 16) {
      	int* newBoard = SwapThem(board, blankInd, ind);
      	Node* cand = new Node(FromBoard(newBoard));
      	cand->parent = n;
      	cands.push_back(cand);
      }
    }
	return cands;
}

// Driver which reads from standard input and hands it off to the graph search
// to solve the problem.
class Board {
  public:
  	Board();
  	void Create(Reader* r);
  	void Solve();
  private:
  	string board;
};

Board::Board() {}

void Board::Create(Reader* r) {
  int* arr = new int[16];
  for (int i = 0; i < 4; i++) {
  	vector<string> tokens;
  	Split(r->Read(), ' ', tokens);
    for (int j = 0; j < 4; ++j) {
    	int k = i * 4 + j;
    	arr[k] = atoi(tokens[j].c_str());
    }
  }
  board = FromBoard(arr);
  cout << "Board: " << board << "\n";
}

void Board::Solve() {
	Solver* s = new Solver();
	Frontier* f = new Frontier();
    Explored* e = new Explored();
    Node* initial = new Node(board);
    f->Add(initial);
	Node* goal = GraphSearch(e, f, s);
	if (goal != NULL) {
		cout << "Found goal with properties" << goal->str() << '\n';
		cout << "# my steps: " << goal->f << '\n';
		cout << "# guesses: " << f->guesses() << '\n';
		cout << "# on frontier: " << f->size() << '\n';
	} else {
		cout << "Could not find goal it is empty. " << '\n';
	}
}

void tests() {
	string board = "1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16";
	assert(board == FromBoard(ToBoard(board)));
	assert(0 == Heuristic(board));
	assert(2 == H1Dist("3 2 1 4 5 6 7 8 9 10 11 12 13 14 15 16"));
	assert(4 == H2Dist("3 2 1 4 5 6 7 8 9 10 11 12 13 14 15 16"));
	string board1 = "16 2 3 4 5 6 7 8 9 10 11 12 13 14 15 1";
	assert(board1.compare(FromBoard(SwapThem(ToBoard(board), 15, 0))) == 0);
}

int main() {
	tests();
	cout << "Ready to read the board.\n";
	Reader* r = new Reader();
	int T = atoi(r->Read().c_str());
	for (int i = 0; i < T; i++) {
		Board b;
		b.Create(r);
		b.Solve();
	}
	return 0;
}