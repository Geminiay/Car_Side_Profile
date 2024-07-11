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
base = 406.603 #Without Curves
roof = 250.793
backHeight = 83.301
##real hood = 115.816
##real frontHeight = 86.207


#Parameters
rearWindow = 75.563
backAngle = random.randint(73.26,83.26) #78.26 
frontAngle = random.randint(53.19,63.19) #58.19
windShield = 66.475



#Width Parameters
wP1 = 10-10*math.cos(math.radians(90-hoodAngle))
wP3 = math.sqrt(200-200*math.cos(math.radians(frontAngle-hoodAngle)))*math.cos(math.radians(((frontAngle-hoodAngle)/2)+hoodAngle))
wP4 = windShield*math.cos(math.radians(frontAngle))
wP5 = math.sqrt(200-200*math.cos(math.radians(frontAngle+roofAngle)))*math.cos(math.radians(((frontAngle+roofAngle)/2)+90-frontAngle))
wP6 = roof*math.cos(math.radians(roofAngle))
wP7 = math.sqrt(200-200*math.cos(math.radians(backAngle-roofAngle)))*math.cos(math.radians(((((backAngle-roofAngle)/2)+backAngle))))
wP8 = rearWindow*math.cos(math.radians(90-backAngle))
wP9 = 10-10*math.cos(math.radians(90-backAngle))


#Height Parameters
hP3 = 0
hP4 = 0
hP5 = 0
hP6 = 0
hP7 = 0
hP8 = 0
hP9 = 0
hP10 = 0
hP11 = 0
hP12 = 0


#Parameter Calculations
hood = (totalWidth-wP1-wP3-wP4-wP5-wP6-wP7-wP8-wP9)/math.cos(math.radians(hoodAngle))
frontHeight = (-hP3-hP4-hP5-hP6-hP7+hP8+hP9+hP10+hP11+hP12)
frontHeight = 86.207
hood = 115.816

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
t.circle(10,90)
t.fd(backHeight)
t.circle(10,90-backAngle)
t.fd(rearWindow)
t.circle(10,backAngle-roofAngle)
t.fd(roof)
t.circle(10,frontAngle+roofAngle)
t.fd(windShield)
t.circle(-10,frontAngle-hoodAngle)
t.fd(hood)
t.circle(10,90-hoodAngle)
t.fd(frontHeight)
t.circle(10,90)
t.fd(10)
t.hideturtle()
turtle.done()