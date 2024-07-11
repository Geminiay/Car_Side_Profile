import turtle
import math

turtle.title("Vehicle Side Profile")
s = turtle.getscreen()
t = turtle.Turtle()

roofJoint = 246
i = 0
t.lt(90)
while math.pow(i,2) < 81:
    t.circle(math.pow(i,2)-80,math.pow(i,2)-40)
    i+=1

t.hideturtle()
turtle.done()

