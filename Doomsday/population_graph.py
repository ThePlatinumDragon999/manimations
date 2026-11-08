from manim import *
import random
import numpy as np

# I really should document this better since not everyone has my math background.
# The following two functions are implementing a classic computational geometry trick for
# determining whether two lines intersect.

# ccw (clockwise or counterclockwise) determines whether the pointd are arranged counterclocwise or clockwise
# (with a particular convention if the points are collinear)
# So if it is clockwise, it means going from a to b to c means you do a right turn, and if it is counterclockwise,
# you do a left turn.

# Mathematically, you can use the 2D cross product (3D cross product with Z = 0)
# If you have vectors AB = B - A and AC = C - A, then the 2d cross product is
# AB x AC = (B_x - A_x)(C_y - A_y) - (B_y - A_y)(C_x - A_x)
# The sign tells us orientation. Positive is counterclockwise, negative is clockwise, and 0 is collinear

# I take the negative of the above expression since that makes the math easier
# So it turns True for clockwise orientation, rather than counterclockwise
def ccw(A, B, C):
    return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])

# We have two line segments, AB and CD. This function checks whether they intersect.
def segments_intersect(A, B, C, D):
    # If segments share an endpoint (connected to the same human), they don't cross
    # np.allclose() checks whether two NumPy arrays are approximately equal (since floating point
    # coordinates can have tiny numerical inaccuracies)
    if np.allclose(A, C) or np.allclose(A, D) or np.allclose(B, C) or np.allclose(B, D):
        return False

    # The first condition checks whether A and B lie on opposite sides of line CD
    # If they do, the segment AB crosses the infinity line passing through CD
    # The second condition checks whether C and D lie on opposite sides of the line AB

    # It works in the general case. It does not, however, work for collinear points.
    # That is too much of a hassle to deal with right now.
    return (ccw(A, C, D) != ccw(B, C, D)) and (ccw(A, B, C) != ccw(A, B, D))

class RandomSVGGraph(MovingCameraScene):
    def construct(self):
        # Set random seed for reproducible graph
        random.seed(43)
        np.random.seed(42)

        x_bound = 22
        y_bound = 12

        # distance
        spawn_distance = 2.0

        node_template = SVGMobject("mini_human.svg")
        node_template.scale(0.8)
        node_template.set_z_index(2)

        node_radius = max(node_template.width, node_template.height) / 2 * 0.9

        num_nodes = 300
        positions = []
        for _ in range(num_nodes):
            attempts = 0
            max_attempts = 1000
            placed = False

            while attempts < max_attempts:
                pos = np.array([
                    random.uniform(-x_bound, x_bound),
                    random.uniform(-y_bound, y_bound),
                    0
                ])

                if all(np.linalg.norm(pos - p) > spawn_distance for p in positions):
                    positions.append(pos)
                    placed = True
                    break

                attempts += 1

            if not placed:
                print(f"Notice: Stopped adding nodes at {len(positions)} due to spatial density limits.")
                break

        num_nodes = len(positions)

        # Create the node mobjects at the chosen positions
        nodes = VGroup()
        for pos in positions:
            node = node_template.copy().move_to(pos)
            nodes.add(node)

        # Create the edges needed via connection radius threshold
        edges = VGroup()
        edges.set_z_index(1)

        # max distance for connections to form
        connection_radius = 10
        # This prevents any one human from taking all of the connections
        max_degree = 5
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

            # Check if the edge passes too close to any intermediate node (person)
            passes_through_node = False
            for k in range(num_nodes):
                if k == i or k == j:
                    continue

                # Calculates distance from node k to line segment (p1, p2)
                ab = p2 - p1
                ab_len_sq = np.dot(ab, ab)
                if ab_len_sq > 0:
                    t = np.dot(positions[k] - p1, ab) / ab_len_sq
                    t = max(0.0, min(1.0, t))
                    proj = p1 + t * ab
                    if np.linalg.norm(positions[k] - proj) < node_radius * 1.3:
                        passes_through_node = True
                        break

            if passes_through_node:
                continue

            # Check if this new edge intersects any already accepted edge
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
                    p1,
                    p2
                )
                edges.add(edge)

        self.play(
            *[GrowFromCenter(node) for node in nodes],
            run_time=2
        )

        self.play(FadeIn(edges), run_time=1.5)

        self.wait(1)

        self.play(
            self.camera.frame.animate.scale(2.2),
            run_time=2.5
        )
        self.wait(1)