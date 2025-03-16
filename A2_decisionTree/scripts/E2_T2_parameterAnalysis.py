"""Code for exercise 2, task 2 using Bokeh for visualization and saving figures."""

import numpy as np
import pandas as pd
from bokeh.plotting import figure, output_notebook, show
from bokeh.io import export_png
from bokeh.models import ColumnDataSource, ColorBar, BasicTicker, PrintfTickFormatter
from bokeh.transform import linear_cmap
from bokeh.palettes import Spectral6
from sklearn import tree
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score

output_notebook()

# Load the data and make a copy with numerical entries only
df = pd.read_csv('../data/adult.csv', na_values='?').dropna()
df.drop(['fnlwgt'], axis=1, inplace=True)

datasetnum = df.copy()
datasetnum.drop(['education'], axis=1, inplace=True)

# Convert categorical variables to codes
for i in list(datasetnum):
    if not (datasetnum[i].dtype == np.float64 or datasetnum[i].dtype == np.int64):
        datasetnum[i] = datasetnum[i].astype('category')
        datasetnum[i] = datasetnum[i].cat.codes

# Define function to compute number of distinct features used by the decision tree
def num_features(clf, df):
    """Compute the number of distinct features used by the decision tree."""
    tree_features = list(filter(lambda a: a != -2, clf.tree_.feature))
    unique_features = set([df.columns[a] for a in tree_features])
    return len(unique_features)

# Prepare the data
X = datasetnum.iloc[:, 0:-1]
Y = datasetnum.iloc[:, -1]

# --- Analyze max_depth parameter ---
max_depth_range = range(1, 21)
training_accuracies_depth = []
cv_accuracies_depth = []
features_used_depth = []

for max_depth in max_depth_range:
    clf = tree.DecisionTreeClassifier(max_depth=max_depth, random_state=42)
    clf.fit(X, Y)
    
    train_accuracy = accuracy_score(Y, clf.predict(X))
    training_accuracies_depth.append(train_accuracy)
    
    cv_scores = cross_val_score(clf, X, Y, cv=10)
    cv_accuracies_depth.append(cv_scores.mean())
    
    feature_count = num_features(clf, X)
    features_used_depth.append(feature_count)

# Bokeh plot for max_depth
source_depth = ColumnDataSource(data=dict(
    max_depth=max_depth_range,
    training_accuracy=training_accuracies_depth,
    cv_accuracy=cv_accuracies_depth,
    features_used=features_used_depth
))

# Set up color mapping
color_mapper = linear_cmap(field_name='features_used', palette=Spectral6, low=min(features_used_depth), high=max(features_used_depth))

p1 = figure(title="Effect of max_depth on Decision Tree Accuracy",
            x_axis_label='max_depth', y_axis_label='Accuracy', width=800, height=400)
p1.line('max_depth', 'training_accuracy', source=source_depth, line_width=2, legend_label='Training Accuracy', color='blue')
p1.circle('max_depth', 'training_accuracy', source=source_depth, fill_color='blue', size=8)

p1.line('max_depth', 'cv_accuracy', source=source_depth, line_width=2, legend_label='Cross-Validation Accuracy', color='orange')
p1.square('max_depth', 'cv_accuracy', source=source_depth, fill_color='orange', size=8)

# Add a color bar
color_bar = ColorBar(color_mapper=color_mapper['transform'], location=(0,0), ticker=BasicTicker(),
                     formatter=PrintfTickFormatter(format='%d features'))

p1.add_layout(color_bar, 'right')

# Show and save the plot
show(p1)
export_png(p1, filename="../E2-figures/max_depth.png")

best_index = np.argmax(cv_accuracies_depth)
best_max_depth = max_depth_range[best_index]
best_cv_accuracy_depth = cv_accuracies_depth[best_index]

print(f'Sweet spot for max_depth: {best_max_depth} with cross-validation accuracy: {best_cv_accuracy_depth:.2f}')

# --- Analyze max_leaf_nodes parameter ---
max_leaf_nodes_range = range(2, 51, 2)
training_accuracies_leaf = []
cv_accuracies_leaf = []
features_used_leaf = []

for max_leaf_nodes in max_leaf_nodes_range:
    clf = tree.DecisionTreeClassifier(max_leaf_nodes=max_leaf_nodes, random_state=42)
    clf.fit(X, Y)
    
    train_accuracy = accuracy_score(Y, clf.predict(X))
    training_accuracies_leaf.append(train_accuracy)
    
    cv_scores = cross_val_score(clf, X, Y, cv=10)
    cv_accuracies_leaf.append(cv_scores.mean())
    
    feature_count = num_features(clf, X)
    features_used_leaf.append(feature_count)

# Bokeh plot for max_leaf_nodes
source_leaf = ColumnDataSource(data=dict(
    max_leaf_nodes=max_leaf_nodes_range,
    training_accuracy=training_accuracies_leaf,
    cv_accuracy=cv_accuracies_leaf,
    features_used=features_used_leaf
))

# Set up color mapping
color_mapper = linear_cmap(field_name='features_used', palette=Spectral6, low=min(features_used_leaf), high=max(features_used_leaf))

p2 = figure(title="Effect of max_leaf_nodes on Decision Tree Accuracy",
            x_axis_label='max_leaf_nodes', y_axis_label='Accuracy', width=800, height=400)
p2.line('max_leaf_nodes', 'training_accuracy', source=source_leaf, line_width=2, legend_label='Training Accuracy', color='blue')
p2.circle('max_leaf_nodes', 'training_accuracy', source=source_leaf, fill_color='blue', size=8)

p2.line('max_leaf_nodes', 'cv_accuracy', source=source_leaf, line_width=2, legend_label='Cross-Validation Accuracy', color='orange')
p2.square('max_leaf_nodes', 'cv_accuracy', source=source_leaf, fill_color='orange', size=8)

# Add a color bar
color_bar = ColorBar(color_mapper=color_mapper['transform'], location=(0,0), ticker=BasicTicker(),
                     formatter=PrintfTickFormatter(format='%d features'))

p2.add_layout(color_bar, 'right')

# Show and save the plot
show(p2)
export_png(p2, filename="../E2-figures/max_leaf_nodes.png")

best_index = np.argmax(cv_accuracies_leaf)
best_max_leaf_nodes = max_leaf_nodes_range[best_index]
best_cv_accuracy_leaf = cv_accuracies_leaf[best_index]

print(f'Sweet spot for max_leaf_nodes: {best_max_leaf_nodes} with cross-validation accuracy: {best_cv_accuracy_leaf:.2f}')

# --- Analyze min_samples_leaf parameter ---
min_samples_leaf_range = range(1, 21)
training_accuracies_samples = []
cv_accuracies_samples = []
features_used_samples = []

for min_samples_leaf in min_samples_leaf_range:
    clf = tree.DecisionTreeClassifier(min_samples_leaf=min_samples_leaf, random_state=42)
    clf.fit(X, Y)
    
    train_accuracy = accuracy_score(Y, clf.predict(X))
    training_accuracies_samples.append(train_accuracy)
    
    cv_scores = cross_val_score(clf, X, Y, cv=10)
    cv_accuracies_samples.append(cv_scores.mean())
    
    feature_count = num_features(clf, X)
    features_used_samples.append(feature_count)

# Bokeh plot for min_samples_leaf
source_samples = ColumnDataSource(data=dict(
    min_samples_leaf=min_samples_leaf_range,
    training_accuracy=training_accuracies_samples,
    cv_accuracy=cv_accuracies_samples,
    features_used=features_used_samples
))

# Set up color mapping
color_mapper = linear_cmap(field_name='features_used', palette=Spectral6, low=min(features_used_samples), high=max(features_used_samples))

p3 = figure(title="Effect of min_samples_leaf on Decision Tree Accuracy",
            x_axis_label='min_samples_leaf', y_axis_label='Accuracy', width=800, height=400)
p3.line('min_samples_leaf', 'training_accuracy', source=source_samples, line_width=2, legend_label='Training Accuracy', color='blue')
p3.circle('min_samples_leaf', 'training_accuracy', source=source_samples, fill_color='blue', size=8)

p3.line('min_samples_leaf', 'cv_accuracy', source=source_samples, line_width=2, legend_label='Cross-Validation Accuracy', color='orange')
p3.square('min_samples_leaf', 'cv_accuracy', source=source_samples, fill_color='orange', size=8)

# Add a color bar
color_bar = ColorBar(color_mapper=color_mapper['transform'], location=(0,0), ticker=BasicTicker(),
                     formatter=PrintfTickFormatter(format='%d features'))

p3.add_layout(color_bar, 'right')

# Show and save the plot
show(p3)
export_png(p3, filename="../E2-figures/min_samples_leaf.png")

best_index = np.argmax(cv_accuracies_samples)
best_min_samples_leaf = min_samples_leaf_range[best_index]
best_cv_accuracy_samples = cv_accuracies_samples[best_index]

print(f'Sweet spot for min_samples_leaf: {best_min_samples_leaf} with cross-validation accuracy: {best_cv_accuracy_samples:.2f}')
