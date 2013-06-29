#include <iostream>

using namespace std;

// Want to create a binary search tree where I can remove, insert, and find.

class Node;

class Node {
  public:
  	// constructors
    Node(int data);
    ~Node();
    Node();
    // methods
    void Insert(Node* n);
    Node* Find(int data);
    string Print();
    int Val();
    void InOrder(int level);
  private:
  	int data;
  	Node* left;
  	Node* right;
};

Node::Node(int dataIn) : data(dataIn), left(NULL), right(NULL) {
}

Node::Node() : data(0){
}

Node::~Node() {
	left = NULL;
	right = NULL;
}

int Node::Val() {
	return data;
}

void Node::Insert(Node* n) {
	if (n->Val() > data) {
		if (right == NULL) {
			right = n;
			return;
		} else {
			right->Insert(n);
			return;
		}
	} else {
		if (left == NULL) {
			left = n;
			return;
		} else {
			left->Insert(n);
			return;
		}
	}
}

Node* Node::Find(int dataIn) {
  if (data == dataIn) {
  	return this;
  } else if (dataIn > data) {
    if (right == NULL) {
    	return NULL;
    }
    return right->Find(dataIn);
  } else {
  	if (right == NULL) {
  		return NULL;
  	}
  	return left->Find(dataIn);
  }
}

string Node::Print() {
  return "Found:";
}

void Node::InOrder(int depth) {
	if (left != NULL) {
		left->InOrder(depth + 1);
	}
	cout << "Val: " << data << " Level: " << depth << "\n";
	if (right != NULL) {
		right->InOrder(depth + 1);
	}
}

int main() {
  int vals[5] = {10, 2, 4, 13, 5};
  Node* root = new Node(vals[0]);
  int size = sizeof(vals)/ sizeof(int);
  cout << "About to print some nodes!!" << "\n";
  for (int i = 1; i < size; ++i) {
    root->Insert(new Node(vals[i]));
  }
  cout << root->Find(4)->Val() << "\n";
  root->InOrder(0);
  return 0;
}