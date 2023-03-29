from tkinter import *
#from PIL import ImageTk
from arpesufmg import *
from tkinter import filedialog 

root = Tk()
root.withdraw()

#Set the path with data

file_path = filedialog.askopenfile(initialdir='C:/', title='Select a file', filetypes=(('png files', '*.png'),('all files','*.*')))

print(file_path.name)

arpes_object = ArpesUFMG()

# Choose dimensions (w x h - respect ratio) energy range (Ei -> E_f) and Angle accptance range (Chi_i -> Chi_f) 

df, m, n = arpes_object.put_axes(file_path.name, resize=True, w=100, h=100, E_i=19.000, E_f=22.000, Chi_i=-10, Chi_f=10)

# Choose azimutal position phi
da = arpes_object.k_warp(df,  m, n, phi=0, verbose=False)

# Plot the result
arpes_object.plot_k_warp(da)