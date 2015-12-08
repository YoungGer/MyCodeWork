
# coding: utf-8

# In[1]:

cd 'Desktop/ProblemSet5/'


# # 定义基本的数据结构

# In[53]:

# 6.00.2x Problem Set 5
# Graph optimization
#
# A set of data structures to represent graphs
#

class Node(object):
    def __init__(self, name):
        self.name = str(name)
    def getName(self):
        return self.name
    def __str__(self):
        return self.name
    def __repr__(self):
        return self.name
    def __eq__(self, other):
        return self.name == other.name
    def __ne__(self, other):
        return not self.__eq__(other)
    def __hash__(self):
        # Override the default hash method
        # Think: Why would we want to do this?
        return self.name.__hash__()

class Edge(object):
    def __init__(self, src, dest):
        self.src = src
        self.dest = dest
    def getSource(self):
        return self.src
    def getDestination(self):
        return self.dest
    def __str__(self):
        return '{0}->{1}'.format(self.src, self.dest)

class WeightedEdge(Edge):
    def __init__(self,src,dest,totalD,outD):
        Edge.__init__(self,src,dest)
        self.totalD = totalD
        self.outD = outD
    def getTotalDistance(self):
        return self.totalD
    def getOutdoorDistance(self):
        return self.outD
    def __str__(self):
        return str(self.getSource()) + '->' +str(self.getDestination()) + ' '+ '(' +str(self.getTotalDistance()) + ', '+ str(self.getOutdoorDistance())+')'
    
    
class Digraph(object):
    """
    A directed graph
    """
    def __init__(self):
        # A Python Set is basically a list that doesn't allow duplicates.
        # Entries into a set must be hashable (where have we seen this before?)
        # Because it is backed by a hashtable, lookups are O(1) as opposed to the O(n) of a list (nifty!)
        # See http://docs.python.org/2/library/stdtypes.html#set-types-set-frozenset
        self.nodes = set([])
        self.edges = {}
    def addNode(self, node):
        if node in self.nodes:
            # Even though self.nodes is a Set, we want to do this to make sure we
            # don't add a duplicate entry for the same node in the self.edges list.
            raise ValueError('Duplicate node')
        else:
            self.nodes.add(node)
            self.edges[node] = []
    def addEdge(self, edge):
        src = edge.getSource()
        dest = edge.getDestination()
        if not(src in self.nodes and dest in self.nodes):
            raise ValueError('Node not in graph')
        self.edges[src].append(dest)
    def childrenOf(self, node):
        return self.edges[node]
    def hasNode(self, node):
        return node in self.nodes
    def __str__(self):
        res = ''
        for k in self.edges:
            for d in self.edges[str(k)]:
                res = '{0}{1}->{2}\n'.format(res, k, d)
        return res[:-1]

class WeightedDigraph(Digraph):
    def __init__(self):
        Digraph.__init__(self)
        self.EDGES = []
    def addEdge(self,edge):
        src = edge.getSource()
        dest = edge.getDestination()
        if not(src in self.nodes and dest in self.nodes):
            raise ValueError('Node not in graph')
        self.edges[src].append([dest,(edge.getTotalDistance(),edge.getOutdoorDistance())])
        self.EDGES.append(edge)
    def childrenOf(self,node):
        return [i[0] for i in self.edges[node]]
    def __str__(self):
        L = ''
        for i in self.EDGES:
            k = str(i.getSource()) + '->' +str(i.getDestination()) + ' '+ '(' +str(float(i.getTotalDistance())) + ', '+ str(float(i.getOutdoorDistance()))+')'
            L = L+k+'\n'
        return L[0:-1]


# # 未优化步骤的暴力power的DFS算法

# In[102]:

# 6.00.2x Problem Set 5
# Graph optimization
# Finding shortest paths through MIT buildings
#

import string
# This imports everything from `graph.py` as if it was defined in this file!
# from graph import * 

#
# Problem 2: Building up the Campus Map
#
# Before you write any code, write a couple of sentences here 
# describing how you will model this problem as a graph. 

# This is a helpful exercise to help you organize your
# thoughts before you tackle a big design problem!
# 

def load_map(mapFilename):
    """ 
    Parses the map file and constructs a directed graph

    Parameters: 
        mapFilename : name of the map file

    Assumes:
        Each entry in the map file consists of the following four positive 
        integers, separated by a blank space:
            From To TotalDistance DistanceOutdoors
        e.g.
            32 76 54 23
        This entry would become an edge from 32 to 76.

    Returns:
        a directed graph representing the map
    """
    # TODO
    print "Loading map from file..."
    #建立图
    G = WeightedDigraph()
    #遍历每一行，建立对应的node还有edge
    with open(r'mit_map.txt') as f:
        for line in f:
            params = map(int,line.split())
            src = Node(params[0])
            dest = Node(params[1])
            edge = WeightedEdge(src,dest,params[2],params[3])
            try:
                G.addNode(src)
            except ValueError:
                print 'Duplicate Src Node'
            try:
                G.addNode(dest)
            except ValueError:
                print 'Duplicate Dest Node'
            try:
                G.addEdge(edge)
            except ValueError:
                print 'Node Not in the Graph'
    return G

#
# Problem 3: Finding the Shortest Path using Brute Force Search
#
# State the optimization problem as a function to minimize
# and what the constraints are
#


def findAllPaths(digraph, start, end, path=[],paths=[]):
    path = path + [start] #创建了一个新的path
    if start==end:
        paths.append(path[:])
    for node in digraph.childrenOf(start):
        if node not in path:
            findAllPaths(digraph, node, end, path=path[:],paths=paths)
    return paths

            
def calPathDistance(digraph,path):
    #计算单个path的路径数据
    #path: list的Node数据
    #return ： 这个list的maxTotalDist, maxDistOutdoors数据
#     for i in range(len(path)):
#         path[i] = Node(path[i])
        
    total = 0
    out = 0
    for i in range(len(path)-1):
        src = path[i]
        dest = path[i+1]
        flag = 0 #等于0表示未找到对应这个循环src对dest的路径
        for j in digraph.edges[src]:
            if j[0]==dest:
                totalD = j[1][0]
                outD = j[1][1]
                flag = 1
                total += int(totalD)
                out += int(outD)
                break
        if flag== 0:
            raise ValueError('找不到path对应的graph中的路径')
    return (total,out)       
        
            
def findNeededPaths(digraph,paths, maxTotalDist, maxDistOutdoors):
    #已经找到所有的路线，下面求出满足特定条件的路线集合
    #另外在找到最佳的路线
    NEEDEDPATHS = []
    bestpath = []
    besttotald = 100000000000000000000000
    bestoutd = 0
    for path in paths:
        totalDi,outDi = calPathDistance(digraph,path)
        if totalDi <= maxTotalDist and outDi<=maxDistOutdoors:
            NEEDEDPATHS.append(path[:])
            if totalDi < besttotald:
                besttotald = totalDi
                bestpath = path[:]
#             if outDi < bestoutd:
#                 bestoutd = outDi
#                 bestpath = path[:]
    for i in range(len(bestpath)):
        bestpath[i] = str(bestpath[i])
    return (NEEDEDPATHS,bestpath,besttotald)


def bruteForceSearch(digraph, start, end, maxTotalDist, maxDistOutdoors):    
    """
    Finds the shortest path from start to end using brute-force approach.
    The total distance travelled on the path must not exceed maxTotalDist, and
    the distance spent outdoor on this path must not exceed maxDistOutdoors.

    Parameters: 
        digraph: instance of class Digraph or its subclass
        start, end: start & end building numbers (strings)
        maxTotalDist : maximum total distance on a path (integer)
        maxDistOutdoors: maximum distance spent outdoors on a path (integer)

    Assumes:
        start and end are numbers for existing buildings in graph

    Returns:
        The shortest-path from start to end, represented by 
        a list of building numbers (in strings), [n_1, n_2, ..., n_k], 
        where there exists an edge from n_i to n_(i+1) in digraph, 
        for all 1 <= i < k.

        If there exists no path that satisfies maxTotalDist and
        maxDistOutdoors constraints, then raises a ValueError.
    """
    paths = findAllPaths(digraph, Node(start), Node(end), path=[],paths=[])
    (NEEDEDPATHS,bestpath,besttotald) = findNeededPaths(digraph,paths, maxTotalDist, maxDistOutdoors)
    if bestpath == []:
        raise ValueError
    return bestpath

#
# Problem 4: Finding the Shorest Path using Optimized Search Method
#
def directedDFS(digraph, start, end, maxTotalDist, maxDistOutdoors):
    """
    Finds the shortest path from start to end using directed depth-first.
    search approach. The total distance travelled on the path must not
    exceed maxTotalDist, and the distance spent outdoor on this path must
	not exceed maxDistOutdoors.

    Parameters: 
        digraph: instance of class Digraph or its subclass
        start, end: start & end building numbers (strings)
        maxTotalDist : maximum total distance on a path (integer)
        maxDistOutdoors: maximum distance spent outdoors on a path (integer)

    Assumes:
        start and end are numbers for existing buildings in graph

    Returns:
        The shortest-path from start to end, represented by 
        a list of building numbers (in strings), [n_1, n_2, ..., n_k], 
        where there exists an edge from n_i to n_(i+1) in digraph, 
        for all 1 <= i < k.

        If there exists no path that satisfies maxTotalDist and
        maxDistOutdoors constraints, then raises a ValueError.
    """
    #TODO
    pass


# In[61]:

mitMap = load_map("mit_map.txt")
print mitMap.nodes
print mitMap.edges
print mitMap.edges[Node(54)]
print mitMap.edges[Node(56)]
print calPathDistance(mitMap,[54, 56,68])
#测试
print findAllPaths(mitMap, Node(54), Node(56), path=[],paths=[])


# # 优化步骤的DFS算法

# In[209]:

class WeightedEdge(Edge):
    def __init__(self,src,dest,totalD,outD):
        Edge.__init__(self,src,dest)
        self.totalD = totalD
        self.outD = outD
    def getTotalDistance(self):
        return self.totalD
    def getOutdoorDistance(self):
        return self.outD
    def __str__(self):
        return str(self.getSource()) + '->' +str(self.getDestination()) + ' '+ '(' +str(self.getTotalDistance()) + ', '+ str(self.getOutdoorDistance())+')'

class WeightedDigraph(Digraph):
    def __init__(self):
        Digraph.__init__(self)
        self.EDGES = []
    def addEdge(self,edge):
        src = edge.getSource()
        dest = edge.getDestination()
        if not(src in self.nodes and dest in self.nodes):
            raise ValueError('Node not in graph')
        self.edges[src].append([dest,(edge.getTotalDistance(),edge.getOutdoorDistance())])
        self.EDGES.append(edge)
    def childrenOf(self,node):
        return [i[0] for i in self.edges[node]]
    def __str__(self):
        L = ''
        for i in self.EDGES:
            k = str(i.getSource()) + '->' +str(i.getDestination()) + ' '+ '(' +str(float(i.getTotalDistance())) + ', '+ str(float(i.getOutdoorDistance()))+')'
            L = L+k+'\n'
        return L[0:-1]

def findAllPaths(digraph, start, end, maxTotalDist, maxDistOutdoors, path=[],paths=[],shortestD = 1e20):
    path = path + [start] #创建了一个新的path
    (total,out)  = calPathDistance(digraph,path) #当前这个path的距离信息
    if total>shortestD:
        return None
    if start==end and total<shortestD and total<=maxTotalDist and out<=maxDistOutdoors:
        paths.append(path[:])
        shortestD = total
    for node in digraph.childrenOf(start):
        if node not in path:  # 避免循环的情况出现
                if total<=maxTotalDist and out<=maxDistOutdoors:
                    findAllPaths(digraph, node, end, maxTotalDist, maxDistOutdoors, path=path[:],paths=paths,shortestD=shortestD)
    return paths

            
def calPathDistance(digraph,path):
    #计算单个path的路径数据
    #path: list的Node数据
    #return ： 这个list的maxTotalDist, maxDistOutdoors数据
#     for i in range(len(path)):
#         path[i] = Node(path[i])
        
    total = 0
    out = 0
    for i in range(len(path)-1):
        src = path[i]
        dest = path[i+1]
        flag = 0 #等于0表示未找到对应这个循环src对dest的路径
        for j in digraph.edges[src]:
            if j[0]==dest:
                totalD = j[1][0]
                outD = j[1][1]
                flag = 1
                total += int(totalD)
                out += int(outD)
                break
        if flag== 0:
            raise ValueError('找不到path对应的graph中的路径')
    return (total,out)       

# Problem 4: Finding the Shorest Path using Optimized Search Method
#
def directedDFS(digraph, start, end, maxTotalDist, maxDistOutdoors):
    """
    Finds the shortest path from start to end using directed depth-first.
    search approach. The total distance travelled on the path must not
    exceed maxTotalDist, and the distance spent outdoor on this path must
	not exceed maxDistOutdoors.

    Parameters: 
        digraph: instance of class Digraph or its subclass
        start, end: start & end building numbers (strings)
        maxTotalDist : maximum total distance on a path (integer)
        maxDistOutdoors: maximum distance spent outdoors on a path (integer)

    Assumes:
        start and end are numbers for existing buildings in graph

    Returns:
        The shortest-path from start to end, represented by 
        a list of building numbers (in strings), [n_1, n_2, ..., n_k], 
        where there exists an edge from n_i to n_(i+1) in digraph, 
        for all 1 <= i < k.

        If there exists no path that satisfies maxTotalDist and
        maxDistOutdoors constraints, then raises a ValueError.
    """
    #TODO
    paths = findAllPaths(digraph, Node(start), Node(end),  maxTotalDist, maxDistOutdoors,path=[],paths=[],shortestD = 1e20)
    if paths == []:
        raise ValueError
    else:
        #选择best_path
        x = [calPathDistance(digraph,path)[0] for path in paths]
        bestpath = paths[x.index(min(x))]
        for i in range(len(bestpath)):
            bestpath[i] = str(bestpath[i])
        return bestpath


# In[210]:

n1 = Node('1')
n2 = Node('2')
n3 = Node('3')
n4 = Node('4')
n5 = Node('5')



e1 = WeightedEdge(n1, n2, 5, 2)
e2 = WeightedEdge(n2, n3, 20, 10)
e3 = WeightedEdge(n2, n4, 10, 5)
e4 = WeightedEdge(n3, n5, 6, 3)
e5 = WeightedEdge(n4, n3, 2, 1)
e6 = WeightedEdge(n4, n5, 20, 10)

g = WeightedDigraph()

g.addNode(n1)
g.addNode(n2)
g.addNode(n3)
g.addNode(n4)
g.addNode(n5)

g.addEdge(e1)
g.addEdge(e2)
g.addEdge(e3)
g.addEdge(e4)
g.addEdge(e5)
g.addEdge(e6)


# In[198]:

print g


# In[211]:

directedDFS(g,'4','5',21,11)

