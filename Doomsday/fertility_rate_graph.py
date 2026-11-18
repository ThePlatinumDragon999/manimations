import math
from manim import *

FONT = "OpenDyslexic"

def label(text, size=22, color=WHITE):
    # Render large, then scale down. Small font sizes get uneven glyph
    # spacing because of pixel rounding.
    BASE = 96
    t = Text(str(text), font=FONT, font_size=BASE, color=color)
    return t.scale(size / BASE)

class FertilityRate(Scene):
    def construct(self):
        data = [
            (1950, 3.15),
            (1951, 3.2),
            (1952, 3.26),
            (1953, 3.31),
            (1954, 3.37),
            (1955, 3.42),
            (1956, 3.47),
            (1957, 3.53),
            (1958, 3.58),
            (1959, 3.51),
            (1960, 3.44),
            (1961, 3.37),
            (1962, 3.3),
            (1963, 3.23),
            (1964, 3.1),
            (1965, 2.96),
            (1966, 2.82),
            (1967, 2.68),
            (1968, 2.54),
            (1969, 2.44),
            (1970, 2.34),
            (1971, 2.24),
            (1972, 2.13),
            (1973, 2.03),
            (1974, 1.98),
            (1975, 1.93),
            (1976, 1.88),
            (1977, 1.82),
            (1978, 1.77),
            (1979, 1.78),
            (1980, 1.79),
            (1981, 1.79),
            (1982, 1.8),
            (1983, 1.8),
            (1984, 1.83),
            (1985, 1.85),
            (1986, 1.87),
            (1987, 1.89),
            (1988, 1.92),
            (1989, 1.94),
            (1990, 1.96),
            (1991, 1.98),
            (1992, 2.01),
            (1993, 2.03),
            (1994, 2.02),
            (1995, 2.02),
            (1996, 2.01),
            (1997, 2.0),
            (1998, 2.0),
            (1999, 2.01),
            (2000, 2.01),
            (2001, 2.02),
            (2002, 2.03),
            (2003, 2.04),
            (2004, 2.05),
            (2005, 2.05),
            (2006, 2.05),
            (2007, 2.05),
            (2008, 2.06),
            (2009, 2.02),
            (2010, 1.98),
            (2011, 1.95),
            (2012, 1.91),
            (2013, 1.88),
            (2014, 1.86),
            (2015, 1.84),
            (2016, 1.82),
            (2017, 1.8),
            (2018, 1.78),
            (2019, 1.78),
            (2020, 1.78),
            (2021, 1.78),
            (2022, 1.78),
            (2023, 1.78),
            (2024, 1.79),
            (2025, 1.79),
            (2026, 1.79)
        ]

        years, fertility = zip(*data)
        assert all(a < b for a, b in zip(years, years[1:])), \
            "Years must be strictly increasing."

        # Ranges
        x_min = 10 * math.floor(years[0] / 10)
        x_max = 10 * math.ceil(years[-1] / 10)

        # Title
        title = label("Global fertility rate", 34).to_edge(UP, buff=0.4)

        # Axes
        axes = Axes(
            x_range=[x_min, x_max, 10],
            y_range=[1.5, 4, 0.5],
            x_length=11,
            y_length=5,
            axis_config={"include_numbers": False, "color": WHITE, "stroke_width": 5},
            tips=False,
        )

        axes.set_z_index(1)

        # Sit the graph just below the title instead of at the bottom edge
        axes.next_to(title, DOWN, buff=0.3)

        # Labels
        axes.x_axis.add_labels(
            {x: label(x) for x in range(x_min, x_max + 1, 10)},
            font_size = 22
        )
        axes.y_axis.add_labels(
            {y: label(y) for y in [1.5, 2, 2.5, 3, 3.5, 4]},
            font_size = 22
        )

        x_label = axes.get_x_axis_label(
            label("Year", 22), edge=DOWN, direction=DOWN, buff=0.45
        )
        y_label = axes.get_y_axis_label(
            label("Births per woman", 22).rotate(PI / 2),
            edge=LEFT, direction=LEFT, buff=0.6,
        )

        # Bars
        # width of one year on screen
        unit_x = axes.x_length / (x_max - x_min)
        # small gap between bars
        bar_width = unit_x * 0.9
        base_y = axes.c2p(0, 1.5)[1]

        colors = color_gradient(["#87FF78", "#9AB5FF"], len(data))

        bars = VGroup()
        for (year, rate), color in zip(data, colors):
            height = axes.c2p(0, rate)[1] - base_y
            x_center = axes.c2p(year, 0)[0]

            is_first = (year == x_min)
            width = bar_width / 2 if is_first else bar_width

            bar = Rectangle(
                width=width,
                height=height,
                stroke_width=0,
                fill_color=color,
                fill_opacity=1,
            )

            # Left edge on the axis for the first bar, centered on the year for the rest
            left_x = x_center if is_first else x_center - width / 2
            bar.move_to([left_x + width / 2, base_y + height / 2, 0])
            bars.add(bar)

        # Animation
        self.play(FadeIn(title, axes, x_label, y_label), run_time=2)
        self.play(
            LaggedStart(
                *[GrowFromEdge(bar, DOWN) for bar in bars],
                lag_ratio=0.3,
            ),
            run_time=8,
            rate_func=linear,
        )
        self.wait(2)