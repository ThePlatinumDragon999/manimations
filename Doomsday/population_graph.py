from manim import *
import random
import numpy as np

# Helper function to check if two line segments cross each other:
def ccw(A, B, C):
    return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])

def segments_intersect(A, B, C, D):
    # If segments share an endpoint (connected to the same human), they don't cross
    if np.allclose(A, C) or np.allclose(A, D) or np.allclose(B, C) or np.allclose(B, D):
        return False
    return (ccw(A, C, D) != ccw(B, C, D)) and (ccw(A, B, C) != ccw(A, B, D))

class RandomSVGGraph(Scene):
    def construct(self):
        # Set random seed for reproducible graph
        random.seed(42)
        np.random.seed(42)

        # distance
        spawn_distance = 2.0

        node_template = SVGMobject("mini_human.svg")
        node_template.scale(0.8)
        node_template.set_z_index(2)

        num_nodes = 20
        positions = []
        for _ in range(num_nodes):
            while True:
                pos = np.array([
                    random.uniform(-7, 7),
                    random.uniform(-3.2, 3.2),
                    0
                ])

                if all(np.linalg.norm(pos - p) > spawn_distance for p in positions):
                    positions.append(pos)
                    break

        # Create the node mobjects at the chosen positions
        nodes = VGroup()
        for pos in positions:
            node = node_template.copy().move_to(pos)
            nodes.add(node)

        # Create the edges needed via connection radius threshold
        edges = VGroup()
        edges.set_z_index(1)

        # max distance for connections to form
        connection_radius = 5
        # This prevents any one human from taking all of the connections
        max_degree = 3
        degrees = {i : 0 for i in range(num_nodes)}

        # Check every unique pair of nodes
        candidates = []
        for i in range(num_nodes):
            for j in range(i + 1, num_nodes):
                distance = np.linalg.norm(positions[i] - positions[j])

                # Connect if they fall within the specified radius
                if distance <= connection_radius:
                    candidates.append((i, j, distance))

        random.shuffle(candidates)

        accepted_edges = []
        for i, j, distance in candidates:
            if degrees[i] >= max_degree or degrees[j] >= max_degree:
                continue

            p1, p2 = positions[i], positions[j]

            # Check if this new edge intersecvts any already accepted edge
            intersects = False
            for (u, v) in accepted_edges:
                q1, q2 = positions[u], positions[v]
                if segments_intersect(p1, p2, q1, q2):
                    intersects = True
                    break

            # If it doesn't cross anything, accept the connection
            if not intersects:
                accepted_edges.append((i, j))
                degrees[i] += 1
                degrees[j] += 1

                edge = DashedLine(
                    positions[i],
                    positions[j]
                )
                edges.add(edge)

        self.play(
            LaggedStart(
                *[GrowFromCenter(node) for node in nodes],
                lag_ratio=0.1
            ),
            run_time=2
        )

        self.play(FadeIn(edges, lag_ratio=0.1), run_time=1.5)
        self.wait(1)