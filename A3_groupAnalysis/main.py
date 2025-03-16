import numpy as np
import pandas as pd

from bokeh.models.widgets import Slider, Button, CheckboxGroup, Div
from bokeh.layouts import row, column
from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource

from scripts.dendrogram import DendrogramRenderer
from scripts.clustering import Clustering
from scripts.plotting import Scatterplots


def updateSelectionInfo(attr, old, new):
    selectedIds.text = "Selected Ids: "+' '.join([str(source.data['id'][i]) for i in new])


data = pd.read_csv('A3_groupAnalysis/data/groups.csv', index_col=0,
                   parse_dates=['Arrival','Departure'])
source = ColumnDataSource(data)
source.selected.on_change('indices', updateSelectionInfo)


# callback to handle a change in the clustering settings
def updateClustering():
    nclusters = nclusterslider.value
    labels = [ features.labels[i] for i in features.active ]
    clu = Clustering()
    button.button_type = 'warning'
    try:
        den, colors = clu.computeClustering(data.loc[:,labels], nclusters=nclusters)
        print('Successfully clustered')
        button.button_type = 'success'
        scatter.updateColors(colors)
        renderer.update(den)
    except Exception as e:
        print(e)
        button.button_type = 'danger'


# create the controls
def createControls():
    global features
    divFeatures = Div(text="""<b>Active features</b>""", width=170, height=20)
    fvals = sorted(list(data.columns), key=lambda s: s.lower())
    #features = CheckboxGroup(labels=fvals, active=list(range(0,len(fvals)-1)))
    features = CheckboxGroup(labels=fvals, active=[2,6])

    global nclusterslider
    nclusterslider = Slider(start=1, end=20, value=1, step=1, title="max clusters", width=170)
    
    global button
    button = Button(label="recompute", button_type="success")
    button.on_click(updateClustering)

    controls = column([divFeatures, features,nclusterslider,button], width=200)
    
    return controls


# create the user control panel
controls = createControls()

# create a figure for the dendrogram
p = figure(width=360, height=840)
p.grid.visible = False
p.xaxis.visible = False

# add renderers for the dendrogram
renderer = DendrogramRenderer()
p.renderers.append(renderer.edge_renderer)
p.renderers.append(renderer.node_renderer)

# create scatterplots
#plot_variables = [('GroupSize', 'Kiddie'), ('CheckinSum', 'Park Time'), ('GroupSize', 'Beer Garden')]
#plot_variables = [('Departure', 'Arrival'),('Kiddie', 'Beer Garden Time'), ('Departure', 'Arrival')]
plot_variables = [('GroupSize', 'Shopping'), ('Shopping', 'Park Time'), ('Thrill', 'GroupSize'), ('GroupSize', 'Kiddie'), ('CheckinSum', 'Park Time'), ('GroupSize', 'Beer Garden'), ('Departure', 'Arrival'),('Kiddie', 'Beer Garden Time'), ('GroupSize', 'Shopping Time')]
scatter = Scatterplots(source, cols=plot_variables)

# update the dendrogram and its rendering
updateClustering()

selectedIds = Div(text="""Selected IDs:""", height=100, width=1200)

# init the GUI
curdoc().add_root(column(row(controls, scatter.plot, p), selectedIds))