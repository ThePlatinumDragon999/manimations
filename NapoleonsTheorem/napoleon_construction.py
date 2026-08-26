from manim import *
import numpy as np
from napoleon_helpers import *

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

        self.all = VGroup(
            self.triangle,
            self.EA,
            self.EB,
            self.EC
        )