from sympy import symbols, Eq, sqrt, solve

x, y = symbols('x y')

x1, y1 = 0.035, 0.025
x2, y2 = 0.21, 0.26
x3, y3 = 0.38, 0.025

# -0.000261 -4.1e-05

del_12 =  -0.000261
del_13 = -4.1e-05

eq1 = Eq(sqrt(x**2 + y**2) - sqrt((x - x2)**2 + (y - y2)**2), del_12)
eq2 = Eq(sqrt(x**2 + y**2) - sqrt((x - x3)**2 + y**2), del_13)

solution = solve((eq1, eq2), (x,y))

print(solution)