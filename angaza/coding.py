import csv

def populate(d, sent):
  words = sent.split(' ')
  curWord = '*'
  for nextWord in words:
    if curWord not in d:
      d[curWord] = {}
      d[curWord]['***'] = 0
    dWords = d[curWord]
    if nextWord not in dWords:
      dWords[nextWord] = 0
    dWords[nextWord] += 1
    dWords['***'] += 1
    curWord = nextWord

  # Last word in the sentence.
  if curWord not in d:
    d[curWord] = {}
    d[curWord]['***'] = 0

import random

def pickWord(nextWordsD):
  listProbs = []
  words = []
  denom = nextWordsD['***']
  curProb = 0.0
  for _, key in enumerate(nextWordsD):
    if key == '***':
      continue
    num = nextWordsD[key]
    prob = num / (denom * 1.0)
    curProb += prob
    words.append(key)
    listProbs.append(curProb)

  r = random.random()
  for i, prob in enumerate(listProbs):
    if r < prob:
      return words[i]
  print 'End of sentence'
  return False

def endOfSent(word):
  char = word[-1]
  return char == '!' or char == '.' or char == '?' 

def generateSentence(d, numWords):
  curWord = '*'
  sentence = []
  for _ in xrange(numWords):
    try:
      nextWordsD = d[curWord]
    except Exception as e:
      print 'Next words key error: %s. %s' % (str(e), d)
    word = pickWord(nextWordsD)
    if word == False:
      break
    sentence.append(word)
    curWord = word
    if endOfSent(curWord):
      break

  print ' '.join(sentence)

def main():
  c = csv.reader(open('angaza_tweets.csv', 'r'))
  colNum = 5
  d = {}  # From word to following words and counts.
  d['*'] = {}
  d['*']['***'] = 0
  i = 0 
  for r in c:
    i += 1
    if i == 1:
      continue
    #if i > 100:
    #  break
    sent = r[colNum]
    #print sent
    populate(d, r[colNum])
    #for col in r:
    #  print col 
  #for _, key in enumerate(d):
  #  otherD = d[key]
  #  print '%s, %s' % (key, str(otherD))
  print '\nGENERATED TWEET:' 
  generateSentence(d, 100)

main()
