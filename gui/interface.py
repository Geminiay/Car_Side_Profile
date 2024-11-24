import customtkinter as ctk
from tkinter import filedialog, messagebox, Tk, Canvas
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
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
        file_label.configure(text=f"Selected File: {selected_file}")  # Update the label with the selected file path

# Function to read data from selected file
def read_file_to_matrix(file_path):
    if not file_path:
        raise ValueError("Please select a valid file.")
        
    if file_path.endswith('.csv'):
        data = pd.read_csv(file_path)
    elif file_path.endswith('.xlsx') or file_path.endswith('.xls'):
        data = pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file type. Please select a CSV or Excel file.")
    
    if data.empty:
        raise ValueError("The file is empty or could not be read properly.")
    
    data_X = data.iloc[:, 1:-1].values
    data_y = data.iloc[:, -1].values

    return np.array(data_X), np.array(data_y)

# Linear regression model fitting
def linearRegression(X, y):
    if X is None or y is None or len(X) == 0 or len(y) == 0:
        raise ValueError("Invalid input data for training.")
    
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
        # Get input values from the user interface
        rearWindow = float(rearWindow_entry.get()) if rearWindow_entry.get() else None
        windShield = float(windShield_entry.get()) if windShield_entry.get() else None
        roof = float(roof_entry.get()) if roof_entry.get() else None
        backAngle = float(backAngle_entry.get()) if backAngle_entry.get() else None
        frontAngle = float(frontAngle_entry.get()) if frontAngle_entry.get() else None

        if None in [rearWindow, windShield, roof, backAngle, frontAngle]:
            raise ValueError("All input fields must be filled.")

        if not file_path.get():
            raise ValueError("Please select a file.")

        # Read the file and train the model
        X, y = read_file_to_matrix(file_path.get())
        lin_model = linearRegression(X, y)

        # Initial guess for optimization
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

        # Update results on the GUI with larger font
        result_label.configure(text=f"Optimized Values:\n"
                                   f"Rear Window: {X_optimized[0]:.2f}\n"
                                   f"Wind Shield: {X_optimized[1]:.2f}\n"
                                   f"Roof: {X_optimized[2]:.2f}\n"
                                   f"Back Angle: {X_optimized[3]:.2f}\n"
                                   f"Front Angle: {X_optimized[4]:.2f}\n"
                                   f"Predicted Minimum Target: {y_optimized:.4f}",
                                   font=("Arial", 16))

        draw(X_optimized[0], X_optimized[1], X_optimized[2], X_optimized[3], X_optimized[4])

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# GUI setup
root = ctk.CTk()
root.title("Vehicle Profile Optimizer")

# Disable resizing of the window
root.resizable(False, False)

file_path = ctk.StringVar()

# Apply dark mode theme to the entire GUI
ctk.set_appearance_mode("dark")

# Left Panel (Inputs)
left_frame = ctk.CTkFrame(root)
left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="n",)

ctk.CTkLabel(left_frame, text="Rear Window:").grid(row=0, column=0, sticky="w", pady=2)
rearWindow_entry = ctk.CTkEntry(left_frame)
rearWindow_entry.grid(row=0, column=1, pady=2)

ctk.CTkLabel(left_frame, text="Wind Shield:").grid(row=1, column=0, sticky="w", pady=2)
windShield_entry = ctk.CTkEntry(left_frame)
windShield_entry.grid(row=1, column=1, pady=2)

ctk.CTkLabel(left_frame, text="Roof:").grid(row=2, column=0, sticky="w", pady=2)
roof_entry = ctk.CTkEntry(left_frame)
roof_entry.grid(row=2, column=1, pady=2)

ctk.CTkLabel(left_frame, text="Back Angle:").grid(row=3, column=0, sticky="w", pady=2)
backAngle_entry = ctk.CTkEntry(left_frame)
backAngle_entry.grid(row=3, column=1, pady=2)

ctk.CTkLabel(left_frame, text="Front Angle:").grid(row=4, column=0, sticky="w", pady=2)
frontAngle_entry = ctk.CTkEntry(left_frame)
frontAngle_entry.grid(row=4, column=1, pady=2)

ctk.CTkButton(left_frame, text="Select File", command=select_file).grid(row=5, column=0, columnspan=2, pady=5)
file_label = ctk.CTkLabel(left_frame, text="No file selected", text_color="white")
file_label.grid(row=6, column=0, columnspan=2)

# Right Panel (Results)
right_frame = ctk.CTkFrame(root)
right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="n")

# Start Button to trigger optimization (above Optimized Values)
start_button = ctk.CTkButton(right_frame, text="Start Optimization", command=start_optimization)
start_button.grid(row=0, column=0, columnspan=2, pady=5)

# Optimized Values label (larger font)
ctk.CTkLabel(right_frame, text="Optimized Values", font=("Arial", 20)).grid(row=1, column=0, columnspan=2, pady=5)

# Result label (larger font)
result_label = ctk.CTkLabel(right_frame, text="Optimized values will appear here.", font=("Arial", 16))
result_label.grid(row=2, column=0, padx=10, pady=10)

# Canvas for Turtle Screen
canvas = Canvas(root, width=920, height=400)
canvas.grid(row=1, column=0, columnspan=2, pady=10)
screen = turtle.TurtleScreen(canvas)
t = turtle.RawTurtle(screen)

# Start the Tkinter event loop
root.mainloop()
