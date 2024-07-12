import turtle
import random
import math
from sympy import symbols, solve
import openpyxl
from PIL import Image

turtle.title("Vehicle Side Profile")
screen = turtle.Screen()
s = turtle.getscreen()
t = turtle.Turtle()
x, y, z = symbols('x y z')
workbook = openpyxl.load_workbook("Results.xlsx")
sheet = workbook.active
next_row = sheet.max_row + 1


#Constants
totalWidth = 4166.03
totalHeight = 1535.63
base = 4166.03
roof = 2507.93
backHeight = 833.01
hood = 1158.16
hoodAngle = 4.88
frontHeight = 862.07


#Parameters
backAngle = round(random.uniform(70,85), 2) #actual value is 78.26
frontAngle = round(random.uniform(50,65), 2) #actual value is 58.19


#Angles
hoodCos = math.cos(math.radians(hoodAngle))
hoodSin = math.sin(math.radians(hoodAngle))
frontCos = math.cos(math.radians(frontAngle))
frontSin = math.sin(math.radians(frontAngle))
backCos = math.cos(math.radians(backAngle))
backSin = math.sin(math.radians(backAngle))


#Calculations
widthEq = hood*hoodCos+x*frontCos+z+y*backCos-base
heightEq1 = frontHeight+hood*hoodSin+x*frontSin-totalHeight
heightEq2 = backHeight+y*backSin-totalHeight
eq = solve((widthEq, heightEq1, heightEq2),(x, y, z),dict=True)
windShield = round(eq[0][x],3) #actual value is 66.475
rearWindow = round(eq[0][y],3) #actual value is 75.563
roof = round(eq[0][z],3) #actual value is 250.793


#Print Parameter Results 
print("Wind Shield Length: ",windShield)
print("Wind Shield Angle: ",frontAngle)
print("Rear Window Length: ",rearWindow)
print("Rear Window Angle: ",backAngle)
print("Roof Length: ",roof)


#Write Outputs to Excel
sheet.cell(row=next_row, column=1).value = "{:.3f}".format(windShield)
sheet.cell(row=next_row, column=2).value = "{:.2f}".format(frontAngle)
sheet.cell(row=next_row, column=3).value = "{:.3f}".format(rearWindow)
sheet.cell(row=next_row, column=4).value = "{:.2f}".format(backAngle)
sheet.cell(row=next_row, column=5).value = "{:.3f}".format(roof)
workbook.save("Results.xlsx")
print("Outputs saved to Excel.")


# Create turtle screen
screen.setup(width=800, height=600)


# Move the turtle to the starting position
t.hideturtle()


#Draw
t.fd(base/10)
t.lt(90)
t.fd(backHeight/10)
t.lt(90-backAngle)
t.fd(rearWindow/10)
t.lt(backAngle)
t.fd(roof/10)
t.lt(frontAngle)
t.fd(windShield/10)
t.rt(frontAngle-hoodAngle)
t.fd(hood/10)
t.lt(90-hoodAngle)
t.fd(frontHeight/10)


# Save the drawing as an EPS file and convert EPS file to PNG
canvas = turtle.getcanvas()
canvas.postscript(file='drawing.eps')
turtle.done()
with Image.open('drawing.eps') as img:
    img.save('drawing.png')