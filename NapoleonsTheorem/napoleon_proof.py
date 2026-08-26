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