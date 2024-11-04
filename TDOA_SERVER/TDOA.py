from sympy import symbols, Eq, solve, sqrt

tx, ty = symbols('tx ty')
x1, y1, d1 = 3, 3,sqrt(17)
x2, y2, d2 = 3, 10, sqrt(10)
x3, y3, d3 = 7,7, 3


eq1 = Eq((tx - x1)**2 + (ty - y1)**2, d1**2)
eq2 = Eq((tx - x2)**2 + (ty - y2)**2, d2**2)
eq3 = Eq((tx - x3)**2 + (ty - y3)**2, d3**2)


solution = solve((eq1,eq2,eq3), (tx,ty))


print(solution)
