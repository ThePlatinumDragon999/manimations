from manim import *
import numpy as np
from napoleon_construction import *
from napoleon_helpers import equilateral_on_side

class NapoleonOutro(MovingCameraScene):
    def construct(self):

        # Rule of thumb:
        # x in [-7.1, 7.1]
        # y in [-4, 4]

        # Invisible control points
        X = Dot(
            [-1.0, -1.0, 0],
            radius=0.2,
            fill_opacity=0,
            stroke_opacity=0,
            color="#f05f01"
        )

        Y = Dot(
            [-1.0, 0.8, 0],
            radius=0.2,
            fill_opacity=0,
            stroke_opacity=0,
            color="#27A830"
        )

        Z = Dot(
            [1.0, -0.5, 0],
            radius=0.2,
            fill_opacity=0,
            stroke_opacity=0,
            color="#206B87"
        )

        opacity = 0.7

        construction = NapoleonConstruction(X, Y, Z, opacity)

        self.play(
            FadeIn(construction.triangle),
            run_time=1
        )

        self.wait(1)

        # Animate construction of equilateral triangles
        self.play(
            FadeIn(construction.EX),
            FadeIn(construction.EY),
            FadeIn(construction.EZ),
            run_time=3
        )

        self.wait(1)

        # Set up the basis vectors
        pos_X = X.get_center()
        pos_Y = Y.get_center()
        pos_Z = Z.get_center()
        pos_EQX = equilateral_on_side(pos_Y, pos_Z, pos_X)
        pos_EQZ = equilateral_on_side(pos_X, pos_Y, pos_Z)

        # Basis vectors
        vector1 = (pos_X - pos_Z) + (pos_Z - pos_EQX)
        vector2 = (pos_Y - pos_Z) + (pos_EQZ - pos_Y)

        # Tile the plane
        tiled_group = VGroup()
        for i in range(-4, 5):
            for j in range(-4, 5):
                if i == 0 and j == 0:
                    continue  # Skip the central original construction
                
                offset = i * vector1 + j * vector2
                
                sub_X = Dot(pos_X + offset, fill_opacity=0, stroke_opacity=0)
                sub_Y = Dot(pos_Y + offset, fill_opacity=0, stroke_opacity=0)
                sub_Z = Dot(pos_Z + offset, fill_opacity=0, stroke_opacity=0)
                
                sub_construction = NapoleonConstruction(sub_X, sub_Y, sub_Z, opacity)
                tiled_group.add(sub_construction.all)

        # Fade in the entire tiled plane
        self.play(
            FadeIn(tiled_group, lag_ratio=0.01),
            run_time=3
        )
        self.wait(1)

        # Zoom out to reveal the full tessellation pattern
        self.play(
            self.camera.frame.animate.set_width(26),
            run_time=3
        )
        self.wait(2)

