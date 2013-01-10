# Dykstras algorithm 1/9/2013

import sys

def Assert(val1, val2):
  if val1 != val2:
    raise AssertionError(str(val1) + ' != ' + str(val2))

# Graph has a node. Each node has a list of nodes that connect to it.

class Node(object):
  def __init__(self, name, names_with_costs):
    self.prev = names_with_costs  # list of previous nodes.
    self.name = name  # A

class Graph(object):
  def __init__(self, nodes):
    self.nodes = nodes

  def ShortestPath(self, source, sink):
    # Trivial case.
    if source == sink:
      return (0, [])

    nameToNode = {}
    for node in self.nodes:
      nameToNode[node.name] = node

    working_set = set([]) # Working set of nodes.
    paths = {}  # Paths from source to sink.
    for node in self.nodes:
      paths[node.name] = []

    # Initialize distances to inf.
    distances = {}  # Maps node name to distance to sink.
    for node in self.nodes:
      distances[node.name] = sys.maxint
    distances[sink] = 0  # No distance coming from the sink node.

    # Start at sink node and fill in original costs.
    cur_node = nameToNode[sink]
    working_set.add(cur_node)

    while len(working_set) != 0:
      cur_node = working_set.pop()
      # Update distances of previous nodes and add those nodes to the working set.
      for name, cost in cur_node.prev:
        new_cost = distances[cur_node.name] + cost
        if distances[name] > new_cost:
          paths[name] = paths[cur_node.name] + [cur_node.name]
          distances[name] = new_cost
        working_set.add(nameToNode[name])

    paths[source].reverse()
    return (distances[source], paths[source]) 

def Test1():
  # Construct graph.
  a = Node('a', [('d', 1), ('b', 3), ('c', 5)])
  b = Node('b', [('c', 1)])
  c = Node('c', [])
  d = Node('d', [])
  g = Graph([a, b, c, d])
  Assert((4, ['b', 'a']), g.ShortestPath('c', 'a'))
  Assert((1, ['a']), g.ShortestPath('d', 'a'))
  Assert((3, ['a']), g.ShortestPath('b', 'a'))
  Assert((0, []), g.ShortestPath('a', 'a'))
  print 'Test1 passes'

def Test2():
  # Add a more complicated graph.
  a = Node('a', [('d', 1), ('b', 10), ('c', 3)])
  b = Node('b', [('c', 5), ('d', 1)])
  c = Node('c', [])
  d = Node('d', [('c', 1)])
  g = Graph([a, b, c, d])
  Assert((2, ['d', 'a']), g.ShortestPath('c', 'a'))
  print 'Test2 passes'

def main():
  Test1()
  Test2()

main()
