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
            stroke_width=stroke_width,
            color="white"
        ).set_cap_style(CapStyleType.ROUND),

        Line(
            Q, R,
            stroke_width=stroke_width,
            color="white"
        ).set_cap_style(CapStyleType.ROUND),

        Line(
            R, P,
            stroke_width=stroke_width,
            color="white"
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

def shade_color(hex_color, opacity):
    """
    Darken a hex color as if it were drawn with the given opacity
    over a black background.
    """
    hex_color = hex_color.lstrip("#")

    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)

    r = round(r * opacity)
    g = round(g * opacity)
    b = round(b * opacity)

    return f"#{r:02X}{g:02X}{b:02X}"

class NapoleonConstruction:
    def __init__(self, A, B, C):
        # Store the control points
        self.A = A
        self.B = B
        self.C = C

        self.triangle = always_redraw(
            lambda: triangle_lines(
                self.A.get_center(),
                self.B.get_center(),
                self.C.get_center(),
                stroke_width=10,
            )
        )

        # Equilateral triangle EA
        # (constructed on side BC, opposite A)
        self.EA = always_redraw(lambda: VGroup(
            Polygon(
                self.B.get_center(),
                self.C.get_center(),
                equilateral_on_side(
                    self.B.get_center(),
                    self.C.get_center(),
                    self.A.get_center(),
                ),
                fill_color=shade_color("#87FF78", 0.2),
                fill_opacity=1,
                stroke_width=10,
                stroke_color="white",
                stroke_opacity=1
            ),

            Line(
                self.B.get_center(),
                equilateral_on_side(
                    self.B.get_center(),
                    self.C.get_center(),
                    self.A.get_center(),
                ),
                stroke_width=10,
                color="white"
            ).set_cap_style(CapStyleType.ROUND),

            Line(
                self.C.get_center(),
                equilateral_on_side(
                    self.B.get_center(),
                    self.C.get_center(),
                    self.A.get_center(),
                ),
                stroke_width=10,
                color="white"
            ).set_cap_style(CapStyleType.ROUND),
        ))

        # Equilateral triangle EB
        # (constructed on side CA, opposite B)
        self.EB = always_redraw(lambda: VGroup(
            Polygon(
                self.C.get_center(),
                self.A.get_center(),
                equilateral_on_side(
                    self.C.get_center(),
                    self.A.get_center(),
                    self.B.get_center(),
                ),
                fill_color=shade_color("#9AB5FF", 0.2),
                fill_opacity=1,
                stroke_width=10,
                stroke_color="white",
                stroke_opacity=1
            ),

            Line(
                self.C.get_center(),
                equilateral_on_side(
                    self.C.get_center(),
                    self.A.get_center(),
                    self.B.get_center(),
                ),
                stroke_width=10,
                color="white"
            ).set_cap_style(CapStyleType.ROUND),

            Line(
                self.A.get_center(),
                equilateral_on_side(
                    self.C.get_center(),
                    self.A.get_center(),
                    self.B.get_center(),
                ),
                stroke_width=10,
                color="white"
            ).set_cap_style(CapStyleType.ROUND),
        ))

        # Equilateral triangle EC
        # (constructed on side AB, opposite C)
        self.EC = always_redraw(lambda: VGroup(
            Polygon(
                self.A.get_center(),
                self.B.get_center(),
                equilateral_on_side(
                    self.A.get_center(),
                    self.B.get_center(),
                    self.C.get_center(),
                ),
                fill_color=shade_color("#B00B69", 0.2),
                fill_opacity=1,
                stroke_width=10,
                stroke_color="white",
                stroke_opacity=1
            ),

            Line(
                self.A.get_center(),
                equilateral_on_side(
                    self.A.get_center(),
                    self.B.get_center(),
                    self.C.get_center(),
                ),
                stroke_width=10,
                color="white"
            ).set_cap_style(CapStyleType.ROUND),

            Line(
                self.B.get_center(),
                equilateral_on_side(
                    self.A.get_center(),
                    self.B.get_center(),
                    self.C.get_center(),
                ),
                stroke_width=10,
                color="white"
            ).set_cap_style(CapStyleType.ROUND),
        ))

        # Centroid GB
        self.GB = always_redraw(lambda: Dot(
            (
                self.B.get_center()
                + self.C.get_center()
                + equilateral_on_side(
                    self.B.get_center(),
                    self.C.get_center(),
                    self.A.get_center(),
                )
            ) / 3,
            radius=0.16,
            color="#87FF78",
        ))

        # Centroid GC
        self.GC = always_redraw(lambda: Dot(
            (
                self.C.get_center()
                + self.A.get_center()
                + equilateral_on_side(
                    self.C.get_center(),
                    self.A.get_center(),
                    self.B.get_center(),
                )
            ) / 3,
            radius=0.16,
            color="#9AB5FF",
        ))

        # Centroid GA
        self.GA = always_redraw(lambda: Dot(
            (
                self.A.get_center()
                + self.B.get_center()
                + equilateral_on_side(
                    self.A.get_center(),
                    self.B.get_center(),
                    self.C.get_center(),
                )
            ) / 3,
            radius=0.16,
            color="#B00B69",
        ))

        self.centroids = VGroup(
            self.GA,
            self.GB,
            self.GC,
        )

        self.all = VGroup(
            self.triangle,
            self.EA,
            self.EB,
            self.EC,
            self.GA,
            self.GB,
            self.GC,
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
            fill_opacity=1,
            stroke_opacity=0,
            color="#f05f01"
        )

        B = Dot(
            [-1.0, 1.0, 0],
            radius=0.2,
            fill_opacity=1,
            stroke_opacity=0,
            color="#27A830"
        )

        C = Dot(
            [1.0, -1.0, 0],
            radius=0.2,
            fill_opacity=1,
            stroke_opacity=0,
            color="#206B87"
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
        E1 = always_redraw(lambda: VGroup(
            Polygon(
                A.get_center(),
                B.get_center(),
                equilateral_on_side(
                    A.get_center(),
                    B.get_center(),
                    C.get_center(),
                ),
                fill_color="#B00B69",
                fill_opacity=0.2,
                stroke_opacity=0,
            ),

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
            Polygon(
                B.get_center(),
                C.get_center(),
                equilateral_on_side(
                    B.get_center(),
                    C.get_center(),
                    A.get_center(),
                ),
                fill_color="#87FF78",
                fill_opacity=0.2,
                stroke_opacity=0,
            ),

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
            Polygon(
                C.get_center(),
                A.get_center(),
                equilateral_on_side(
                    C.get_center(),
                    A.get_center(),
                    B.get_center(),
                ),
                fill_color="#9AB5FF",
                fill_opacity=0.2,
                stroke_opacity=0,
            ),

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
            FadeIn(E1),
            FadeIn(E2),
            FadeIn(E3),
            run_time=3
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
        )).set_z_index(2)

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
        )).set_z_index(2)

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
        )).set_z_index(2)

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
                stroke_width=10,
                color="#C5C100",
            ).set_cap_style(CapStyleType.ROUND),

            Line(
                G2.get_center(),
                G3.get_center(),
                stroke_width=10,
                color="#C5C100",
            ).set_cap_style(CapStyleType.ROUND),

            Line(
                G3.get_center(),
                G1.get_center(),
                stroke_width=10,
                color="#C5C100",
            ).set_cap_style(CapStyleType.ROUND),

        )).set_z_index(1)

        self.play(
            FadeIn(centroid_triangle),
            run_time=1
        )

        self.wait(1)

        # Deform the original triangles
        self.play(
            A.animate.move_to([-1.5, -1.2, 0]),
            B.animate.move_to([-1.0, 2.0, 0]),
            C.animate.move_to([2.0, -0.0, 0]),
            run_time=3,
        )

        self.wait(1)

        self.play(
            A.animate.move_to([-2.0, 1.0, 0]),
            B.animate.move_to([0.8, 1.5, 0]),
            C.animate.move_to([2.0, -1.5, 0]),
            run_time=3,
        )

        self.wait(1)
        
        self.play(
            A.animate.move_to([1.7, 1.2, 0]),
            B.animate.move_to([2.0, -0.2, 0]),
            C.animate.move_to([-1.5, 1.0, 0]),
            run_time=3,
        )

        self.wait(1)

        self.play(
            A.animate.move_to([-0.0, np.sqrt(3) - 1, 0]),
            B.animate.move_to([1.0, -1.0, 0]),
            C.animate.move_to([-1.0, -1.0, 0]),
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
            [-1.5, -0.3, 0],
            radius=0.2,
            fill_opacity=1,
            stroke_opacity=0,
            color="#f05f01"
        )

        B = Dot(
            [-1.0, 2.4, 0],
            radius=0.2,
            fill_opacity=1,
            stroke_opacity=0,
            color="#27A830"
        )

        C = Dot(
            [1.0, 0.0, 0],
            radius=0.2,
            fill_opacity=1,
            stroke_opacity=0,
            color="#206B87"
        )

        A1 = A.copy()
        B1 = B.copy()
        C1 = C.copy()

        construction2 = NapoleonConstruction(A1, B1, C1)

        A2 = A.copy()
        B2 = B.copy()
        C2 = C.copy()

        construction3 = NapoleonConstruction(A1, B1, C1)

        self.play(
            FadeIn(construction2.triangle),
            FadeIn(construction2.EA),
            FadeIn(construction2.EB),
            FadeIn(construction2.EC),
            FadeIn(construction2.GA),
            FadeIn(construction2.GB),
            FadeIn(construction2.GC),
            run_time=1,
        )

        self.add(
            construction3.triangle,
            construction3.EA,
            construction3.EB,
            construction3.EC,
            construction3.GA,
            construction3.GB,
            construction3.GC,
        )

        construction = NapoleonConstruction(A, B, C)

        self.add(
            construction.triangle,
            construction.EA,
            construction.EB,
            construction.EC,
            construction.GA,
            construction.GB,
            construction.GC,
        )

        self.wait(1)

        # Labels
        label_A = always_redraw(lambda: Text(
            "A",
            font="OpenDyslexic",
            font_size=32,
            color="white",
        ).next_to(
            construction.GA.get_center(),
            UP + LEFT,
            buff=0.15
        ))

        label_B = always_redraw(lambda: Text(
            "B",
            font="OpenDyslexic",
            font_size=32,
            color="white",
        ).next_to(
            construction.GB.get_center(),
            UP + RIGHT,
            buff=0.15
        ))

        label_C = always_redraw(lambda: Text(
            "C",
            font="OpenDyslexic",
            font_size=32,
            color="white",
        ).next_to(
            construction.GC.get_center(),
            DOWN + RIGHT,
            buff=0.15
        ))

        self.play(
            FadeIn(label_A),
            FadeIn(label_B),
            FadeIn(label_C),
            run_time=1,
        )

        BC_line = always_redraw(lambda: Line(
            construction.GB.get_center(),
            construction.GC.get_center(),
            stroke_width=10,
            color="#C5C100",
            )
        ).set_z_index(1)

        BC_line_copy = BC_line.copy()

        self.play(FadeIn(BC_line))

        rotation_center_2 = construction.GC.get_center()

        self.play(
            Rotate(
                VGroup(A1, B1, C1, BC_line_copy),
                angle=2 * PI / 3,
                about_point=rotation_center_2,
            ),
            run_time=4,
        )