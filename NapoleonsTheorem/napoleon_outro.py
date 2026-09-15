from manim import *
import numpy as np
from napoleon_construction import *
from napoleon_helpers import equilateral_on_side, generate_order

class NapoleonOutro(MovingCameraScene):
    def construct(self):

        self.camera.frame.set_width(35)

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

        # Animate construction of equilateral triangles
        self.play(
            FadeIn(construction.EX),
            FadeIn(construction.EY),
            FadeIn(construction.EZ),
            run_time=1
        )

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
        tiles = {}
        labels = {}

        for i in range(-6, 7):
            for j in range(-6, 7):
                if i == 0 and j == 0:
                    # Skip the central original construction
                    continue
                
                offset = i * vector1 + j * vector2
                
                sub_X = Dot(
                    pos_X + offset, 
                    fill_opacity=0, 
                    stroke_opacity=0
                )

                sub_Y = Dot(
                    pos_Y + offset, 
                    fill_opacity=0, 
                    stroke_opacity=0
                )

                sub_Z = Dot(
                    pos_Z + offset, 
                    fill_opacity=0, 
                    stroke_opacity=0
                )
                
                sub_construction = NapoleonConstruction(
                    sub_X, sub_Y, sub_Z, opacity
                )

                tiles[(i, j)] = sub_construction.all

                center_pos = (
                    sub_X.get_center()
                    + sub_Y.get_center()
                    + sub_Z.get_center()
                ) / 3

                label = Text(
                    f"({i}, {j})",
                    font_size=80,
                    color=WHITE
                ).move_to(center_pos)

                box = BackgroundRectangle(
                    label,
                    color=BLACK,
                    fill_opacity=0.8,
                    buff=0.15
                )

                labels[(i, j)] = VGroup(
                    box,
                    label
                ).set_z_index(1000)

        order = generate_order(6)

        tile_fade_ins = [
            FadeIn(tiles[position])
            for position in order
        ]

        # Fade in the tiled plane
        self.play(
            LaggedStart(
                *tile_fade_ins,
                lag_ratio=0.05,
                run_time=len(order) / 8
            ),
            rate_func=linear
        )
        self.wait(1)