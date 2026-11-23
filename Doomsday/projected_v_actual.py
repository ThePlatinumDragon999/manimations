
from manim import *
import numpy as np

FONT = "OpenDyslexic"
CURVE_COLOR = "#B00B69"
DOT_COLOR = "#9AB5FF"

class PopulationComparison(Scene):
    def construct(self):

        # Population data (year, population in millions)
        population_data = [
            (0, 100), 
            (1000, 200), 
            (1650, 545), 
            (1750, 694),
            (1800, 906),
            (1800, 906), 
            (1800, 919),
            (1810, 682), 
            (1828, 847), 
            (1845, 1009),
            (1850, 1171), 
            (1850, 1098), 
            (1850, 1094),
            (1874, 1391), 
            (1886, 1483), 
            (1900, 1550), 
            (1920, 1834),
            (1935, 1995), 
            (1939, 2170), 
            (1950, 2517), 
            (1950, 2406),
            # This one is also new
            (1955, 2758),
            (1958, 2852),
            # New estimates
            # (1959, 2970),
            (1960, 3018),
            # (1961, 3068),
            # (1962, 3126),
            (1963, 3195),
            # (1964, 3267),
            # (1965, 3332),
            # (1966, 3406),
            # (1967, 3475),
            # (1968, 3546),
            # (1969, 3620),
            (1970, 3682),
            # (1971, 3770),
            # (1972, 3844),
            # (1973, 3920),
            (1974, 3995),
            (1975, 4061),
            # (1976, 4142),
            # (1977, 4215),
            # (1978, 4289),
            # (1979, 4365),
            (1980, 4440),
            # (1981, 4524),
            # (1982, 4607),
            (1983, 4691),
            # (1984, 4775),
            (1985, 4853),
            # (1986, 4950),
            # (1987, 5040),
            (1988, 5132),
            (1989, 5223),
            (1990, 5310),
            # (1991, 5406),
            # (1992, 5492),
            # (1993, 5577),
            # (1994, 5660),
            (1995, 5735),
            # (1996, 5825),
            # (1997, 5906),
            (1998, 5987),
            # (1999, 6067),
            (2000, 6127),
            # (2001, 6230),
            # (2002, 6312),
            # (2003, 6393),
            # (2004, 6475),
            (2005, 6520),
            # (2006, 6641),
            # (2007, 6725),
            # (2008, 6811),
            # (2009, 6898),
            (2010, 6930),
            # (2011, 7073),
            # (2012, 7161),
            # (2013, 7250),
            # (2014, 7339),
            (2015, 7349),
            # (2016, 7513),
            (2017, 7599),
            # (2018, 7683),
            # (2019, 7764),
            # (2020, 7887),
            # (2021, 7909),
            # (2022, 7975),
            (2023, 8045),
            (2024, 8161),
            (2025, 8232)
        ]

        # Hyperbolic model parameters
        K = 1.79e11
        k = 0.990
        t0 = 2026.87

        def population_model(t):
            return K / ((t0 - t) ** k) / 1e6

        # Axes
        x_min, x_max = 1880, 2020
        y_min, y_max = 0, 20000

        axes = Axes(
            x_range=[x_min, x_max, 20],
            y_range=[y_min, y_max, 2000],
            x_length=11,
            y_length=5.5,
            tips=False,
        )

        x_labels = VGroup(*[
            Text(str(year), font=FONT, font_size=22)
            .next_to(axes.c2p(year, 0), DOWN, buff=0.2)
            for year in range(x_min, x_max + 1, 20)
        ])
        y_labels = VGroup(*[
            Text(str(value // 1000), font=FONT, font_size=22)
            .next_to(axes.c2p(x_min, value), LEFT, buff=0.2)
            for value in range(2000, y_max + 1, 2000)
        ])

        # Main title centered above the graph
        title = Text("Population (billions)", font=FONT, font_size=24)
        title.next_to(axes, UP, buff=0.4)

        # Small axis titles, centered along their axes
        x_title = Text("Year", font=FONT, font_size=20).next_to(x_labels, DOWN, buff=0.25)

        # Legend box (top-left, inside the empty part of the plot)
        line_sample = Line(LEFT * 0.3, RIGHT * 0.3, color=CURVE_COLOR, stroke_width=4)
        line_text = Text("Hyperbolic model", font=FONT, font_size=18)
        line_text.next_to(line_sample, RIGHT, buff=0.25)

        dot_sample = Dot(color=DOT_COLOR, radius=0.055)
        dot_sample.move_to(line_sample.get_center() + DOWN * 0.45)
        dot_text = Text("Historical estimates", font=FONT, font_size=18)
        dot_text.next_to(dot_sample, RIGHT, buff=0.25).align_to(line_text, LEFT)

        legend_content = VGroup(line_sample, line_text, dot_sample, dot_text)
        legend_box = SurroundingRectangle(
            legend_content, buff=0.25, color=GREY_B, stroke_width=2,
        )
        legend = VGroup(legend_box, legend_content)
        legend.move_to(axes.c2p(x_min, y_max), aligned_edge=UL).shift(RIGHT * 0.4 + DOWN * 0.3)

        self.play(
            FadeIn(axes, x_labels, y_labels, x_title, title, legend)
        )

        # Tracker = the year the curve has reached so far
        curve_end = min(x_max, t0 - (K / 1e6 / y_max) ** (1 / k))

        year_tracker = ValueTracker(x_min)

        curve = always_redraw(lambda: axes.plot(
            population_model,
            x_range=[x_min, max(x_min + 0.01, min(year_tracker.get_value(), curve_end)), 0.25],
            color=CURVE_COLOR,
            stroke_width=4,
            use_smoothing=True,
        ))

        # Dots: each fades in as the tracker passes its year
        FADE_YEARS = 6  # bigger = slower fade-in

        dots = VGroup()
        for year, population in population_data:
            if not (x_min <= year <= x_max):
                continue
            dot = Dot(axes.c2p(year, population), color=DOT_COLOR, radius=0.055)
            dot.set_opacity(0)
            dot.add_updater(
                lambda d, y=year: d.set_opacity(
                    float(np.clip((year_tracker.get_value() - y) / FADE_YEARS, 0, 1))
                )
            )
            dots.add(dot)

        self.add(curve, dots)

        # Sweep a little past 2020 so the last dots finish fading in
        sweep_end = x_max + FADE_YEARS
        sweep_time = 8 * (sweep_end - x_min) / (x_max - x_min)  # same speed as before

        self.play(
            year_tracker.animate.set_value(sweep_end),
            run_time=sweep_time,
            rate_func=linear,
        )

        self.wait(3)

        # Section for moving newer population estimates closer to hyperbolic model
        START_YEAR = 1960
        # Maximum deviation from the model, in millions
        DEVIATION = 100

        animations = []

        for (year, population), dot in zip(
            [(y, p) for y, p in population_data if x_min <= y <= x_max],
            dots
        ):
            if year < START_YEAR:
                continue

            # Target population from the hyperbolic model
            target_population = population_model(year)

            # Keep small deviation from curve
            # Use sine to alternate slightly above and below
            offset = DEVIATION * np.sin(year * 1.7)

            target = axes.c2p(year, target_population + offset)

            animations.append(
                dot.animate.move_to(target)
            )

        self.play(
            AnimationGroup(
                *animations,
                lag_ratio=0.08,
            ),
            run_time=3,
            rate_func=smooth,
        )

        self.wait(3)