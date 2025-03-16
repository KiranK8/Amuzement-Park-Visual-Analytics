"""Code for exercise 3, task 1 and task 2."""

import numpy as np
import pandas as pd
from itertools import permutations
from pandas.api.types import CategoricalDtype

# scikit-learn for decision tree classification and evaluation
from sklearn import tree
from sklearn.model_selection import cross_val_score
from sklearn.metrics import classification_report, accuracy_score

# Load the data and make a copy with numerical entries only
df = pd.read_csv('../data/adult.csv', na_values='?').dropna()
df.drop(['fnlwgt'], axis=1, inplace=True)

# Identify and convert all categorical columns to codes for numeric processing
for col in df.select_dtypes(include=['object', 'category']).columns:
    df[col] = df[col].astype('category')

# Explicitly identify and convert categorical columns
categorical_columns = [
    'workclass', 'marital-status', 'occupation', 'relationship', 'race', 'sex', 'native-country'
]

# Convert identified categorical columns to 'category' dtype
for col in categorical_columns:
    df[col] = df[col].astype('category')

def IG(df, var):
    """
    Compute information gain for a given dataframe w.r.t. income 
    when splitting into categorical variable var.
    
    Return:
        float: information gain
    """
    # Entropy before split
    entropy1 = df.income.value_counts(normalize=True).apply(lambda x: -x*np.log2(x)).sum()
    
    # Entropy after split
    grouped_entropy = df.groupby([var]).income.value_counts(normalize=True).apply(lambda x: -x*np.log2(x)).groupby(level=0).sum()
    weights = df[var].value_counts(normalize=True)
    entropy2 = (grouped_entropy * weights).sum()
    
    # Return information gain
    info_gain = entropy1 - entropy2
    return info_gain

# List all categorical variables (excluding 'income')
categorical_vars = df.select_dtypes(include=['category']).columns.tolist()
categorical_vars.remove('income')

# Compute and print the information gain for all categorical variables
print("Information Gain for all categorical variables:")
for var in categorical_vars:
    ig = IG(df, var)
    print(f"Information gain for {var}: {ig:.6f}")


# Function to reorder and test new categories for 'relationship'
def test_reordering_relationship(df):
    var = 'relationship'
    categories = df[var].astype('category').cat.categories.tolist()
    orderings = list(permutations(categories))
    
    best_ig = 0
    best_ordering = categories
    print(f"\nTesting reorderings for {var}:")
    
    for ordering in orderings[:10]:  # Limit to first 10 permutations for simplicity
        cat_type = CategoricalDtype(categories=ordering, ordered=True)
        df_reordered = df.copy()
        df_reordered[var] = df_reordered[var].astype(cat_type).cat.codes
        
        ig = IG(df_reordered, var)
        print(f"Ordering: {ordering} -> Information Gain: {ig:.6f}")
        
        if ig > best_ig:
            best_ig = ig
            best_ordering = ordering
    
    return best_ordering, best_ig

# Test reorderings for 'relationship'
best_ordering_relationship, best_ig_relationship = test_reordering_relationship(df)


# Apply the best ordering to create a new dataset
df_reordered = df.copy()
df_reordered['relationship'] = df_reordered['relationship'].astype(CategoricalDtype(categories=best_ordering_relationship, ordered=True)).cat.codes

# Convert all categorical variables to numeric codes in the reordered dataset
for col in df_reordered.select_dtypes(include=['category']).columns:
    df_reordered[col] = df_reordered[col].cat.codes

# Prepare data for training and evaluation
X_reordered = df_reordered.drop('income', axis=1)
y_reordered = df_reordered['income']

# Train a decision tree on the reordered dataset
clf_reordered = tree.DecisionTreeClassifier(random_state=42)
clf_reordered.fit(X_reordered, y_reordered)

# Training and cross-validation accuracy
train_accuracy_reordered = accuracy_score(y_reordered, clf_reordered.predict(X_reordered))
cv_scores_reordered = cross_val_score(clf_reordered, X_reordered, y_reordered, cv=10)

print(f"\nTraining accuracy with reordered dataset: {train_accuracy_reordered:.2f}")
print(f"Cross-validation accuracy for reordered dataset: {cv_scores_reordered.mean():.2f} (+/- {cv_scores_reordered.std() * 2:.2f})")

# Classification report for the reordered dataset
print("\nClassification report for the decision tree with reordered dataset:")
classification_report_reordered = classification_report(y_reordered, clf_reordered.predict(X_reordered))
print(classification_report_reordered)

# Save the new dataset to a CSV file
df_reordered.to_csv('../data/adult_reordered.csv', index=False)
print("\nReordered dataset saved as 'adult_reordered.csv' in the 'data' directory.")
