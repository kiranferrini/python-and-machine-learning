# -*- coding: utf-8 -*-
"""
Created on Wed Oct 12 10:57:59 2022

@author: kiranferrini
"""



class Node:
    def __init__(self, name):
        self.name = name
        self.edges = {}    
        
    def get_weight(self, n):
        if n in self.edges:
            return self.edges[n]
        else:
            return -1
    
    def add_edge(self, n, w):
        self.edges[n] = w
    
    def num_neighbors(self):
        return len(self.edges)
    
    def get_neighbors(self):
        return list(self.edges.keys())
    
class Graph:
    def __init__(self):
        self.nodes = {}
    
    def size(self):
        return len(self.nodes)
    
    def add_nodes(self, names):
        for c in names:
            if c not in self.nodes:
                self.nodes[c] = Node(c)
   
    def add_edge(self, n1, n2, w):
        if (n1 in self.nodes.keys()) and (n2 in self.nodes.keys()):
            self.nodes[n1].add_edge(n2, w)
            self.nodes[n2].add_edge(n1, w)

    def get_names(self):
        return list(self.nodes.keys())    
        
    def get_node(self, n):
        if n in self.nodes:
            return self.nodes[n] 
        else:
            return -1

    def shortest_path(self, n1, n2):
        if (n1 not in self.nodes.keys()) or (n2 not in self.nodes.keys()):
            return -1 
        E = dict()
        D = dict()
        path = dict()
        for c in self.get_names():
            E[c] = 0 
            D[c] = 'pl'
            path[c] = 'pl'
        while D != E: 
            for c in self.get_names():
                D[c] = E[c]
            for n in self.get_names():
                if n != n2:
                    d = dict()
                    for m in self.nodes[n].get_neighbors(): 
                        d[m] = self.nodes[n].get_weight(m) + D[m]     
                    E[n] = min(d.values())
                    for o in d.keys():
                        if d[o] == min(d.values()):
                            path[n] = o    
        pathlist = list(n1)
        w = n1                     
        while w != n2:
            pathlist.append(path[w])
            w = path[w]
        return [D[n1], pathlist ,D]
                    
'''                                  
g = Graph()
l = ['0','1','2','3','4']
g.add_nodes(l)

g.add_edge('0', '1', 5)
g.add_edge('0', '1', 3)
g.add_edge('0', '8', 42)
g.add_edge('0', '3', 4)
g.add_edge('0', '4', 8)


g.add_edge('1', '0', 3)
g.add_edge('1', '3', 4)
g.add_edge('1', '2', 1)

g.add_edge('2', '1', 1)
g.add_edge('2', '3', 2)

g.add_edge('3', '2', 2)
g.add_edge('3', '1', 4)
g.add_edge('3', '0', 7)
g.add_edge('3', '4', 3)

g.add_edge('4', '0', 8)
g.add_edge('4', '3', 3)

g.shortest_path('4','2')
g.shortest_path('0','2')
'''