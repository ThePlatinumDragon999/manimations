from manim import *

class GraphConfig:
    def __init__(self, vertices, edges, layout):
        self.vertices = vertices
        self.edges = edges
        self.layout = layout

    def get_graph(self):
        return Graph(
            self.vertices,
            self.edges,
            layout=self.layout,
            vertex_config={
                "radius": 0.18,
            },
            edge_config={
                "stroke_width": 6,
            },
        )

    def get_adjacency_list(self):
        g = [[] for _ in self.vertices]

        for u, v in self.edges:
            g[u].append(v)
            g[v].append(u)

        return g

def cycle_graph_5():
    vertices = [0,1,2,3,4]

    edges = [
        (0,1),
        (1,2),
        (2,3),
        (3,4),
        (4,0),
    ]

    layout = {
        0: UP*2,
        1: RIGHT*2,
        2: RIGHT*2+DOWN*2,
        3: LEFT*2+DOWN*2,
        4: LEFT*2,
    }

    return GraphConfig(vertices, edges, layout)

def grid_graph_3x3():

    vertices = list(range(9))

    edges = []

    # horizontal edges
    for row in range(3):
        for col in range(2):
            edges.append(
                (row*3+col, row*3+col+1)
            )

    # vertical edges
    for row in range(2):
        for col in range(3):
            edges.append(
                (row*3+col, (row+1)*3+col)
            )

    layout = {}

    for row in range(3):
        for col in range(3):
            vertex = row*3+col
            layout[vertex] = (
                (col-1)*RIGHT +
                (1-row)*UP
            )

    return GraphConfig(vertices, edges, layout)

def grid_graph_4x4():

    vertices = list(range(16))

    edges = []

    # horizontal edges
    for row in range(4):
        for col in range(3):
            edges.append(
                (row*4+col, row*4+col+1)
            )

    # vertical edges
    for row in range(3):
        for col in range(4):
            edges.append(
                (row*4+col, (row+1)*4+col)
            )

    layout = {}

    for row in range(4):
        for col in range(4):
            vertex = row*4+col
            layout[vertex] = (
                (col-1)*RIGHT +
                (1-row)*UP
            )

    return GraphConfig(vertices, edges, layout)