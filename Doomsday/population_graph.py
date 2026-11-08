from manim import *
import random

class RandomSVGGraph(Scene):
    def construct(self):
        # Set random seed for reproducible graph
        random.seed(42)

        node_template = SVGMobject("mini_human.svg")
        node_template.scale(0.8)
        node_template.set_z_index(2)

        num_nodes = 12
        positions = []
        for _ in range(num_nodes):
            while True:
                pos = np.array([
                    random.uniform(-7, 7),
                    random.uniform(-3.2, 3.2),
                    0
                ])

                if all(np.linalg.norm(pos - p) > 2.0 for p in positions):
                    positions.append(pos)
                    break

        # Create the node mobjects at the chosen positions
        nodes = VGroup()
        for pos in positions:
            node = node_template.copy().move_to(pos)
            nodes.add(node)

        # Create the edges needed
        edges = VGroup()
        edges.set_z_index(1)
        connected_pairs = set()

        # Connect each node to 1 - 3 random neighbors to form a sparse graph
        for i, pos_i in enumerate(positions):
            possible_neighbors = [j for j in range(num_nodes) if j != i]
            num_connections = random.randint(1, 3)
            chosen_neighbors = random.sample(possible_neighbors, min(num_connections, len(possible_neighbors)))

            for j in chosen_neighbors:
                pair = tuple(sorted((i, j)))
                if pair not in connected_pairs:
                    connected_pairs.add(pair)
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