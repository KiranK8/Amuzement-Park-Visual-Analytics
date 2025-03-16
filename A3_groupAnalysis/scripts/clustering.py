# clustering routines
from scipy.cluster.hierarchy import linkage, to_tree, fcluster
from sklearn.preprocessing import StandardScaler

# pandas for data tables
import pandas as pd

# networkx for graph representation
import networkx as nx

# priority queue for cluster selection
import queue as Q

class Clustering:
    '''
    
    '''
    
    # The clustering info as scipy.linkage output
    root = None
    
    # The number of clusters
    nclusters = 0

    # colors for the clusters
    colors10 = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
    colors = ['#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5', '#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f', '#c7c7c7', '#bcbd22', '#dbdb8d', '#17becf', '#9edae5']
    
    def __init__(self):
        self.nclusters = 0
      
    def getDendrogram( self, root ):
        # the final dendrogram
        G = nx.DiGraph()

        # priority queue for cluster selection with high distance values
        q = Q.PriorityQueue()
        
        # init the queue with the root node, 
        # negative distance for inverse sorting
        q.put((-root.dist,root))
        
        # the root node is always part of the dendrogram
        G.add_node( root.id, count=root.count, dist=root.dist, x=0 )
        
        # counter for leaves in dendrogram (which is the number of clusters)
        i = 1

        # split clusters until we have enough
        while i < self.nclusters:
            # split the cluster with the highest distance value
            k,n = q.get()

            # add respective nodes and edges to the dendrogram
            G.add_node( n.left.id, count=n.left.count, dist=n.left.dist, x=0 )
            G.add_edge( n.id, n.left.id )
            G.add_node( n.right.id, count=n.right.count, dist=n.right.dist, x=0 )
            G.add_edge( n.id, n.right.id )

            i += 1

            # if the children are internal nodes store them in the queue 
            # for splitting
    
            if n.left.left is not None:
                q.put((-n.left.dist,n.left))
            if n.right.right is not None:
                q.put((-n.right.dist,n.right))
        
        return G

    
    def computeLayout( self, G ):
        xmin = 5
        color = 0
        nleaves = (len(G.nodes.keys())+1)/2

        for i in nx.dfs_postorder_nodes( G, source=list(G.nodes.keys())[0] ):
            if G.out_degree(i) == 0:
                G.nodes[i]['x'] = xmin
                xmin += 5
                G.nodes[i]['color'] = self.colors[color]

                color += 1
            else:
                x = 0
                cnt = 0

                for j in G.successors(i):
                    x += G.nodes[j]['x']
                    if G.nodes[j]['count'] > cnt:
                        G.nodes[i]['color'] = G.nodes[j]['color']
                        cnt = G.nodes[j]['count']
                G.nodes[i]['x'] = x/2
                
        return G
                    
    # compute the color for each datapoint according to its cluster
    def computeColors( self, Z ):
        ids = fcluster( Z, self.nclusters, criterion='maxclust' )
        return [self.colors[i-1] for i in ids]

        
    def computeClustering( self, df, nclusters = 0 ):
        # if nclusters is unspecified, report the full tree
        if nclusters == 0:
            self.nclusters = len(df)
        else:
            self.nclusters = nclusters
        
        for i in df.columns:
            if isinstance( df.loc[0,i], pd.Timestamp ) or \
               isinstance( df.loc[0,i], pd.Timedelta ):
               df.loc[:,i] =  (df.loc[:,i] - pd.Timestamp('06.06.2014 08:00:00')).astype('timedelta64[ns]')

        # normalize data
        X = StandardScaler().fit_transform(df)

        # compute the clustering hierarchy
        Z = linkage( X, 'ward' )
        
        # create the full clustering tree
        self.root = to_tree( Z )
        
        # generate a graph for the dendrogram
        dendrogram = self.getDendrogram( self.root )
        
        # compute the positions for the nodes
        dendrogram = self.computeLayout( dendrogram )
        
        # compute the colors for each original datapoint
        colors = self.computeColors( Z )
        
        return (dendrogram, colors)
