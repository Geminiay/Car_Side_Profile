import random
from sympy import symbols, solve

x, y = symbols('x y')

a = solve((5*x+12*y-72,18*x-12*y-108),(x,y), dict = True)

print(a[0][x])