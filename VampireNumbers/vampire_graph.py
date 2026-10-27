from manim import *


class VampireZoom4(Scene):
    def construct(self):
        # Configuration
        max_limit = 100_000
        start_limit = 10_000
        tick_step = 10_000

        image_path = "graphs/vampire_density_7_g64_lim100000_scale50.svg"
        new_image_path = "graphs/vampire_density_7_full_lim100000_scale50.svg"
        graph_size = 5.5
        graph_shift = UP * 0.6   # move the whole graph up
        fade_zone = 0.3          # new ticks fade in over this distance just past the axis end
        num_buff = 0.15          # gap between a tick and its number
        x_title_buff = 0.6       # gap between x axis and "Fang 1"
        y_title_buff = 0.9       # gap between y axis and "Fang 2" (wider: "100k")

        # Reference axes, only used for positioning (origin / center)
        axes = Axes(
            x_range=[0, max_limit, tick_step],
            y_range=[0, max_limit, tick_step],
            x_length=graph_size,
            y_length=graph_size,
            tips=False,
        )
        axes.shift(graph_shift)
        origin = axes.c2p(0, 0)

        # Static axis lines (never change, so stroke width stays constant)
        x_line = Line(origin, origin + RIGHT * graph_size, color=WHITE, stroke_width=2)
        y_line = Line(origin, origin + UP * graph_size, color=WHITE, stroke_width=2)

        # Axis labels, pushed out past the tick numbers
        x_label = Text("Fang 1", font_size=30, font="OpenDyslexic", color="#B00B69")
        x_label.next_to(x_line, DOWN, buff=x_title_buff)
        y_label = Text("Fang 2", font_size=30, font="OpenDyslexic", color="#B00B69")
        y_label.rotate(90 * DEGREES)
        y_label.next_to(y_line, LEFT, buff=y_title_buff)

        for m in (x_line, y_line, x_label, y_label):
            m.set_z_index(3)

        # Zoom tracker: 1.0 = start view (0-10k), 0.1 = end view (0-100k)
        zoom = ValueTracker(1.0)

        tick_fade = ValueTracker(0.0)

        def make_ticks():
            s = zoom.get_value()
            ticks = VGroup()
            for v in range(0, max_limit + 1, tick_step):
                pos = v / start_limit * graph_size * s

                # Still too far past the end of the axis: not visible yet
                if pos > graph_size + fade_zone:
                    continue

                # Fully opaque anywhere on the axis (including the very end),
                # fading in only while it's approaching from past the end
                if pos <= graph_size + 1e-6:
                    opacity = 1.0
                else:
                    opacity = (graph_size + fade_zone - pos) / fade_zone
                opacity = max(0.0, min(1.0, opacity))
                opacity *= tick_fade.get_value()

                label_text = "0" if v == 0 else f"{v // 1000}k"

                # x-axis tick + number
                x_pt = origin + RIGHT * pos
                x_tick = Line(x_pt + DOWN * 0.07, x_pt + UP * 0.07, stroke_width=2, color=WHITE)
                x_num = Text(label_text, font_size=20).next_to(x_tick, DOWN, buff=num_buff)

                # y-axis tick + number
                y_pt = origin + UP * pos
                y_tick = Line(y_pt + LEFT * 0.07, y_pt + RIGHT * 0.07, stroke_width=2, color=WHITE)
                y_num = Text(label_text, font_size=20).next_to(y_tick, LEFT, buff=num_buff)

                group = VGroup(x_tick, x_num, y_tick, y_num)
                group.set_opacity(opacity)
                ticks.add(group)
            ticks.set_z_index(3)
            return ticks

        ticks = always_redraw(make_ticks)

        # Mask
        mask_kwargs = dict(fill_color=config.background_color, fill_opacity=1, stroke_width=0)
        big = 50
        right_mask = Rectangle(width=big, height=big * 2, **mask_kwargs)
        right_mask.move_to(origin + RIGHT * graph_size, aligned_edge=LEFT)
        top_mask = Rectangle(width=big * 2, height=big, **mask_kwargs)
        top_mask.move_to(origin + UP * graph_size, aligned_edge=DOWN)
        right_mask.set_z_index(2)
        top_mask.set_z_index(2)
        self.add(right_mask, top_mask)

        # Density image
        density = SVGMobject(image_path)
        density.set_width(graph_size)
        density.move_to((axes.c2p(0, 0) + axes.c2p(max_limit, max_limit)) / 2)
        density.scale(10, about_point=origin) 
        density.set_opacity(0)
        self.add(density)

        self.add(ticks)  # always_redraw mobject: add so it updates
        self.play(
            FadeIn(VGroup(x_line, y_line, x_label, y_label)), 
            tick_fade.animate.set_value(1.0),
            run_time=1
        )

        self.wait(0.5)

        self.play(density.animate.set_opacity(1), run_time=1.5, rate_func=smooth)

        self.wait(2)

        # Zoom out: image shrinks and tick positions follow the same scale
        self.play(
            density.animate.scale(0.1, about_point=origin),
            zoom.animate.set_value(0.1),
            run_time=18,
            rate_func=smooth,
        )

        self.wait(6)

        # Replace density image
        new_density = SVGMobject(new_image_path)
        new_density.set_width(graph_size)
        new_density.move_to((axes.c2p(0, 0) + axes.c2p(max_limit, max_limit)) / 2)
        new_density.set_opacity(0)
        self.add(new_density)

        self.play(new_density.animate.set_opacity(1), run_time=2, rate_func=smooth)
        self.wait(4)