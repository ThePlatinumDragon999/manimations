from manim import *
import numpy as np
from napoleon_construction import *

class NapoleonProof(Scene):
    def construct(self):
        ANGLE_RADIUS=0.4
        
        # Rule of thumb:
        # x in [-7.1, 7.1]
        # y in [-4, 4]

        # Invisible control points
        X = Dot(
            [-0.8, 0.3, 0],
            radius=0.2,
            fill_opacity=0,
            stroke_opacity=0,
            color="#f05f01"
        )

        Y = Dot(
            [-0.0, 2.4, 0],
            radius=0.2,
            fill_opacity=0,
            stroke_opacity=0,
            color="#27A830"
        )

        Z = Dot(
            [1.7, 0.6, 0],
            radius=0.2,
            fill_opacity=0,
            stroke_opacity=0,
            color="#206B87"
        )

        # Top layer
        construction = NapoleonConstruction(X, Y, Z)

        X1 = X.copy()
        Y1 = Y.copy()
        Z1 = Z.copy()

        construction1 = NapoleonConstruction(X1, Y1, Z1)

        X2 = X.copy()
        Y2 = Y.copy()
        Z2 = Z.copy()

        construction2 = NapoleonConstruction(X2, Y2, Z2)

        # Construct the centroids:
        # Centroid GB
        GB = always_redraw(lambda: Dot(
            (
                construction.Y.get_center()
                + construction.Z.get_center()
                + equilateral_on_side(
                    construction.Y.get_center(),
                    construction.Z.get_center(),
                    construction.X.get_center(),
                )
            ) / 3,
            radius=0.16,
            color="#87FF78",
        ))

        # Centroid GC
        GC = always_redraw(lambda: Dot(
            (
                construction.Z.get_center()
                + construction.X.get_center()
                + equilateral_on_side(
                    construction.Z.get_center(),
                    construction.X.get_center(),
                    construction.Y.get_center(),
                )
            ) / 3,
            radius=0.16,
            color="#9AB5FF",
        ))

        # Centroid GA
        GA = always_redraw(lambda: Dot(
            (
                construction.X.get_center()
                + construction.Y.get_center()
                + equilateral_on_side(
                    construction.X.get_center(),
                    construction.Y.get_center(),
                    construction.Z.get_center(),
                )
            ) / 3,
            radius=0.16,
            color="#B00B69",
        ))

        centroids = VGroup(
            GA,
            GB,
            GC,
        ).set_z_index(3)

        self.add(
            construction2.triangle,
            construction2.EX,
            construction2.EY,
            construction2.EZ,
        )

        self.play(
            FadeIn(construction1.triangle),
            FadeIn(construction1.EX),
            FadeIn(construction1.EY),
            FadeIn(construction1.EZ),
            FadeIn(centroids),
            run_time=1,
        )

        self.add(
            construction.triangle,
            construction.EX,
            construction.EY,
            construction.EZ,
        )

        self.wait(1)

        # Labels
        label_A = always_redraw(lambda: Text(
            "A",
            font="OpenDyslexic",
            font_size=24,
            color="white",
        ).next_to(
            GA.get_center(),
            UP + LEFT,
            buff=0.15
        ))

        label_B = always_redraw(lambda: Text(
            "B",
            font="OpenDyslexic",
            font_size=24,
            color="white",
        ).next_to(
            GB.get_center(),
            UP + RIGHT,
            buff=0.15
        ))

        label_C = always_redraw(lambda: Text(
            "C",
            font="OpenDyslexic",
            font_size=24,
            color="white",
        ).next_to(
            GC.get_center(),
            DOWN + RIGHT,
            buff=0.15
        ))

        self.play(
            FadeIn(label_A),
            FadeIn(label_B),
            FadeIn(label_C),
            run_time=1,
        )

        BC_line = always_redraw(lambda: Line(
            GB.get_center(),
            GC.get_center(),
            stroke_width=10,
            color="#C5C100",
            )
        ).set_z_index(1)

        CD_line = BC_line.copy()

        self.play(FadeIn(BC_line))
        self.add(CD_line)

        GD = GB.copy()

        GD.move_to(GB.get_center())

        self.add(GD)

        # Angle arc
        angle1 = always_redraw(lambda: angle_arc(
            GC.get_center(),
            GB.get_center(),
            GD.get_center(),
            radius=ANGLE_RADIUS,
            color="white",
        ))

        self.add(angle1)

        rotation_center_2 = GC.get_center()

        self.play(
            Rotate(
                VGroup(X1, Y1, Z1, CD_line, GD),
                angle=2 * PI / 3,
                about_point=rotation_center_2,
            ),
            run_time=4,
        )

        self.wait(1)

        angle_label_1 = always_redraw(lambda: Text(
            "120°",
            font="OpenDyslexic",
            font_size=24,
            color="white"
        ).add_background_rectangle(
            color="black",
            opacity=0.8,
            buff=0.06,
        ).move_to(
            angle1.get_center() + 0.5 * UP
        ).set_z_index(3)
        )

        self.play(FadeIn(angle_label_1))

        self.wait(1)

        # Add label for D centroid
        label_D = always_redraw(lambda: Text(
            "D",
            font="OpenDyslexic",
            font_size=24,
            color="white",
        ).next_to(
            GD.get_center(),
            UP + LEFT,
            buff=0.15
        ))

        self.play(
            FadeIn(label_D),
            run_time=1
        )

        self.wait(1)

        AB_line = always_redraw(lambda: Line(
            GA.get_center(),
            GB.get_center(),
            stroke_width=10,
            color="#206B87",
            )
        ).set_z_index(1)

        AD_line = AB_line.copy()

        self.play(FadeIn(AB_line))
        self.add(AD_line)

        GD2 = GB.copy()
        
        GD2.move_to(GB.get_center())

        self.add(GD2)

        # Angle arc
        angle2 = always_redraw(lambda: angle_arc(
            GA.get_center(),
            GB.get_center(),
            GD2.get_center(),
            radius=ANGLE_RADIUS,
            color="white",
        ))

        self.add(angle2)

        # Second rotation
        rotation_center_3 = GA.get_center()
        
        self.play(
            Rotate(
                VGroup(X2, Y2, Z2, AD_line, GD2),
                angle=-2 * PI / 3,
                about_point=rotation_center_3,
            ),
            run_time=4,
        )

        self.wait(1)

        angle_label_2 = always_redraw(lambda: Text(
            "120°",
            font="OpenDyslexic",
            font_size=24,
            color="white"
        ).add_background_rectangle(
            color="black",
            opacity=0.8,
            buff=0.06,
        ).move_to(
            angle2.get_center() + RIGHT * 0.8 + DOWN * 0.2
        ).set_z_index(3)
        )

        self.play(FadeIn(angle_label_2))

        self.wait(2)

        self.play(
            FadeOut(angle_label_1),
            FadeOut(angle_label_2),
            run_time=1
        )

        AC_line = always_redraw(lambda: Line(
            GA.get_center(),
            GC.get_center(),
            stroke_width=10,
            color="#27a830",
            )
        ).set_z_index(1)

        self.play(FadeIn(AC_line))

        # Change angles into 2 other angles to fade in
        angle3 = always_redraw(lambda: angle_arc(
            GA.get_center(),
            GB.get_center(),
            GC.get_center(),
            radius=ANGLE_RADIUS,
            color="white",
        ))

        angle4 = always_redraw(lambda: angle_arc(
            GC.get_center(),
            GA.get_center(),
            GB.get_center(),
            radius=ANGLE_RADIUS,
            color="white",
        ))

        self.add(angle3)
        self.add(angle4)

        angle_label_3 = always_redraw(lambda: Text(
            "60°",
            font="OpenDyslexic",
            font_size=24,
            color="white"
        ).add_background_rectangle(
            color="black",
            opacity=0.8,
            buff=0.06,
        ).next_to(
            angle3, 
            RIGHT * 0.4, 
            buff=0.1
        ).set_z_index(3)
        )

        angle_label_3d = always_redraw(lambda: Text(
            "60°",
            font="OpenDyslexic",
            font_size=24,
            color="white"
        ).add_background_rectangle(
            color="black",
            opacity=0.8,
            buff=0.06,
        ).move_to(
            angle3.get_center() + 0.6 * DOWN + 0.2 * LEFT, 
        ).set_z_index(3)
        )

        angle_label_4 = always_redraw(lambda: Text(
            "60°",
            font="OpenDyslexic",
            font_size=24,
            color="white"
        ).add_background_rectangle(
            color="black",
            opacity=0.8,
            buff=0.06,
        ).next_to(
            angle4, 
            UP,
            buff=0.1
        ).set_z_index(3)
        )

        angle_label_4d = always_redraw(lambda: Text(
            "60°",
            font="OpenDyslexic",
            font_size=24,
            color="white"
        ).add_background_rectangle(
            color="black",
            opacity=0.8,
            buff=0.06,
        ).move_to(
            angle4.get_center() + 0.6 * LEFT + 0.1 * DOWN, 
        ).set_z_index(3)
        )

        self.play(
            FadeIn(angle_label_3),
            FadeIn(angle_label_4),
            FadeIn(angle_label_3d),
            FadeIn(angle_label_4d)
        )

        self.wait(1)

        self.play(
            FadeOut(angle1),
            FadeOut(angle2),
            FadeOut(angle_label_3d),
            FadeOut(angle_label_4d),
            FadeOut(GD),
            FadeOut(GD2),
            FadeOut(label_D),
            FadeOut(AD_line),
            FadeOut(CD_line),
            run_time=0.5
        )

        self.play(
            FadeOut(construction1.triangle),
            FadeOut(construction1.EX),
            FadeOut(construction1.EY),
            FadeOut(construction1.EZ),
            FadeOut(construction2.triangle),
            FadeOut(construction2.EX),
            FadeOut(construction2.EY),
            FadeOut(construction2.EZ),
            run_time=0.5
        )

        self.wait(2)

        # Final centroid
        final_centroid = (
            X.get_center()
            + Y.get_center()
            + Z.get_center()
        ) / 3

        scale_factor = 1.2

        self.play(
            X.animate.move_to(
                scale_factor * (X.get_center() - final_centroid)
            ),
            Y.animate.move_to(
                scale_factor * (Y.get_center() - final_centroid)
            ),
            Z.animate.move_to(
                scale_factor * (Z.get_center() - final_centroid)
            ),
            run_time=2
        )

        # Angle arc
        angle5 = always_redraw(lambda: angle_arc(
            GB.get_center(),
            GA.get_center(),
            GC.get_center(),
            radius=ANGLE_RADIUS,
            color="white",
        ))

        angle_label_5 = always_redraw(lambda: Text(
            "60°",
            font="OpenDyslexic",
            font_size=24,
            color="white"
        ).add_background_rectangle(
            color="black",
            opacity=0.8,
            buff=0.06,
        ).move_to(
            angle5.get_center() + 0.4 * LEFT + 0.2 * DOWN
        ).set_z_index(3)
        )

        self.play(FadeIn(angle5))

        self.wait(1)

        self.play(FadeIn(angle_label_5))

