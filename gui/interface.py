import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression
from scipy.optimize import minimize
import warnings
import math
import turtle


# Constants
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

# Draw the vehicle profile using turtle
def draw(rearWindow, windShield, roof, backAngle, frontAngle):
    t.clear()  # Clear previous drawings
    t.hideturtle()
    t.penup()
    t.goto(-totalWidth / 10, -totalHeight / 10)
    t.pendown()
    t.fd(base / 5)
    t.lt(90)
    t.fd(backHeight / 5)
    t.lt(90 - backAngle)
    t.fd(rearWindow / 5)
    t.lt(backAngle)
    t.fd(roof / 5)
    t.lt(frontAngle)
    t.fd(windShield / 5)
    t.rt(frontAngle - hoodAngle)
    t.fd(hood / 5)
    t.lt(90 - hoodAngle)
    t.fd(frontHeight / 5)
    t.lt(90)

# Suppress the specific UserWarning for delta_grad == 0.0
warnings.filterwarnings("ignore", message="delta_grad == 0.0", category=UserWarning)

# File selection dialog
def select_file():
    selected_file = filedialog.askopenfilename(
        filetypes=[("Excel files", "*.xlsx;*.xls"), ("CSV files", "*.csv")]
    )
    if selected_file:
        file_path.set(selected_file)
        file_label.config(text=f"Selected File: {selected_file}")  # Update the label with the selected file path

# Function to read data from selected file
def read_file_to_matrix(file_path):
    if file_path.endswith('.csv'):
        data = pd.read_csv(file_path)
    elif file_path.endswith('.xlsx') or file_path.endswith('.xls'):
        data = pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file type. Please select a CSV or Excel file.")

    data_X = data.iloc[:, 1:-1].values
    data_y = data.iloc[:, -1].values

    return np.array(data_X), np.array(data_y)

# Linear regression model fitting
def linearRegression(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    lin_model = LinearRegression()
    lin_model.fit(X_train, y_train)
    return lin_model

# Constraints for optimization
def constraint1(X):
    return np.sin(np.radians(X[4])) * X[1] - 575.75

def constraint2(X):
    return np.sin(np.radians(X[3])) * X[0] - 690.33

def constraint3(X):
    return np.cos(np.radians(X[3])) * X[0] + np.cos(np.radians(X[4])) * X[1] + X[2] - 3001.2

# Optimization objective function
def objective_function(X_input, lin_model):
    X_input = np.array(X_input).reshape(1, -1)
    y_pred = lin_model.predict(X_input)
    return y_pred[0]

# Run optimization and draw the vehicle
def start_optimization():
    try:
        rearWindow = float(rearWindow_entry.get())
        windShield = float(windShield_entry.get())
        roof = float(roof_entry.get())
        backAngle = float(backAngle_entry.get())
        frontAngle = float(frontAngle_entry.get())

        if not file_path.get():
            raise ValueError("Please select a file.")

        X, y = read_file_to_matrix(file_path.get())
        lin_model = linearRegression(X, y)

        initial_guess = np.array([rearWindow, windShield, roof, backAngle, frontAngle])
        bounds = [(min(X[:, i]), max(X[:, i])) for i in range(X.shape[1])]

        constraints = [
            {'type': 'eq', 'fun': constraint1},
            {'type': 'eq', 'fun': constraint2},
            {'type': 'eq', 'fun': constraint3}
        ]

        result = minimize(objective_function, initial_guess, args=(lin_model), bounds=bounds, constraints=constraints, method='trust-constr')
        X_optimized = result.x
        y_optimized = result.fun

        # Update results on the GUI
        result_label.config(text=f"Optimized Values:\n"
                                 f"Rear Window: {X_optimized[0]:.2f}\n"
                                 f"Wind Shield: {X_optimized[1]:.2f}\n"
                                 f"Roof: {X_optimized[2]:.2f}\n"
                                 f"Back Angle: {X_optimized[3]:.2f}\n"
                                 f"Front Angle: {X_optimized[4]:.2f}\n"
                                 f"Predicted Minimum Target: {y_optimized:.4f}")

        draw(X_optimized[0], X_optimized[1], X_optimized[2], X_optimized[3], X_optimized[4])

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# GUI setup
root = tk.Tk()
root.title("Vehicle Profile Optimizer")

file_path = tk.StringVar()

# Left Panel (Inputs and Results)
left_frame = tk.Frame(root)
left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="n")

tk.Label(left_frame, text="Rear Window:").grid(row=0, column=0, sticky="w", pady=2)
rearWindow_entry = tk.Entry(left_frame)
rearWindow_entry.grid(row=0, column=1, pady=2)

tk.Label(left_frame, text="Wind Shield:").grid(row=1, column=0, sticky="w", pady=2)
windShield_entry = tk.Entry(left_frame)
windShield_entry.grid(row=1, column=1, pady=2)

tk.Label(left_frame, text="Roof:").grid(row=2, column=0, sticky="w", pady=2)
roof_entry = tk.Entry(left_frame)
roof_entry.grid(row=2, column=1, pady=2)

tk.Label(left_frame, text="Back Angle:").grid(row=3, column=0, sticky="w", pady=2)
backAngle_entry = tk.Entry(left_frame)
backAngle_entry.grid(row=3, column=1, pady=2)

tk.Label(left_frame, text="Front Angle:").grid(row=4, column=0, sticky="w", pady=2)
frontAngle_entry = tk.Entry(left_frame)
frontAngle_entry.grid(row=4, column=1, pady=2)

tk.Button(left_frame, text="Select File", command=select_file).grid(row=5, column=0, columnspan=2, pady=5)
file_label = tk.Label(left_frame, text="No file selected", fg="blue")
file_label.grid(row=6, column=0, columnspan=2)

tk.Button(left_frame, text="Start", command=start_optimization).grid(row=7, column=0, columnspan=2, pady=5)

# Results Display
result_label = tk.Label(left_frame, text="Results will be displayed here", fg="green", justify="left")
result_label.grid(row=8, column=0, columnspan=2, pady=10)

# Right Panel (Turtle Drawing)
right_frame = tk.Frame(root)
right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="n")

canvas = tk.Canvas(right_frame, width=920, height=400)
canvas.pack()

# Embed turtle screen
screen = turtle.TurtleScreen(canvas)
t = turtle.RawTurtle(screen)
screen.bgcolor("white")

root.mainloop()
