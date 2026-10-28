from manim import *
import numpy as np

# von Foerster, Mora & Amiot (1960): N(t) = K / (t0 - t)^k
K_CONST = 1.79e11
EXP_K   = 0.990
# Friday, Nov 13, 2026
T_DOOM  = 2026.87
T_START = 1700
T_END   = 2100     # right end of the x-axis (leaves room for the date tag)
POP_MAX = 1000     # population axis tops out at 1 trillion (units: billions)
FONT    = "OpenDyslexic"

# Colors
CURVE_COLOR = "#9AB5FF"   # the graph
TIP_COLOR   = "#87FF78"   # dot + population readout
DOOM_COLOR  = "#B00B69"   # asymptote, date tag, arrow


def pop(t):
    return K_CONST / (T_DOOM - t) ** EXP_K


def fmt_pop(n):
    b = n / 1e9
    return f"{b / 1000:,.2f} trillion" if b >= 1000 else f"{b:,.2f} billion"


class DoomsdayGraph(Scene):
    # Years before t0 where the dot stops
    END_TAU = 0.05
    # Tick spacing
    X_TICK = 50      # years
    Y_TICK = 100     # billions

    def construct(self):
        # ---------- Axes (fixed for the whole animation) ----------
        axes = Axes(
            x_range=[T_START, T_END, self.X_TICK],
            y_range=[0, POP_MAX, self.Y_TICK],
            x_length=10,
            y_length=6,
            axis_config={"include_tip": False, "stroke_width": 2},
        )
        axes.shift(LEFT * 0.4 + UP * 0.25)

        # Measure positions after shifting
        origin_y = axes.c2p(T_START, 0)[1]
        axes_left = axes.c2p(T_START, 0)[0]
        wall_x = axes.c2p(T_DOOM, 0)[0]
        frame_top = config.frame_height / 2

        # Tick labels (Text, so no LaTeX is needed)
        x_labels = VGroup(*[
            Text(str(yr), font_size=18, font=FONT).next_to(
                axes.c2p(yr, 0), DOWN, buff=0.2)
            for yr in range(T_START, T_END + 1, self.X_TICK)
        ])
        y_labels = VGroup(*[
            Text(f"{v:,}", font_size=18, font=FONT).next_to(
                axes.c2p(T_START, v), LEFT, buff=0.2)
            for v in range(0, POP_MAX + 1, self.Y_TICK)
        ])

        # Axis titles
        x_title = Text("Year", font_size=24, font=FONT).next_to(
            x_labels, DOWN, buff=0.25)
        y_title = Text("Population (billions)", font_size=24, font=FONT).rotate(
            PI / 2).next_to(y_labels, LEFT, buff=0.25)

        # ---------- Parametrization ----------
        # tau = years remaining = e^(-u). Constant speed in u gives even curve
        # sampling and a smooth exponential approach, however steep it gets.
        u0 = -np.log(T_DOOM - T_START)
        u1 = -np.log(self.END_TAU)
        u = ValueTracker(u0)

        def tau_now():
            return np.exp(-u.get_value())

        def point(uu):
            t = T_DOOM - np.exp(-uu)
            return axes.c2p(t, pop(t) / 1e9)

        # ---------- Curve + dot ----------
        # Nothing clips the curve, so it simply runs off the top of the frame.
        curve = always_redraw(lambda: ParametricFunction(
            point, t_range=[u0, max(u.get_value(), u0 + 1e-3), 0.02],
            color=CURVE_COLOR, stroke_width=4,
        ))
        dot = always_redraw(lambda: Dot(
            point(u.get_value()), color=TIP_COLOR, radius=0.08,
        ))

        # ---------- Asymptote (fades in as the wall approaches) ----------
        wall = DashedLine(
            [wall_x, origin_y, 0],
            [wall_x, frame_top + 0.3, 0],
            dash_length=0.25, color=DOOM_COLOR, stroke_width=3,
        )

        def update_wall(m):
            m.set_opacity(float(np.clip((70 - tau_now()) / 30, 0, 1)))

        wall.set_opacity(0)
        wall.add_updater(update_wall)

        # ---------- Live N(t) readout ----------
        # Sits up-and-left of the tip. Once the tip runs off the top of the
        # frame the readout stays pinned at the top, just left of the wall.
        def make_label():
            tau = tau_now()
            t = T_DOOM - tau
            yr = f"{int(t)}" if tau >= 5 else f"{t:.2f}"
            rows = [
                Text(yr, font_size=22, color=WHITE, font=FONT),
                Text(fmt_pop(pop(t)), font_size=22, color=TIP_COLOR, font=FONT),
            ]
            g = VGroup(*rows).arrange(DOWN, buff=0.08)
            bg = BackgroundRectangle(g, color=BLACK, fill_opacity=0.6, buff=0.08)
            grp = VGroup(bg, g)

            tip = point(u.get_value())
            w, h = grp.width, grp.height
            x = max(tip[0] - 0.2 - w / 2, axes_left + 0.1 + w / 2)
            y = min(tip[1] + 0.2 + h / 2, frame_top - 0.15 - h / 2)
            grp.move_to([x, y, 0])
            return grp

        label = always_redraw(make_label)

        self.add(axes, x_labels, y_labels, x_title, y_title,
                 wall, curve, dot, label)

        # ---------- Run ----------
        self.wait(0.5)
        self.play(u.animate.set_value(u1), run_time=12,
                  rate_func=rate_functions.ease_in_sine)

        # Tip is long gone off the top: fade out the readout that followed it
        label.clear_updaters()
        self.play(FadeOut(label), run_time=1)

        # ---------- Date tag ----------
        # Above the x-axis, right of the asymptote, arrow down to the axis.
        date = VGroup(
            Text("November 13th,", font=FONT, color=DOOM_COLOR),
            Text("2026", font=FONT, color=DOOM_COLOR),
        ).arrange(DOWN, buff=0.12)
        date.scale_to_fit_width(3.3)
        date.move_to([wall_x + 0.6 + date.width / 2, origin_y + 1.7, 0])

        arrow = Arrow(
            start=[wall_x + 0.9, date.get_bottom()[1] - 0.1, 0],
            end=[wall_x + 0.04, origin_y + 0.04, 0],
            buff=0, color=DOOM_COLOR, stroke_width=4,
        )

        self.play(
            LaggedStart(
                GrowArrow(arrow),
                FadeIn(date, shift=UP * 0.2),
                lag_ratio=0.5,
            ),
            run_time=1.5,
        )
        self.wait(3)