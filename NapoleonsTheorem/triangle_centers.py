from manim import *
import numpy as np

class TriangleCenters(Scene):
    def get_centroid(self, A, B, C):
         return (A + B + C) / 3

    def get_circumcenter(self, A, B, C):
        M = np.array([
            2 * (B - A)[:2],
            2 * (C - A)[:2]
        ])
                     
        rhs = np.array([
            np.dot(B, B) - np.dot(A, A),
            np.dot(C, C) - np.dot(A, A)
        ])

        return np.array([
             *np.linalg.solve(M, rhs),
             0
        ])

    def get_incenter(self, A, B, C):
         side_a = np.linalg.norm(B - C)
         side_b = np.linalg.norm(A - C)
         side_c = np.linalg.norm(A - B)

         return (
              side_a * A +
              side_b * B +
              side_c * C
         ) / (side_a + side_b + side_c)

    def get_orthocenter(self, A, B, C):
         return A + B + C - 2 * self.get_circumcenter(A, B, C)
    
    def construct(self):

        # Triangle positions on screen
        posCenters = [
            LEFT * 4.8,
            LEFT * 1.6,
            RIGHT * 1.6,
            RIGHT * 4.8
        ]

        # Makes one base triangle, then moves to four centers
        A = np.array([-1.0, -1.0, 0])
        B = np.array([1.0, -1.0, 0])
        C = np.array([0.0, 1.0, 0])

        triangles = []
        center_dots = []

        # Now actually create the triangles
        for position in posCenters:
            triangle = Polygon(
                A + position,
                B + position,
                C + position,
                stroke_width = 10,
                color = "white"
            )

            triangles.append(triangle)

        # Calculate triangle centers
        for position in posCenters:
            a = A + position
            b = B + position
            c = C + position

            center_dots.append([
                Dot(self.get_centroid(a, b, c)),
                Dot(self.get_circumcenter(a, b, c)),
                Dot(self.get_incenter(a, b, c)),
                Dot(self.get_orthocenter(a, b, c))
            ])

        # Pick a center for each triangle
        dots = [
            center_dots[0][0], # Centroid
            center_dots[1][1], # Circumcenter
            center_dots[2][2], # Incenter
            center_dots[3][3] # Orthocenter
        ]

        # Labels
        labels = [
            Text("Centroid").scale(0.6),
            Text("Circumcenter").scale(0.6),
            Text("Incenter").scale(0.6),
            Text("Orthocenter").scale(0.6)
        ]

        for label, position in zip(labels, posCenters):
            label.move_to(position + UP * 1.7)

        # Animation
        self.play(
            *[FadeIn(triangle) for triangle in triangles]
        )

        self.play(
            *[FadeIn(dot) for dot in dots]
        )

        self.play(
            *[Write(label) for label in labels]
        )

        self.wait(1)

        # TODO: Fix these triangles. 
        # They don't update with the correct centers / positions

        triangle_shapes = [
            # Triangle 1
            (
                np.array([-0.5, -1.0, 0]),
                np.array([0.5, -1.0, 0]),
                np.array([0.3, 1.5, 0])
            )
        ]

        for A_new, B_new, C_new in triangle_shapes:
            new_triangles = []
            new_centers = []

            for position in posCenters:
                a = A_new + position
                b = B_new + position
                c = C_new + position

                new_triangles.append(
                    Polygon(a, b, c, stroke_width=10, color="white")
                )

                new_centers.append([
                    self.get_centroid(a, b, c),
                    self.get_circumcenter(a, b, c),
                    self.get_incenter(a, b, c),
                    self.get_orthocenter(a, b, c)
                ])

        self.play(
            # Triangle 1
            triangles[0].animate.become(new_triangles[0]),
            dots[0].animate.move_to(new_centers[0][0]),

            # Triangle 2
            triangles[1].animate.become(new_triangles[1]),
            dots[1].animate.move_to(new_centers[1][1]),

            # Triangle 3
            triangles[2].animate.become(new_triangles[2]),
            dots[2].animate.move_to(new_centers[2][2]),

            # Triangle 4
            triangles[3].animate.become(new_triangles[3]),
            dots[3].animate.move_to(new_centers[3][3]),

            run_time=3,
        )

        self.wait()