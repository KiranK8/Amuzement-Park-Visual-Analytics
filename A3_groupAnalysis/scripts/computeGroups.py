import sqlite3
import sys
import numpy as np
import pandas as pd
from pandas.tseries.offsets import *

from scipy.spatial import KDTree

db_filename = '../../data/dinofun.db'
csv_filename = 'groups.csv'

if len(sys.argv) > 1:
    db_filename = sys.argv[1]
if len(sys.argv) > 2:
    csv_filename = sys.argv[2]

df = pd.DataFrame()
df_ci = pd.DataFrame()
    
with sqlite3.connect( db_filename ) as con:
    # arrival and departure
    query = """SELECT m.id, max(m.Timestamp) as Departure, min(m.Timestamp) as Arrival,
                      a.id as Entrance FROM movementFri m 
                LEFT JOIN attractions a ON m.X = a.x AND m.Y = a.y 
                GROUP BY m.id ORDER BY m.Timestamp"""
    df = pd.read_sql_query( query, con, parse_dates=['Arrival','Departure'] )
    
    # sum of all check-ins for group identification
    query = """SELECT m.id,sum(a.id) as CheckinSum FROM movementFri m 
               LEFT JOIN attractions a ON m.X = a.x AND m.Y = a.y 
               WHERE m.type='check-in' GROUP BY m.id"""
    df_ci = pd.read_sql_query( query, con ).sort_values(by=['id'])

# merge the two dataframes
df = pd.merge(df, df_ci, how='inner', on='id').sort_values(by=['Arrival'])

# assign group-ids and subgroup-ids to each person
df = df.assign( GroupId=df.groupby(['Arrival','Entrance']).ngroup()+1,
                SubgroupId=df.groupby(['Arrival','Entrance','CheckinSum']).ngroup()+1)

# now form groups for people doing the same things
# create a dataframe with one entry per subgroup
df_groups = df.groupby(['GroupId','SubgroupId']).first().reset_index()

# compute the number of subgroups per group
nsubgroups = df.groupby(['GroupId']).SubgroupId.nunique().to_frame( name='nSubgroups')
df_groups = df_groups.join( nsubgroups, on='GroupId' )

# compute the size of each subgroup
df_groups = df_groups.join( df.SubgroupId.value_counts().to_frame(name='SubgroupSize'), on='SubgroupId' )

# compute the size of each group
df_groups = df_groups.join( df_groups.groupby(['GroupId']).SubgroupSize.sum().to_frame(name='GroupSize'), on='GroupId' )

#---------------------------------------------
# compute counts and times for attractions
#---------------------------------------------
with sqlite3.connect( db_filename ) as con:
    attractions = pd.read_sql_query( "select * from attractions", con )

# list all available attractions
features = np.concatenate((attractions.type.unique(), [x+' Time' for x in attractions.type.unique()]))

# append empty entries to the data frame for each feature
for f in features:
    df_groups[f] = 0

# Helper structures for location
kdtree = KDTree( attractions[['X','Y']] )

def findLocation( x, y ):
    i = kdtree.query( [x,y] )
    if i[0] < 5:
        return attractions.at[i[1], 'RealWorld'] + ' ' + str(attractions.at[i[1], 'id'])
    return 'Stop'

def getLocationType( x, y ):
    i = kdtree.query( [x,y] )
    if i[0] < 5:
        return attractions.at[i[1], 'type']
    #return 'Stop'

# Read the movement data of a person and find locations where they stayed for more than 5 minutes and all check-ins.
def getStays( id ):
    with sqlite3.connect( db_filename ) as con:
        df = pd.read_sql_query( "select * from movementFRI where id = ?", con, params=(id,), parse_dates=['Timestamp'] )
    df['tdiff'] = df['Timestamp'].diff().shift(-1)
    df = df[((df['tdiff'] > pd.Timedelta('00:05:00')) & (df['type'] == 'movement')) |
            (df['type'] == 'check-in')]
    if len(df) == 0:
        return df
    
    df['loc'] = df.apply( lambda x: findLocation(x.X,x.Y), axis=1)
    df['locType'] = df.apply( lambda x: getLocationType(x.X,x.Y), axis=1)
    return df
     
def computeAttractionStats(x):
    df_stays = getStays(x.id).groupby(['locType']).tdiff
    
    # count the number of visits
    for i,v in df_stays.count().iteritems():
        x[i] = v
     
    # compute the total time spend in each attraction type
    for i,v in df_stays.sum().apply(lambda x: x.total_seconds()/60/60).iteritems():
        x[i+' Time'] = v
    return x

df_groups = df_groups.apply(computeAttractionStats, axis=1)
df_groups['Park Time'] = (df_groups.Departure - df_groups.Arrival).apply(lambda x: x.total_seconds()/60/60) - df_groups['Entrance Time']

# save the groups as csv
df_groups.to_csv(path_or_buf=csv_filename)
