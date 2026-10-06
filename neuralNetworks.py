import numpy as np

class nNetwork():
    def __init__(self, shape, weights = None, biases = None):
        
        self.shape = shape
        self.neurones = []
        self.weights = []
        self.biases = []
        for i in range(len(shape) - 1):
            self.weights.append(np.random.uniform(-0.99900000,0.99900000,(shape[i+1], shape[i])))
            self.biases.append(np.random.uniform(-0.99900000,0.99900000,shape[i+1]))
            self.neurones = [np.zeros(s) for s in shape]

            
        if weights:
            self.weights = weights
        if biases:
            self.biases = biases


    def feedForward(self,a):
        for b, w in zip(self.biases,self.weights):
            
            a = sigmoid(np.dot(w,a) + b)
        return a[0]

    def evolve(self, numOffspring,change):
        offspring = []
        for _ in range(numOffspring-1):
            newWeights = []
            newBiases = []
            for w in self.weights:
                #print(w)
                #mutated = w# + #np.random.uniform(-0.000, 0.000, w.shape)
                #mutated = w + np.arange()
                newWeights.append(w+np.random.uniform(-change, change, w.shape))
            for b in self.biases:
                newBiases.append(b + np.random.uniform(-change, change, b.shape))

            offspring.append(nNetwork(self.shape, newWeights, newBiases))

        offspring.append(self)
        return offspring





newNet = nNetwork([5,4,1])


def sigmoid(vector):
    return 1 / (1 + np.exp(-vector))


