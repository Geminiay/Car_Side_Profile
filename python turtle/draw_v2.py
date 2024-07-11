import turtle
import random
import math

turtle.title("Vehicle Side Profile")
s = turtle.getscreen()
t = turtle.Turtle()


totalSide = 520
totalHeight = 180
rearWindow = 80
windShield = 80
base = 500
roof = 250
hoodAngle = random.randint(7,11)
backAngle = random.randint(45,65)
frontAngle = random.randint(45,65)
backHeight = totalHeight-20-math.cos(math.radians(backAngle))*rearWindow
frontHeight = totalHeight-40-math.sin(math.radians(frontAngle))*windShield+10*math.cos(math.radians(frontAngle))+10*math.cos(math.radians(frontAngle))
hood = totalSide-roof-20-math.cos(math.radians(frontAngle))*windShield-math.sin(math.radians(backAngle))*rearWindow-10*math.sin(math.radians(frontAngle))-10*math.sin(math.radians(frontAngle))

print("---------------------------------------Results---------------------------------------")
print("Base Length: ",base,"\t\t\t\tBack Height: ",backHeight,"\nRear Window Angle: ",backAngle,"\t\t\t\tRear Window Length: ",rearWindow,"\nRoof Length: ",roof,"\nWind Shield Angle: ",frontAngle,"\t\t\t\tWind Shield Length: ",windShield,"\nHood Length: ",hood,"\t\tFront Height: ",frontHeight)
print("\nRear Window Cosinus: ",math.cos(math.radians(backAngle))*rearWindow,"\t\t Wind Shield Cosinus: ",math.cos(math.radians(frontAngle))*windShield,"\nRear Window Sinus: ",math.sin(math.radians(backAngle))*rearWindow,"\t\tWind Shield Sinus: ",math.sin(math.radians(frontAngle))*windShield)
print("-------------------------------------------------------------------------------------")

t.penup()
t.lt(90)
t.fd(50)
t.lt(90)
t.fd(260)
t.lt(180)
t.pendown()
t.fd(base)
t.circle(10,90)
t.fd(backHeight)
t.circle(10,backAngle)
t.fd(rearWindow)
t.circle(10,90-backAngle)
t.fd(roof)
t.circle(10,frontAngle)
t.fd(windShield)
t.circle(-10,frontAngle)
t.fd(hood)
t.circle(10,90)
t.fd(31.1)
t.circle(10,90)
t.fd(10)
t.hideturtle()
turtle.done()