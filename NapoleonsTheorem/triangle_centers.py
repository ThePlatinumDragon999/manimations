from manim import *
import numpy as np

class TriangleCenters(Scene):
    def construct(self):

        # Triangle positions
        centers = [
            LEFT * 4.5,
            LEFT * 1.5,
            RIGHT * 1.5,
            RIGHT * 4.5
        ]

        # Makes one base triangle, then moves to four centers
        A = np.array([-1.0, -1.0, 0])
        B = np.array([1.0, -1.0, 0])
        C = np.array([0.0, 1.0, 0])

        triangles = []
        center_dots = []

        # Now actually create the triangles
        for position in centers:
            triangle = Polygon(
                A + position,
                B + position,
                C + position
            )

            triangles.append(triangle)

        # TODO: centers

        # Animation
        self.play(
            LaggedStart(
                *[Create(triangle) for triangle in triangles],
                lag_ratio = 0.5
            )
        )

        self.wait()