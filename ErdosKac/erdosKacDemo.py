import numpy as np
from manim import *


def omega_sieve(N):
    omega = np.zeros(N + 1, dtype=int)

    for p in range(2, N + 1):
        if omega[p] == 0:
            omega[p::p] += 1

    return omega


# Precompute histograms
sizes = list(range(10000, 1000001, 10000))

omega = omega_sieve(max(sizes))

histograms = {}

for N in sizes:
    values = omega[2:N+1]
    counts = np.bincount(values)
    counts = counts / len(values)   # normalize to probabilities
    histograms[N] = counts


class ErdosKac2(Scene):

    def make_histogram(self, counts, axes):

        bars = VGroup()

        for k, c in enumerate(counts):

            # Convert data coordinates into screen coordinates
            left = axes.c2p(k, 0)
            right = axes.c2p(k + 0.8, c)

            width = right[0] - left[0]
            height = right[1] - left[1]

            bar = Rectangle(
                width=width,
                height=height,
                fill_opacity=1,
                stroke_width=0,
                color=BLUE,
            )

            bar.align_to(left, DL)

            bars.add(bar)

        return bars


    def construct(self):

        # Fixed axes
        xmax = max(len(c) for c in histograms.values()) - 1
        ymax = max(max(c) for c in histograms.values())

        axes = Axes(
            x_range=[0, xmax + 1, 1],
            y_range=[0, ymax * 1.1, ymax / 5],
            x_length=8,
            y_length=5,
            tips=False,

            x_axis_config={
                "include_numbers": True,
            },

            y_axis_config={
                "include_numbers": False,
                "include_ticks": False,
                "stroke_width": 0,
            },
        )

        labels = axes.get_axis_labels(
            x_label="\\omega(n)",
            y_label=""
        )


        # Initial histogram
        bars = self.make_histogram(
            histograms[10000],
            axes
        )

        self.play(
            FadeIn(axes),
            FadeIn(labels),
            FadeIn(bars)
        )


        # Animate growing N
        for N in sizes[1:]:

            new_bars = self.make_histogram(
                histograms[N],
                axes
            )

            self.play(
                Transform(bars, new_bars),
                run_time=0.05
            )

        self.wait(2)