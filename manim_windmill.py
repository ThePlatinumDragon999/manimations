from manim import *
import numpy as np

class ZagierInvolution3D(ThreeDScene):
    def construct(self):
        ############################################
        # Parameters
        ############################################
        p = 37  # prime of form 4k+1
        fixed_point = np.array([1, 1, (p - 1) / 4])

        ############################################
        # Prime scale / label
        ############################################
        prime_label = MathTex(rf"p = {p} \equiv 1 \pmod 4")
        prime_label.to_edge(UP)
        self.add_fixed_in_frame_mobjects(prime_label)

        ############################################
        # Axes
        ############################################
        axes = ThreeDAxes(
            x_range=[0, 8, 1],
            y_range=[0, 8, 1],
            z_range=[0, 8, 1],
            x_length=6,
            y_length=6,
            z_length=4
        )
        labels = axes.get_axis_labels(x_label="x", y_label="y", z_label="z")

        self.set_camera_orientation(phi=65 * DEGREES, theta=-90 * DEGREES)
        self.add(axes, labels)

        ############################################
        # Continuous surface: x^2 + 4yz = p
        ############################################
        def surface_func(u, v):
            x = u
            y = v
            z = (p - x**2) / (4 * y)
            return axes.c2p(x, y, z)

        surface = Surface(
            surface_func,
            u_range=[0.5, 6],
            v_range=[0.5, 6],
            resolution=(18, 18),
            fill_opacity=0.35,
            fill_color=BLUE,
            stroke_width=0.5,
        )

        self.play(Create(surface), run_time=3)
        self.wait()

        ############################################
        # Highlight central (middle) region
        ############################################
        central_plane = Surface(
            surface_func,
            u_range=[1, 4],     # rough visual bounds for x
            v_range=[1, 4],     # rough bounds for y
            resolution=(12, 12),
            fill_opacity=0.5,
            fill_color=TEAL
        )

        self.play(Transform(surface, central_plane), run_time=2)
        self.wait()

        ############################################
        # Fixed point
        ############################################
        fixed_dot = Dot3D(
            point=axes.c2p(*fixed_point),
            color=RED,
            radius=0.08
        )
        fixed_label = MathTex(r"(1,1,\tfrac{p-1}{4})").next_to(
            fixed_dot, UP
        )
        self.add_fixed_in_frame_mobjects(fixed_label)

        self.play(FadeIn(fixed_dot), Write(fixed_label))
        self.wait(2)

        ############################################
        # Pick a specific point (continuous)
        ############################################
        start_point = np.array([3.0, 2.0, (p - 9) / 8])
        start_dot = Dot3D(
            axes.c2p(*start_point),
            color=YELLOW,
            radius=0.07
        )

        self.play(FadeIn(start_dot))
        self.wait()

        ############################################
        # Zagier involution (middle case)
        ############################################
        def zagier_map(pt):
            x, y, z = pt
            if x < y - z:
                return np.array([x + 2*z, z, y - x - z])
            elif y - z <= x <= 2*y:
                return np.array([2*y - x, y, x - y + z])
            else:
                return np.array([x - 2*y, x - y + z, y])

        image_point = zagier_map(start_point)

        image_dot = Dot3D(
            axes.c2p(*image_point),
            color=ORANGE,
            radius=0.07
        )

        arrow1 = Arrow3D(
            start=axes.c2p(*start_point),
            end=axes.c2p(*image_point),
            color=ORANGE
        )

        self.play(GrowArrow(arrow1), FadeIn(image_dot), run_time=2)
        self.wait()

        ############################################
        # Map back (involution)
        ############################################
        back_point = zagier_map(image_point)

        arrow2 = Arrow3D(
            start=axes.c2p(*image_point),
            end=axes.c2p(*back_point),
            color=YELLOW
        )

        self.play(GrowArrow(arrow2), run_time=2)
        self.wait(2)

        ############################################
        # Snap to integer lattice points
        ############################################
        self.play(FadeOut(surface), FadeOut(arrow1), FadeOut(arrow2))
        self.wait()

        integer_dots = VGroup()
        for y in range(1, p):
            for x in range(1, p):
                z = (p - x**2) / (4 * y)
                if z.is_integer() and z > 0:
                    integer_dots.add(
                        Dot3D(
                            axes.c2p(x, y, z),
                            radius=0.05,
                            color=BLUE
                        )
                    )

        self.play(LaggedStartMap(FadeIn, integer_dots, lag_ratio=0.02))
        self.wait(3)
