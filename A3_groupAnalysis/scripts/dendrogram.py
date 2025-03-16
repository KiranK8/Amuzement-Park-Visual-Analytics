from bokeh.models import ColumnDataSource, GlyphRenderer, Circle, MultiLine

class DendrogramRenderer():
    '''Renderer for dendrograms/trees represented as a networkx directed graph.'''
    
    
    # renderers for nodes and edges
    # node_renderer = GlyphRenderer()
    # edge_renderer = GlyphRenderer()
    
    def __init__(self):
        # Data sources to store nodes and edges.
        # ColumnDataSource has a signalling mechanism for changes in the data that causes plots that use them to update.
        self.nodes = ColumnDataSource(data=dict(x=[],y=[],color=[],size=[]))
        self.edges = ColumnDataSource(data=dict(xs=[],ys=[],color=[]))
        self.node_renderer = GlyphRenderer(
            glyph=Circle(x='x', y='y', fill_color='color', line_color='color', radius='size'), data_source=self.nodes)
        self.edge_renderer = GlyphRenderer(
            glyph = MultiLine(xs='xs', ys='ys', line_color='color'), data_source=self.edges)
    
    # Generate the edge datasource from a given graph
    def createEdges(self, G):
        xs = []
        ys = []
        colors = []
        
        for i in G.nodes.keys():
            if G.out_degree(i) > 0:
                for j in G.successors(i):
                    xs.append([ G.nodes[j]['x'], G.nodes[j]['x'],G.nodes[i]['x'] ])
                    ys.append([ G.nodes[j]['dist'], G.nodes[i]['dist'],G.nodes[i]['dist'] ])
                    colors.append(G.nodes[j]['color'])
        
        self.edges.data = dict( xs=xs, ys=ys, color=colors )
    
    # create datasources representing the given graph
    def update(self, G):
        # print('DendrogramRenderer.update')
        n = max([ k['count'] for i,k in G.nodes.data() ])
        self.nodes.data = dict(
            x=[ k['x'] for i,k in G.nodes.data() ], 
            y=[ k['dist'] for i,k in G.nodes.data() ], 
            size=[ 0.5 + k['count']/n*1.25 for i,k in G.nodes.data() ], 
            color=[ k['color'] for i,k in G.nodes.data() ])
        self.createEdges(G)
