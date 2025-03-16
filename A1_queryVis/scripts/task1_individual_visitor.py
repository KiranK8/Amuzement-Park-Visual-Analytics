# Did by Junze Jia.
# The preference description is in the Markdown file.

from os import path

import sqlite3
import pandas as pd

from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.models.layouts import TabPanel
from bokeh.models.widgets import RadioButtonGroup, Select
from bokeh.layouts import column, row
from bokeh.models import HoverTool
from bokeh.models import LabelSet


def individual_visitor():
    """ Create a tab to profiles a visitor's activity
    :return: bokeh TabPanel object 
    """
    appDirpath = path.basename(path.split(path.dirname(__file__))[0])
    dbFilepath = path.join(appDirpath, 'data', 'dinofun.db')
    
    
    def make_plot(trajectory, checkIns):
        """ Create the figure with map and the visitor's trajectory
        :return: bokeh Figure object 
        """
        plotSize = 800
        p = figure(x_range=(0,100), y_range=(0,100), width=plotSize, height=plotSize)
        
        url = path.join(appDirpath, 'static', 'parkmapgray.jpg')
        p.image_url(url=[url], x=0, y=100, w=100, h=100)
        
        p.line(source=trajectory, x='x', y='y', color='red')
        
        circles = p.circle(source=checkIns, x='x', y='y', radius=1.25) # TODO
        p.text(x='x', y='y', text='checkinfo', source=checkIns, text_align='center', text_baseline='middle')
        hover = HoverTool(renderers=[circles])
        
        hover.tooltips = [
            ("DinoFunName:","@dinoFunName"),
            ("Type", "@type"),
        ]
        p.add_tools(hover)
        return p
    
    
    def load_trajectory_data(visitorId, day='Fri'):
        ''' Load trajectory data from the database
        :param visitorId: ID of the visitor to be queried
        :param day: day to be queried
        :return: bokeh ColumnDataSource object 
        '''
        try:
            with sqlite3.connect(dbFilepath) as con:
                # read data from the database; 
                # attention: the table name cannot be passed as a parameter
                table = 'movement' + day
                q = 'SELECT x, y FROM ' + table + ' WHERE id=?'
                df = pd.read_sql_query(q, con, params=(visitorId,))
                return ColumnDataSource(df)
        except sqlite3.Error as e:
            print('load_trajectory_data: sqlite3.Error:', e)
        
        return ColumnDataSource()
    
    
    def load_checkin_data(visitorId, day='Fri'):
        """ Load checkin data from the database
        :param visitorId: ID of the visitor to be queried
        :param day: day to be queried
        :return: bokeh ColumnDataSource object 
        """
        try:
            with sqlite3.connect(dbFilepath) as con:
                # read data from the database; 
                # attention: the table name cannot be passed as a parameter
                table = 'movement' + day
                q = 'SELECT a.dinoFunName,a.type,a.x,a.y,COUNT(m.id) AS checkinfo FROM ' + table + ' m JOIN attractions a ON m.x = a.x AND m.y = a.y'+' WHERE id=? and m.type="check-in"'+'GROUP BY a.dinoFunName'# TODO
                df = pd.read_sql_query(q, con, params=(visitorId,))
                if df.empty:
                  print('load_checkin_data: visitor', visitorId, 'did not visit the park on', day)
                return ColumnDataSource(df)
        except sqlite3.Error as e:
            print('load_checkin_data: sqlite3.Error:', e)
        return ColumnDataSource()
    
    
    def update(attr, old, new):
        """ Update the data after a user interaction
        """
        idNew = selectId.value
        dayNew = radioselectDay.labels[radioselectDay.active]
        
        trajectoryNew = load_trajectory_data(idNew, dayNew)
        trajectoryCur.data.update(trajectoryNew.data)
        checkInNew = load_checkin_data(idNew, dayNew)
        checkInsCur.data.update(checkInNew.data)
        
        # TODO
    
    
    # Create the user controls and link the interactions         
    selectId = Select(title='Visitor ID:', value='173593', options=['173593', '1955415','2007070'])
    selectId.on_change('value', update)
    
    radioselectDay = RadioButtonGroup(labels=['Fri', 'Sat', 'Sun'], active=0)
    radioselectDay.on_change('active', update)
    
    controls = column(selectId, radioselectDay, width=200)

    # Create the plot
    trajectoryCur = load_trajectory_data(selectId.value)
    checkInsCur = load_checkin_data(selectId.value)
    
    p = make_plot(trajectoryCur, checkInsCur)
    
    # Create a layout for the tab and initialize it
    layout = row(controls, p)
    tab = TabPanel(child=layout, title='Individual visitor')
    
    return tab
  
