# -*- coding: utf-8 -*-
"""
Created on Sun May 10 16:16:10 2020

@author: josep
"""
from math import log
from queue import Queue
from pandas import DataFrame, read_csv

# Entropy Driven Decision Tree
#   1. Compute the Entropy for the entire Dataset (Entropy(S))
#   2. For every attribute/Feature:
#       1. Calculate Entropy for all other attributes (Entropy(A))
#       2. Take Average Information Entropy for the Current Attribute
#       3. Calculate Gain for the current Attribute
#   3. Pick the highest Gain Attribute
#   4. Repeat until the tree is finished.        
class Node:
    def __init__(self, layer, attribute = '', type_ = ''):
        
        # Nodes beneath this one.
        self._children = []
        # The attribute that represents a destination node. Can be yes or no, for example.
        self._attribute = attribute
        self._type = type_ # What was the if ____, then attribute? the type.
        
        self._layer = layer # for formatting
        
    def add_child(self, child):
        self._children.append(child)
        
    # Goes and finds the node in the tree and returns the associated prediction or rejects the result
    def predict(self, dataset):
        node = self
        while len(node._children):
            didnt_find_node = True
            for child in node._children:
                if child._type in dataset:
                    node = child
                    didnt_find_node = False
                    break
            if didnt_find_node:
                return 'no'
        return node._attribute
    
    def __repr__(self):
        # layer by layer traversal and printing of tree
        node = self
        repr_str = ''
        curlayer = 0
        queue = Queue()
        queue.put(node)
        while not queue.empty():
            node = queue.get()
            for child in node._children:
                queue.put(child)
            if node._layer != curlayer:
                repr_str += '\n'
                curlayer += 1
            repr_str += " " + str(("ATRR: " + node._attribute, "FRM: " + node._type))
        return repr_str


'''
id3 splits the tree whenever there is entropy to be found. Concepts are reflected by pure nodes.
Returns single node capable of making predictions.
'''        
def id3(dataset, outcome_label, truth_value = 'yes', false_value = 'no', layer = 0):
    #  Calculate entropy from dataset
    n_dataset = dataset.shape[0]
    pos_dataset = list(dataset[outcome_label] == truth_value).count(True)
    dataset_entropy = entropy(n_dataset, pos_dataset)
    
    # if there isn't any entropy left in the dataset, don't split. This is a finish node
    if dataset_entropy == 0:
        return Node(layer, attribute = (truth_value if pos_dataset != 0 else false_value))
    # Otherwise, split!!!!!
    node = Node(layer) # Come back to me
    best_attribute, max_gain = None, 0
    
    # Find the gainiest node
    for attribute in dataset.columns:
        if attribute == outcome_label:
            continue
        gain = calculate_gain_from_attribute(dataset_entropy,
                                             compute_average_information_entropy_attribute(
                                                     dataset, attribute, outcome_label, truth_value))
        if gain > max_gain:
            best_attribute, max_gain = attribute, gain
    node._attribute = best_attribute
    #( if the gain is never > than 0, don't split and just return 1 partitoin)
    if max_gain == 0:
        return Node(layer, attribute = (truth_value if pos_dataset != 0 else false_value))
    # We found the gainiest node. Now, we make the subnodes.
    types_ = get_types_from_attribute(dataset, best_attribute)
    for type_ in types_:
        new_node = id3(dataset.loc[dataset[best_attribute] == type_,:], outcome_label, truth_value, layer=layer+1)
        new_node._type = type_
        node.add_child(new_node)
    # And return our node with its children in its backpack!
    return node

# Entropy function for decision tree
def entropy(num_entries, num_positive):
    if num_positive == num_entries or num_positive == 0:
        return 0
    pos_prob = num_positive/num_entries
    neg_prob = 1-pos_prob
    return -pos_prob*log(pos_prob, 2) - neg_prob*log(neg_prob,2)

# When finishing this development, make sure when you call this function, give the truth value
    # "yes" or "no" to work with the tennis dataset.
def compute_entropy_for_attribute_types(dataset, attribute, outcome_label, truth_value=True, false_value='no'):
    types = get_types_from_attribute(dataset, attribute)
    entropies = DataFrame(columns=['p','N','entropy'])
    for type_ in types:
        slice_ = slice_for_attribute_type_and_value(dataset, attribute, type_, outcome_label)
        entropies.loc[type_, 'p'] = list(slice_[outcome_label] == truth_value).count(True)
        #print(slice_[type_].value_counts())
        #.loc[truth_value, 1] # Get the count of the positive outcomes
        entropies.loc[type_, 'N'] = slice_[attribute].shape[0] # get the number of entries of the type
        entropies.loc[type_, 'entropy'] = entropy(entropies.loc[type_, 'N'],
                     entropies.loc[type_, 'p'])
    return entropies

# Helper function that calculates average information from the entropy of an attribute.
def compute_average_information_entropy_attribute(dataset, attribute, outcome_label, truth_value='yes', false_value = 'no'):
    types = get_types_from_attribute(dataset, attribute)
    entropies = compute_entropy_for_attribute_types(dataset, attribute, outcome_label, truth_value, false_value)
    average_information_entropy = 0
    n_dataset = dataset.shape[0] # number of entries in whole dataset
    for type_ in types:
        average_information_entropy += entropies.loc[type_, 'N']/n_dataset*entropies.loc[type_, 'entropy']
    return average_information_entropy

# self explanatory
def calculate_gain_from_attribute(dataset_entropy, average_information_attribute):
    return dataset_entropy - average_information_attribute

# Helper function for entropy calculations
def slice_for_attribute_type_and_value(dataset, attribute, attribute_type, result):
    return dataset.loc[dataset[attribute]==attribute_type, [attribute, result]]

# Helper function for type analysis
def get_types_from_attribute(dataset, attribute):
    return set(dataset[attribute])

# LOO- Cross-checking accuracy checking
def compute_accuracy(dataset, outcome_label, truth_value='yes', false_value = 'no'):
    successes = 0
    for trial in range(dataset.shape[0]):
        train = dataset.drop(trial, axis=0)
        test = dataset.loc[trial, :]
        
        tree = id3(train, outcome_label, truth_value, false_value)
        
        prediction = tree.predict({attribute for attribute in test} - {outcome_label})
        print('Test: ' + str(list(test)), 'Predicted: ' + str(prediction), 'actual: ' + test[outcome_label])
        successes += 1 if tree.predict({attribute for attribute in test} - {outcome_label}) == test[outcome_label] else 0
        
    print(tree)
    return successes / dataset.shape[0]
        
''' USAGE 

run id3 with training data, the label of the column of the decision for reach row, the positive decision value, and the negative decision value to get a tree node.
Otherwise, just run compute accuracy to get results
'''

def main():
    filename = 'pets.txt'
    data = read_csv(filename, delimiter = '\t')
    return compute_accuracy(data, 'iscat','yes', 'no')

if __name__ == '__main__':
    res = main()