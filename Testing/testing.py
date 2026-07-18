from manim import *

class Test(Scene):
    def construct(self):

        plane = (
            NumberPlane(x_range=[-10, 10, 2], x_length=10, y_range=[-10,10,2], y_length=10).add_coordinates() 
            )
            
        labels = plane.get_axis_labels(x_label="x", y_label="f(x)")

        parab = plane.plot(lambda x: x ** 2, x_range=[-4, 4], color=RED)
        func_label = MathTex("f(x)={x}^{2}").next_to(parab, DOWN)
        
        self.play(Create(plane))
        self.play(Create(VGroup(labels, func_label), run_time=3))
        self.play(Create(parab, run_time=6))