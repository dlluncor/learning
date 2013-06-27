#include <iostream>
#include <sstream>

using namespace std;

class El {
  public:
  	El(int);
  	El();
    struct El* next;
    int data;
  	string printList();
};

El::El() {
  data = 0;
}

El::El(int dataIn) {
  data = dataIn;
}

string El::printList() {
  string asStr = "";
  std::stringstream ss;

  ss << data << " ";
  El* cur = next;
  while (cur != NULL) {
  	ss << cur->data << " ";
  	cur = cur->next;
  }

  asStr = asStr + ss.str();
  return asStr;
}

bool insertInFront (El** head, int data) {
	El* newEl = new El(data);
	if (!newEl) return false;
	newEl->next = *head;
	*head = newEl;
	return true;
}

El* findElement (El* head, int data) {
	El* cur = head;
	while (cur != NULL) {
		if (cur->data == data) { return cur;}
		cur = cur->next;
	}
	return NULL;
}

bool deleteElement(El** head, El* deleteEl) {
	// If we delete from the head, we must move the pointer.
    if (*head == deleteEl) {
    	El* newHead = (*head)->next;
    	*head = newHead;
    	return true;
    }
	// We are deleting regular old nodes.
	El* cur = *head;
	while (cur->next != NULL) {
		if (cur->next == deleteEl) {
			El* deletesNext = deleteEl->next;
			delete deleteEl;
			cur->next = deletesNext;
			return true;
		}
		cur = cur->next;
	}
	return false;
}

void deleteList(El** head) {
	El* cur = *head;
	while(cur->next != NULL) {
		El* deleteMe = cur;
		cur = cur->next;
		delete deleteMe;
	}
	delete *head;
}

int main() {
  El* el = new El(5);
  cout << "hello world" << "\n";
  int numbers[5] = {1, 2, 10, 4};
  El* curEl = el;
  for (int i = 0; i < 5; ++i) {
    El* nextEl = new El(numbers[i]);
    curEl->next = nextEl;
    curEl = nextEl;
  }
  cout << el->printList() << "\n";
  bool success = insertInFront(&el, 20);
  cout << el->printList() << "\n";
  cout << findElement(el, 2)->data << "\n";
  cout << findElement(el, 2000) << "\n";
  deleteElement(&el, el->next->next->next->next);
  cout << el->printList() << "\n";
  // Delete from the head.
  deleteElement(&el, el);
  cout << el->printList() << "\n";
  deleteList(&el);
  cout << el << "\n";
  return 1;
}