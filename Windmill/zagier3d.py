from manim import *
import numpy as np

# This is a class that shows the Zagier involution in action.
# It generates a 3d surface, namely x^2 + 4yz = p (for a fixed prime of the form 4k + 1)

# Even though the involution is only defined over the integers (aka lattice points in R^3),
# I think this is useful for visualization.

# The code then looks at pseudo-Pythagorean triples x, y, z that satisfy
# x^2 + 4yz = p, and performs the Zagier involution on them.

# It then plots them on the graph. It also considers the fixed point, and colors it
# a different color

# Normally, you would inherit from Scene, but since this is 3D, you inherit
# from the specific ThreeDScene class. Note that you still overwrite the constructor
# as you would with a normal Scene subclass.
class ZagierInv1(ThreeDScene):
    def construct(self):

        # p should be a prime of the form 4k + 1
        p = 17

        # For a prime of the form 4k + 1, a fixed point of the Zagier
        # involution is (1, 1, k).
        # Note that if p = 4k + 1, then k = (p - 1) / 4
        fixed_point = np.array([1, 1, (p - 1) / 4])

        # Axes
        axes = ThreeDAxes(
            x_range=[0, 8, 1],
            y_range=[0, 8, 1],
            z_range=[0, 8, 1],
            x_length=6,
            y_length=6,
            z_length=4
        )
        labels = axes.get_axis_labels(x_label="x", y_label="y", z_label="z")

        # Adds a camera to the scene. phi is the vertical viewing angle
        # and theta is the horizontal viewing angle
        # Phi is defined the same as in spherical coordinates.
        # phi = 0 looks down on x-y plane vertically

        # theta = 0 has +x pointing into the screen, and +y to the right
        # Increasing theta rotates the xy-plane clockwise relative to +z (up)

        # Best viewing angles I've found are phi = 65 and theta = 45
        self.set_camera_orientation(phi=65 * DEGREES, theta=45 * DEGREES)

        # Adds the axes and labels to the scene without animation
        self.add(axes, labels)

        # Continuous surface: x^2 + 4yz = p
        # Note that p is fixed, and I define the surface that
        # takes parameters x and y, then spits out the corresponding z value
        def surface_func(u, v):
            x = u
            y = v
            z = (p - x**2) / (4 * y)
            # This converts mathematical coordinates to points on the screen
            return axes.c2p(x, y, z)
        
        # This tells Manim to sample lots of (u,v) values and build a mesh
        surface = Surface(
            surface_func,
            # u and v ranges are defined in math coordinates
            u_range=[0.5, np.sqrt(p)],
            v_range=[0.5, 8],
            resolution=(18, 18),
            fill_opacity=0.85,
            fill_color=GREEN,
            stroke_width=0.5,
        )

        self.add(surface)

        # Fixed point
        fixed_dot = Dot3D(
            # Unpacks the fixed_point coordinate vector created earlier
            point=axes.c2p(*fixed_point),
            color=RED,
            radius=0.2
        )

        self.add(fixed_dot)

        # Zagier involution
        def zagier_map(pt):
            x, y, z = pt
            if x < y - z:
                return np.array([x + 2*z, z, y - x - z])
            elif y - z <= x <= 2*y:
                return np.array([2*y - x, y, x - y + z])
            else:
                return np.array([x - 2*y, x - y + z, y])

        # Create a vertex group of all of the psuedo-Pythagorean triples
        integer_dots = VGroup()
        for y in range(1, p):
            for x in range(1, p):
                z = (p - x**2) / (4 * y)
                if z.is_integer() and z > 0:
                    integer_dots.add(
                        Dot3D(
                            axes.c2p(x, y, z),
                            radius=0.1,
                            color=ORANGE
                        )
                    )

        # Fade in all of the vertex dots
        self.play(LaggedStartMap(FadeIn, integer_dots, lag_ratio=0.02))
        self.wait(3)
