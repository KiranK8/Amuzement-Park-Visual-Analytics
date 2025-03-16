from os import path

import sqlite3
import pandas as pd
import numpy as np

from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Div
from bokeh.models.layouts import TabPanel
from bokeh.layouts import column, row

def visit_timespan():
    """ Create a tab for visitors' park time analysis
    :return: bokeh TabPanel object
    """
    appDirpath = path.basename(path.split(path.dirname(__file__))[0])
    dbFilepath = path.join(appDirpath, 'data', 'dinofun.db')
    
    
    def make_scatterplot(src):
        """ Create a scatterplot for the arrival/departure date
        :param src: ColumnDataSource with arrival and departure times
        :return: bokeh Figure object
        """

        df = pd.DataFrame(src.data)
        if 'arrival' not in df or 'departure' not in df:
            print("Error: Data source must include 'arrival_time' and 'departure_time'.")
            return None

        # Update data source if necessary
        src.data = df[['arrival', 'departure']].to_dict('list')

        p = figure(x_axis_type='datetime', y_axis_type='datetime', title="Arrival and Departure Times")
        p.scatter(source=src, x='arrival', y='departure',size=10, color='red', alpha=0.5)
        p.xaxis.axis_label = "Arrival on Friday"
        p.yaxis.axis_label = "Departure on Friday"
        return p
    
    
    def make_histogram(src):
        ''' Create a histogram of visitors' time in the park
        :param src: ColumnDataSource with arrival and departure times
        :return: bokeh Figure object
        '''
        #p = figure(width=300, height=600, y_axis_type='datetime')
        
        # create dummy data for demo purposes, use src instead
        #timespan = [pd.Timedelta('1h'), pd.Timedelta('10h')]
        #count = [3, 7]
        #src = ColumnDataSource({'timespan': timespan, 'count': count})
        
        #p.hbar(source=src, y="timespan", right="count", left=0, height=60*60*1000,
        #       fill_color="#b3de69")

        # Convert data source to DataFrame to compute durations
        df = pd.DataFrame(src.data)
        # Calculate duration in hours
        df['duration'] = (df['departure'] - df['arrival']).dt.total_seconds() / 3600
        
        # Histogram data
        freq, edges = np.histogram(df['duration'], bins=10)  # Adjust bins as needed
        
        # Midpoints for the y-axis
        y = [start + (end - start) / 2 for start, end in zip(edges[:-1], edges[1:])]
        
        # Create a new ColumnDataSource with duration data for hbar
        src_new = ColumnDataSource(data=dict(timespan=y, count=freq, top=edges[1:], bottom=edges[:-1]))
        
        p = figure(title="Histogram of Visit Durations", tools="pan,wheel_zoom,box_zoom,reset",
                x_axis_label='Number of Visits', y_axis_label='Duration (Hours)')
        
        # Use horizontal bars
        p.hbar(y="timespan", right="count", left=0, height=(edges[1] - edges[0]),
            source=src_new, fill_color="#b3de69", line_color="#033649")
    
        return p
    
    
    def load_source(day='Fri'):
        """ Load visitor park times from the database
        :param day: day to be queried
        :return: bokeh ColumnDataSource object
        """
        table = 'movement' + day
        q = ('SELECT id AS visitor_id, MIN(timestamp) AS arrival, MAX(timestamp) AS departure FROM ' + table + ' GROUP BY visitor_id LIMIT 100')
        df = None
        try:
            with sqlite3.connect(dbFilepath) as con:
                df = pd.read_sql_query(q, con, parse_dates=['arrival', 'departure'])
                df.reset_index(drop=True, inplace=True)
        except sqlite3.Error as e:
            print('Visit timespan: load_source: sqlite3.Error:', e)
            return ColumnDataSource()
        
        print(day, '-'*76)
        print(df)
        print(f"DATA: {df}")
        return ColumnDataSource(df)
    
    
    # Create the plot
    src = load_source()
    scatterPlot = make_scatterplot(src)
    histogram = make_histogram(src)
    Explaination = '''Arrival and Departure Times Scatterplot Description :\n\n
    POINT 1. Most visitors arrive in moring from 8:00 to 9:00 and depart around 20:00 to 23:00 in the night indicating that many visitors stay for the majority of the day.\n
    POINT 2. Some visitor (very few) arrive around 9:15 to 10:00 but depart early by 15:00 to 16:00, which depicts that they spent less hours in the park.\n
    POINT 3. There are 2 outliers (very few), which depicts that they spent less hours in the park.\n
    a) one that arrived lately at around 14:30 and departed late around 23:30.\n
    b) other one that arrived early around 09:00 and also departed early around 13:30.\n\n\n\n
    
    Visit Durations Histogram Description :\n\n
    POINT 1. majority of the visitors spent most of the day in the park that is around 11:00 to 14:30 hours.\n
    POINT 2. around 4 visitor spent only 5:00 to 6:00 hours.\n
    POINT 3. around 2 people spent around 8:00 to 11:00.\n\n\n\n
    '''
    Text = Div(text=Explaination)
    
    # Create a layout for the tab and initialize it
    plot_layout = row(scatterPlot, histogram)
    layout = column(plot_layout, Text) 
    tab = TabPanel(child=layout, title='Visit timespan')
    return tab
  
