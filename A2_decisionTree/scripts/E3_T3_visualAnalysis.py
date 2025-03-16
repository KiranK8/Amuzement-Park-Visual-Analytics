"""Code for exercise 3, task 3."""

import numpy as np
import pandas as pd
from pandas.api.types import CategoricalDtype

# graphviz for tree drawing
import graphviz

# scikit-learn for decision tree classification and evaluation
from sklearn import tree
from sklearn.tree import export_graphviz
from sklearn.model_selection import cross_val_score
from sklearn.metrics import classification_report

# load the data and make a copy with numerical entries only
df = pd.read_csv('../data/adult.csv', na_values='?').dropna()

# print the code for the education
display(df[['education', 'education-num']].drop_duplicates().sort_values(['education-num']))

df.drop(['fnlwgt', 'education'], axis=1, inplace=True)

for i in list(df):
    if not (df[i].dtype == np.float64 or df[i].dtype == np.int64):
        # define a specific order for race
        if 'race' in i:
            cat_type = CategoricalDtype(categories=[
              'Amer-Indian-Eskimo', 'Asian-Pac-Islander', 'Black', 'Other', 'White'], ordered=True)
            df[i] = df[i].astype(cat_type)
        else:
            df[i] = df[i].astype('category')
        df[i] = df[i].cat.codes
        
# select the data
datasub = df
# you can descend in the tree by selecting respective data
#datasub = df[df.relationship >1]
X = datasub.iloc[:,0:-1]
Y = datasub.iloc[:,-1]

clf = tree.DecisionTreeClassifier(criterion="entropy", max_leaf_nodes=20)
clf = clf.fit(X, Y)

# compute dot layout of tree
rawdot = export_graphviz(clf, out_file=None, feature_names=X.columns, 
                         class_names=['<=50k', '>50k'], filled=True)#, proportion=True)
# scale the nodes
rawdot = rawdot[:15] + 'graph [size="10"];' + rawdot[15:]

# render the tree
display(graphviz.Source(rawdot).render('../E3-figures/decisionTree_manual', format='png'))

'''
display(graphviz.Source(digraph Tree {
node [shape=box];
graph [ranksep=.75, size="7 3"];
0 [label="Do you intend\n to get married?"];
1 [label="Will you go\n to college?", style=filled, fillcolor="red"]; 0 -> 1 [labeldistance=3, labelangle=45, headlabel="yes"];
2 [label="Your capital gain:"]; 0 -> 2 [labeldistance=3, labelangle=-45, headlabel="no"];
3 [label="?", style=filled, fillcolor="red"]; 2 -> 3 [labeldistance=3, labelangle=45, headlabel="<=7000"];
6 [label="Your chances\n are high!", style=filled, fillcolor="green"]; 2 -> 6 [labeldistance=3, labelangle=-45, headlabel=">7000"];
}).render('E3-figures/decisionTree_manual', format='png')
'''
# write to file: graphviz.Source(...).render('E3-figures/decisionTree_manual', format='png')