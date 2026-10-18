from manimlib import *
from scipy.integrate import solve_ivp

# class Test(InteractiveScene):
#     def construct(self):
#         text = Text("Hello World", font_size=72)
#         text.to_edge(UP)
#         self.play(
#             Write(text, run_time=3)
#             )


#         circle = Circle()
#         circle.set_flat_stroke(True)
#         circle.f_always.move_to(lambda: math.cos(self.time) * RIGHT)


#         square = Square()
#         square.always.next_to(circle, DOWN)



#         self.add(circle)
#         self.add(square)
#         self.wait(10)

#         self.add(ThreeDAxes())
#         self.embed()

def lorenz_system(t, state, sigma=10, rho=28, beta=8/3):
    x, y, z = state
    dxdt = sigma * (y - x)
    dydt = x * (rho - z) - y
    dzdt = x * y - beta * z
    return [dxdt, dydt, dzdt]

def ode_solution_points(function, state0, time, dt=0.01):
    solution = solve_ivp(
        function, 
        t_span=(0, time),
        y0=state0,
        t_eval=np.arange(0, time, dt))

    return solution.y.T

class LorenzAttractor(InteractiveScene):
    def construct(self):
        # Initial state
        axes = ThreeDAxes(
            x_range=(-50, 50, 5),
            y_range=(-50, 50, 5),
            z_range=(-0, 50, 5),
            width=16,
            height=16,
            depth=8,
        )
        axes.set_width(FRAME_WIDTH)
        axes.center()

        self.frame.reorient(43, 76, 1, IN, 10)
        self.add(axes)

        # Define the initial state and compute the solution points
        epsilon = 1e-3
        evolution_time = 120
        states = [[10, 10, 10 + n * epsilon] for n in range(30)] 
        colors = color_gradient([BLUE_E, BLUE_D, BLUE_C, BLUE_B, BLUE_A], len(states))
        curves = VGroup()
        for state, color in zip(states, colors):
            points = ode_solution_points(lorenz_system, state, evolution_time)
            curve = VMobject().set_points_smoothly(axes.c2p(*points.T))
            curve.set_stroke(color, 1, opacity=0.25)
            curves.add(curve)
        curves.set_stroke(width=1, opacity=0.25)
        dots = Group(GlowDot(color=color, radius=0.25) for color in colors)

        globals().update(locals())
        def update_dots(dots):
            for dot, curve in zip(dots, curves):
                dot.move_to(curve.get_end())
        dots.add_updater(update_dots)

        tail = VGroup (TracingTail(dot, time_traced=5).match_color(dot)
                       for dot in dots)

        self.add(dots)
        self.add(tail)
        curves.set_opacity(0)
        self.play(
            *(ShowCreation(curve, rate_func=linear) for curve in curves),
            run_time=evolution_time,
        )


        self.embed()
