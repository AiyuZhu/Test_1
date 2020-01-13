import tkinter as tk
import numpy as np
import pandas as pd

a = np.array([1,2,3,4])


unit = 100
width_N = 6
height_N = 5

window = tk.Tk()
window.title('show value test')
window.geometry('{0}x{1}'.format(unit*width_N,unit*height_N))

canvas = tk.Canvas(window, bg='white', height =unit*height_N, width = unit*width_N)

line = canvas.create_line(0,300,600,300)
#create grids
for w in range(0, unit*width_N, unit):
    x0, x1, y0, y1 = w, 0, w, unit*height_N
    line_w = canvas.create_line(x0,x1,y0,y1, fill= 'black')

for h in range(0, unit*height_N, unit):
    x0, x1, y0, y1 = 0, h , unit*width_N, h
    line_h = canvas.create_line(x0, x1, y0, y1, fill= 'black')

origin_point = np.array([50,50])
value_broad = canvas.create_rectangle(
    origin_point[0] - 40, origin_point[1] - 40,
    origin_point[0] + 40, origin_point[1] + 40,
)

# tk.Label(window, text = a[0]).place(origin_point[0], origin_point[1], anchor = 'center')
label = tk.Label(window, text = a[0])
label.place(x = origin_point[0], y = origin_point[1] - 20, anchor = 'center')
# label.place_forget()

canvas.pack()
window.mainloop()
