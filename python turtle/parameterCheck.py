import turtle
from PIL import Image
from openpyxl.drawing.image import Image as OpenpyxlImage

backAngle = 78.26
frontAngle = 58.19
windShield = 664.75
rearWindow = 755.63
roof = 2507.93
totalWidth = 4166.03
totalHeight = 1535.63
base = 4166.03
roof = 2507.93
backHeight = 833.01
hood = 1158.16
hoodAngle = 4.88
frontHeight = 862.07

s = turtle.getscreen()
t = turtle.Turtle()
screen = turtle.Screen()
canvas = turtle.getcanvas()


#Draw
t.hideturtle()
t.penup()
t.goto(-totalWidth/10, -totalHeight/10)
t.pendown()
t.fd(base/5)
t.lt(90)
t.fd(backHeight/5)
t.lt(90-backAngle)
t.fd(rearWindow/5)
t.lt(backAngle)
t.fd(roof/5)
t.lt(frontAngle)
t.fd(windShield/5)
t.rt(frontAngle-hoodAngle)
t.fd(hood/5)
t.lt(90-hoodAngle)
t.fd(frontHeight/5)
t.lt(90)

# Save the drawing as an EPS file and convert EPS file to PNG
canvas.postscript(file = f'original.eps')
with Image.open(f'original.eps') as img:
    img.save(f'original.png')