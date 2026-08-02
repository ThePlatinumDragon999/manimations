from dominatingSetCalc import minimum_dominating_set
from manim import *

class DominatingSet1(Scene):
    def construct(self):
        vertices = [0,1,2,3,4]

        edges = [
            (0,1),
            (1,2),
            (2,3),
            (0,3),
            (3,4),
            (2,4),
        ]

        graph = Graph(
            vertices, 
            edges)

        g = [[] for _ in vertices]

        for u, v in edges:
            g[u].append(v)
            g[v].append(u)

        S = minimum_dominating_set(g)

        # Actal Manim code now
        self.play(FadeIn(graph))

        self.play(
            AnimationGroup(
                *[
                graph.vertices[v].animate.set_fill("#b00b69")
                for v in S
                ]
            )
        )

        self.wait(2)

        self.play(FadeOut(graph))