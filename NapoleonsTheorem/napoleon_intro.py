from manim import *
import numpy as np
from napoleon_construction import *

class NapoleonIntro(Scene):
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
            [-1.0, 1.0, 0],
            radius=0.2,
            fill_opacity=0,
            stroke_opacity=0,
            color="#27A830"
        )

        Z = Dot(
            [1.0, -1.0, 0],
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

        # Centroids
        GA = always_redraw(lambda: Dot(
            (
                construction.X.get_center()
                + construction.Y.get_center()
                + equilateral_on_side(
                    construction.X.get_center(),
                    construction.Y.get_center(),
                    construction.Z.get_center(),
                )
            ) / 3,
            radius=0.16,
            color="#B00B69",
        )).set_z_index(2)

        GB = always_redraw(lambda: Dot(
            (
                construction.Y.get_center()
                + construction.Z.get_center()
                + equilateral_on_side(
                    construction.Y.get_center(),
                    construction.Z.get_center(),
                    construction.X.get_center(),
                )
            ) / 3,
            radius=0.16,
            color="#87FF78",
        )).set_z_index(2)

        GC = always_redraw(lambda: Dot(
            (
                construction.Z.get_center()
                + construction.X.get_center()
                + equilateral_on_side(
                    construction.Z.get_center(),
                    construction.X.get_center(),
                    construction.Y.get_center(),
                )
            ) / 3,
            radius=0.16,
            color="#9AB5FF",
        )).set_z_index(2)

        centroid_dots = VGroup(
            GA,
            GB,
            GC,
        )

        self.play(
            FadeIn(centroid_dots),
            run_time=1
        )

        self.wait(1)

        # Connect the centroids
        centroid_triangle = always_redraw(lambda: VGroup(

            Line(
                GA.get_center(),
                GB.get_center(),
                stroke_width=10,
                color="#C5C100",
            ).set_cap_style(CapStyleType.ROUND),

            Line(
                GB.get_center(),
                GC.get_center(),
                stroke_width=10,
                color="#C5C100",
            ).set_cap_style(CapStyleType.ROUND),

            Line(
                GA.get_center(),
                GC.get_center(),
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
            construction.X.animate.move_to([-1.5, -1.2, 0]),
            construction.Y.animate.move_to([-1.0, 2.0, 0]),
            construction.Z.animate.move_to([2.0, -0.0, 0]),
            run_time=3,
        )

        self.wait(1)

        self.play(
            construction.X.animate.move_to([-2.0, 1.0, 0]),
            construction.Y.animate.move_to([0.8, 1.5, 0]),
            construction.Z.animate.move_to([2.0, -1.5, 0]),
            run_time=3,
        )

        self.wait(1)
        
        self.play(
            construction.X.animate.move_to([1.7, 1.2, 0]),
            construction.Y.animate.move_to([2.0, -0.2, 0]),
            construction.Z.animate.move_to([-1.5, 1.0, 0]),
            run_time=3,
        )

        self.wait(1)

        self.play(
            construction.X.animate.move_to([-0.0, np.sqrt(3) - 1, 0]),
            construction.Y.animate.move_to([1.0, -1.0, 0]),
            construction.Z.animate.move_to([-1.0, -1.0, 0]),
            run_time=3,
        )

        self.wait(2)