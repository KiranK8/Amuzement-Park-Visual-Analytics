"""Code for exercise 2, task 1."""

import numpy as np
import pandas as pd

# graphviz for tree drawing
import graphviz

# scikit-learn for decision tree classification and evaluation
from sklearn import tree
from sklearn.tree import export_graphviz
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score, classification_report

# load the data and make a copy with numerical entries only
df = pd.read_csv('../data/adult.csv', na_values='?').dropna()
df.drop(['fnlwgt'], axis=1, inplace=True)

datasetnum = df.copy()
datasetnum.drop(['education'], axis=1, inplace=True)

for i in list(datasetnum):
    if not (datasetnum[i].dtype == np.float64 or datasetnum[i].dtype == np.int64):
        datasetnum[i] = datasetnum[i].astype('category')
        datasetnum[i] = datasetnum[i].cat.codes
        

def num_features(clf, df):
    """Compute the number of distinct features used by the decision tree.
    
    Args:
        clf: A scikit-learn DecisionTreeClassifier
        
    Returns:
        int: The number of unique features used by the decision tree.    
    """
    
    # get all features used in the tree
    treefeatures = list(filter(lambda a: a != -2, clf.tree_.feature))
    
    # find unique features and their names
    uniquef = set([df.columns[a] for a in treefeatures])
    print(sorted(uniquef))
    
    return len(uniquef)
    

# Train a classifier with a all given data and compute accuracy
X = datasetnum.iloc[:,0:-1]
Y = datasetnum.iloc[:,-1]
clf = tree.DecisionTreeClassifier()
clf = clf.fit(X,Y)
acc = accuracy_score(clf.predict(X),Y)
tree_size = clf.tree_.node_count
num_features_used= num_features(clf, X)

print('Accuracy on training data:', acc) # TODO
print('Size of tree:', tree_size, 'nodes') # TODO
print('Number of features:', num_features_used) # TODO


# print the classification report
target_names = df.income.astype('category').cat.categories
print('Classification report:')
print(classification_report(clf.predict(X),Y, target_names=target_names))


# Create a decision tree classifier with a subset of the data 
# and do cross-validation to determine accuracy 
clf = tree.DecisionTreeClassifier()
scores = cross_val_score(clf, X, Y, cv=10)
print('Accuracy: %0.2f (+/- %0.2f)' % (scores.mean(), scores.std() * 2))

# Train a classifier limited to 20 leaf nodes
clf_pruned = tree.DecisionTreeClassifier(max_leaf_nodes=20, random_state=42)
clf_pruned.fit(X, Y)

# Accuracy on the training data for the pruned tree
acc_pruned = accuracy_score(clf_pruned.predict(X), Y)
print('Accuracy on training data (pruned to 20 leaf nodes):', acc_pruned)

# Cross-validation accuracy for the pruned tree
scores_pruned = cross_val_score(clf_pruned, X, Y, cv=10)
print('Cross-validation accuracy (pruned tree): %0.2f (+/- %0.2f)' % (scores_pruned.mean(), scores_pruned.std() * 2))
