import networkx as nx
import matplotlib.pyplot as plt
import scipy

import plotly.offline as py
import plotly.graph_objects as go
import networkx as nx

def graph_network(households, offices, infected_people, unique_locations, N, N_households, N_offices):
    g = nx.Graph()

    for i in range(N):
            g.add_edge(households[i],offices[i])

    color_map = []
    for node in g:
        if node in unique_locations:
            color_map.append('red')
        elif node <= N_households:
            color_map.append('orange')
        else: 
            color_map.append('blue')

    pos_ = nx.spring_layout(g)

    def make_edge(x, y, colour, text):
        return  go.Scatter(x=x, y=y, hoverinfo="text",line=dict(color = colour), text = ([text]), mode='lines')

    # For each edge, make an edge_trace, append to list
    edge_trace = []
    i = 1
    for edge in g.edges():
        i_1 = edge[0]
        i_2 = edge[1]

        x0, y0 = pos_[i_1]
        x1, y1 = pos_[i_2]

        if i in infected_people:
            trace = make_edge([x0, x1, None], [y0, y1, None], 'red', str(i))
        else:
            trace  = make_edge([x0, x1, None], [y0, y1, None], 'cornflowerblue', text=str(i))

        edge_trace.append(trace)
        i += 1

    node_trace = go.Scatter(x         = [],
                            y         = [],
                            text      = [],
                            textposition = "middle center",
                            mode = "markers",
                            marker    = dict(color=color_map, size=10))
    for node in g.nodes():
        x, y = pos_[node]
        node_trace['x'] += tuple([x])
        node_trace['y'] += tuple([y])
        node_trace['text'] += tuple(["House/Office Index " + str(node)])
            # Customize layout
    layout = go.Layout(
        paper_bgcolor='rgba(0,0,0,0)', # transparent background
        plot_bgcolor='rgba(0,0,0,0)', # transparent 2nd background
        xaxis =  {'showgrid': False, 'zeroline': False}, # no gridlines
        yaxis = {'showgrid': False, 'zeroline': False}, # no gridlines
    )
    
    # Create figure
    fig = go.Figure(layout = layout)
    # Add all edge traces
    for trace in edge_trace:
        fig.add_trace(trace)
    # Add node trace
    fig.add_trace(node_trace)
    # Remove legend
    fig.update_layout(showlegend = False)
    # Remove tick labels
    fig.update_xaxes(showticklabels = False)
    fig.update_yaxes(showticklabels = False)
    # Show figure
    fig.show()