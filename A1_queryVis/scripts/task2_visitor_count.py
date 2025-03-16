from os import path

import sqlite3
import pandas as pd

from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.models.layouts import TabPanel
from bokeh.models.widgets import Select
from bokeh.layouts import column, row
from bokeh.models import DatetimeTickFormatter
from bokeh.models import ColumnDataSource, Div 

def visitor_count():
    """ Create a tab with an interactive histogram of visitor numbers
    :return: bokeh TabPanel object 
    """
    appDirpath = path.basename(path.split(path.dirname(__file__))[0])
    #dbFilepath = path.join(appDirpath, 'data', 'dinofun.db')
    dbFilepath = path.join(appDirpath, 'data', 'minifun.db')
    
    binSizeDict = {
        '---': None,
        '10 min': 10, '15 min': 15, '20 min': 20, '30 min': 30,
        '1 h': 60, '2 h': 120
    }
    days = ('Fri', 'Sat', 'Sun')
    
    
    def make_plot(src, legendLabel='Fri'):
        """ Create the figure with the histogram
        :return: bokeh Figure object 
        """

        p = figure(width=800, height=300, x_axis_type='datetime', title="Visitor Movement Over Time")
        # VBar.x refers to the center of the bar
        p.vbar(source=src, x='binCen', top='count', width='width')

        # Format the datetime axis for better readability
        p.xaxis.formatter = DatetimeTickFormatter(
            hours=["%H:%M"],  # Format for hours
            days=["%d %b %H:%M"],  # Format for days
            months=["%d %b %Y"],  # Format for months
            years=["%Y"]  # Format for years
        )

        p.xaxis.axis_label = "Time of Day"
        p.yaxis.axis_label = "Number of Visitors"
        p.xgrid.grid_line_color = None
        return p
    
    
    def load_source(binSizeStr='---', day='Fri'):
        """ Load trajectory data from the database
        :param binSizeStr: a key from `binSizeDict`
        :param day: day to be queried
        :return: bokeh ColumnDataSource object 
        """
        if binSizeStr == "---":
            return ColumnDataSource({ 'binCen': [], 'count': [], 'width': [] })
        
        table = 'miniMovement' + day
        binSizeInMinutes = binSizeDict[binSizeStr]
        # Group the date by temporal bins for a histogram.
        # Notice that the month (June) is given as "6", not "06" in the table.
        # `substr(timestamp,-8)` selects the time (not the date) part of the *timestamp* column.
        # `strftime("%s",foo)` formats the string foo as seconds since 1970-01-01.
        # The binning happens through rounding the seconds to the specified minutes.
        # After the following query, column binCen has values that could be called binMin;
        # it is easier to fix this in a second step.
        q = ('SELECT min(timestamp) binCen, count(distinct id) count '
             'FROM ' + table + ' WHERE type="movement" '
             'GROUP BY cast((strftime("%s",substr(timestamp,-8))/60/?) AS INT);')
        df = None
        try:
            with sqlite3.connect(dbFilepath) as con:
                df = pd.read_sql_query(q, con, params=(binSizeInMinutes,), parse_dates=['binCen'])
        except sqlite3.Error as e:
            print('Visitor count: load_source: sqlite3.Error:', e)
            return ColumnDataSource()
                
        # binMin to binCen
        df['binCen'] = df.binCen + pd.Timedelta(str(binSizeInMinutes/2) + ' min')
        
        # constant width of bars in milliseconds
        width = binSizeInMinutes*60*1000
        df['width'] = [width]*len(df)
        
        print(day, '-'*76)
        print(df)
        return ColumnDataSource(df)
    
    
    def update(attr, old, new):
        """ Update the data after a user interaction
        """
        print(f"Updating plot with bin size {selectBinSize.value} and day {selectDay.value}")
        binSize = selectBinSize.value
        print('Visitor count: update: binSize =', binSize)
        # srcNew = load_source(binSize)
        # srcCur.data.update(srcNew.data)
        # possibly a good place for extension
        day = selectDay.value
        srcNew = load_source(binSize, day)
        srcCur.data.update(srcNew.data)

        
    
    
    # Create the user controls and link the interactions         
    #selectBinSize = Select(title='Bin size:', value="---", options=list(binSizeDict.keys()))
    #selectBinSize.on_change('value', update)
    
    #controls = column(selectBinSize, width=200)
    
    # Create the plot
    #srcCur = load_source()
    #p = make_plot(srcCur, 'Fri')
    
    # Create a layout for the tab and initialize it
    #layout = row(controls, p)
    # possibly a good place for extension
    selectBinSize = Select(title='Bin size:', value="---", options=list(binSizeDict.keys()))
    selectDay = Select(title="Day:", value="Fri", options=list(days))
    selectBinSize.on_change('value', update)
    selectDay.on_change('value', update)

    controls = column(selectBinSize, selectDay, width=200)
    srcCur = load_source('10 min', 'Fri')  # Load default data
    p = make_plot(srcCur, 'Fri')  # Initialize plot

    # New text widget to display text below the plot
    explaination = '''SIMILARITIES :\n\n
    POINT 1. From 8:00 to 9:00 the visitor count starts increasing\n
    POINT 2. Around 9:00 to 10:00 the visitor count is more\n
    POINT 3. But around 10:00 to 11:00 the visior count decrases\n
    POINT 4. Around 11:00 it again reaches the peak\n
    POINT 5. From 20:00 to 24:00 the visitor count starts decreasing.\n\n\n\n
    
    DIFFERENCES :\n\n
    POINT 1. On average there are more number of visitors on Sunday, compared to Friday and Saturday\n
    POINT 2. On Friday and Saturday the least number of visitors are from 15:00 to 16:00 and around 16:00 it has a sudden spike up,
       where as on Sunday it stays average during that period and the spike is less compared to other days
    '''
    textDiv = Div(text=explaination, width=800, height=50)

    layout = column(row(controls, p), textDiv)
    tab = TabPanel(child=layout, title='Visitor count')
    
    return tab
  
