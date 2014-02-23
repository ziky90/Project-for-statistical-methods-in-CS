import random

class Graph:
        
    def __init__(self, matrix, nodes):
        """
        constructor saving the graph twice is speed for memory tradeof
        """
        self.matrix = matrix
        self.nodes = nodes
        self.switches = self.setSwitches(len(matrix))


    def setSwitches(self, len):
        result = []
        for i in range(len):
            use = random.choice(['L', 'R'])
            result.append(use)
            self.nodes[i].switch = use
        return result

    def oppositeConnection(self, v, e):
        """
        function that returns the oposite connection
        """
        if e == 'O':
            e = '0'
        connections = self.adjecents(v)
        for connection in connections:
            for edge in connection[1]:
                if edge == e:
                    return (connection[0], self.invertedDirection(v, connection[0], edge))
    
    def invertedDirection(self, v1, v2, e):
        """
        function to get the inverted direction of the edge 
        """
        pos = self.matrix[v2][v1]
        return pos[self.matrix[v1][v2].index(e)]
    
    def to(self, v, e):
        """
        function to find the end of the connection
        """
        return self.nodes[v].adjecents[e]

    def adjecents(self, v):
        """
        function to return all the adjecent nodes in the graph
        """
        result = []
        for key in self.nodes[v].adjecents.keys():
            result.append((self.nodes[v].adjecents[key], key))
        return result
        
    def generateStates(self):
        """
        function to generate all the possible states of the HMM
        """
        result = []
        for v in range(len(self.matrix)):
            for e in self.adjecents(v):
                if self.matrix[v][e[0]] != 0:
                    result.append((v, e))
        return result


    def addObservation(self, observation):
        """
        observations setter for the Graph object
        """
        self.observation = observation

    def dp(self, v1, e, sigma, p):
        """
        dynamic programming as it was described in the assignment description
        """
        #return self.dodp(v1, e, sigma, len(sigma)-1, p)
        edge = e[1]
        probability = 1.0/len(self.observation)
        rewobs = reversed(self.observation)
        for o in rewobs:
            if edge == '0':
                be = ['L', 'R'][sigma[v1] == 'L']     
            else:
                be = '0'
            if o == edge or (o == 'O' and edge == '0'):
                probability = probability*p/2
            else:
                probability = probability*(1-p)
            v2 = self.to(v1, be)
            edge = self.invertedDirection(v1, v2, be)
            v1 = v2
        return probability

    def dodp(self, v, e, sigma, t, p):
        """
        dynamic programming slower oo representation based computation using recursion old version
        """
        if t == 0:
            return 1.0/(len(self.matrix))*3
        elif self.observation[t] == '0' or 'O':
            v1 = self.to(v,'L')
            v2 = self.to(v,'R')
            if sigma[t] == '0':
                return (self.dodp(v1, 'L', sigma, t-1, p) + self.dodp(v2, 'R', sigma, t-1, p))*(1-p)
            else:
                return (self.dodp(v1, 'L', sigma, t-1, p) + self.dodp(v2, 'R', sigma, t-1, p))*p
        else:
            v1 = self.to(v,'0')
            if sigma[t] == self.observation[t]:
                return self.dodp(v1, '0', sigma, t-1, p)*(1-p)
            else:
                return self.dodp(v1, '0', sigma, t-1, p)*p

    
    def next(self, v1, e1):
        v2, e2 = self.oppositeConnection(v1, e1)
        if e2 == '0' or e2 == 'O':
            if self.switches[v2] == 'L':
                if random.random() < 0.05:
                    return v2, random.choice(['R','O','0'])
                else:
                    return v2, 'L'
            else:
                if random.random() < 0.05:
                    return v2, random.choice(['L','O','0'])
                else:
                    return v2, 'R'
        elif self.switches[v2] == 'L':
            if random.random() < 0.05:
                return v2, random.choice(['R','L','0'])
            else:
                return v2, 'O'
        else:
            if random.random() < 0.05:
                return v2, random.choice(['R','L','O'])
            else:
                return v2, '0'
            
class Node:
    """
    class that represents the node in the Graph for the OO based representation
    """
    def __init__(self):
        self.adjecents = {}
        self.switch = 'X'



def graphFromMatrix(matrix):
    """
    method for the creation of the graph
    """
    nodes = []
    for i in range(len(matrix)):
        nodes.append(Node())
    for i in range(len(matrix)):
        for (index, connection) in enumerate(matrix[i]):
            if connection != 0:
                for c in connection:
                    nodes[i].adjecents[c] = index

    return Graph(matrix, nodes)