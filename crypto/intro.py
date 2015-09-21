import sys

def assertEquals(a, b):
  assert a == b

def encrypt(text, key):
  return text

def decrypt(cypher, public_key):
  return cypher

def main():
  text = "cheese and crackers"
  private_key = "abcd"
  public_key = "xyx"
  cypher = encrypt(text, private_key)
  output_text = decrypt(cypher, public_key)
  assertEquals(text, output_text)
  print '%s tests pass.' % (sys.argv[0])

main()