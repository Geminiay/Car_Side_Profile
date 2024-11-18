import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import turtle

def select_file():
    file_path = filedialog.askopenfilename()
    entry_file.delete(0, tk.END)
    entry_file.insert(0, file_path)


def start_process():
    file_path = entry_file.get()
    if not file_path:
        messagebox.showerror("Hata", "Lütfen bir CSV dosyası seçiniz!")
        return
    
    try:
        initial_rearWindow = float(entry1.get())
        initial_windShield = float(entry2.get())
        initial_roof = float(entry3.get())
        initial_backAngle = float(entry4.get())
        initial_frontAngle = float(entry5.get())
        
        cmd = [
            "python", "app.py", 
            str(initial_rearWindow),
            str(initial_windShield),
            str(initial_roof),
            str(initial_backAngle),
            str(initial_frontAngle),
            file_path 
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        output = result.stdout
        
        info_box.config(state=tk.NORMAL)
        info_box.delete(1.0, tk.END)
        info_box.insert(tk.END, output)
        info_box.config(state=tk.DISABLED)

        t.clear()
        t.penup()
        t.goto(-150, -150)  
        t.pendown()
        t.forward(initial_rearWindow) 
        t.left(initial_backAngle)
        t.forward(initial_roof) 
        t.left(initial_frontAngle)
        t.forward(initial_windShield)  

    except ValueError:
        messagebox.showerror("Hata", "Lütfen geçerli sayısal değerler giriniz!")

root = tk.Tk()
root.title("Araç Profili Optimizasyonu")
root.geometry("1000x800") 


tk.Label(root, text="CSV Dosya Seç:").pack()
entry_file = tk.Entry(root, width=50)
entry_file.pack()
tk.Button(root, text="Dosya Seç", command=select_file).pack()

tk.Label(root, text="Rear Window:").pack()
entry1 = tk.Entry(root)
entry1.pack()

tk.Label(root, text="Wind Shield:").pack()
entry2 = tk.Entry(root)
entry2.pack()

tk.Label(root, text="Roof:").pack()
entry3 = tk.Entry(root)
entry3.pack()

tk.Label(root, text="Back Angle:").pack()
entry4 = tk.Entry(root)
entry4.pack()

tk.Label(root, text="Front Angle:").pack()
entry5 = tk.Entry(root)
entry5.pack()

tk.Button(root, text="Başlat", command=start_process).pack()

info_box = tk.Text(root, height=10, state=tk.DISABLED)
info_box.pack()

canvas_frame = tk.Frame(root)
canvas_frame.pack()

canvas = tk.Canvas(canvas_frame, width=800, height=600)  # Canvas boyutunu büyüttüm
canvas.pack()

t = turtle.RawTurtle(canvas)
t.speed(10)


root.mainloop()
