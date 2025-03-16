
# When loading this in a jupyter notebook, enter the following code in the first line of this cell
# to write changes back to the file. Attention: this will overwrite the original file!
# %%writefile ../E1_datasetFeatures.py

"""Code for exercise 1."""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns # work with seaborn for rapid chart testing

%matplotlib inline

sns.set_context('notebook') # 'talk'

# load the data
df = pd.read_csv('../data/adult.csv', na_values='?').dropna()

# example for continuous variables
g = sns.catplot(data=df, x='age', y='income', kind='violin', inner='quartile', aspect=1.5, palette='Set2')
g.fig.suptitle('Age distribution by income')
g.fig.savefig('../E1-figures/1-1_age.png')

# example for categorical variable
g = sns.catplot(data=df, y='workclass', hue='income', kind='count', aspect=1.5, palette='Set2')
g.fig.suptitle('Income by workclass')
g.fig.savefig('../E1-figures/3-1_workclass.png')



# Age and Income
plt.figure(figsize=(12, 6))
sns.violinplot(data=df, x='income', y='age', inner='quartile', palette='Set2')
plt.title('Age Distribution by Income')
plt.savefig('../E1-figures/1-1_age.png')
plt.show()

# Observation: Older individuals tend to have higher income, with the median age for those earning >50k being higher.

# Race and Income
plt.figure(figsize=(12, 6))
sns.countplot(data=df, x='race', hue='income', palette='Set2')
plt.title('Income Distribution by Race')
plt.savefig('../E1-figures/1-2_race.png')
plt.show()

# Observation: A higher proportion of 'White' individuals earn more than 50k compared to other races.

# Native Country and Income
plt.figure(figsize=(12, 10))
sns.countplot(data=df, y='native-country', hue='income', order=df['native-country'].value_counts().index, palette='Set2')
plt.title('Income Distribution by Native Country')
plt.savefig('../E1-figures/1-3_native_country.png')
plt.show()

# Observation: Most people earning >50k are from the United States, with very few from other countries.

# Capital Gain and Income
plt.figure(figsize=(12, 6))
sns.violinplot(data=df, x='income', y='capital-gain', inner='quartile', palette='Set2')
plt.title('Income Distribution by Capital Gain')
plt.yscale('log')  # Applying log scale for better visualization of wide range
plt.savefig('../E1-figures/1-4_capital_gain.png')
plt.show()

# Observation: People earning >50k have significantly higher capital gains compared to those earning <=50k.

# Marital Status and Income
plt.figure(figsize=(12, 6))
sns.countplot(data=df, x='marital-status', hue='income', palette='Set2')
plt.title('Income Distribution by Marital Status')
plt.xticks(rotation=45)
plt.savefig('../E1-figures/2-1_marital_status.png')
plt.show()

# Observation: Married individuals, especially those with spouse present, tend to earn more than 50k.

# Relationship and Income
plt.figure(figsize=(12, 6))
sns.countplot(data=df, x='relationship', hue='income', palette='Set2')
plt.title('Income Distribution by Relationship')
plt.xticks(rotation=45)
plt.savefig('../E1-figures/2-2_relationship.png')
plt.show()

# Observation: 'Husband' and 'Wife' categories show higher income levels compared to other relationship statuses.

# Sex and Income
plt.figure(figsize=(12, 6))
sns.countplot(data=df, x='sex', hue='income', palette='Set2')
plt.title('Income Distribution by Sex')
plt.savefig('../E1-figures/2-3_sex.png')
plt.show()

# Observation: Males have a higher proportion of >50k earners compared to females.

# Education and Income
plt.figure(figsize=(12, 10))
sns.countplot(data=df, y='education', hue='income', order=df['education'].value_counts().index, palette='Set2')
plt.title('Income Distribution by Education Level')
plt.savefig('../E1-figures/2-4_education.png')
plt.show()

# Observation: Higher education levels (like 'Bachelors', 'Masters', 'Doctorate') are associated with higher incomes.

# Workclass and Income
plt.figure(figsize=(12, 6))
sns.countplot(data=df, x='workclass', hue='income', palette='Set2')
plt.title('Income Distribution by Workclass')
plt.xticks(rotation=45)
plt.savefig('../E1-figures/3-1_workclass.png')
plt.show()

# Observation: Individuals in the 'Self-emp-not-inc' and 'Private' work classes have a higher proportion of >50k earners.

# Occupation and Income
plt.figure(figsize=(12, 10))
sns.countplot(data=df, y='occupation', hue='income', order=df['occupation'].value_counts().index, palette='Set2')
plt.title('Income Distribution by Occupation')
plt.savefig('../E1-figures/3-2_occupation.png')
plt.show()

# Observation: Certain occupations like 'Exec-managerial' and 'Prof-specialty' have a higher proportion of >50k earners.


# Hours Per Week and Income
plt.figure(figsize=(12, 6))
sns.boxplot(data=df, x='income', y='hour-per-week', palette='Set2')
sns.catplot(
    data=df, x="income", y="hour-per-week", hue="sex",
    kind="violin", bw_adjust=.5, cut=0, split=True
)
plt.title('Income Distribution by Hours Per Week')
plt.savefig('../E1-figures/3-3_hours_per_week.png')
plt.show()

# Observation: People earning >50k tend to work more hours per week on average compared to those earning <=50k.

plt.figure(figsize=(12, 6))
sns.violinplot(data=df, x='income', y='capital-loss', inner='quartile', palette='Set2')
plt.yscale('log')
plt.title('Income Distribution by Capital Loss (Log Scale)')
plt.xlabel('Income')
plt.ylabel('Capital Loss (Log Scale)')
plt.savefig('../E1-figures/3-4_capital_loss_violin.png')
plt.show()


