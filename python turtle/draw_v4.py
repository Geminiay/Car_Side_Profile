import turtle
import random
import math

turtle.title("Vehicle Side Profile")
s = turtle.getscreen()
t = turtle.Turtle()

#Constants
totalWidth = 416.603
totalHeight = 153.563
rearWindow = 75.563
windShield = 66.475
base = 416.603 #416.603 but a 20 came from circles
roof = 250.793
backHeight = 83.301 #83.301 but a 10 came from a circle
hoodAngle = 4.88
##real hood = 115.816
##real frontHeight = 86.207

#Parameters
rearWindow = 75.563
backAngle = 78.26 
frontAngle = 58.19
windShield = 66.475


hood = 115.816
frontHeight = 86.207 #86.207 but a 10 came from a circle


#Pre-Draw
t.penup()
t.lt(90)
t.fd(50)
t.lt(90)
t.fd(260)
t.lt(180)
t.pendown()


#Draw
t.fd(base)
t.lt(90)
t.fd(backHeight)
t.lt(90-backAngle)
t.fd(rearWindow)
t.lt(backAngle)
t.fd(roof)
t.lt(frontAngle)
t.fd(windShield)
t.rt(frontAngle-hoodAngle)
t.fd(hood)
t.lt(90-hoodAngle)
t.fd(frontHeight)
t.fd(5)
t.hideturtle()
turtle.done()