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

def grid_graph(rows, cols):

    vertices = list(range(rows * cols))

    edges = []

    # horizontal edges
    for row in range(rows):
        for col in range(cols - 1):
            edges.append(
                (row * cols + col,
                 row * cols + col + 1)
            )

    # vertical edges
    for row in range(rows - 1):
        for col in range(cols):
            edges.append(
                (row * cols + col,
                 (row + 1) * cols + col)
            )

    layout = {}

    for row in range(rows):
        for col in range(cols):
            vertex = row * cols + col
            layout[vertex] = (
                (col - (cols-1)/2) * RIGHT +
                ((rows-1)/2 - row) * UP
            )

    return GraphConfig(vertices, edges, layout)