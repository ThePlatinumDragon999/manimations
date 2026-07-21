from manim import *
import numpy as np

# A Gaussian integer is a complex number whose real and imaginary parts are
# both integers.

# Note that if we have a prime p of the form 4k + 1, Fermat's two squares theorem implies
# that there are positive integers x and y such that x^2 + y^2 = p. 
# Given p, we want to show that x and y exist.

# An explicit algorithm would be one that takes a prime p, and spits out the x and y
# that "work". But this is equivalent to factoring into (x + yi)(x - yi) = p, 
# where x and y are integers.

# The Gaussian integer z = x + yi has norm x^2 + y^2 = p
# So the modulus is \sqrt{x^2 + y^2} = \sqrt{p}

# So every Gaussian factor of p lies exactly on the circle
# x^2 + y^2 = p

# This is a Manim class that illustrates the "guess-and-check" problem.
# To represent p as a sum of two squares requires finding an x component 
# and a y component that are both integers. But that's hard to do, so 
# we change the angle randomly and hope we land on an integer.
class FactorGaussian9(Scene):
    # Every Manim animation is a subclass of Scene.
    # Overriding the construct method is how one creates animations.
    def construct(self):
        
        # p is a prime of the form 4K + 1
        p = 29

        # radius of the circle we'll be going over to check at various angles
        r = np.sqrt(p)

        # Defines a number plane with visible coordinates
        # Third param for x_range and y_range is step size
        # Add_coordinates adds tics
        plane = NumberPlane(
            x_range=[0, 6, 1],
            y_range=[0, 6, 1],
            background_line_style={"stroke_opacity": 0.4}
        ).add_coordinates()

        # Move plane so origin is bottom-left of frame
        plane.to_corner(DL)

        # Adds the plane to the scene automatically without animating it
        self.add(plane)

        # Axis labels
        # Also adds them without animating them
        re_label = MathTex(r"\mathrm{Re}").next_to(plane.x_axis, RIGHT)
        im_label = MathTex(r"\mathrm{Im}").next_to(plane.y_axis, UP)
        self.add(re_label, im_label)

        # Angle tracker
        theta = ValueTracker(0)

        # This draws an arrow starting from the origin of the coordinate plane
        # to the circle x^2 + y^2 = p^2

        # always_redraw is a function that takes another function that creates an
        # object and makes sure that it is updated ever frame.
        # Since theta will change over the course of the animation, we want to make
        # sure that the arrow is also updated over the course of the animation.
        vector = always_redraw(
            # Anonymous function that creates an Arrow from the origin
            # to the circle

            # plane.c2p takes a coordinate (on the plane) and gives the point on the
            # screen. This makes sure that the arrow is drawn correctly if I later
            # decide to move the screen (since the arrow is at the origin of the plane)
            lambda: Arrow(
                plane.c2p(0, 0),
                plane.c2p(
                    r * np.cos(theta.get_value()),
                    r * np.sin(theta.get_value())
                ),
                # Makes sure that there is no buffer between the arrow and the
                # two endpoints
                buff=0,
                color="#b00b69"
            )
        )

        # Dotted projections
        # Same idea as before, using an anonymous function and always_redraw
        # We draw the horizontal and vertical components of the arrow
        x_component = always_redraw(
            lambda: DashedLine(
                plane.c2p(0, 0),
                plane.c2p(r * np.cos(theta.get_value()), 0),
                stroke_width=6,
                color="#9ab5ff"
            )
        )

        y_component = always_redraw(
            lambda: DashedLine(
                plane.c2p(r * np.cos(theta.get_value()), 0),
                plane.c2p(
                    r * np.cos(theta.get_value()),
                    r * np.sin(theta.get_value())
                ),
                stroke_width=6,
                color="#87ff78"
            )
        )

        # Adds the vector and its projections to the scene without animation
        self.add(vector, x_component, y_component)

        # Arrow length label
        length_label = always_redraw(
            lambda: MathTex(r"\sqrt{p}=\sqrt{29}")
            .scale(0.7)
            .next_to(vector.get_end(), UP)
        )

        # Adds vector label to scene without animation
        self.add(length_label)

        # Live x and y readouts
        # Set at the right of the coordinate plane
        x_value = always_redraw(
            lambda: DecimalNumber(
                r * np.cos(theta.get_value()),
                num_decimal_places=2,
                color="#9ab5ff"
            ).next_to(plane, RIGHT, buff=1).shift(UP)
        )

        y_value = always_redraw(
            lambda: DecimalNumber(
                r * np.sin(theta.get_value()),
                num_decimal_places=2,
                color="#87ff78"
            ).next_to(plane, RIGHT, buff=1).shift(DOWN)
        )

        # Labels for the x and y readouts.
        x_label = MathTex("x =", color="#9ab5ff"
                          ).next_to(x_value, LEFT)
        y_label = MathTex("y =", color="#87ff78"
                          ).next_to(y_value, LEFT)
        
        # Adds the x and y readouts and corresponding labels to the scene
        # without animating them
        self.add(x_label, x_value, y_label, y_value)

        # Wait for a bit before starting the animation (aka changing theta)
        self.wait(0.5)

        # List of angles to guess-and-check (non-monotone)
        angles = [
            PI / 6,
            PI / 12,
            PI / 4,
            PI / 8,
            PI / 3
        ]

        # Iterate over the angle list
        # This changes theta, which then updates the arrow, its projections, and the
        # x and y readouts since they are plugged into the always_redraw() function
        for a in angles:
            self.play(
                # The animate keyword makes the theta change slowly (specified by
                # run_time variable)
                theta.animate.set_value(a),
                run_time=1.7,
                # This makes the animation use ease-in ease-out
                rate_func=smooth
            )
            # Wait for a bit before changing to the next theta value
            self.wait(0.5)

        self.wait(1)