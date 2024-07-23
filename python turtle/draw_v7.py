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
totalWidth = 4166.03
totalHeight = 1535.63
base = 4166.03
roof = 2507.93
backHeight = 833.01
hood = 1158.16
hoodAngle = 4.88
frontHeight = 862.07
hoodCos = math.cos(math.radians(hoodAngle))
hoodSin = math.sin(math.radians(hoodAngle))
workbook = openpyxl.Workbook()
sheet = workbook.active

def calculateParameters():
    #Parameters
    x, y, z = symbols('x y z')
    backAngle = round(random.uniform(70,85), 2) #actual value is 78.26
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
    windShield = round(eq[0][x],2) #actual value is 664.75
    rearWindow = round(eq[0][y],2) #actual value is 755.63
    roof = round(eq[0][z],2) #actual value is 2507.93
    
    return windShield, frontAngle, rearWindow, backAngle, roof

def draw(windShield, frontAngle, rearWindow, backAngle, roof):

    turtle.title("Vehicle Side Profile")
    
    #Draw
    t.hideturtle()
    t.penup()
    t.goto(-totalWidth/20, -totalHeight/20)
    t.pendown()
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
    t.lt(90)

def saveResults(windShield, frontAngle, rearWindow, backAngle, roof, cd):
    
    #Print Parameter Results 
    print("Wind Shield Length: ",windShield)
    print("Wind Shield Angle: ",frontAngle)
    print("Rear Window Length: ",rearWindow)
    print("Rear Window Angle: ",backAngle)
    print("Roof Length: ",roof)
    
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
    sheet.cell(row=next_row, column=6).value = png_filename
    if isRandom == True:
        sheet.cell(row=next_row, column=7).value = cd
    
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
sheet.append(["Wind Shield Length", "Wind Shield Angle (50-65)", "Rear Window Length", "Rear Window Angle (70-85)", "Roof Length", "Image Path", "Cd Coefficient" ])

#Create turtle screen
s = turtle.getscreen()
t = turtle.Turtle()
screen = turtle.Screen()
canvas = turtle.getcanvas()
screen.setup(width=460, height=200)

#Draws the original values and saves
draw(664.75, 58.19, 755.63, 78.26, 2507.93)
saveResults(664.75, 58.19, 755.63, 78.26, 2507.93, 0.471)
t.clear()

#Iteration
x = 0
while x < iteration: 
    windShield, frontAngle, rearWindow, backAngle, roof = calculateParameters()
    draw(windShield, frontAngle, rearWindow, backAngle, roof)
    saveResults(windShield, frontAngle, rearWindow, backAngle, roof, round(random.uniform(0,1), 3))
    t.clear()
    x += 1

print(f"Dataset has been created into dataset-{current_date} file.")