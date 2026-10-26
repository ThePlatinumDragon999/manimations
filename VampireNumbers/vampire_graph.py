from manim import *


class VampireZoom(MovingCameraScene):
    def construct(self):
        # Configuration
        max_limit = 100_000
        start_limit = 10_000

        image_path = "graphs/vampire_density_7_lim10000_scale50.svg"
        new_image_path = "graphs/vampire_density_7_full_lim10000_scale50.svg"
        graph_size = 12

        # Axes
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

        # Initial Axes (0 to 10k range with 1k ticks)
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

        # Labels brought closer using a smaller buff (0.15)
        x_label_small = Text(
            "Fang 1", font_size=30, font="OpenDyslexic", color="#B00B69"
        )
        x_label_small.next_to(axes_small.x_axis, DOWN, buff=0.15)

        y_label_small = Text(
            "Fang 2", font_size=30, font="OpenDyslexic", color="#B00B69"
        )
        y_label_small.rotate(90 * DEGREES)
        y_label_small.next_to(axes_small.y_axis, LEFT, buff=0.15)

        group_small = VGroup(axes_small, x_label_small, y_label_small)

        # Final Axes (0 to 100k range with 10k ticks)
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
        x_label_large.next_to(axes_large.x_axis, DOWN, buff=0.15)

        y_label_large = Text(
            "Fang 2", font_size=30, font="OpenDyslexic", color="#B00B69"
        )
        y_label_large.rotate(90 * DEGREES)
        y_label_large.next_to(axes_large.y_axis, LEFT, buff=0.15)

        group_large = VGroup(axes_large, x_label_large, y_label_large)
        group_large.set_opacity(0)  # Start hidden

        # Density image
        density = SVGMobject(image_path)

        density.stretch_to_fit_width(graph_size)
        density.stretch_to_fit_height(graph_size)

        # Center the image on the axes' coordinate square.
        density.move_to((axes.c2p(0, 0) + axes.c2p(max_limit, max_limit)) / 2)

        # Start with the image invisible.
        density.set_opacity(0)

        # Add density image to the regular scene (so it scales/moves)
        self.add(density)

        # Lock the axes group to the camera frame so they stay fixed on screen
        self.camera.frame.add(group_small, group_large)
        # Also add them to the scene so they render
        self.add(group_small, group_large)

        # The origin is in the lower left corner of the graph.
        origin = axes.c2p(0, 0)

        self.play(FadeIn(group_small), run_time=1)
        self.wait(0.5)

        # Then fade in the density image.
        self.play(
            density.animate.set_opacity(1),
            run_time=1.5,
            rate_func=smooth,
        )

        self.wait(1)

        # Zoom out (scale down) while cross-fading the small grid into the large grid
        self.play(
            density.animate.scale(0.1, about_point=origin),
            group_small.animate.set_opacity(0),
            group_large.animate.set_opacity(1),
            run_time=8,
            rate_func=smooth,
        )

        self.wait(2)

        # Replace density image
        new_density = SVGMobject(new_image_path)
        new_density.stretch_to_fit_width(graph_size)
        new_density.stretch_to_fit_height(graph_size)

        # Match the position and scale of the original image.
        new_density.move_to(
            (axes.c2p(0, 0) + axes.c2p(max_limit, max_limit)) / 2
        )

        # Apply the exact same zoom transformation about the origin
        new_density.scale(0.1, about_point=origin)

        # Start invisible, then fade in over the original.
        new_density.set_opacity(0)
        self.add(new_density)

        self.play(
            new_density.animate.set_opacity(1),
            run_time=2,
            rate_func=smooth,
        )

        self.wait(2)