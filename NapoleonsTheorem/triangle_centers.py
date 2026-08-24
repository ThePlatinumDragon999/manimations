from manim import *
import numpy as np
from enum import Enum

class Center(Enum):
    CENTROID = 1
    CIRCUMCENTER = 2
    INCENTER = 3
    ORTHOCENTER = 4

class TriangleCenters(Scene):

    GUIDE_STROKE_WIDTH = 10
    GUIDE_COLOR = "#808080"
    GUIDE_OPACITY = 0.7

    def get_centroid(self, A, B, C):
         return (A + B + C) / 3

    def get_circumcenter(self, A, B, C):
        M = np.array([
            2 * (B - A)[:2],
            2 * (C - A)[:2]
        ])
                     
        rhs = np.array([
            np.dot(B, B) - np.dot(A, A),
            np.dot(C, C) - np.dot(A, A)
        ])

        return np.array([
             *np.linalg.solve(M, rhs),
             0
        ])

    def get_incenter(self, A, B, C):
         side_a = np.linalg.norm(B - C)
         side_b = np.linalg.norm(A - C)
         side_c = np.linalg.norm(A - B)

         return (
              side_a * A +
              side_b * B +
              side_c * C
         ) / (side_a + side_b + side_c)

    def get_orthocenter(self, A, B, C):
         return A + B + C - 2 * self.get_circumcenter(A, B, C)

    def get_center(self, center_type, A, B, C):
        if center_type == Center.CENTROID:
            return self.get_centroid(A, B, C)

        elif center_type == Center.CIRCUMCENTER:
            return self.get_circumcenter(A, B, C)

        elif center_type == Center.INCENTER:
            return self.get_incenter(A, B, C)

        elif center_type == Center.ORTHOCENTER:
            return self.get_orthocenter(A, B, C)

    def get_centroid_guides(self, A, B, C):
        midpoint_BC = (B + C) / 2
        midpoint_AC = (A + C) / 2
        midpoint_AB = (A + B) / 2

        return VGroup(
            DashedLine(A, midpoint_BC,
                stroke_width=self.GUIDE_STROKE_WIDTH,
                color=self.GUIDE_COLOR,
                stroke_opacity=self.GUIDE_OPACITY),
            DashedLine(B, midpoint_AC,
                stroke_width=self.GUIDE_STROKE_WIDTH,
                color=self.GUIDE_COLOR,
                stroke_opacity=self.GUIDE_OPACITY),
            DashedLine(C, midpoint_AB,
                stroke_width=self.GUIDE_STROKE_WIDTH,
                color=self.GUIDE_COLOR,
                stroke_opacity=self.GUIDE_OPACITY)
        )

    def get_circumcenter_guides(self, A, B, C):
        center = self.get_circumcenter(A, B, C)
        radius = np.linalg.norm(center - A)

        circle = Circle(
            radius=radius,
            color=self.GUIDE_COLOR,
            stroke_width=self.GUIDE_STROKE_WIDTH,
            stroke_opacity=self.GUIDE_OPACITY
        ).move_to(center)

        return DashedVMobject(
            circle,
            num_dashes=32
        )

    def get_incenter_guides(self, A, B, C):
        center = self.get_incenter(A, B, C)

        radius = np.linalg.norm(
            np.cross(B - A, center - A)
        ) / np.linalg.norm(B - A)

        circle = Circle(
            radius=radius,
            color=self.GUIDE_COLOR,
            stroke_width=self.GUIDE_STROKE_WIDTH,
            stroke_opacity=self.GUIDE_OPACITY
        ).move_to(center)

        return DashedVMobject(
            circle,
            num_dashes=32
        )

    def get_orthocenter_guides(self, A, B, C):

        def altitude(A, B, C):
            #Find the projection of A onto line BC
            BC = C - B

            t = np.dot(A - B, BC) / np.dot(BC, BC)

            foot = B + t * BC

            line = DashedLine(
                A,
                foot,
                stroke_width=self.GUIDE_STROKE_WIDTH,
                color=self.GUIDE_COLOR,
                stroke_opacity=self.GUIDE_OPACITY
            )

            return line, foot

        # Three altitudes
        altitude_A, foot_A = altitude(A, B, C)
        altitude_B, foot_B = altitude(B, A, C)
        altitude_C, foot_C = altitude(C, A, B)

        # Right angle markers
        right_angle_A = RightAngle(
            Line(foot_A, A),
            Line(B, C),
            length=0.15,
            color=self.GUIDE_COLOR
        )

        right_angle_B = RightAngle(
            Line(foot_B, B),
            Line(A, C),
            length=0.15,
            color=self.GUIDE_COLOR
        )

        right_angle_C = RightAngle(
            Line(foot_C, C),
            Line(A, B),
            length=0.15,
            color=self.GUIDE_COLOR
        )

        return VGroup(
            altitude_A,
            altitude_B,
            altitude_C,
            right_angle_A,
            right_angle_B,
            right_angle_C
        )

    def get_guides(self, center_type, A, B, C):
        if center_type == Center.CENTROID:
            return self.get_centroid_guides(A, B, C)

        elif center_type == Center.CIRCUMCENTER:
            return self.get_circumcenter_guides(A, B, C)

        elif center_type == Center.INCENTER:
            return self.get_incenter_guides(A, B, C)

        elif center_type == Center.ORTHOCENTER:
            return self.get_orthocenter_guides(A, B, C)
    
    def construct(self):
        SHOW_GUIDES = True

        # Which center belongs to which triangle
        center_types = [
            Center.CENTROID,
            Center.CIRCUMCENTER,
            Center.INCENTER,
            Center.ORTHOCENTER
        ]

        # Triangle positions on screen
        posCenters = [
            LEFT * 4.8,
            LEFT * 1.6,
            RIGHT * 1.6,
            RIGHT * 4.8
        ]

        # Initial triangle
        A = np.array([-1.0, -1.0, 0])
        B = np.array([1.0, -1.0, 0])
        C = np.array([0.0, 1.0, 0])

        triangles = {}
        dots = {}

        colors = {
            Center.CENTROID: "#B00B69",
            Center.CIRCUMCENTER: "#87FF78",
            Center.INCENTER: "#9AB5FF",
            Center.ORTHOCENTER: "#C5C100"
        }

        labels = {
            Center.CENTROID: Text(
                "Centroid", 
                font="OpenDyslexic",
                color=colors[Center.CENTROID]
            ).scale(0.5),

            Center.CIRCUMCENTER: Text(
                "Circumcenter", 
                font="OpenDyslexic",
                color=colors[Center.CIRCUMCENTER]
            ).scale(0.5),

            Center.INCENTER: Text(
                "Incenter", 
                font="OpenDyslexic",
                color=colors[Center.INCENTER]
            ).scale(0.5),

            Center.ORTHOCENTER: Text(
                "Orthocenter", 
                font="OpenDyslexic",
                color=colors[Center.ORTHOCENTER]
            ).scale(0.5)
        }

        guides = {}

        # Now actually create the triangles
        for center_type, position in zip(center_types, posCenters):
            a = A + position
            b = B + position
            c = C + position

            triangles[center_type] = Polygon(
                a,
                b,
                c,
                stroke_width = 10,
                color = colors[center_type]
            )

            # Appropriate center
            center = self.get_center(
                center_type,
                a,
                b,
                c
            )

            # Center dot
            dots[center_type] = Dot(
                center,
                color=colors[center_type])

            labels[center_type].move_to(position + DOWN * 1.7)

            if SHOW_GUIDES:
                guides[center_type] = self.get_guides(
                    center_type,
                    a,
                    b,
                    c
                )

        # Animation
        self.play(
            *[FadeIn(triangles[center_type]) for center_type in center_types]
        )

        self.play(
            *[FadeIn(dots[center_type]) for center_type in center_types]
        )

        self.play(
            *[FadeIn(guides[center_type]) for center_type in center_types]
        )

        self.play(
            *[FadeIn(labels[center_type]) for center_type in center_types]
        )

        self.wait(1)

        triangle_shapes = [
            # Triangle 1
            (
                np.array([-0.5, -1.0, 0]),
                np.array([0.5, -1.0, 0]),
                np.array([0.3, 1.5, 0])
            ),

            # Triangle 2
            (
                np.array([-0.75, -1.0, 0]),
                np.array([0.75, -1.0, 0]),
                np.array([-0.5, -0.2, 0])
            ),

            # Triangle 2
            (
                np.array([-1, -1.0, 0]),
                np.array([1, -1.0, 0]),
                np.array([0, np.sqrt(3) - 1, 0])
            )
        ]

        for A_new, B_new, C_new in triangle_shapes:
            new_triangles = {}
            new_centers = {}
            new_guides = {}

            for center_type, position in zip(center_types, posCenters):
                a = A_new + position
                b = B_new + position
                c = C_new + position

                new_triangles[center_type] = \
                    Polygon(a, b, c, stroke_width=10, color=colors[center_type])

                new_centers[center_type] = self.get_center(
                    center_type,
                    a,
                    b,
                    c
                )

                if SHOW_GUIDES:
                    new_guides[center_type] = self.get_guides(
                        center_type,
                        a,
                        b,
                        c
                    )

            self.play(
                # Morph triangles
                *[
                    triangles[center_type].animate.become(
                        new_triangles[center_type]
                    )
                    for center_type in center_types
                ],

                # Move center dots
                *[
                    dots[center_type].animate.move_to(
                        new_centers[center_type]
                    )
                    for center_type in center_types
                ],

                # Guides
                *[
                    guides[center_type].animate.become(
                        new_guides[center_type]
                    )
                    for center_type in center_types
                ] if SHOW_GUIDES else [],

                run_time=3,
            )

            self.wait(1)

        self.wait(1)

        # Fade out the labels
        self.play(
            *[
                FadeOut(labels[center_type])
                for center_type in center_types
            ],
            run_time=1
        )

        self.play(
            *[
                FadeOut(guides[center_type])
                for center_type in center_types
            ],
            run_time=1
        )

        for center_type in center_types:
            new_centers[center_type] = self.get_center(
                center_type,
                A_new,
                B_new,
                C_new
            )

        self.play(
            *[
                triangles[center_type].animate.become(
                    Polygon(
                        A_new,
                        B_new,
                        C_new,
                        stroke_width=10,
                        color = "white"
                    )
                )
                for center_type in center_types
            ],

            *[
                dots[center_type].animate.move_to(
                    new_centers[center_type]
                ).set_color("white")
                for center_type in center_types
            ],

            run_time=3
        )

        self.wait(1)