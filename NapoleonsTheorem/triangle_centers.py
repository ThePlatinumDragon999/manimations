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

        # Calculate centers
        for position in centers:
            a = A + position
            b = B + position
            c = C + position

            # Centroid
            centroid = (a + b + c) / 3

            # Circumcenter
            circumcenter = self.get_circumcenter(a, b, c)

            # Incenter
            side_a = np.linalg.norm(b - c)
            side_b = np.linalg.norm(a - c)
            side_c = np.linalg.norm(a - b)

            incenter = (
                side_a * a + side_b * b + side_c * c
            ) / (side_a + side_b + side_c)

            # Orthocenter
            orthocenter = a + b + c - 2 * circumcenter

            center_dots.append([
                Dot(centroid),
                Dot(circumcenter),
                Dot(incenter),
                Dot(orthocenter)
            ])

        # Pick a center for each triangle
        dots = [
            center_dots[0][0], # Centroid
            center_dots[1][1], # Circumcenter
            center_dots[2][2], # Incenter
            center_dots[3][3] # Orthocenter
        ]

        # Animation
        self.play(
            *[FadeIn(triangle) for triangle in triangles]
        )

        self.play(
            *[FadeIn(dot) for dot in dots]
        )

        self.wait()

    def get_circumcenter(self, A, B, C):
        M = np.array([
            2 * (B - A)[:2],
            2 * (C - A)[:2]
        ])

        rhs = np.array([
            np.dot(B, B) - np.dot(A, A),
            np.dot(C, C) - np.dot(A, A)
        ])

        center = np.linalg.solve(M, rhs)

        return np.array([center[0], center[1], 0])