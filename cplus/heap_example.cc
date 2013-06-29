// range heap example
#include <iostream>     // cout
#include <algorithm>    // make_heap, pop_heap, push_heap, sort_heap
#include <vector>       // vector
#include <stdio.h>      
#include <string.h>    // memcpy
#include <string>

#include <map>

using namespace std;

int main2 () {
  double myints[] = {10,20.1,30,5,15};
  vector<double> v(myints,myints+4);

  make_heap (v.begin(),v.end());
  cout << "initial max heap   : " << v.front() << '\n';

  pop_heap (v.begin(),v.end()); v.pop_back();
  cout << "max heap after pop : " << v.front() << '\n';

  v.push_back(99); push_heap (v.begin(),v.end());
  cout << "max heap after push: " << v.front() << '\n';

  sort_heap (v.begin(),v.end());

  cout << "final sorted range :";
  for (unsigned i=0; i<v.size(); i++)
    cout << ' ' << v[i];

  cout << '\n';

  return 0;
}

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
      return x.val < y.val;
    }
};


void mapExample() {
  map<string, int> m;
  m["hi"] = 0;
  // This is like map.Contains() in Java.
  cout << (m.find("hi") != m.end()) << '\n';
}

void copyExample() {
  int i0[3] = {1, 2, 3};
  int i1[3];
  memcpy(i1, i0, sizeof(int) * 3);
  cout << "copyExample\n";
  for (int i = 0; i < 3; i++) {
    cout << i1[i] << '\n';
  }
}

void stringExample() {
  cout << "string example\n";
  string hi = "yo there";
  cout << hi.compare("yo therez") << '\n';
}

int main() {
  Item i0("hithere", 2);
  //Item myints[0];
  //myints[0] = i0;
  vector<Item> v;
  v.push_back(i0);
  make_heap(v.begin(), v.end(), CompareItem());
  cout << "initial max heap : " << v.front().obj << '\n';
  
  Item i1("yo", 20);
  v.push_back(i1);
  // TODO(dlluncor): Why can't I just create one CompareItem() and then
  // pass it into this function?
  push_heap(v.begin(), v.end(), CompareItem());
  cout << "After push: " << v.front().obj << '\n';

  mapExample();
  copyExample();
  stringExample();
  //cout << CompareItem()(i0, i1) << '\n';
  /*
  pop_heap(v.begin(), v.end()); v.pop_back();
  cout << "after pop " << v.front() << '\n';

  v.push_back(99); push_heap(v.begin(), v.end());
  cout << "after push " << v.front() << '\n';

  // Kind of useless for me but I'll try it.
  sort_heap(v.begin(), v.end());

  for (int i = 0; i < v.size(); ++i) {
    cout << ' ' << v[i];
  }
  cout << '\n';
  */
  return 0;
}