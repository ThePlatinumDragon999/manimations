from manim import *
import numpy as np

FONT = "OpenDyslexic"
FS = 30

# Sets the geometry of the x-axis (the paper's t0)
T0_AXIS = 2026.87

# Shifts so that year 0 sits at x = 0 (log10(2026.87) = 3.307)
LOG_OFF = 3.31

# Right edge of the axis (the present)
YEAR_MAX = 2022

# (year, population in millions)
DATA = [
    (0, 100), (1000, 200), (1650, 545), (1750, 694),
    (1800, 906), (1800, 906), (1800, 919),
    (1810, 682), (1828, 847), (1845, 1009),
    (1850, 1171), (1850, 1098), (1850, 1094),
    (1874, 1391), (1886, 1483), (1900, 1550), (1920, 1834),
    (1935, 1995), (1939, 2170), (1950, 2517), (1950, 2406),
    (1958, 2852),   # ref 11: World Almanac 1960
    (1957, 2800),   # STANDBY for ref 25 (Britannica 1959)
    (1955, 2700),   # STANDBY for ref 26 (World Almanac 1958)
]

# Source (ref number) of each point in DATA, same order
REFS = [14, 14, 14, 20, 14, 21, 22, 23, 23, 23, 14, 21, 20,
        23, 23, 20, 20, 10, 24, 14, 20, 11, 25, 26]
assert len(REFS) == len(DATA)

# box order: 2 rows of 5
REF_ORDER = [10, 11, 14, 20, 21, 22, 23, 24, 25, 26]

# refs I don't have yet
STANDINS = {11, 25, 26}

# DATA indices of the guessed values
FUZZY = {5, 11}

# Curves tried, as (K in units of 1e11, k, t0). The last one is the paper's published fit.
# The earlier t0 values are placeholders: edit freely (keep t0 > 1958).
ATTEMPTS = [
    (0.16, 0.550, 2100.00),
    (2.00, 1.050, 2080.00),
    (1.00, 0.850, 2050.00),
    (1.40, 0.950, 2035.00),
    (1.79, 0.990, 2026.87),   # paper
]

# calendar years to label
X_TICKS = (0, 1000, 1700, 1900, 2000, 2020)

# log10 of population in millions
Y_MIN, Y_MAX = 1.6, 4.6


def txt(s, size=FS, **kw):
    return MarkupText(s, font=FONT, font_size=size, **kw)


def X_of(year):
    """Axis position: log of the time left to 2026.87, flipped so time runs left to right."""
    return LOG_OFF - np.log10(T0_AXIS - year)


def Y(pop_millions):
    return np.log10(pop_millions)


class DoomsdayLogLog(Scene):
    def construct(self):
        K_t = ValueTracker(ATTEMPTS[0][0])
        k_t = ValueTracker(ATTEMPTS[0][1])
        t0_t = ValueTracker(ATTEMPTS[0][2])
        line_op = ValueTracker(0)
        rows_op = ValueTracker(0)

        # ------------------------- axes (fixed) -------------------------
        axes = Axes(
            x_range=[0, X_of(YEAR_MAX), 1], y_range=[Y_MIN, Y_MAX, 1],
            x_length=7.0, y_length=3.7, tips=False,
            axis_config={"include_ticks": False, "stroke_width": 2},
        ).move_to(LEFT * 2.3 + UP * 0.55)

        x_ticks, x_labels = VGroup(), VGroup()
        for yr in X_TICKS:
            p = axes.c2p(X_of(yr), Y_MIN)
            x_ticks.add(Line(p, p + DOWN * 0.1, stroke_width=2))
            x_labels.add(txt(str(yr), 22).move_to(p + DOWN * 0.35))

        y_ticks, y_labels = VGroup(), VGroup()
        for v, lbl in {2: "100M", 3: "1B", 4: "10B"}.items():
            p = axes.c2p(0, v)
            y_ticks.add(Line(p, p + LEFT * 0.1, stroke_width=2))
            y_labels.add(txt(lbl, 22).next_to(p, LEFT, buff=0.15))

        x_title = txt("Year (log scale)", 24).move_to(
            axes.c2p(X_of(YEAR_MAX) / 2, Y_MIN) + DOWN * 0.85)
        y_title = txt("World population (log scale)", 24).move_to(
            axes.get_corner(UL) + UP * 0.3, aligned_edge=LEFT)

        # "Well, the authors had a way to test it."
        self.play(Create(axes), FadeIn(x_ticks, y_ticks, x_labels, y_labels, x_title, y_title))
        self.wait(1)

        # "They took 24 different estimates..."
        dots = VGroup(*[
            Dot(axes.c2p(X_of(yr), Y(n)), radius=0.07, color=BLUE, fill_opacity=0.85)
            for yr, n in DATA
        ])
        self.play(FadeIn(dots), run_time=2)
        self.wait(1)

        # "And then they tried to fit their equation to the data"
        num = txt("K", 40)
        den = txt("(t<sub>0</sub> - t)<sup>k</sup>", 40)
        bar = Line(LEFT, RIGHT, stroke_width=3).set_width(max(num.width, den.width) + 0.3)
        frac = VGroup(num, bar, den).arrange(DOWN, buff=0.12)
        eq = VGroup(txt("N(t) =", 40), frac).arrange(RIGHT, buff=0.3)
        eq.to_edge(DOWN, buff=0.4)

        def build_curve():
            # 1e11 -> millions
            K = K_t.get_value() * 1e5
            k = k_t.get_value()
            xs = np.linspace(0, X_of(YEAR_MAX), 400)
            # straight line in the log-log plot: slope k, passing through the paper's axis
            ys = np.log10(K) - k * (LOG_OFF - xs)
            keep = (ys >= Y_MIN) & (ys <= Y_MAX)
            if keep.sum() < 2:
                return VMobject()
            pts = [axes.c2p(x, y) for x, y in zip(xs[keep], ys[keep])]
            curve = VMobject(color=YELLOW)
            curve.set_points_as_corners(pts)
            return curve.set_stroke(YELLOW, width=5, opacity=line_op.get_value())

        fit_curve = always_redraw(build_curve)

        row_ys = [1.7, 0.7, -0.3]

        def build_rows():
            items = [
                ("K =", f"{K_t.get_value():.2f} × 10<sup>11</sup>"),
                ("k =", f"{k_t.get_value():.3f}"),
                ("t<sub>0</sub> =", f"{t0_t.get_value():.2f}"),
            ]
            g = VGroup()
            for (lab, val), y in zip(items, row_ys):
                g.add(txt(lab).move_to([2.2, y, 0], aligned_edge=LEFT))
                g.add(txt(val).move_to([3.5, y, 0], aligned_edge=LEFT))
            return g.set_opacity(rows_op.get_value())

        rows = always_redraw(build_rows)

        self.play(FadeIn(eq))
        self.wait(0.5)
        self.add(fit_curve, rows)
        self.play(line_op.animate.set_value(1), rows_op.animate.set_value(1))
        self.wait(1.5)

        # "They used a method called least squares..."
        for K, k, t0 in ATTEMPTS[1:]:
            self.play(
                K_t.animate.set_value(K),
                k_t.animate.set_value(k),
                t0_t.animate.set_value(t0),
                run_time=2.5, rate_func=smooth,
            )
            self.wait(0.7)

        self.wait(1.5)

        # Fade everything except the points, then sort the points into boxes
        # stop always_redraw from fighting the fade
        fit_curve.clear_updaters()
        rows.clear_updaters()
        self.play(FadeOut(
            axes, x_ticks, y_ticks, x_labels, y_labels, x_title, y_title,
            eq, fit_curve, rows,
        ))
        self.wait(0.5)

        # build boxes and labels, but not shown yet
        BOX, GAP = 2.3, 0.3
        boxes, box_labels, box_of = VGroup(), VGroup(), {}
        for i, ref in enumerate(REF_ORDER):
            r, c = divmod(i, 5)
            sq = Square(BOX, stroke_width=2).move_to(
                [(c - 2) * (BOX + GAP), 1.5 - r * 3.1, 0])
            name = f"Ref {ref}" + (" (stand-in)" if ref in STANDINS else "")
            lab = txt(name, 20).next_to(sq, UP, buff=0.12)
            if lab.width > BOX:
                lab.scale_to_fit_width(BOX)
            boxes.add(sq)
            box_labels.add(lab)
            box_of[ref] = sq

        # work out where each dot lands, and its text label
        slot = {ref: 0 for ref in REF_ORDER}
        moves, entry_labels = [], VGroup()
        for i, ((yr, n), ref, dot) in enumerate(zip(DATA, REFS, dots)):
            sq = box_of[ref]
            k = slot[ref]
            slot[ref] += 1
            y = sq.get_top()[1] - 0.3 - 0.3 * k
            x = sq.get_left()[0] + 0.28
            moves.append(dot.animate.move_to([x, y, 0]))

            tilde = "~" if i in FUZZY else ""
            t = txt(f"{yr}: {tilde}{n:,}M", 14)
            avail = BOX - 0.5 - 0.1
            if t.width > avail:
                t.scale_to_fit_width(avail)
            t.move_to([x + 0.22, y, 0], aligned_edge=LEFT)
            entry_labels.add(t)

        # dots travel to their slots, alone on the screen
        self.play(LaggedStart(*moves, lag_ratio=0.08), run_time=4)
        self.wait(0.5)

        # then the boxes, titles and entry text fade in around them
        self.play(FadeIn(boxes, box_labels, entry_labels), run_time=1.5)
        self.wait(3)