import networkx as nx #only used for visualization and parsing graph6 format into vertices and edges
import matplotlib.pyplot as plt #used for graph visualization
import random #used for randomly assigning rgb value for each vertex

def is_chordal(vertices, edges):
    neighbors = {vertex: [] for vertex in vertices} #dictionary consisting of neighbors for each vertex
    for e in edges:
        neighbors[e[0]].append(e[1])
        neighbors[e[1]].append(e[0])

    # MCS Algorithm for Ordering
    weights = [0 for vertex in vertices] #initially sets all weights for vertices to 0
    ordering = [] #list for final ordering (the reverse of which will be PEO if the graph is chordal)

    for i in range(0, len(vertices)):
        ordering.append(weights.index(max(weights))) #adds to the ordering the vertex with the largest weight value
        weights[ordering[-1]] = -len(vertices)

        for neighbor in neighbors[ordering[-1]]:
            weights[neighbor]+=1

    ordering = ordering[::-1] #the reverse of the ordering will be the perfect elimination ordering (PEO aka simplicial ordering)
    if not is_simplicial_ordering(neighbors, ordering):
        return None

    return ordering


def is_simplicial_ordering(neighbors, simplicial_ordering):
    ordering = [node for node in simplicial_ordering]
    for index in range(0, len(ordering)): #iterates through each vertex in the ordering
        vertex = ordering[index]
        ordering[index] = -1 #essentially removes vertex from ordering by replacing it with -1

        higher_neighbor = ordering[-1] #sets to the last element in ordering
        for neighbor in neighbors[vertex]: #iterates through the neighbors in vertex to set higher_neighbor to first neighbor that appears in ordering
            if neighbor in ordering and ordering.index(neighbor) < ordering.index(higher_neighbor):
                higher_neighbor = neighbor

        for i in range(0, len(neighbors[vertex])):
            if neighbors[vertex][i] not in ordering or neighbors[vertex][i] == higher_neighbor:
                continue
            if neighbors[vertex][i] not in neighbors[higher_neighbor]:
                return False
    return True


def color_graph(graph):
    chordal_graph = nx.from_graph6_bytes(graph)

    vertices = chordal_graph.nodes()
    edges = chordal_graph.edges()
    neighbors = {vertex: [] for vertex in vertices}  # dictionary consisting of neighbors for each vertex
    for e in edges:
        neighbors[e[0]].append(e[1])
        neighbors[e[1]].append(e[0])

    elimination_ordering = is_chordal(vertices, edges)
    coloring = [-1 for vertex in vertices]

    if elimination_ordering is None:
        print("Not Chordal Graph")
        return [-1]

    for i in range(len(elimination_ordering)-1, -1, -1):
        cur_vertex = elimination_ordering[i]
        color = coloring[cur_vertex]+1
        for neighbor in neighbors[cur_vertex]:
            if color == coloring[neighbor]:
                color+=1
        coloring[cur_vertex] = color

    print("perfect elimination ordering:",elimination_ordering)
    print("vertices:", vertices)
    print("coloring of vertices:", coloring)
    return coloring



def visualize(graph, color_order):
    chordal_graph = nx.from_graph6_bytes(graph)
    hex_coloring = {vertex:(255,255,255)for vertex in color_order}

    color_index = 0
    for c in color_order:
        if hex_coloring[c] == (255,255,255):
            #in an attempt to ensure that each vertex color appears visually distinct
            hex_coloring[c] = (
                255 if color_index%6 in [0,4,5] else random.randint(0,127), #red
                255 if color_index%6 in [1,3,5] else random.randint(0,127), #green
                255 if color_index%6 in [2,3,4] else random.randint(0,127)  #blue
            )
            color_index+=1 #to iterate through colors red, green, magenta, cyan, yellow

    #converting rgb tuple to hex values for visual
    coloring = [f"#{hex_coloring[color][0]:02X}{hex_coloring[color][1]:02X}{hex_coloring[color][2]:02X}" for color in color_order]
    print("assigned hex values for color:", coloring)


    nx.draw_networkx(chordal_graph, nx.circular_layout(chordal_graph), with_labels=True, node_color=coloring, font_weight='bold')
    plt.show()

if __name__ == "__main__":
    graph6 = b'ICOcaRozG'  #graph to test if chordal (bytes in graph6 format)
    colors = color_graph(graph6)
    visualize(graph6,colors)

