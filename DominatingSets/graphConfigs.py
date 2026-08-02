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

def cycle_graph(n, radius=2):

    vertices = list(range(n))

    edges = []

    for i in range(n):
        edges.append(
            (i, (i+1) % n)
        )

    layout = {}

    for i in range(n):
        theta = 2 * PI * i / n

        layout[i] = (
            radius * np.cos(theta) * RIGHT +
            radius * np.sin(theta) * UP
        )

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

def path_graph(n, spacing=1):

    vertices = list(range(n))

    edges = []

    for i in range(n-1):
        edges.append(
            (i, i+1)
        )

    layout = {}

    for i in range(n):
        layout[i] = (
            (i - (n-1)/2) * spacing * RIGHT
        )

    return GraphConfig(vertices, edges, layout)