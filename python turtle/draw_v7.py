import turtle
import random
import math
from sympy import symbols, solve
import openpyxl
from openpyxl.drawing.image import Image as OpenpyxlImage
from PIL import Image
import os
from datetime import datetime

#Constants
totalWidth = 4147.65
totalHeight = 1540.87
base = 4147.65
roof = 2493.97
backHeight = 850.54
hood = 1150.29
hoodAngle = 4.68
frontHeight = 871.27
hoodCos = math.cos(math.radians(hoodAngle))
hoodSin = math.sin(math.radians(hoodAngle))
workbook = openpyxl.Workbook()
sheet = workbook.active

def calculateParameters():
    #Parameters
    x, y, z = symbols('x y z')
    backAngle = round(random.uniform(70,85), 2) #actual value is 77.73
    frontAngle = round(random.uniform(50,65), 2) #actual value is 58.19
    frontCos = math.cos(math.radians(frontAngle))
    frontSin = math.sin(math.radians(frontAngle))
    backCos = math.cos(math.radians(backAngle))
    backSin = math.sin(math.radians(backAngle))
    
    #Calculations
    widthEq = hood*hoodCos+x*frontCos+z+y*backCos-base
    heightEq1 = frontHeight+hood*hoodSin+x*frontSin-totalHeight
    heightEq2 = backHeight+y*backSin-totalHeight
    eq = solve((widthEq, heightEq1, heightEq2),(x, y, z),dict=True)
    windShield = round(eq[0][x],2) #actual value is 677.49
    rearWindow = round(eq[0][y],2) #actual value is 706.46
    roof = round(eq[0][z],2) #actual value is 2493.97

    if isRandom == True: cd = round(random.uniform(0,1), 3)
    else: cd = None
    
    return windShield, frontAngle, rearWindow, backAngle, roof, cd

def draw(windShield, frontAngle, rearWindow, backAngle, roof):

    turtle.title("Vehicle Side Profile")
    
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

def saveResults(windShield, frontAngle, rearWindow, backAngle, roof, cd):
    
    #Print Parameter Results 
    print("Wind Shield Length: ",windShield)
    print("Wind Shield Angle: ",frontAngle)
    print("Rear Window Length: ",rearWindow)
    print("Rear Window Angle: ",backAngle)
    print("Roof Length: ",roof)
    print("Cd: ",cd)

    # Next row for the data
    next_row = sheet.max_row + 1

    # Generate a unique filename based on the current row number
    eps_filename = f'dataset-{current_date}/eps_images/drawing_{next_row}.eps'
    png_filename = f'dataset-{current_date}/images/drawing_{next_row}.png'
    
    # Save the drawing as an EPS file and convert EPS file to PNG
    canvas.postscript(file=eps_filename)
    with Image.open(eps_filename) as img:
        img.save(png_filename)
    
    # Insert the image and parameters into the Excel file
    sheet.cell(row=next_row, column=1).value = "{:.2f}".format(windShield)
    sheet.cell(row=next_row, column=2).value = "{:.2f}".format(frontAngle)
    sheet.cell(row=next_row, column=3).value = "{:.2f}".format(rearWindow)
    sheet.cell(row=next_row, column=4).value = "{:.2f}".format(backAngle)
    sheet.cell(row=next_row, column=5).value = "{:.2f}".format(roof)
    sheet.cell(row=next_row, column=6).value = cd
    
    workbook.save(datasetfile)
    workbook.close()

    print(f"Outputs saved to Excel in row {next_row}.")

#Getting input for iteration from user
iteration = int(input("How many iterations needed?:\n"))
while True:
    userBool = input("Do you want random values for coefficient?: (y/n)").lower()
    if userBool in ['y', 'n']:
        isRandom = userBool == 'y'
        break
    else:
        print("Enter a valid input.\n") 

#Create files
current_date = datetime.now().strftime('%Y_%m_%d')
os.makedirs(f'dataset-{current_date}')
os.makedirs(f'dataset-{current_date}/images')
os.makedirs(f'dataset-{current_date}/eps_images')
datasetfile = f'dataset-{current_date}/dataset.xlsx'
sheet.append(["Wind Shield Length", "Wind Shield Angle (50-65)", "Rear Window Length", "Rear Window Angle (70-85)", "Roof Length", "Cd" ])

#Create turtle screen
s = turtle.getscreen()
t = turtle.Turtle()
screen = turtle.Screen()
canvas = turtle.getcanvas()
screen.setup(width=920, height=400)

#Draws the original values and saves
draw(677.49, 58.19, 706.46, 77.73, 2493.97)
saveResults(677.49, 58.19, 706.46, 77.73, 2493.97, 0.54)
t.clear()

#Iteration
x = 0
while x < iteration: 
    windShield, frontAngle, rearWindow, backAngle, roof, cd = calculateParameters()
    draw(windShield, frontAngle, rearWindow, backAngle, roof)
    saveResults(windShield, frontAngle, rearWindow, backAngle, roof, cd)
    t.clear()
    x += 1

print(f"Dataset has been created into dataset-{current_date} file.")