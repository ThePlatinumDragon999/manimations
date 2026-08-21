from manim import *
import numpy as np

class Napoleon1(Scene):
    def construct(self):

        A = np.array([-3.0, -1.5, 0])
        B = np.array([3.0, -1.0, 0])
        C = np.array([-0.5, -2.0, 0])

        triangle = Polygon(
            A, B, C,
            stroke_width=4,
            color="white"
        )

        self.play(FadeIn(triangle))
        self.wait(3)
