import pandas as pd
import numpy as np

from bokeh.models import DataRange1d, FactorRange, ColumnDataSource, LabelSet, HoverTool
from bokeh.plotting import figure
from bokeh.layouts import gridplot
from bokeh.models import Legend

#import plots
import datetime

class Scatterplots:
    '''
    Create a scatterplot matrix of the given data.
    '''
    source = ColumnDataSource()
    
    plot = gridplot(children=[], ncols=3)
    
    def __init__(self, source: ColumnDataSource, splom_width=0, nbins_histogram=0, **kwargs ):
        if not isinstance(source, ColumnDataSource ):
            raise TypeError("source has to be a pandas DataFrame. Received ", type(source))

        self.source = source
        
        # Read the keyword arguments and set defaults if not provided
        cols      = kwargs['cols']      if 'cols'      in kwargs else source.column_names 
        x_padding = kwargs['x_padding'] if 'x_padding' in kwargs else 40
        y_padding = kwargs['y_padding'] if 'y_padding' in kwargs else 80
        width     = int(splom_width / (len(cols)+1)) if splom_width > 0 else 300
        height    = int(splom_width / (len(cols)+1)) if splom_width > 0 else 300

        if 'color' not in self.source.column_names:
            self.source.add( ['#1f77b4']*len(source.data[source.column_names[0]]), 'color' )
        
    
        TOOLS = "box_select,lasso_select,pan,wheel_zoom,reset,save,help"
    
        plots = []
        
        for i,j in cols:
            myargs = self.getAxisParameters( source, j, i )
            p = figure( tools=TOOLS, width=width, height=height, **myargs )
            p.xaxis.axis_label = i
            p.yaxis.axis_label = j

            p.scatter( source=self.source, x=i, y=j, color='color' )
            plots.append(p)
        
        #self.setAxisTitles( plots, cols, x_padding, y_padding )
        
        self.plot = gridplot([plots])

    def getAxisParameters( self, source, x, y ):
        '''
        Return axis formatting parameters (numeric vs. categorical).
        '''
        args = {}
        if isinstance( source.data[x][0], np.datetime64 ):
              args['x_axis_type'] = "datetime"
        if x != y and isinstance( source.data[y][0], np.datetime64 ) :
            args['y_axis_type'] = "datetime"
        
        return args

    def updateColors( self, colors ):
        self.source.data['color'] = colors
