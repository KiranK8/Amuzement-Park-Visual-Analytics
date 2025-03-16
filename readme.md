## Visual Analytics Assignments

This repository contains the templates for the assignments of lecture Visual Analytics.


### Application scenario

In most of the assignments we will work on the VAST Challenge 2015.

> The IEEE Visual Analytics Science and Technology (VAST) Challenge is an annual 
contest with the goal of advancing the field of visual analytics through competition. 
The VAST Challenge is designed to help researchers understand how their software 
would be used in a novel analytic task and determine if their data transformations, 
visualizations, and interactions would be beneficial for particular analytic tasks. 
VAST Challenge problems provide researchers with realistic tasks and data sets 
for evaluating their software, as well as an opportunity to advance the field 
by solving more complex problems.

More information concerning the 2015 challenge can be found in the [challenge description](docs/VastChallenge2015.md) which is a local reader friendly copy of the official documents.


### Assignments

The exercises are grouped into four assignments, each treating a specific aspect covered in the lecture. 
Every student group must achieve at least 50% of the points of each assignment to be admitted to the exam at the end of the semester. 
The assignments are usually released after the lecture and submissions are then due two or three weeks later **before the lecture**. 
Discussion/presentation of the solutions of an assignment takes place roughly one week after the due date (given in the information table in OLAT).

1. [Working with databases and Bokeh](A1_queryVis/assignment1.md)
2. [Decision trees and getting rich](A2_decisionTree/assignment2.md)
3. [Temporal analysis and clustering](A3_groupAnalysis/assignment3.md)
4. [Crime investigation](A4_crimeInvestigation/assignment4.md)


### Additional information

#### Tutorials and documentation

In this section we list introductions and tutorials to the techniques used in the assignments. Many of them are hopefully already known to you and it is not expected that you work through the material in detail. If one of the required techniques is not familiar to you, try one or two of the tutorials to get started and look deeper once you have a question. 

Also remember that there are fellow students that may help you.

[Tutorial](tutorial/tutorial-visana.ipynb) prepared by the staff.

**Git:**

- [Git Tutorials](https://www.atlassian.com/git/tutorials/)
- [Git in 15 minutes](https://try.github.io/levels/1/challenges/1) (interactive tutorial)
- [Git, the Simple Guide](http://rogerdudler.github.io/git-guide/)

**Python libraries:**

- [Bokeh](https://bokeh.pydata.org/en/latest/docs/user_guide.html)
- [Pandas](https://pandas.pydata.org)


### Submission instructions

- We use GitLab for the assignments. Your assignments are described in Markdown files and we provide space to answer the questions. Additionally there is demo code provided that you need to expand. References to the code directories are given in the respective task.
- Please push your work regularly to GitLab. This ensures that you do not lose intermediate results and we can check your work if necessary.
- We will mark the last stage of your work before the deadline (see below).
- Please make sure that the code runs with a Python environment as set up in the tutorial.
- Make sure you are aware of your tasks. All actions on your side that will give credit are usually marked with `todo` stating the respective amount of credit points. 

#### Tag the final commit

We ask you to kindly use git tags to mark the final commit concerning an assignment.
This is as simple as executing

```sh
git tag submissionA1
git push origin --tags
```

after your final commit.
For batch processing on our side, make sure to spell the tag name exactly like this: 
"submissionA" + number.

Should you ever want to revisit that state of your repository, you can do

```sh
git fetch
git checkout submissionA1
```

And `git checkout main` to return to your current work.


### Update the template

We will update the template from time to time to contain the new assignments. 
This requires you to fetch updates from the template. 
There is a detailed description of [how to keep your downstream repository up to date](docs/updateDownstream.md).
