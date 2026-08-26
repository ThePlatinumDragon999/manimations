from manim import *
import numpy as np
from napoleon_helpers import *

class NapoleonConstruction:
    def __init__(self, X, Y, Z):
        # Store the control points
        self.X = X
        self.Y = Y
        self.Z = Z

        self.triangle = always_redraw(
            lambda: triangle_lines(
                self.X.get_center(),
                self.Y.get_center(),
                self.Z.get_center(),
                stroke_width=10,
            )
        )

        # Equilateral triangle EX
        # (constructed on side YZ, opposite X)
        self.EX = always_redraw(lambda: VGroup(
            Polygon(
                self.Y.get_center(),
                self.Z.get_center(),
                equilateral_on_side(
                    self.Y.get_center(),
                    self.Z.get_center(),
                    self.X.get_center(),
                ),
                fill_color=shade_color("#87FF78", 0.2),
                fill_opacity=1,
                stroke_width=10,
                stroke_color="white",
                stroke_opacity=1
            ),

            Line(
                self.Y.get_center(),
                equilateral_on_side(
                    self.Y.get_center(),
                    self.Z.get_center(),
                    self.X.get_center(),
                ),
                stroke_width=10,
                color="white"
            ).set_cap_style(CapStyleType.ROUND),

            Line(
                self.Z.get_center(),
                equilateral_on_side(
                    self.Y.get_center(),
                    self.Z.get_center(),
                    self.X.get_center(),
                ),
                stroke_width=10,
                color="white"
            ).set_cap_style(CapStyleType.ROUND),
        ))

        # Equilateral triangle EY
        # (constructed on side XZ, opposite Y)
        self.EY = always_redraw(lambda: VGroup(
            Polygon(
                self.Z.get_center(),
                self.X.get_center(),
                equilateral_on_side(
                    self.Z.get_center(),
                    self.X.get_center(),
                    self.Y.get_center(),
                ),
                fill_color=shade_color("#9AB5FF", 0.2),
                fill_opacity=1,
                stroke_width=10,
                stroke_color="white",
                stroke_opacity=1
            ),

            Line(
                self.Z.get_center(),
                equilateral_on_side(
                    self.Z.get_center(),
                    self.X.get_center(),
                    self.Y.get_center(),
                ),
                stroke_width=10,
                color="white"
            ).set_cap_style(CapStyleType.ROUND),

            Line(
                self.X.get_center(),
                equilateral_on_side(
                    self.Z.get_center(),
                    self.X.get_center(),
                    self.Y.get_center(),
                ),
                stroke_width=10,
                color="white"
            ).set_cap_style(CapStyleType.ROUND),
        ))

        # Equilateral triangle EZ
        # (constructed on side XY, opposite Z)
        self.EZ = always_redraw(lambda: VGroup(
            Polygon(
                self.X.get_center(),
                self.Y.get_center(),
                equilateral_on_side(
                    self.X.get_center(),
                    self.Y.get_center(),
                    self.Z.get_center(),
                ),
                fill_color=shade_color("#B00B69", 0.2),
                fill_opacity=1,
                stroke_width=10,
                stroke_color="white",
                stroke_opacity=1
            ),

            Line(
                self.X.get_center(),
                equilateral_on_side(
                    self.X.get_center(),
                    self.Y.get_center(),
                    self.Z.get_center(),
                ),
                stroke_width=10,
                color="white"
            ).set_cap_style(CapStyleType.ROUND),

            Line(
                self.Y.get_center(),
                equilateral_on_side(
                    self.X.get_center(),
                    self.Y.get_center(),
                    self.Z.get_center(),
                ),
                stroke_width=10,
                color="white"
            ).set_cap_style(CapStyleType.ROUND),
        ))

        self.all = VGroup(
            self.triangle,
            self.EX,
            self.EY,
            self.EZ
        )