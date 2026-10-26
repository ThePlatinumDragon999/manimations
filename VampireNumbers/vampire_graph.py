from manim import *


class VampireZoom(MovingCameraScene):
    def construct(self):
        # --------------------------------------------------
        # Configuration
        # --------------------------------------------------
        max_limit = 100_000
        start_limit = 10_000
        image_path = "graphs/vampire_density_7_lim10000_scale50.svg"
        graph_size = 12

        # --------------------------------------------------
        # Initial Axes (10k range for zoomed-in start)
        # --------------------------------------------------
        axes_small = Axes(
            x_range=[0, start_limit, 1_000],
            y_range=[0, start_limit, 1_000],
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

        x_label_small = Text(
            "Fang 1", font_size=30, font="OpenDyslexic", color="#B00B69"
        )
        x_label_small.next_to(axes_small.x_axis, DOWN, buff=0.45)

        y_label_small = Text(
            "Fang 2", font_size=30, font="OpenDyslexic", color="#B00B69"
        )
        y_label_small.rotate(90 * DEGREES)
        y_label_small.next_to(axes_small.y_axis, LEFT, buff=0.45)

        group_small = VGroup(axes_small, x_label_small, y_label_small)

        # --------------------------------------------------
        # Target Axes (100k range for final zoomed-out view)
        # --------------------------------------------------
        axes_large = Axes(
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

        x_label_large = Text(
            "Fang 1", font_size=30, font="OpenDyslexic", color="#B00B69"
        )
        x_label_large.next_to(axes_large.x_axis, DOWN, buff=0.45)

        y_label_large = Text(
            "Fang 2", font_size=30, font="OpenDyslexic", color="#B00B69"
        )
        y_label_large.rotate(90 * DEGREES)
        y_label_large.next_to(axes_large.y_axis, LEFT, buff=0.45)

        group_large = VGroup(axes_large, x_label_large, y_label_large)

        # --------------------------------------------------
        # Density image
        # --------------------------------------------------
        density = SVGMobject(image_path)
        density.stretch_to_fit_width(graph_size)
        density.stretch_to_fit_height(graph_size)

        # Center the image on the initial coordinate square
        density.move_to(
            (axes_small.c2p(0, 0) + axes_small.c2p(start_limit, start_limit))
            / 2
        )

        # Start zoomed in on the 10k region (scale up by 10 relative to full frame)
        origin = axes_small.c2p(0, 0)
        density.scale(10, about_point=origin)

        # Add density to scene
        self.add(density)

        # Lock the initial axes group to the camera frame so they stay fixed on screen
        self.camera.frame.add(group_small)
        self.add(group_small)

        self.wait(1)

        # Scale outwards (zoom out) while transforming the axes/ticks to the 100k range
        self.play(
            density.animate.scale(0.1, about_point=origin),
            Transform(group_small, group_large),
            run_time=8,
            rate_func=smooth,
        )

        self.wait(2)