from manim import *
import numpy as np
from napoleon_helpers import *
from napoleon_construction import *

class NapoleonProof(Scene):
    def construct(self):
        # Rule of thumb:
        # x in [-7.1, 7.1]
        # y in [-4, 4]

        # Invisible control points
        A = Dot(
            [-1.5, -0.3, 0],
            radius=0.2,
            fill_opacity=0,
            stroke_opacity=0,
            color="#f05f01"
        )

        B = Dot(
            [-1.0, 2.4, 0],
            radius=0.2,
            fill_opacity=0,
            stroke_opacity=0,
            color="#27A830"
        )

        C = Dot(
            [1.0, 0.0, 0],
            radius=0.2,
            fill_opacity=0,
            stroke_opacity=0,
            color="#206B87"
        )

        # Top layer
        construction = NapoleonConstruction(A, B, C)

        A1 = A.copy()
        B1 = B.copy()
        C1 = C.copy()

        construction2 = NapoleonConstruction(A1, B1, C1)

        A2 = A.copy()
        B2 = B.copy()
        C2 = C.copy()

        construction3 = NapoleonConstruction(A1, B1, C1)

        # Construct the centroids:
        # Centroid GB
        GB = always_redraw(lambda: Dot(
            (
                construction.B.get_center()
                + construction.C.get_center()
                + equilateral_on_side(
                    construction.B.get_center(),
                    construction.C.get_center(),
                    construction.A.get_center(),
                )
            ) / 3,
            radius=0.16,
            color="#87FF78",
        ))

        # Centroid GC
        GC = always_redraw(lambda: Dot(
            (
                construction.C.get_center()
                + construction.A.get_center()
                + equilateral_on_side(
                    construction.C.get_center(),
                    construction.A.get_center(),
                    construction.B.get_center(),
                )
            ) / 3,
            radius=0.16,
            color="#9AB5FF",
        ))

        # Centroid GA
        GA = always_redraw(lambda: Dot(
            (
                construction.A.get_center()
                + construction.B.get_center()
                + equilateral_on_side(
                    construction.A.get_center(),
                    construction.B.get_center(),
                    construction.C.get_center(),
                )
            ) / 3,
            radius=0.16,
            color="#B00B69",
        ))

        centroids = VGroup(
            GA,
            GB,
            GC,
        ).set_z_index(3)

        self.play(
            FadeIn(construction2.triangle),
            FadeIn(construction2.EA),
            FadeIn(construction2.EB),
            FadeIn(construction2.EC),
            FadeIn(centroids),
            run_time=1,
        )

        self.add(
            construction3.triangle,
            construction3.EA,
            construction3.EB,
            construction3.EC,
        )

        self.add(
            construction.triangle,
            construction.EA,
            construction.EB,
            construction.EC,
        )

        self.wait(1)

        # Labels
        label_A = always_redraw(lambda: Text(
            "A",
            font="OpenDyslexic",
            font_size=32,
            color="white",
        ).next_to(
            GA.get_center(),
            UP + LEFT,
            buff=0.15
        ))

        label_B = always_redraw(lambda: Text(
            "B",
            font="OpenDyslexic",
            font_size=32,
            color="white",
        ).next_to(
            GB.get_center(),
            UP + RIGHT,
            buff=0.15
        ))

        label_C = always_redraw(lambda: Text(
            "C",
            font="OpenDyslexic",
            font_size=32,
            color="white",
        ).next_to(
            GC.get_center(),
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
            GB.get_center(),
            GC.get_center(),
            stroke_width=10,
            color="#C5C100",
            )
        ).set_z_index(1)

        BC_line_copy = BC_line.copy()

        self.play(FadeIn(BC_line))

        GD = GB.copy()

        GD.move_to(GB.get_center())

        self.add(GD)

        rotation_center_2 = GC.get_center()

        self.play(
            Rotate(
                VGroup(A1, B1, C1, BC_line_copy, GD),
                angle=2 * PI / 3,
                about_point=rotation_center_2,
            ),
            run_time=4,
        )

        label_D = always_redraw(lambda: Text(
            "D",
            font="OpenDyslexic",
            font_size=32,
            color="white",
        ).next_to(
            GD.get_center(),
            UP + LEFT,
            buff=0.15
        ))

        self.play(
            FadeIn(label_D),
            run_time=1
        )