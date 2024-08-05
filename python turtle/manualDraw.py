import turtle
from PIL import Image
from openpyxl.drawing.image import Image as OpenpyxlImage
from datetime import datetime

backAngle = 77.73
frontAngle = 58.19
windShield = 677.49
rearWindow = 706.46
totalWidth = 4147.65
totalHeight = 1540.87
base = 4147.65
roof = 2493.97
backHeight = 850.54
hood = 1150.29
hoodAngle = 4.68
frontHeight = 871.27    
s = turtle.getscreen()
t = turtle.Turtle()
screen = turtle.Screen()
canvas = turtle.getcanvas()

def draw():

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


isManual = input("Do you want to use dataset(D) or enter manually(M)?\n") == 'D'