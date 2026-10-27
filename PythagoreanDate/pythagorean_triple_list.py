
from math import isqrt
from manim import *


# Colors for the three numbers
A_COLOR = "#B00B69"
B_COLOR = "#87FF78"
C_COLOR = "#9AB5FF"

FONT = "OpenDyslexic"

def make_term(number, color, font_size=26):
    """Create a colored number with a properly positioned superscript."""
    base = Text(
        str(number),
        font=FONT,
        font_size=font_size,
        color=color,
    )

    exponent = Text(
        "2",
        font=FONT,
        font_size=font_size * 0.60,
    )

    # Position the exponent above and to the right of the base.
    exponent.move_to(
        base.get_corner(UR) + 0.05 * UP + 0.08 * RIGHT
    )

    return VGroup(base, exponent)


def make_equation(a, b, c, font_size=26):
    """Create a² + b² = c² with independently colored base numbers."""
    term_a = make_term(a, A_COLOR, font_size)
    term_b = make_term(b, B_COLOR, font_size)
    term_c = make_term(c, C_COLOR, font_size)

    plus = Text("+", font=FONT, font_size=font_size)
    equals = Text("=", font=FONT, font_size=font_size)

    equation = VGroup(
        term_a, plus, term_b, equals, term_c
    ).arrange(RIGHT, buff=0.12, aligned_edge=DOWN)

    return equation


class PythagoreanTriples(Scene):
    def construct(self):
        min_hypotenuse=26
        max_hypotenuse = 88
        columns = 4
        cell_width = 3.0
        x_spacing = 3.35
        y_spacing = 0.80

        # Find all triples with c strictly less than 100.
        triples = []

        for a in range(1, max_hypotenuse):
            for b in range(a, max_hypotenuse):
                c_squared = a * a + b * b
                c = isqrt(c_squared)

                if c * c == c_squared and min_hypotenuse < c < max_hypotenuse:
                    triples.append((a, b, c))

        # Sort by hypotenuse, then by the two legs.
        triples.sort(key=lambda triple: (
            triple[2], triple[0], triple[1]
        ))

        # Build the grid.
        equations = []

        for i, (a, b, c) in enumerate(triples):
            equation = make_equation(a, b, c)

            if equation.width > cell_width:
                equation.scale_to_fit_width(cell_width)

            row = i // columns
            col = i % columns

            x = (col - (columns - 1) / 2) * x_spacing
            y = 3.1 - row * y_spacing

            equation.move_to([x, y, 0])
            equations.append(equation)

        # Reveal equations one after another, with overlap.
        self.play(
            LaggedStart(
                *[
                    FadeIn(eq, shift=0.08 * UP)
                    for eq in equations
                ],
                lag_ratio=0.05,
            ),
            run_time=4,
        )

        self.wait(1)