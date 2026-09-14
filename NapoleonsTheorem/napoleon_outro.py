from manim import *
import numpy as np
from napoleon_construction import *
from napoleon_helpers import equilateral_on_side

class NapoleonOutro(Scene):
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

        construction = NapoleonConstruction(X, Y, Z)

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

        label_X = always_redraw(lambda: MathTex("X").scale(0.8).move_to(X.get_center() + DOWN * 0.4))
        label_Y = always_redraw(lambda: MathTex("Y").scale(0.8).move_to(Y.get_center() + UP * 0.4))
        label_Z = always_redraw(lambda: MathTex("Z").scale(0.8).move_to(Z.get_center() + RIGHT * 0.4))

        self.play(
            FadeIn(label_X),
            FadeIn(label_Y),
            FadeIn(label_Z),
            run_time=1
        )

        pos_X = X.get_center()
        pos_Y = Y.get_center()
        pos_Z = Z.get_center()
        pos_EQ = equilateral_on_side(pos_Y, pos_Z, pos_X)

        # Component vectors
        vec1 = pos_X - pos_Z
        vec2 = pos_Z - pos_EQ

        # First arrow starting from X:
        arrow1 = Arrow(pos_X, pos_X + vec1, color=BLUE, buff=0)

        # Second arrow
        arrow2 = Arrow(pos_X + vec1, pos_X + vec1 + vec2, color=GREEN, buff=0)

        resultant_arrow = Arrow(pos_X, pos_X + vec1 + vec2, color=YELLOW, buff=0)

        self.play(
            FadeIn(arrow1),
            FadeIn(arrow2),
            FadeIn(resultant_arrow),
            run_time=2
        )