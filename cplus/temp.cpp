#include <iostream>

using namespace std;

class CRectangle {
  private:
    int* width;
    int* height;
    void init_object(int, int);
  public:
    // Constructor.
    CRectangle(int, int);
    CRectangle();
    CRectangle(const CRectangle&); // copy constructor.
    // Destructor.
    ~CRectangle();
    // Getter setters.
    void set_values(int, int);
    int get_height() const;
    int get_width() const;
    int area() { return (*width * *height); };
    void print_values(void);
    // Overloading.
    int operator + (CRectangle);
};

CRectangle::CRectangle (int a, int b) {
  init_object(a, b);
}

// Default constructor.
CRectangle::CRectangle () {
  init_object(5, 5);
}

// Destructor.
CRectangle::~CRectangle() {
  delete width;
  delete height;
}

// Copy constructor. (Prevents directly copying pointers and having
// bad behavior when passing an object by reference and inadvertently
// changing a pointer's value which is a member of that object.

CRectangle::CRectangle(const CRectangle& oldRect) {
  init_object(oldRect.get_height(), oldRect.get_width()); 
}

void CRectangle::init_object(int new_height, int new_width) {
  width = new int;
  height = new int;
  *width = new_width;
  *height = new_height; 
}

void CRectangle::set_values (int new_height, int new_width) {
  *height = new_height;
  *width = new_width;
}

int CRectangle::get_height () const {
  return *height;
}

int CRectangle::get_width () const {
  return *width;
}

void CRectangle::print_values () {
  cout << "area: " << area() << endl;
}

void test_pointer_logic () {
  CRectangle * b = new CRectangle[3];
  b->set_values(4, 5);
  b->print_values();
  b[0].set_values(2, 2);
  b->print_values();
  b[2].print_values();
  delete[] b;
}

// Overloading operators.
int CRectangle::operator+ (CRectangle param) {
  return *width + param.get_width();
}

int main() {
  CRectangle rect(3, 4);
  CRectangle* rect2 = new CRectangle();
  // Copy constructor.
  CRectangle rect3(rect);
  // Does this change rect's values? // Yes! it did
  // we need to define our own copy constructor.
  rect3.set_values(10, 20);
  (&rect)->print_values();
  rect2->print_values();
  rect3.print_values();

  // Test pointer logic.
  test_pointer_logic();

  cout << "Overloaded: " << (rect + *rect2) << endl;
  return 0;
}
