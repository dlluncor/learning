from multiprocessing import Process, Queue, Pool
import os
import time

glo = 'woo'

def now():
  # Returns time in millis.
  return int(round(time.time() * 1000))

####### Example 3
def longtime(n):
  return sum([i for i in xrange(n * 1000)])
    

def pools(num_procs):
  print 'Num processes: ', num_procs
  pool = Pool(processes=num_procs)
  result = pool.apply_async(longtime, [100])
  a = now()
  pool.map(longtime, range(1000))
  b = now()
  timetook = b-a
  print 'pools', timetook
  return (num_procs, timetook)

def nopools():
  a = now()
  map(longtime, range(1000))
  b = now()
  print 'no pools', b-a


####### Example 2

def f2(q, string):
  el = string * 16000
  ans = 1
  sign = 1
  for char in el:
    ans *= 20 + sign
    sign *= -1
  q.put(ans)

strings = ['cheese', 'oh']

def nothreads():
  a0 = now()
  q = Queue()
  for i in xrange(len(strings)):
    f2(q, strings[i])
  a1 = now()
  print 'no threads', a1 - a0

def threads():
  q = Queue()
  a0 = now()
  procs = []
  for i in xrange(len(strings)):
    p = Process(target=f2, args=(q,strings[i]))
    p.start()
    procs.append(p)
  # Print results
  for i in xrange(len(strings)):
    #print q.get()
    procs[i].join()
  a1 = now()
  print 'threads', a1 - a0

######## Example 1

def info(title):
  print title
  print 'module name: ', __name__
  for i in xrange(10):
    glo = title
    print 'glo: ', glo
  if hasattr(os, 'getppid'): # Only available on Unix
    print 'parent process: ', os.getpid()

def f(name):
  info('function f')
  print 'hello', name

def main1():
  info('main line')
  p = Process(target=f, args=('bob',))
  p.start()
  p.join()

if __name__ == '__main__':
  #threads()
  #nothreads()
  els = []
  for i in range(1, 40):
    els.append(pools(i))
  nopools()
  f = open('procs.txt', 'w')
  f.write('\n'.join([','.join(el) for el in els]))
  f.close()
