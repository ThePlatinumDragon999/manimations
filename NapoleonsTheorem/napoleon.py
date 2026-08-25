from manim import *
import numpy as np

def equilateral_on_side(P, Q, opposite_vertex):
    """
    Given side PQ and the opposite vertex of the original triangle,
    return the third vertex of the equilerateral triangle constructed
    on the outside of the original triangle
    """

    v = Q - P

    # Rotate v by +60 degrees 
    # (since equilateral triangle angles are all 60 degrees)
    # Recall that a counterclockwise rotation matrix is [(cosθ, -sinθ), (sinθ, cosθ)]
    rotation = np.array([
        [np.cos(np.pi / 3), -np.sin(np.pi / 3), 0],
        [np.sin(np.pi / 3),  np.cos(np.pi / 3), 0],
        [0,                  0,                 1],
    ])

    # @ is matrix-vector multiplication 
    # ccR stands for counter clockwise rotation
    ccR = P + rotation @ v

    # Rotate v by -60 degrees
    rotation = np.array([
        [np.cos(np.pi / 3),  np.sin(np.pi / 3), 0],
        [-np.sin(np.pi / 3), np.cos(np.pi / 3), 0],
        [0,                  0,                 1],
    ])

    # cR stands for clockwise rotation
    cR = P + rotation @ v

    # Pick the point that is on the opposite side of PQ
    # from the original triangle's third vertex.
    # If to get to v faster from u you rotate counterclockwise, this is positive
    # Otherwise negative
    def cross_2d(u, v):
        return u[0] * v[1] - u[1] * v[0]

    # Gets the side of the opposite vertex compared to the triangle side
    side = cross_2d(v, opposite_vertex - P)

    candidate_1 = cross_2d(v, ccR - P)
    candidate_2 = cross_2d(v, cR - P)

    if np.sign(candidate_1) != np.sign(side):
        return ccR
    else:
        return cR

class Napoleon1(Scene):
    def construct(self):

        # Rule of thumb:
        # x in [-7.1, 7.1]
        # y in [-4, 4]
        A = np.array([-1.0, -1.0, 0])
        B = np.array([-1.0, 1.0, 0])
        C = np.array([1.0, -1.0, 0])

        triangle = Polygon(
            A, B, C,
            stroke_width=10,
            color="white",
        )

        triangle = VGroup(
            Line(A, B, stroke_width=10).set_cap_style(CapStyleType.ROUND),
            Line(A, C, stroke_width=10).set_cap_style(CapStyleType.ROUND),
            Line(B, C, stroke_width=10).set_cap_style(CapStyleType.ROUND)
        )

        self.play(FadeIn(triangle))
        self.wait(1)

        # Construct equilateral triangles

        D = equilateral_on_side(A, B, C)
        E = equilateral_on_side(B, C, A)
        F = equilateral_on_side(C, A, B)

        equilateral_1 = VGroup(
            Line(B, D, stroke_width=10).set_cap_style(CapStyleType.ROUND),
            Line(D, A, stroke_width=10).set_cap_style(CapStyleType.ROUND)
        )

        equilateral_2 = VGroup(
            Line(C, E, stroke_width=10).set_cap_style(CapStyleType.ROUND),
            Line(E, B, stroke_width=10).set_cap_style(CapStyleType.ROUND)
        )

        equilateral_3 = VGroup(
            Line(A, F, stroke_width=10).set_cap_style(CapStyleType.ROUND),
            Line(F, C, stroke_width=10).set_cap_style(CapStyleType.ROUND)
        )

        # First side
        self.play(
            FadeIn(equilateral_1),
            run_time=1
        )

        self.wait(0.3)

        # Second side
        self.play(
            FadeIn(equilateral_2),
            run_time=1
        )

        self.wait(0.3)

        # Third side
        self.play(
            FadeIn(equilateral_3),
            run_time=1
        )

        self.wait(1)

        # Centroids
        G1 = (A + B + D) / 3
        G2 = (B + C + E) / 3
        G3 = (A + C + F) / 3

        centroid_dots = VGroup(
            Dot(G1, radius=0.16, color="#B00B69"),
            Dot(G2, radius=0.16, color="#87FF78"),
            Dot(G3, radius=0.16, color="#9AB5FF")
        )

        self.play(
            FadeIn(centroid_dots),
            run_time=1
        )
