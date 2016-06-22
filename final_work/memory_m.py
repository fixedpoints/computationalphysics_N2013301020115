import math
import numpy as np
import matplotlib.pyplot as plt

#calculate J(i,j)
def connection(pattern,i,j,row):
    return pattern[i//row, i%row] * pattern[j//row, j%row]

#calculate the sum of J(i,j)(m) in m
def connection_mean(pattern,i,j,row):
    m = len(pattern)
    return np.mean([connection(pattern[p],i,j,row) for p in range(m)])

#calculate the energy of the network
def energy(connection,sample):
    row = sample.shape[0]
    column = sample.shape[1]
    size = row * column
    energy_sum = 0
    for i in range(size):
        sample_i = sample[i//row, i%row]
        energy_sum += np.sum([connection[i*size + j] * 
            sample_i * sample[j//row,j%row] 
            for j in range(size)])
    return -energy_sum

#simulate the memory process
class Memory(object):
    def __init__(self,pattern):
        self.pattern = pattern
        self.row = pattern[0].shape[0]
        self.column = pattern[0].shape[1]
        self.size = np.prod(pattern[0].shape)
        self.connection_ = [connection_mean(pattern,i,j,self.row) \
                for i in range(self.size) \
                for j in range(self.size)]

    def damage_con(self,n):
        num = len(self.connection_)
        pos = np.random.choice([p for p in range(num)],size=n,replace=0)
        for i in pos:
            self.connection_[i] = 0

#Monte Carlo method
    def monte(self,sample,step):
        row = self.row
        column = self.column
        size_ = row * column
        for _ in range(step):
            pos = np.random.randint(size_,size=3*size_)
            for i in pos:
                sample_flip = sample.copy()
                sample_flip[i//row,i%row] = -sample_flip[i//row,i%row]
                if energy(self.connection_,sample_flip) - \
                        energy(self.connection_,sample) < 0:
                    sample[i//row,i%row] = -sample[i//row,i%row]
#when all s(i)=-s(i), the energy would not change.
#so the next condition is used to prevent this situation
#in my work, sample[7,3] should always be blank or its value is -1
        if sample[7,3] == 1:
            sample *= -1
        return sample

#randomly flip the state of sample
def damage(sample,n):
    row = sample.shape[0]
    num = np.prod(sample.shape)
    pos = np.random.choice([p for p in range(num)],size=n,replace=0)
    for i in pos:
        sample[i//row,i%row] *= -1

#plot the network
def pattern_plot(sample):
    pos = np.argwhere(sample==1)
    pos = pos.T
    plt.clf()
    plt.scatter(pos[1],-pos[0])
    plt.show()

a_pattern = np.array([[-1,-1,-1,-1,1,1,-1,-1,-1,-1],\
                        [-1,-1,-1,1,1,1,1,-1,-1,-1],\
                        [-1,-1,1,1,-1,-1,1,1,-1,-1],\
                        [-1,1,1,-1,-1,-1,-1,1,1,-1],\
                        [-1,1,1,1,1,1,1,1,1,-1],\
                        [1,1,1,1,1,1,1,1,1,1],\
                        [1,1,1,-1,-1,-1,-1,1,1,1],\
                        [1,1,-1,-1,-1,-1,-1,-1,1,1],\
                        [1,1,-1,-1,-1,-1,-1,-1,1,1],\
                        [1,1,-1,-1,-1,-1,-1,-1,1,1]])

c_pattern = np.array([[-1,1,1,1,1,1,1,1,1,1],\
                    [1,1,1,1,1,1,1,1,1,1,],\
                    [1,1,1,-1,-1,-1,-1,-1,-1,-1],\
                    [1,1,-1,-1,-1,-1,-1,-1,-1,-1],\
                    [1,1,-1,-1,-1,-1,-1,-1,-1,-1],\
                    [1,1,-1,-1,-1,-1,-1,-1,-1,-1],\
                    [1,1,-1,-1,-1,-1,-1,-1,-1,-1],\
                    [1,1,1,-1,-1,-1,-1,-1,-1,-1],\
                    [1,1,1,1,1,1,1,1,1,1,],\
                    [-1,1,1,1,1,1,1,1,1,1]])

t_pattern = np.array([[1,1,1,1,1,1,1,1,1,1],\
                    [1,1,1,1,1,1,1,1,1,1],\
                    [-1,-1,-1,-1,1,1,-1,-1,-1,-1],\
                    [-1,-1,-1,-1,1,1,-1,-1,-1,-1],\
                    [-1,-1,-1,-1,1,1,-1,-1,-1,-1],\
                    [-1,-1,-1,-1,1,1,-1,-1,-1,-1],\
                    [-1,-1,-1,-1,1,1,-1,-1,-1,-1],\
                    [-1,-1,-1,-1,1,1,-1,-1,-1,-1],\
                    [-1,-1,-1,-1,1,1,-1,-1,-1,-1],\
                    [-1,-1,-1,-1,1,1,-1,-1,-1,-1]])