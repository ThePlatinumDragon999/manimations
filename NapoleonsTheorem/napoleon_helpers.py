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