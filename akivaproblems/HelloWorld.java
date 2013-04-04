public class HelloWorld {

  public int getVal(String str, int index) {
    String c = "" + str.charAt(index);
    return Integer.parseInt(c);
  }

  public String addBinaryNumbers(String num1, String num2) {
    String bigger = num1;
    String smaller = num2;
    if (num1.length() < num2.length()) {
      bigger = num2; smaller = num1;
    }
    String newS = ""; int carry = 0; int smallStart = smaller.length() -1;
    int bigStart = bigger.length() - 1;
    for (int i = smallStart; i >= 0; i--) {
      int d0 = getVal(bigger, bigStart);
      int d1 = getVal(smaller, smallStart);
      int sum = d0 + d1 + carry;
      if (sum == 0) { newS += "0"; carry = 0;}
      else if (sum == 1) {newS += "1"; carry = 0;}
      else if (sum == 2) {newS += "0"; carry = 1;}
      else {newS += "1"; carry = 1;}
      System.out.println(d0 + " " + d1 + " " + sum + " " + carry);
      bigStart -= 1;
      smallStart -= 1;
    }
    for (int j = bigStart; j >= 0; j--) {
      int d0 = getVal(bigger, j);
      int sum = d0 + carry;
      if (sum == 0) { newS += "0"; carry = 0; }
      else if (sum == 1) { newS += "1"; carry = 0;}
      else { newS += "0"; carry = 1;}  
    }
    newS += "" + carry;
    return new StringBuffer(newS).reverse().toString();
  }

  public static void main(String[] args) {
    FB fb = new FB();
    //String actual = fb.addBinaryNumbers("110", "01101");
    //System.out.println("Expected: 10011. Actual: " + actual);
    String actual = fb.addBinaryNumbers("11", "11");
    System.out.println("Expected: 110... Actual: " + actual);
  }
}
