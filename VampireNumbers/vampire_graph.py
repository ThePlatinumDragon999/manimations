
from manim import *


class VampireZoom(MovingCameraScene):
    def construct(self):
        # --------------------------------------------------
        # Configuration
        # --------------------------------------------------
        max_limit = 100_000
        start_limit = 10_000

        image_path = (
            "vampire_density_6_full_lim100000_scale50.svg"
        )

        graph_size = 12

        # --------------------------------------------------
        # Axes
        # --------------------------------------------------
        axes = Axes(
            x_range=[0, max_limit, 10_000],
            y_range=[0, max_limit, 10_000],
            x_length=graph_size,
            y_length=graph_size,
            axis_config={
                "color": WHITE,
                "stroke_width": 2,
                "include_ticks": True,
                "include_numbers": True,
                "font_size": 20,
            },
            tips=False,
        )

        # Axis labels
        x_label = Text("Fang 1", font_size=30)
        x_label.next_to(
            axes.x_axis, DOWN, buff=0.45
        )

        y_label = Text("Fang 2", font_size=30)
        y_label.rotate(90 * DEGREES)
        y_label.next_to(
            axes.y_axis, LEFT, buff=0.45
        )

        # --------------------------------------------------
        # Density image
        # --------------------------------------------------
        density = SVGMobject(image_path)

        density.stretch_to_fit_width(graph_size)
        density.stretch_to_fit_height(graph_size)

        # Center the image on the axes' coordinate square.
        density.move_to(
            (axes.c2p(0, 0) + axes.c2p(
                max_limit, max_limit
            )) / 2
        )

        # Put the image behind the axes
        self.add(density)

        # Keep the axes and labels fixed on screen
        self.add_fixed_in_frame_mobjects(
            axes, x_label, y_label
        )

        # The origin is in the lower left corner of the graph.
        origin = axes.c2p(0, 0)

        # Start with the full-sized image, but show only the
        # lower-left 10% region using a clipping window.
        # For this approach, keep the camera stationary and
        # animate the image around the origin instead.

        self.wait(1)

        self.play(
            density.animate.scale(
                0.1, about_point=origin
            ),
            run_time=8,
            rate_func=smooth,
        )

        self.wait(2)