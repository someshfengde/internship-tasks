# there will be multiple ap's we have the distances from each AP to the other AP's.
# input will be graph and output will be the channel allocation for the graph.
# we will use the channel allocation to calculate the interference.
# for working with the graph we will use the networkx library.
# we have no of AP's and the distance between them, The number of devices we have to allocate is also given.
#%%
import random
import networkx as nx
import matplotlib.pyplot as plt

NO_CHANNELS = 5
DIST_BEFORE_INTERFERENCE = 10

def input_data():
    """
    function for taking input no of devices and no of AP's, distances between each ap and the other ap's.)
    """
    no_of_aps = int(input("Enter the number of AP's: "))
    distances = []
    for i in range(no_of_aps):
        distances.append([])
        for j in range(no_of_aps):
            if i == j : 
                distances[i].append(0)
            else:
                if j < i and distances[j][i] != 0:
                    distances[i].append(distances[j][i])
                else: 
                    distances[i].append(int(input("Enter the distance between AP"+str(i+1)+" and AP"+str(j+1)+": ")))
    return no_of_aps, distances


def visualize(no_of_aps, distances):
    """
    visualizing based on above input_data
    """
    G = nx.Graph()
    G.add_nodes_from(range(no_of_aps))
    for i in range(no_of_aps):
        for j in range(no_of_aps):
            if distances[i][j] != 0:
                G.add_edge(i, j, weight=distances[i][j])
    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, node_size=500)
    nx.draw_networkx_edges(G, pos, width=6)

    labels = {}
    for u,v,data in G.edges(data=True):
        labels[(u,v)] = data['weight']
    nx.draw_networkx_labels(G, pos, font_size=20, font_family='sans-serif')
    nx.draw_networkx_edge_labels(G,edge_labels=labels, pos=nx.spring_layout(G),font_size=10)
    plt.axis('off')
    plt.show()

def channel_allocation(no_of_aps, distances):
    """
    allocating channel to every AP 
        inputs: no_of_aps ( total no of AP we have) 
        distances: the distances between each AP and the other AP's
    """
    allocated_channels = {}
    for i in range(no_of_aps):
        allocated_channels[i] = (random.choice(range(NO_CHANNELS)))
    return allocated_channels

#%%
no_of_aps, distances = input_data()

#%% 
visualize(no_of_aps, distances)
#%%
allocated_channels = channel_allocation(no_of_aps, distances)
# %%
#function for visualizing the channel allocation based on the graph showing colors according to allocated channels 
def visualize_channel_allocation(no_of_aps, allocated_channels, distances):
    """
    visualizing the channel allocation based on the graph showing colors according to allocated channels
    """
    G = nx.Graph()
    G.add_nodes_from(range(no_of_aps))
    for i in range(no_of_aps):
        for j in range(no_of_aps):
            if distances[i][j] != 0:
                G.add_edge(i, j, length = distances[i][j])
    labels = {}
    for u,v,data in G.edges(data=True):
        labels[(u,v)] = data['length']
    nx.draw_networkx_edge_labels(G,edge_labels=labels, pos=nx.spring_layout(G),font_size=10)
    nx.draw(G,  labels = dict(allocated_channels), with_labels = True)
    plt.axis(False)
    plt.show()

# %%
visualize_channel_allocation(no_of_aps, allocated_channels, distances)

# function for calculating the interference based on the channel allocation
def interference(no_of_aps, allocated_channels, distances):
    """
    calculating the interference based on the channel allocation
    """
    interference = 0
    for i in range(no_of_aps):
        if list(allocated_channels.values()).count(allocated_channels[i]) > 1 : 
            index = [i for i, x in enumerate(allocated_channels.values()) if x == allocated_channels[i]]
            for j in index:
                if distances[i][j] < DIST_BEFORE_INTERFERENCE:
                    interference += 1
    return interference


# %%
interference(no_of_aps, allocated_channels, distances)
