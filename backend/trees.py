# This file holds the class to make a basic decision tree for classication
# Utilized in my proprietary gradient boosted trees algorithm

import numpy as np
from collections import Counter

# Default Parameters
DEPTH = 5
SAMPLES = 20

class TreeNode:
    def __init__(self, feature=None, left=None, right=None, threshold=None, gain=None, classification=None):
        self.feature_index: int = feature
        self.threshold: float = threshold
        self.left: TreeNode = left 
        self.right: TreeNode = right
        self.gradient = 0
        self.hessian = 0
        self.gain = gain
        self.classification = classification 


    
class Tree:
    def __init__(self, min_sample = SAMPLES, max_depth = DEPTH):
        self.root: TreeNode = None

        # Stopping Conditions
        self.min_sample = min_sample
        self.max_depth = max_depth

    def make_tree(self, X, Y, depth):

        # n: Amount of features
        # m: Amount of games
        n, m = np.shape(X)

        if m > self.min_sample and depth < self.max_depth:

            best_split = self.split(X, Y, m, n)
            
            if best_split['gain'] > 0:

                left = self.make_tree(best_split['X_left'], best_split['Y_left'], depth+1)
                right = self.make_tree(best_split['X_right'], best_split['Y_right'], depth+1)

                return TreeNode(best_split['f'], best_split['t'], left, right, best_split['gain'])

            leaf = self.get_leaf(Y)
            return TreeNode(classification=leaf)


    def split(self, X, Y, m, n):

        info = {}
        max_gain = -float('inf')

        for f in range(n):
            feature_values = []
            for i in range(m):
                feature_values.append(X[i][f])
            feature_set = set(feature_values)
            for t in feature_set:
                X_left, X_right, Y_left, Y_right = self.cut(X, f, t)
                if len(X_left) > 0 and len(X_right) > 0:
                    gain = self.get_gain(Y, Y_left, Y_right)
                    if gain > max_gain:
                        info['f'] = f
                        info['t'] = t
                        info['X_left'] = X_left
                        info['Y_left'] = Y_left
                        info['X_right'] = X_right
                        info['Y_right'] = Y_right
                        info['gain'] = gain
                        max_gain = gain
        return info
    


    def cut(self, X, Y, f, t):
        X_left = [row for row in X if row[f] <= t]
        X_right = [row for row in X if row[f] > t]
        Y_left = [Y[i] for i in range(len(X)) if X[i][f] <= t]
        Y_right = [Y[i] for i in range(len(X)) if X[i][f] > t]
        return X_left, X_right, Y_left, Y_right

    def get_gain(self, parent, left, right): 
        w_l = len(left) / len(parent)
        w_r = len(right) / len(parent)

        return self.gini(parent) - (w_l * self.gini(left) + w_r * self.gini(right))
    
    def gini(self, node: list[int]):
        labels = set(node)
        out = 0

        for l in labels:
            p_i = node.count(l) / len(node)
            out += (p_i * p_i)

        return 2* (1 - out)
    
    def get_leaf(self, Y):
        return Counter(Y).most_common(1)[0][0]
    
    def train(self, X, Y):
        self.root = self.make_tree(X, Y)

    def predict(self, X):
        return [self.guess(x, self.root) for x in X]
    
    def guess(self, x, node: TreeNode):
        if node.classification != None: return node

        v = x[node.feature_index]
        if v <= node.threshold:
            return self.guess(x, node.left)
        else:
            return self.guess(x, node.right)


    



