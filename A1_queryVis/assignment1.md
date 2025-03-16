# Assignment 1: DinoFun World

In this assignment you practice the fundamentals of working with tabular data 
using SQLite and Bokeh visualizations. Large-scale data, cannot necessarily be
stored in main memory, so you work with a database querying relevant parts 
and aggregated results on demand. With Bokeh you can design interactive charts.

- In exercise 1, you get familiar with the problem setting and data, and
  set up a database. 
- In exercise 2, you learn how to retrieve (aggregated) data from the database.
- In exercise 3, you write interactive visualizations.

Total points in this assignment: 32P

Make sure you have read the top-level [readme.md](../readme.md) before you proceed.


## Exercise 1: Setting up (8P)

First, you should get familiar with the provided data and application scenario.

### Task 1 (4P)

To get started (briefly) read through the
[challenge description](../docs/VastChallenge2015.md) 
and answer the following questions.

**Question 1:**
How many attractions does DinoFun World offer?
(all numbered places including toilets etc.)
Please state briefly where you got this information from.  
Answer: 72 attractions in total. This information can be read
from the list of the number and name of the palces.

**Question 2:**
What was stolen from the pavilion exhibition?  
Answer: An Olympic medal.

**Question 3:**
Where in DinoFun World are the memorabilia of Scott Jones displayed
(name + ID)?  
Answer: Grinosaurus Stage, 63;
        Creighton Pavilion, 32.

**Question 4:**
What is the temporal resolution of the tracking data?
(Hint: Check the data description file.)  
Answer: A second.

Now it is time to set up the database for the provided data.
Please make sure that you **do not commit the data into git**.
There is a size limit of 1 GB and submitting data and (generated) images will
rapidly exceed this limit.


### Task 2 (2P)

Create a database and import the CSV files for the park movement data.

- Download the zipped CSV files containing the movement data for the three days from
  the OLAT directory and extract them into your data folder.  
  Course: Visual Analytics  
  Folder: Material/Data
- On the command line, go to that top-level data folder in your repository (see below).
- Create an empty database and call it dinofun.db.
- `TODO` Import the movement data. Create one table per day.

Here is some code to get you started; it uses the file setupDB.sql from the
repository (you may want to have a look at it).

```sh
cd template/data
sqlite3 dinofun.db
sqlite> .read ../setupDB.sql
sqlite> SELECT * FROM movementFri LIMIT 10;
sqlite> .exit
```

Mind the exact spelling of the column names.
Eventually every group and the coaches should have the same database so that
code can be tested without interchanging data.

Enter the following query in the sqlite command line interface and enter the
output below.

```sql
SELECT * FROM movementSat WHERE id=1202957 LIMIT 10;
```

My output:

"2014-6-07 08:00:50",1202957,check-in,63,99
"2014-6-07 08:01:44",1202957,movement,63,98
"2014-6-07 08:01:49",1202957,movement,63,97
"2014-6-07 08:01:54",1202957,movement,63,96
"2014-6-07 08:01:59",1202957,movement,64,95
"2014-6-07 08:02:04",1202957,movement,64,94
"2014-6-07 08:02:09",1202957,movement,65,93
"2014-6-07 08:02:14",1202957,movement,64,92
"2014-6-07 08:02:19",1202957,movement,63,91
"2014-6-07 08:02:24",1202957,movement,62,90

You should get the following.

```
2014-6-07 08:00:50|1202957|check-in|63|99
2014-6-07 08:01:44|1202957|movement|63|98
2014-6-07 08:01:49|1202957|movement|63|97
2014-6-07 08:01:54|1202957|movement|63|96
2014-6-07 08:01:59|1202957|movement|64|95
2014-6-07 08:02:04|1202957|movement|64|94
2014-6-07 08:02:09|1202957|movement|65|93
2014-6-07 08:02:14|1202957|movement|64|92
2014-6-07 08:02:19|1202957|movement|63|91
2014-6-07 08:02:24|1202957|movement|62|90
```


### Task 3 (2P)

Now import the ride details into a new table *attractions* with
the following schema and answer the questions below.

```sql
CREATE TABLE attractions(parkMapId INTEGER,
realWorldName TEXT, dinoFunName TEXT,
x INTEGER, y INTEGER, type TEXT);
```

Remark: Contrary to what the term “ID” suggests, the *parkMapId* is not unique.

```sql
SELECT parkMapId, count(*) AS c, GROUP_CONCAT(dinoFunName) FROM attractions
GROUP BY parkMapId HAVING c > 1;
```
<br>

```
63|2|Lawn3,Grinosaurus Stage
64|2|Lawn1,SabreTooth Theatre
```

**Question 1:**
How many different attractions from the park map are stored in your table
(in terms of distinct *dinoFunName*s)?

SELECT COUNT(DISTINCT parkMapId) FROM attractions;

Answer: 72.

**Question 2:**
What can you buy at Permafrosties?

SELECT DISTINCT realWorldName FROM attractions WHERE dinoFunName = 'Permafrosties';

Answer: "Ice Cream".


## Exercise 2: Automatic data analysis (12P)

Answer the following data-related questions and give the respective query.
Here is an [SQL cheat sheet](https://jrebel.com/rebellabs/sql-cheat-sheet/)
in case you need a refresher for the more complex queries.

**Question 1 (1P):**
How many check-ins has visitor 173593 on Friday?

SELECT COUNT(*) FROM movementFri WHERE id = 173593 AND type = 'check-in';

Answer: 27.

**Question 2 (1P):**
How many visitors does DinoFun World have on each of the three days?

SELECT COUNT(DISTINCT id) FROM movementFri;
SELECT COUNT(DISTINCT id) FROM movementSat;
SELECT COUNT(DISTINCT id) FROM movementSun;

Answer: 3557, 6411 and 7569.

**Question 3 (2P):**
List the 10 visitors with most check-ins on Sunday.
Also give their number of check-ins.

SELECT id, COUNT(*) FROM movementSun 
WHERE type = 'check-in' 
GROUP BY id 
ORDER BY COUNT(*) DESC 
LIMIT 10;

Answer:

1846955|41
1736555|41
1131984|41
590079|41
1822329|39
197541|39
1725488|38
1529852|38
686158|38
372482|38


**Question 4 (1P):**
How many activities are recorded on Friday between 22:00:00 and 23:00:00? 
Notice that you can do (partial) string comparisons in SQL:
`timestamp>"2014-6-06 14:00"`

SELECT COUNT(*) FROM movementFri 
WHERE timestamp >= "2014-6-06 22:00:00" 
AND timestamp <= "2014-6-06 23:00:00";

Answer: 118531.

**Question 5 (1P):**
When does visitor 84322 enter and leave the park on Saturday?

SELECT timestamp 
FROM movementSat 
WHERE id = 84322 
ORDER BY timestamp ASC 
LIMIT 1;

SELECT timestamp 
FROM movementSat 
WHERE id = 84322 
ORDER BY timestamp DESC 
LIMIT 1;

Answer: 2014-6-07 08:21:25 and 2014-6-07 22:28:12.

**Question 6 (2P):**
Where (*dinoFunName*?) does visitor 1513840 check-in most frequently
(how often?) on the three days?

SELECT a.dinoFunName, COUNT(m.id) AS checkin_count
FROM movementFri m
JOIN attractions a ON m.x = a.x AND m.y = a.y
WHERE m.id = 1513840 AND m.type = 'check-in'
GROUP BY a.dinoFunName
ORDER BY checkin_count DESC
LIMIT 1;

SELECT a.dinoFunName, COUNT(m.id) AS checkin_count
FROM movementSat m
JOIN attractions a ON m.x = a.x AND m.y = a.y
WHERE m.id = 1513840 AND m.type = 'check-in'
GROUP BY a.dinoFunName
ORDER BY checkin_count DESC
LIMIT 1;

SELECT a.dinoFunName, COUNT(m.id) AS checkin_count
FROM movementSun m
JOIN attractions a ON m.x = a.x AND m.y = a.y
WHERE m.id = 1513840 AND m.type = 'check-in'
GROUP BY a.dinoFunName
ORDER BY checkin_count DESC
LIMIT 1;

- Friday: Atmosfear|5;
- Saturday: Flight of the Swingodon|3
- Sunday: TerrorSaur |3

**Question 7 (2P):**
Which attraction (*dinoFunName*?) has most/fewest (how many?) check-ins
on Saturday?

SELECT a.dinoFunName, COUNT(*) AS checkin_count
FROM movementSat m
JOIN attractions a ON m.x = a.x AND m.y = a.y
WHERE m.type = 'check-in'
GROUP BY a.dinoFunName
ORDER BY checkin_count DESC
LIMIT 1;

SELECT a.dinoFunName, COUNT(*) AS checkin_count
FROM movementSat m
JOIN attractions a ON m.x = a.x AND m.y = a.y
WHERE m.type = 'check-in'
GROUP BY a.dinoFunName
ORDER BY checkin_count ASC 
LIMIT 1;

- most: Entrance|6699
- fewest: Liggement Fix-Me-Up|115

**Question 8 (2P):**
For Sunday, compute for each timestamp and attraction the number of check-ins,
i.e., the number of people that check-in at a given attraction at the same time.
Limit your result to the ones with more than 40 concurrent check-ins.  
Which types of attraction have most check-ins?
(Name three types ordered by frequency.
Check the list computed before manually.)

CREATE TABLE frequencyAttrac AS SELECT a.type, COUNT(*) AS frequency
FROM movementSun m
JOIN attractions a ON m.x = a.x AND m.y = a.y
WHERE m.type = 'check-in'
GROUP BY m.timestamp, a.parkMapID
HAVING COUNT(m.id) > 40
ORDER BY frequency DESC;

SELECT DISTINCT(type), COUNT(*) 
FROM frequencyAttrac 
GROUP BY type 
ORDER BY COUNT(*) DESC 
LIMIT 3;


Answer:
Concurrent check-ins:
Entrance|69
Entrance|67
Entrance|66
Entrance|65
Entrance|62
Entrance|59
Entrance|54
Entrance|50
Entrance|49
Entrance|44
Thrill|44
Entrance|43
Kiddie|43
Thrill|43
Entrance|42
Lawn|42
Everybody|41
Thrill|41

Most frequent types:
Entrance|20
Thrill|6
Everybody|2

## Exercise 3: Visualization (12P)

In this exercise, each group member shall work on one of the following
visualization tasks. You can assign on your own or take the last digit(s) of
your student ID to assign tasks (smallest number gets task 1).

You are given starter code in the folder A1_queryVis.
Before you can start the app, you need a link (in your assignment-specific
data folder) to your database (in your top-level data folder).
Do this by creating a symbolic link (the following instructions are for Linux).

```sh
cd A1_queryVis/data
ln -s ../../data/dinofun.db dinofun.db
```

Now you can start the app. Go to the parent folder of A1_queryVis and start a
bokeh server for this app from the command line:

```sh
cd ../..
bokeh serve --show A1_queryVis
```

This will open the app in your web browser and you should see three tabs,
one for each task, with some initial visualization. Additional information for
[bokeh server applications](https://bokeh.pydata.org/en/latest/docs/user_guide/server.html#userguide-server-applications)
can be found on the
[bokeh website](https://bokeh.pydata.org/en/latest/docs/user_guide.html).

We have created a separate file for each of the three tasks to minimize merge
conflicts. Add necessary code to answer the following questions and to fulfill
the requirements.


### Task 1 (4P) (Did by Junze Jia)

Profile a visitor. Where did a given person go and check-in?
The tab "Individual visitor" shows a map of the park and the path the selected
person walked on the selected day. Add the following features.

- Highlight the check-in locations and encode how often the visitor checked in.
- Add hover functionality to give the *dinoFunName* and *type* of the check-in
  location.
- Write a brief text about the preferences of one of the three given visitors.

Answer:
Visitor 173593 prefers Thrill, Kiddie and Show Hall in DinoFun World.


**Hints:**

- See Question 6 from exercise 2 for help with the query.
- The x/y-coordinates in the database match map coordinates in the figure.
- Help with colormaps can be found
  [here](https://bokeh.pydata.org/en/latest/docs/user_guide/styling.html#using-mappers).


### Task 2 (4P)

How many visitors are moving in the park? The park management wants to
understand at which times of the day their park has most visitors. 

- Extend the visualization to provide information for all three days.
- Increase the readability of the time axis. Currently it is difficult to get
  the time for a particular bar.
- Briefly describe similarities and differences between the three days.
  Bullet points are enough.

**Hint:**

- The query is currently rather slow. To improve this you can do the query once
and store the results in additional files or create a database with a sampled
subset of the data.  
Do the following for the movement data to sample every 20th line, then
create a new database, minifun.db, based on the subsamples:  
`awk 'NR % 20 == 0' park-movement-Foo.csv > mini-movement-Foo.csv`  
This may generally be useful for quicker developing/testing.
- Strictly speaking, the given query yields the number of visitors that move
at least once during the respective time frames.


### Task 3 (4P)

How long do visitors stay in the park? The park management wants to understand
if there are patterns in arrival and departure time of their visitors
and how long they stay in total (including possible breaks).
Limit your analysis to the data for Friday.

- Fix the SQL query to read correct arrival and departure times for all visitors
  and display them in the scatterplot.
- Correctly compute and display the histogram of total time spent in the park
  (plot on the right).
- Briefly describe patterns you find in the plots.
