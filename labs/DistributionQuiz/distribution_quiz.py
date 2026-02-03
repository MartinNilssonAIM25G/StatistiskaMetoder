import matplotlib.pyplot as plt
import numpy as np
from numpy.random import default_rng

class DistributionQuiz:
    def __init__(self):
        self.rng = default_rng()
        self.score = 0
        self.streak = 0
        self.distribution = {
            '1': ('Normal', self.generate_normal),
            '2': ('Uniform', self.generate_uniform),
            '3': ('Binominal', self.generate_binomial),
            '4': ('Negative binominal', self.generate_negative_binominal),
            #'5': ('Gamma', self.generate_gamma),
            '6': ('Geometric', self.generate_geometric)
        }

    def generate_normal(self, samples=1000):
        mu = self.rng.uniform(-5, 5)
        stigma = self.rng.uniform(0.8, 2)
        return self.rng.normal(mu, stigma,samples)

    def generate_uniform(self, samples=1000):
        a = self.rng.uniform(0, 50)
        b = a + self.rng.uniform(10, 50)
        return self.rng.uniform(a, b, samples)
    
    def generate_binomial(self, samples=1000):
        n = self.rng.integers(10, 100)     
        p = self.rng.uniform(0.1, 0.9)      
        return self.rng.binomial(n, p, samples)

    def generate_geometric(self, samples=1000):
        p = self.rng.uniform(0.05, 0.3)
        return self.rng.geometric(p, samples)
    
    def generate_negative_binominal(self, samples=1000):
        n = self.rng.integers(3, 15)
        p = self.rng.uniform(0.2, 0.8)
        return self.rng.negative_binomial(n, p, samples)

    #def generate_gamma(self, samples=1000):
        shape = self.rng.uniform(0.5, 8)
        scale = self.rng.uniform(0.5, 3)
        return self.rng.gamma(shape, scale, samples)
    
    def show_distribution(self, data, show_type='histogram'):
        plt.figure(figsize=(12, 6))
        if show_type == 'histogram':
            plt.hist(data, bins=30, edgecolor="black")
        elif show_type == 'ogive':
            hist, edges = np.histogram(data, bins=40)
            cdf = np.cumsum(hist) / np.sum(hist)
            plt.plot(edges[1:], cdf)

        plt.show(block=False)
        plt.pause(0.1)         
