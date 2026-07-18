from math import *
from manim import *

class Test(Scene):
    def construct(self):

        # Set up the plane
        plane = (
            NumberPlane(x_range=[0, 60, 20], x_length=10, y_range=[2, 4, 1], y_length=4
            ).add_coordinates()
        )

        # Compute partial sums of the Leibniz series
        def leibniz_partial_sum(n):
            return 4 * sum(((-1) ** k) / (2 * k + 1) for k in range(n + 1))

        # Create dots for each partial sum
        dots = VGroup(
            *[Dot(plane.c2p(n, leibniz_partial_sum(n)), color=RED, radius=.05) for n in range(1, 60)]
        )
        
        # Add a line at y = pi/4 for reference
        pi_line = DashedLine(
            start=plane.c2p(0, pi),
            end=plane.c2p(60, pi),
            color=YELLOW
        )
        
        pi_label = MathTex("\pi").next_to(pi_line, RIGHT)

        # Add the plane and animate everything
        self.play(Create(plane))

        self.play(LaggedStart(*[FadeIn(dot) for dot in dots], lag_ratio=0.1, run_time=10))
        self.play(Create(pi_line), run_time=1)
        self.play(Write(pi_label), run_time=1)
        self.wait(2)