# Needed for command line arguments
import argparse
import matplotlib.pyplot as plt
import numpy as np


def draw_right_triangle(a, b, thickness=5, output="triangle.png", dpi=300):
    if a <= 0 or b <= 0:
        raise ValueError("Side lengths must be positive.")

    # Vertices: right angle at the origin
    x = [0, a, 0, 0]
    y = [0, 0, b, 0]

    # Scale the canvas to the triangle's proportions
    fig, ax = plt.subplots(figsize=(6, 6), facecolor="black")
    ax.set_facecolor("black")

    ax.plot(
        x, y,
        color="white",
        linewidth=thickness,
        solid_capstyle="round",
        solid_joinstyle="round",
    )

    # Equal scaling preserves the triangle's true proportions
    padding = 0.08 * max(a, b)
    ax.set_xlim(-padding, a + padding)
    ax.set_ylim(-padding, b + padding)
    ax.set_aspect("equal")
    ax.axis("off")

    # Remove all whitespace around the drawing
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)

    fig.savefig(
        output,
        dpi=dpi,
        facecolor="black",
        bbox_inches=None,
        pad_inches=0,
    )
    plt.close(fig)

# Sets up command line
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate a white right triangle on a black background."
    )
    parser.add_argument("a", type=float, help="Horizontal leg length")
    parser.add_argument("b", type=float, help="Vertical leg length")
    parser.add_argument("--thickness", type=float, default=5,
                        help="Line thickness in points (default: 5)")
    parser.add_argument("--output", default="triangle.png",
                        help="Output PNG filename")
    parser.add_argument("--dpi", type=int, default=300,
                        help="Image resolution (default: 300)")

    args = parser.parse_args()

    draw_right_triangle(
        args.a, args.b, args.thickness, args.output, args.dpi
    )
