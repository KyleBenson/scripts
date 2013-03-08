'''I pulled this off a Stack Overflow post: http://stackoverflow.com/questions/13904636/implementing-bronkerbosch-algorithm-in-python''' 

class BronKerbosch:
# dealing with a graph as list of lists

    def __init__(self,graph=None):
        self.graph = graph

    def run(self):
        graph = set(range(len(self.graph)))
        self.bron_kerbosch(set(),graph,set())

#function determines the neighbors of a given vertex
    def neighbors(self, vertex):
        c = 0
        l = set()
        for i in self.graph[vertex]:
            if i is 1 :
                l.add(c)
            c+=1   
        return l

    def nonneighbors(self, vertex):
        c = 0
        l = set()
        for i in self.graph[vertex]:
            if i is not 1 :
                l.add(c)
            c+=1   
        return l

    #the Bron-Kerbosch recursive algorithm
    def bron_kerbosch(self,r,p,x,depth=0):
        #print current options
        print "  "*depth, list(r), list(p), list(x)
        if len(p) == 0:
            if len(x) == 0:
                print "maximal clique:", list(r)
            else:
                print "NO OUTPUT:", list(r), list(p), list(x)
                self.print_graph(self.graph)
            return

        pivot = self.findpivot(r,p,x)
        nn = self.nonneighbors(pivot)
        print "pivot: %i" % pivot

        for vertex in p & nn:
            r_new = set(r)
            r_new.add(vertex)
            p_new = p & self.neighbors(vertex) # p intersects neighbors(vertex)
            x_new = x & self.neighbors(vertex) # x intersects neighbors(vertex)
            self.bron_kerbosch(r_new,p_new,x_new,depth+1)
            p.remove(vertex)
            x.add(vertex)

    def findpivot(self,r,p,x):
        '''Finds a pivot vertex for the Tomita-Tanaka-Takahashi version of the Bron-Kerbosch algorithm.
        The optimal pivot vertex minimizes the size of p intersect non-neighbors of the pivot.'''

        choices = p|x
        if not choices:
            return choices
        minval = len(self.graph)+1
        min_choice = None

        for choice in choices:
            nonneighbors = self.nonneighbors(choice)
            if len(nonneighbors) < minval:
                minval = len(nonneighbors)
                min_choice = choice

        return min_choice

    def print_graph(self, graph=None):
        if graph is None:
            graph = self.graph

        print '\n'.join([' '.join([str(col) for col in row]) for row in graph])

    def graph_permutations(self, nnodes, nperms=200):
        '''Graph generator'''
        import random

        for i in range(nperms):
            #first generate one triangle of the graph
            graph = []
            for j in range(nnodes):
                graph.append([int(random.random() + 0.5) if k > j else 0 for k in range(nnodes)])

            #make some checks to make sure its a worthwhile graph
            if sum([sum(l) for l in graph]) < nnodes - 1:
                continue

            #BFS to ensure connectedness
            '''else:
                visited = [0]*nnodes
                visited[0] = 1
                q = []
                q.append(0);
                
                while len(q):
                    node = q[0]
                    q = q[1:]

                    for i in self.graph[node]:
                        '''

            #mirror over the graph
            for row in range(nnodes-1): #skip the last, it has nothing new
                for idx in reversed(range(nnodes)[row+1:]):
                    graph[idx][row] = graph[row][idx]

            yield graph

    def explore_space(self):
        nnodes = 5

        for graph in self.graph_permutations(nnodes):
            self.graph = graph
            self.run()
            
            print
            print '='*100
            print
        
if __name__ == '__main__':
    '''
    graph = [[0,1,0,0,1,0],
             [1,0,1,0,1,0],
             [0,1,0,1,0,0],
             [0,0,1,0,1,1],
             [1,1,0,1,0,0],
             [0,0,0,1,0,0]]
    '''
    
    '''graph = [[0,1,0,0,0,0],
             [1,0,1,1,1,1],
             [0,1,0,0,0,1],
             [0,1,0,0,1,1],
             [0,1,0,1,0,1],
             [0,1,1,1,1,0]]
    '''
    bronk = BronKerbosch()
    bronk.explore_space()
