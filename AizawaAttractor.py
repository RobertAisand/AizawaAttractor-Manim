from manimlib import *

def aizawa_system(t, state, a=0.95, b=0.7, c=0.6, d=3.5, e=0.25, f=0.1):
    x, y, z = state
    dxdt = (z - b) * x - d * y
    dydt = d * x + (z - b) * y
    dzdt = c + a * z - z**3 / 3 - (x**2 + y**2) * (1 + e * z) + f * z * x**3
    return [dxdt, dydt, dzdt]

def ode_solution_points(function, state0, time, dt=0.01):
    solution = solve_ivp(
        function, 
        t_span=(0, time),
        y0=state0,
        t_eval=np.arange(0, time, dt))

    return solution.y.T


class AizawaAttractor(InteractiveScene):
    def construct(self):
        self.frame.reorient(30, 70, 0, ORIGIN, 8)

        base_height = 8
        evolution_time = 80   # сколько модельного времени считаем
        run_time = 60       # за сколько секунд показываем
        n_curves = 100
        scale = 6
        shift = np.array([0, 0, -0.5]) * scale
        colors = color_gradient([BLUE_E, BLUE_D, BLUE_C, BLUE_B, BLUE_A], n_curves)

        np.random.seed(1)
        states = np.random.uniform(-0.5, 0.5, (n_curves, 3))

        curves = VGroup()
        for state, color in zip(states, colors):
            points = ode_solution_points(aizawa_system, state, evolution_time, dt=0.02)
            points = points[::3]  # прореживание: крупные сегменты
            curve = VMobject().set_points_as_corners(scale * points + shift)
            curve.set_stroke(color, 1.5, opacity=0.9)
            curves.add(curve)

        self.frame.add_updater(lambda m, dt: m.increment_theta(0.3 * dt))
        dots = Group(GlowDot(color=color, radius=0.25) for color in colors)


        globals().update(locals())
        def update_dots(dots):
            for dot, curve in zip(dots, curves):
                dot.move_to(curve.get_end())
        dots.add_updater(update_dots)

        tail = VGroup (TracingTail(dot, time_traced=7).match_color(dot)
                for dot in dots)

        self.add(dots)
        self.add(tail)
        curves.set_opacity(0)

        def camera_motion(frame, dt):
            frame.increment_theta(0.4 * dt)  # вращение вокруг оси
            # плавное приближение и отдаление: высота кадра колеблется около 8
            frame.set_height(base_height * (1 + 0.55 * np.sin(0.4 * self.time)))

        self.frame.add_updater(camera_motion)

        self.play(
            *(ShowCreation(curve, rate_func=linear) for curve in curves),
            run_time=run_time,
        )
        self.wait(5)

# class AizawaAttractor(InteractiveScene):
#     def construct(self):
#         self.frame.reorient(30, 70, 0, ORIGIN, 8)

#         epsilon = 1e-3
#         evolution_time = 30
#         states = [[0.1 + n * epsilon, 0, 0] for n in range(10)]
#         colors = color_gradient([BLUE_E, BLUE_A], len(states))

#         scale = 3
#         shift = np.array([0, 0, -0.5]) * scale

#         curves = VGroup()
#         for state, color in zip(states, colors):
#             points = ode_solution_points(aizawa_system, state, evolution_time)
#             curve = VMobject().set_points_smoothly(scale * points + shift)
#             curve.set_stroke(color, 1, opacity=0.25)
#             curves.add(curve)

#         curves.set_stroke(width=2, opacity=1)
#         dots = Group(GlowDot(color=color, radius=0.25) for color in colors)

#         globals().update(locals())
#         def update_dots(dots):
#             for dot, curve in zip(dots, curves):
#                 dot.move_to(curve.get_end())
#         dots.add_updater(update_dots)

#         # tail = VGroup (TracingTail(dot, time_traced=5).match_color(dot)
#         #                for dot in dots)


#         # Медленное вращение камеры всё время сцены
#         self.frame.add_updater(lambda m, dt: m.increment_theta(0.15 * dt))
#         self.add(dots)
#         # self.add(tail)
#         # curves.set_opacity(0)
#         self.play(
#             *(ShowCreation(curve, rate_func=linear) for curve in curves),
#             run_time=evolution_time,
#         )


        # self.embed()