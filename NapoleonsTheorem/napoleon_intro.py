from manim import *
import numpy as np
from napoleon_helpers import *

class NapoleonIntro(Scene):
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