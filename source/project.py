import random
import pylab as pl
import graph as gr


p = 0.05


def generateSequence(g, length):
    """
    function for generating the observed sequence with respect to the given graph
    """
    v_from = random.randint(0, len(g.matrix) - 1)
    labels = ('O','0','L','R')      #O stands for L0, 0 for R0, L for 0L and R for 0R 
    e_from = random.choice(labels)
    o = [0] * length
    for i in range(length):
        v_from, e_from = g.next(v_from, e_from)
        if random.random() <= p:
            o[i] = random.choice([ l for l in labels if l != o[i] ])
        else:
            o[i] = e_from    
    return o, v_from



def updateSigma(sigma, g):
    """
    function for updating of all the sigmas
    """
    pos = random.randint(0, len(g.matrix) - 1)
    if sigma[pos] == 'L':
        sigma[pos] = 'R'
    else:
        sigma[pos] = 'L'
    return sigma
    

def mcmc(g, v, e, samplesNo):
    """
    MCMC implemntation as metropolis hastings
    """
    sigma = ''.join(random.choice('LR') for x in range(len(g.matrix)))
    sigma = list(sigma)
    sigmas = ['x']*samplesNo
    pts = [0.0]*samplesNo
    psigma = g.dp(v, e, sigma, p)
    for i in range(samplesNo):
        cont = True
        while cont:
            sigmaPrime = updateSigma(sigma, g)
            psigmaPrime = g.dp(v, e, sigmaPrime, p)
            pts[i] = psigmaPrime
            a = psigmaPrime / psigma
            if  random.random() <= a or a >= 1:
                sigma, psigma = sigmaPrime, psigmaPrime
                sigmas[i] = sigma
                pts[i] = psigma
                cont = False            
    return sigmas, pts


def sampler(g, ns, bi):
    """
    function for sampling
    """
    sample = []
    probs = []
    for v, e in g.generateStates():
        sigmas, pts = mcmc(g, v, e, (ns + bi) / (len(g.matrix) * 3))
        probs.extend(pts[bi / (len(g.matrix) * 3)::1])
        sample.extend(sigmas[bi / (len(g.matrix) * 3)::1])
    return sample, probs




def sumDP(g, sigma):
    """
    function that sums out all the states and computes observation probability
    """    
    return sum([g.dp(v, e, sigma, p) for (v, e) in g.generateStates()])
    
    



def posterior(v, e, g, ns, bi):
    """
    function to compute posterior probablity for the state given graph and observation
    """
    sigmas, pt = sampler(g, ns, bi)
    result = []
    for i in range(len(sigmas)):
      result.append(g.dp(v, e, sigmas[i], p) * pt[i] / sumDP(g, sigmas[i]))
    return sum(result), pt


def plotAll(g, ns, bi):
    """
    function for ploting all the states
    """
    for v, e in g.generateStates():
        pr = [0.0]*ns        
        for i in range(bi):
            tmp, probabilities = mcmc(g, v, e, ns)
            for j in range(ns):
                pr[j] += probabilities[j]
        result = []
        for prob in pr:
            result.append(prob/ns)        
        pl.semilogy(result) 
    pl.xlabel('samples')
    pl.ylabel('probability')
    pl.grid(True)    
    pl.show()
    
def plotOne(g, ns, bi, v, e):
    pr = [0.0]*ns        
    for i in range(bi):
        tmp, probabilities = mcmc(g, v, e, ns)
        for j in range(ns):
            pr[j] += probabilities[j]
    result = []
    for prob in pr:
        result.append(prob/ns)  
    pl.semilogy(result)
    pl.xlabel('samples')
    pl.ylabel('probability')
    pl.grid(True)    
    pl.show()

def plotTraceAll(cvg):
    for pr in cvg:
        result = []
        for prob in cvg:
            result.append(prob)
        pl.semilogy(result)
    pl.xlabel('samples')
    pl.grid(True)    
    pl.show() 

def plotTraceBest(cvg):
    result = []
    for prob in cvg:
        result.append(prob)
    pl.semilogy(result)
    pl.xlabel('samples')
    pl.grid(True)    
    pl.show()    
    
"""running the program"""  
samples = 500
burnin = 200


matrix = ((0, '0', 0, 'R', 'L', 0, 0, 0, 0, 0),
          ('0', 0, 'L', 0, 0, 0, 0, 0, 'R', 0),
          (0, 'L', 0, 0, 0, 'R', 0, '0', 0, 0),
          ('R', 0, 0, 0, 0, 0, '0', 0, 0, 'L'),
          ('0', 0, 0, 0, 0, 0, 'L', 'R', 0, 0),
          (0, 0, '0', 0, 0, 0, 0, 0, 'L', 'R'),
          (0, 0, 0, 'L', '0', 0, 0, 0, 0, 'R'),
          (0, 0, 'L', 0, '0', 0, 0, 0, 'R', 0),
          (0, 'R', 0, 0, 0, 'L', 0, '0', 0, 0),
          (0, 0, 0,'L', 0, 'R', '0', 0, 0, 0),)

"""
matrix = ((0, '0', 0, 0, 0, 0, 0, 0, 'R', 'L', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
          ('R', 0, 'L', 0, 0, 0, 0, 0, 0, 0, '0', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
          (0, '0', 0, 'L', 0, 0, 0, 0, 0, 0, 0, 'R', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
          (0, 0, '0', 0, 'L', 0, 0, 0, 0, 0, 0, 0, 'R', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
          (0, 0, 0, 'R', 0, '0', 0, 0, 0, 0, 0, 0, 0, 'L', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
          (0, 0, 0, 0, 'L', 0, 'R', 0, 0, 0, 0, 0, 0, 0, '0', 0, 0, 0, 0, 0, 0, 0, 0, 0),
          (0, 0, 0, 0, 0, '0', 0, 'R', 0, 0, 0, 0, 0, 0, 0, 'L', 0, 0, 0, 0, 0, 0, 0, 0),
          (0, 0, 0, 0, 0, 0, '0', 0, 'L', 0, 0, 0, 0, 0, 0, 'R', 0, 0, 0, 0, 0, 0, 0, 0),
          ('L', 0, 0, 0, 0, 0, 0, 'R', 0, 0, 0, 0, 0, 0, 0, 0, '0', 0, 0, 0, 0, 0, 0, 0),
          ('0', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'L', 'R', 0, 0, 0, 0, 0, 0),
          (0, 'L', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '0', 'R', 0, 0, 0, 0, 0),
          (0, 0, 'R', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '0', 'L', 0, 0, 0, 0),
          (0, 0, 0, 'L', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'R', '0', 0, 0, 0),
          (0, 0, 0, 0, 'R', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'L', '0', 0, 0),
          (0, 0, 0, 0, 0, 'L', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '0', 'R', 0),
          (0, 0, 0, 0, 0, 0, 'L', 'R', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '0'),
          (0, 0, 0, 0, 0, 0, 0, 0, '0', 'L', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'R'),
          (0, 0, 0, 0, 0, 0, 0, 0, 0, 'L', '0', 0, 0, 0, 0, 0, 0, 0, 'R', 0, 0, 0, 0, 0),
          (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'R', 'L', 0, 0, 0, 0, 0, '0', 0, 0, 0, 0, 0, 0),
          (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'L', 'R', 0, 0, 0, 0, 0, 0, 0, '0', 0, 0, 0),
          (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'L', 'R', 0, 0, 0, 0, 0, '0', 0, 0, 0, 0),
          (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '0', 'L', 0, 0, 0, 0, 0, 0, 0, 'R', 0),
          (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '0', 0, 0, 0, 0, 0, 0, 'L', 0, 'R'),
          (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'R', 'L', 0, 0, 0, 0, 0, '0', 0),)
"""
    
observationLength = 15
graph = gr.graphFromMatrix(matrix)
o, start = generateSequence(graph, observationLength)
print o
graph.addObservation(o)        
probabilities = []
convergences = []
states = [ (start, e) for (start, e) in graph.generateStates() ]
    
for start, e in states:
    pr, cvg = posterior(start, e, graph, samples, burnin)
    convergences.append(cvg)
    probabilities.append(pr)
    print "probability:: [", start, e[1], "] =", pr

indexMax = probabilities.index(max(probabilities))
    
print "most probable state:", states[indexMax], "posterior:", probabilities[indexMax]
    
plotAll(graph, samples, burnin)
plotOne(graph, samples, burnin, states[indexMax][0], states[indexMax][1])
plotTraceAll(convergences)
plotTraceBest(convergences[indexMax])