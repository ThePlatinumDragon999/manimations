from dominatingSetCalc import minimum_dominating_set
from manim import *
import graphConfigs

class DominatingSet4(Scene):
    def construct(self):

        config = graphConfigs.grid_graph_4x4()

        graph = config.get_graph()

        g = config.get_adjacency_list()

        S = minimum_dominating_set(g)

        # Actal Manim code now
        self.add(graph)

        self.play(
            LaggedStart(
                *[
                    graph.vertices[v].animate
                        .set_fill("#b00b69")
                        .scale(1.5)
                    for v in S
                ],
                lag_ratio=0.2
            )
        )

        self.wait(2)