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

def triangle_lines(P, Q, R, stroke_width=10):
    """
    Create the three visible sides of a triangle
    """

    return VGroup(
        Line(
            P, Q,
            stroke_width=stroke_width
        ).set_cap_style(CapStyleType.ROUND),

        Line(
            Q, R,
            stroke_width=stroke_width
        ).set_cap_style(CapStyleType.ROUND),

        Line(
            R, P,
            stroke_width=stroke_width
        ).set_cap_style(CapStyleType.ROUND),
    )

def rotated_point(P, center, angle):
    """
    Rotate point P around center by angle radians.
    """
    x = P - center

    rotation = np.array([
        [np.cos(angle), -np.sin(angle), 0],
        [np.sin(angle),  np.cos(angle), 0],
        [0,              0,             1],
    ])

    return center + rotation @ x

def angle_arc(vertex, p1, p2, radius=0.35, color=WHITE):
    """
    Draw an angle arc at 'vertex' from p1 to p2.
    """

    v1 = p1 - vertex
    v2 = p2 - vertex

    a1 = np.arctan2(v1[1], v1[0])
    a2 = np.arctan2(v2[1], v2[0])

    # Normalize so we get the smaller angle
    diff = (a2 - a1 + PI) % TAU - PI

    return Arc(
        radius=radius,
        start_angle=a1,
        angle=diff,
        arc_center=vertex,
        stroke_width=6,
        color=color,
    )

class Napoleon1(Scene):
    def construct(self):

        # Rule of thumb:
        # x in [-7.1, 7.1]
        # y in [-4, 4]

        # Invisible control points
        A = Dot(
            [-1.0, -1.0, 0],
            radius=0.2,
            fill_opacity=0,
            stroke_opacity=0,
        )

        B = Dot(
            [-1.0, 1.0, 0],
            radius=0.2,
            fill_opacity=0,
            stroke_opacity=0,
        )

        C = Dot(
            [1.0, -1.0, 0],
            radius=0.2,
            fill_opacity=0,
            stroke_opacity=0,
        )

        # Original triangle
        triangle = always_redraw(
            lambda: triangle_lines(
                A.get_center(),
                B.get_center(),
                C.get_center(),
                stroke_width=10,
            )
        )

        self.play(
            FadeIn(triangle),
            run_time=1
        )

        self.wait(1)

        # Equilateral triangles
        equilateral_1 = always_redraw(lambda: VGroup(
            Line(
                A.get_center(),
                equilateral_on_side(
                    A.get_center(),
                    B.get_center(),
                    C.get_center(),
                ),
                stroke_width=10,
            ).set_cap_style(CapStyleType.ROUND),

            Line(
                B.get_center(),
                equilateral_on_side(
                    A.get_center(),
                    B.get_center(),
                    C.get_center(),
                ),
                stroke_width=10,
            ).set_cap_style(CapStyleType.ROUND),
        ))

        equilateral_2 = always_redraw(lambda: VGroup(
            Line(
                B.get_center(),
                equilateral_on_side(
                    B.get_center(),
                    C.get_center(),
                    A.get_center(),
                ),
                stroke_width=10,
            ).set_cap_style(CapStyleType.ROUND),

            Line(
                C.get_center(),
                equilateral_on_side(
                    B.get_center(),
                    C.get_center(),
                    A.get_center(),
                ),
                stroke_width=10,
            ).set_cap_style(CapStyleType.ROUND),
        ))

        equilateral_3 = always_redraw(lambda: VGroup(
            Line(
                C.get_center(),
                equilateral_on_side(
                    C.get_center(),
                    A.get_center(),
                    B.get_center(),
                ),
                stroke_width=10,
            ).set_cap_style(CapStyleType.ROUND),

            Line(
                A.get_center(),
                equilateral_on_side(
                    C.get_center(),
                    A.get_center(),
                    B.get_center(),
                ),
                stroke_width=10,
            ).set_cap_style(CapStyleType.ROUND),
        ))

        # Animate construction of equilateral triangles
        self.play(
            FadeIn(equilateral_1),
            run_time=1
        )

        self.wait(0.3)

        self.play(
            FadeIn(equilateral_2),
            run_time=1
        )

        self.wait(0.3)

        self.play(
            FadeIn(equilateral_3),
            run_time=1
        )

        self.wait(1)

        # Centroids
        G1 = always_redraw(lambda: Dot(
            (
                A.get_center()
                + B.get_center()
                + equilateral_on_side(
                    A.get_center(),
                    B.get_center(),
                    C.get_center(),
                )
            ) / 3,
            radius=0.16,
            color="#B00B69",
        ))

        G2 = always_redraw(lambda: Dot(
            (
                B.get_center()
                + C.get_center()
                + equilateral_on_side(
                    B.get_center(),
                    C.get_center(),
                    A.get_center(),
                )
            ) / 3,
            radius=0.16,
            color="#87FF78",
        ))

        G3 = always_redraw(lambda: Dot(
            (
                C.get_center()
                + A.get_center()
                + equilateral_on_side(
                    C.get_center(),
                    A.get_center(),
                    B.get_center(),
                )
            ) / 3,
            radius=0.16,
            color="#9AB5FF",
        ))

        centroid_dots = VGroup(
            G1,
            G2,
            G3,
        )

        self.play(
            FadeIn(centroid_dots),
            run_time=1
        )

        self.wait(1)

        # Connect the centroids
        centroid_triangle = always_redraw(lambda: VGroup(

            Line(
                G1.get_center(),
                G2.get_center(),
                stroke_width=8,
            ).set_cap_style(CapStyleType.ROUND),

            Line(
                G2.get_center(),
                G3.get_center(),
                stroke_width=8,
            ).set_cap_style(CapStyleType.ROUND),

            Line(
                G3.get_center(),
                G1.get_center(),
                stroke_width=8,
            ).set_cap_style(CapStyleType.ROUND),

        ))

        self.play(
            Create(centroid_triangle),
            run_time=1.5
        )

        self.wait(1)

        # Deform the original triangles
        self.play(
            A.animate.move_to([-2.0, -1.5, 0]),
            B.animate.move_to([-1.0, 2.0, 0]),
            C.animate.move_to([2.0, -0.5, 0]),
            run_time=3,
        )

        self.wait(1)

        self.play(
            A.animate.move_to([-2.0, 1.0, 0]),
            B.animate.move_to([1.0, 2.0, 0]),
            C.animate.move_to([2.0, -1.5, 0]),
            run_time=3,
        )

        self.wait(1)

        self.play(
            A.animate.move_to([-2.5, -1.5, 0]),
            B.animate.move_to([0.0, 2.5, 0]),
            C.animate.move_to([2.5, -1.0, 0]),
            run_time=3,
        )

        self.wait(1)

        # Return to original triangle
        self.play(
            A.animate.move_to([-1.0, -1.0, 0]),
            B.animate.move_to([-1.0, 1.0, 0]),
            C.animate.move_to([1.0, -1.0, 0]),
            run_time=3,
        )

        self.wait(2)

class NapoleonProof(Scene):
    def construct(self):
        # Rule of thumb:
        # x in [-7.1, 7.1]
        # y in [-4, 4]

        # Invisible control points
        A = Dot(
            [-1.0, -1.0, 0],
            radius=0.2,
            fill_opacity=0,
            stroke_opacity=0,
        )

        B = Dot(
            [-1.0, 1.0, 0],
            radius=0.2,
            fill_opacity=0,
            stroke_opacity=0,
        )

        C = Dot(
            [1.0, -1.0, 0],
            radius=0.2,
            fill_opacity=0,
            stroke_opacity=0,
        )

        # Original triangle
        triangle = always_redraw(
            lambda: triangle_lines(
                A.get_center(),
                B.get_center(),
                C.get_center(),
                stroke_width=10,
            )
        )

        # Equilateral triangles
        E1 = always_redraw(lambda: VGroup(
            Line(
                A.get_center(),
                equilateral_on_side(
                    A.get_center(),
                    B.get_center(),
                    C.get_center(),
                ),
                stroke_width=10,
            ).set_cap_style(CapStyleType.ROUND),

            Line(
                B.get_center(),
                equilateral_on_side(
                    A.get_center(),
                    B.get_center(),
                    C.get_center(),
                ),
                stroke_width=10,
            ).set_cap_style(CapStyleType.ROUND),
        ))

        E2 = always_redraw(lambda: VGroup(
            Line(
                B.get_center(),
                equilateral_on_side(
                    B.get_center(),
                    C.get_center(),
                    A.get_center(),
                ),
                stroke_width=10,
            ).set_cap_style(CapStyleType.ROUND),

            Line(
                C.get_center(),
                equilateral_on_side(
                    B.get_center(),
                    C.get_center(),
                    A.get_center(),
                ),
                stroke_width=10,
            ).set_cap_style(CapStyleType.ROUND),
        ))

        E3 = always_redraw(lambda: VGroup(
            Line(
                C.get_center(),
                equilateral_on_side(
                    C.get_center(),
                    A.get_center(),
                    B.get_center(),
                ),
                stroke_width=10,
            ).set_cap_style(CapStyleType.ROUND),

            Line(
                A.get_center(),
                equilateral_on_side(
                    C.get_center(),
                    A.get_center(),
                    B.get_center(),
                ),
                stroke_width=10,
            ).set_cap_style(CapStyleType.ROUND),
        ))

        # Centroids
        G1 = always_redraw(lambda: Dot(
            (
                A.get_center()
                + B.get_center()
                + equilateral_on_side(
                    A.get_center(),
                    B.get_center(),
                    C.get_center(),
                )
            ) / 3,
            radius=0.16,
            color="#B00B69",
        ))

        G2 = always_redraw(lambda: Dot(
            (
                B.get_center()
                + C.get_center()
                + equilateral_on_side(
                    B.get_center(),
                    C.get_center(),
                    A.get_center(),
                )
            ) / 3,
            radius=0.16,
            color="#87FF78",
        ))

        G3 = always_redraw(lambda: Dot(
            (
                C.get_center()
                + A.get_center()
                + equilateral_on_side(
                    C.get_center(),
                    A.get_center(),
                    B.get_center(),
                )
            ) / 3,
            radius=0.16,
            color="#9AB5FF",
        ))

        centroid_dots = VGroup(
            G1,
            G2,
            G3,
        )

        self.play(
            FadeIn(triangle),
            FadeIn(E1),
            FadeIn(E2),
            FadeIn(E3),
            FadeIn(G1),
            FadeIn(G2),
            FadeIn(G3),
            run_time=1,
        )

        self.wait(1)