import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression
from scipy.optimize import minimize
import warnings
import turtle
from PIL import Image
import math


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

def draw(rearWindow, windShield, roof, backAngle, frontAngle):
 
    turtle.title(f"Vehicle Side Profile")
    
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
    
    #Generate a unique filename based on the current row number
    eps_filename = f'output/drawing.eps'
    png_filename = f'output/drawing.png'
    
    #Save the drawing as an EPS file and convert EPS file to PNG
    canvas.postscript(file=eps_filename)
    with Image.open(eps_filename) as img:
        img.save(png_filename)
    t.clear()

# Function to read data from a CSV file into feature matrix X and target array y
def read_csv_to_matrix(file_path):
    # Load CSV file using pandas
    data = pd.read_csv(file_path)
    
    # Exclude the first column (which seems to be row indices)
    data_X = data.iloc[:, 1:-1].values  # Select all columns except the first (index) and last (target)
    data_y = data.iloc[:, -1].values    # The last column is the target variable
    
    return np.array(data_X), np.array(data_y)

# Define the linear regression model fitting and evaluation
def linearRegression(X, y):
    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Fit the linear regression model
    lin_model = LinearRegression()
    lin_model.fit(X_train, y_train)

    # Predict and calculate MSE and R-squared
    lin_pred = lin_model.predict(X_test)
    lin_mse = mean_squared_error(y_test, lin_pred)
    lin_r2 = r2_score(y_test, lin_pred)
    
    print(f"Linear Regression Model MSE: {lin_mse}")
    print(f"Linear Regression Model R-squared: {lin_r2}")

    # Return the fitted model
    return lin_model

# Constraint functions for the optimization problem
def constraint1(X):
    return np.sin(np.radians(X[4])) * X[1] - 575.75

def constraint2(X):
    return np.sin(np.radians(X[3])) * X[0] - 690.33

def constraint3(X):
    return np.cos(np.radians(X[3])) * X[0] + np.cos(np.radians(X[4])) * X[1] + X[2] - 3001.2

# Optimization objective function
def objective_function(X_input, lin_model):
    # Reshape input data to match the expected shape
    X_input = np.array(X_input).reshape(1, -1)
    
    # Predict the target value using the model
    y_pred = lin_model.predict(X_input)
    
    # Return the predicted value (we want to minimize this)
    return y_pred[0]


# Suppress the specific UserWarning for delta_grad == 0.0
warnings.filterwarnings("ignore", message="delta_grad == 0.0", category=UserWarning)

# Define the file path (for your CSV file now)
file_path = 'data.csv'

# Read the data from the CSV file into a matrix
X, y = read_csv_to_matrix(file_path)

print("Feature Matrix X:\n", X)
print("Target Array y:\n", y)

# Fit the linear regression model
lin_model = linearRegression(X, y)

# Prompt the user for initial values
initial_rearWindow = float(input("Enter initial value for rearWindow: "))
initial_windShield = float(input("Enter initial value for windShield: "))
initial_roof = float(input("Enter initial value for roof: "))
initial_backAngle = float(input("Enter initial value for backAngle: "))
initial_frontAngle = float(input("Enter initial value for frontAngle: "))

# Use the user-provided initial values as the starting guess for optimization
initial_guess = np.array([initial_rearWindow, initial_windShield, initial_roof, initial_backAngle, initial_frontAngle])

# Bounds for the optimizer (you can set specific bounds for your problem if needed)
bounds = [(min(X[:, i]), max(X[:, i])) for i in range(X.shape[1])]

# Define constraints in a format suitable for the minimize function
constraints = [
    {'type': 'eq', 'fun': constraint1},
    {'type': 'eq', 'fun': constraint2},
    {'type': 'eq', 'fun': constraint3}
]

# Use a minimization algorithm to find the feature values that minimize the target value
result = minimize(objective_function, initial_guess, args=(lin_model), bounds=bounds, constraints=constraints, method='trust-constr')

# Extract the optimized feature values
X_optimized = result.x
y_optimized = result.fun

print("Optimized Feature Values (X):", X_optimized)
print("Predicted Minimum Target Value (y):", y_optimized)

#Create turtle screen
s = turtle.getscreen()
t = turtle.Turtle()
screen = turtle.Screen()
canvas = turtle.getcanvas()
screen.setup(width=920, height=400)
turtle.speed(10)

draw(X_optimized[0], X_optimized[1], X_optimized[2], X_optimized[3], X_optimized[4])

