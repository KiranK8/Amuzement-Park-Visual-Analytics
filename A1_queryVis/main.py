# Bokeh basics
from bokeh.io import curdoc
from bokeh.models.layouts import Tabs

# Each tab comes from one script
from scripts.task1_individual_visitor import individual_visitor
from scripts.task2_visitor_count import visitor_count
from scripts.task3_visit_timespan import visit_timespan


# Create each of the tabs
tab1 = individual_visitor()
tab2 = visitor_count()
tab3 = visit_timespan()

# Put all the tabs into one application
tabs = Tabs(tabs=[tab1, tab2, tab3])

# Put the tabs in the current document for display
curdoc().add_root(tabs)
