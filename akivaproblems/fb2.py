def notGreaterThan(points, n):
  for point in points:
    if point >= n:
     return False
  return True

def longestStr(strings):
  olongest = [] # longest found subsequence
  n = len(strings)
  origPoints = [0 for string in xrange(n)] # Where to start at each string

  def longestStrRec(points, longest):
    while notGreaterThan(points, n):
      matching = strings[0][points[0]]
      for i in xrange(n):
        if matching != strings[i][points[i]]:
           longest = []
           points[i] += 1
           longestStrRec(points, longest)
      # There was a match.
      longest.append(matching)
      for i in xrange(n):
        points[i] += 1
    return longest

  return longestStrRec(origPoints, olongest)

def mergeSort(arr):
  if len(arr) <= 1:
    return arr
  # Split into two and then sort them, then merge.
  n = len(arr)
  mid = n / 2
  bottom = arr[0:mid]
  top = arr[mid:]
  bottomSorted = mergeSort(bottom)
  topSorted = mergeSort(top)

  botInd = 0
  topInd = 0
  sortedArr = []
  while botInd < len(bottomSorted) and topInd < len(topSorted):
    bel = bottomSorted[botInd]
    tel = topSorted[topInd]
    if bel > tel:
      sortedArr.append(tel)
      topInd += 1
    else:
      sortedArr.append(bel)
      botInd += 1
  sortedArr += topSorted[topInd:]
  sortedArr += bottomSorted[botInd:]
  return sortedArr


def quickSort2(arr):
  quickSortHelper(arr, 0, len(arr)-1)
  return arr

def quickSortHelper2(arr, left, right):
  if left >= right: return
  piv = randint(left, right)
  pivot = arr[piv]
  arr[piv], arr[right] = arr[right], arr[piv]
  i, j = left, right-1
  while i < j:
    while arr[i] < pivot and i < j:
      i += 1
    while arr[j] > pivot and j > i:
      j -= 1
    arr[i], arr[j] = arr[j], arr[i]

  arr[j], arr[right] = arr[right], arr[j]
  quickSortHelper(arr, left, j)
  quickSortHelper(arr, j+1, right)

from random import randint
def quickSortHelper(arr, left, right):
  if left >= right: return
  piv = randint(left, right)
  arr[piv], arr[right] = arr[right], arr[piv]
  i, j = left, right-1
  pivot = arr[right]
  while i < j:
    while arr[i] < pivot and i<j: i+=1
    while arr[j] > pivot and i<j: j-=1
    print arr, arr[i], arr[j], i, j
    arr[i], arr[j] = arr[j], arr[i]
  arr[i+1], arr[right] = arr[right], arr[i+1]
  quickSortHelper(arr, left, i)
  quickSortHelper(arr, i+2, right)

def quickSort(arr):
  if len(arr) <= 1:
    return arr

  index = len(arr) / 2 
  pivot = arr[index]
  bottom = []
  top = []
  for i in xrange(len(arr)):
    if i == index:
      continue
    val = arr[i]
    if val < pivot:
      bottom.append(val)
    else:
      top.append(val)
  return quickSort(bottom) + [pivot] + quickSort(top)


def sortit(arr, method='merge'):
  if method == 'merge':
    return mergeSort(arr)
  elif method == 'quick':
    return quickSort2(arr)

def bridge_str(string):
  if len(string) <= 0:
    return string
 
  output = '' # Final output.
  ignore = '-'
  # Seek to the first non - character.
  start_index = 0
  for i in xrange(len(string)):
    c = string[i]
    if c != ignore:
      start_index = i
      break
  
  cur = string[start_index]
  num = 0  # Number of my current character that I print out.
  dashes = 0 # Number of dashes I have seen.
  for c in string[start_index+1:]:
    if c == ignore:
      dashes += 1
      continue
    if c == cur: 
      num += 1  # num = 0 # index = 8 # dashes = 0  # c = 'c' # cur = 'b'
    else:
      if num == 0:
        output += cur
      else:
        output += '+' * (num + 1 + dashes)
        dashes = 0
        num = 0
      cur = c  # This is the new character I am looking to find a bridge for.
      
  # Flush the rest of my output here.
  if num == 0: # there has been no repeats of my characters
    output += cur
  else:
    output += '+' * (num + 1 + dashes)
  return output

def testing():
  print bridge_str('aab-b-bc-a-b--a')
  print sortit([1, 5, 10, 14, 2], 'quick')
  #print longestStr(['aab', 'ab'])

testing()
