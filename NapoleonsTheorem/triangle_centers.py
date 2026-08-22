from manim import *
import numpy as np

class TriangleCenters(Scene):
    def get_centers(self, A, B, C):
            # Centroid
            centroid = (A + B + C) / 3
    
            # Circumcenter
            M = np.array([
                2 * (B - A)[:2],
                2 * (C - A)[:2]
            ])
            
            rhs = np.array([
                np.dot(B, B) - np.dot(A, A),
                np.dot(C, C) - np.dot(A, A)
            ])
            
            circumcenter_2d = np.linalg.solve(M, rhs)
            circumcenter = np.array([
                circumcenter_2d[0],
                circumcenter_2d[1],
                0
            ])
    
            # Incenter
            side_a = np.linalg.norm(B - C)
            side_b = np.linalg.norm(A - C)
            side_c = np.linalg.norm(A - B)
            
            incenter = (
                side_a * A + side_b * B + side_c * C
            ) / (side_a + side_b + side_c)
            
            # Orthocenter
            orthocenter = A + B + C - 2 * circumcenter
            
            return centroid, circumcenter, incenter, orthocenter
    
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

            centroid, circumcenter, incenter, orthocenter = self.get_centers(a, b, c)

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

        # First new triangle to change
        A1 = np.array([-0.5, -1.0, 0])
        B1 = np.array([0.5, -1.0, 0])
        C1 = np.array([0.3, 1.5, 0])
        new_tri_centers = []

        new_triangles = []

        for position in posCenters:
            a = A1 + position
            b = B1 + position
            c = C1 + position

            tri_centers = self.get_centers(a, b, c)

            new_tri_centers.append(tri_centers)

            new_triangles.append(
                Polygon(a, b, c, stroke_width=10, color="white")
            )
             

        self.play(
            # Triangle 1
            triangles[0].animate.become(new_triangles[0]),
            dots[0].animate.move_to(new_tri_centers[0][0]),

            # Triangle 2
            triangles[1].animate.become(new_triangles[1]),
            dots[1].animate.move_to(new_tri_centers[1][1]),

            # Triangle 3
            triangles[2].animate.become(new_triangles[2]),
            dots[2].animate.move_to(new_tri_centers[2][2]),

            # Triangle 4
            triangles[3].animate.become(new_triangles[3]),
            dots[3].animate.move_to(new_tri_centers[3][3]),

            run_time=3,
        )

        self.wait()