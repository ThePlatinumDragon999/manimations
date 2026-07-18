from manim import *
import numpy as np

class FactorGaussian9(Scene):
    def construct(self):
        # Prime
        p = 29
        r = np.sqrt(p)

        # Number plane with visible coordinates
        plane = NumberPlane(
            x_range=[0, 6, 1],
            y_range=[0, 6, 1],
            background_line_style={"stroke_opacity": 0.4}
        ).add_coordinates()

        # Move plane so origin is bottom-left of frame
        plane.to_corner(DL)

        self.add(plane)

        # Axis labels
        re_label = MathTex(r"\mathrm{Re}").next_to(plane.x_axis, RIGHT)
        im_label = MathTex(r"\mathrm{Im}").next_to(plane.y_axis, UP)
        self.add(re_label, im_label)

        # Angle tracker
        theta = ValueTracker(0)

        # Arrow from origin
        vector = always_redraw(
            lambda: Arrow(
                plane.c2p(0, 0),
                plane.c2p(
                    r * np.cos(theta.get_value()),
                    r * np.sin(theta.get_value())
                ),
                buff=0,
                color="#b00b69"
            )
        )

        # Dotted projections
        x_component = always_redraw(
            lambda: DashedLine(
                plane.c2p(0, 0),
                plane.c2p(r * np.cos(theta.get_value()), 0),
                stroke_width=6,
                color="#9ab5ff"
            )
        )

        y_component = always_redraw(
            lambda: DashedLine(
                plane.c2p(r * np.cos(theta.get_value()), 0),
                plane.c2p(
                    r * np.cos(theta.get_value()),
                    r * np.sin(theta.get_value())
                ),
                stroke_width=6,
                color="#87ff78"
            )
        )

        self.add(vector, x_component, y_component)

        # Arrow length label
        length_label = always_redraw(
            lambda: MathTex(r"\sqrt{p}=\sqrt{29}")
            .scale(0.7)
            .next_to(vector.get_end(), UP)
        )

        self.add(length_label)

        # Live x and y readouts
        x_value = always_redraw(
            lambda: DecimalNumber(
                r * np.cos(theta.get_value()),
                num_decimal_places=2,
                color="#9ab5ff"
            ).next_to(plane, RIGHT, buff=1).shift(UP)
        )

        y_value = always_redraw(
            lambda: DecimalNumber(
                r * np.sin(theta.get_value()),
                num_decimal_places=2,
                color="#87ff78"
            ).next_to(plane, RIGHT, buff=1).shift(DOWN)
        )

        x_label = MathTex("x =", color="#9ab5ff"
                          ).next_to(x_value, LEFT)
        y_label = MathTex("y =", color="#87ff78"
                          ).next_to(y_value, LEFT)

        self.add(x_label, x_value, y_label, y_value)

        self.wait(0.5)

        # Guess-and-check angles (non-monotone)
        angles = [
            PI / 6,
            PI / 12,
            PI / 4,
            PI / 8,
            PI / 3
        ]

        for a in angles:
            self.play(
                theta.animate.set_value(a),
                run_time=1.7,
                rate_func=smooth
            )
            self.wait(0.5)

        self.wait(1)