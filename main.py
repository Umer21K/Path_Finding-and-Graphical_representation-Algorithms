import tkinter as tk
import Augmenting_path as au
import Bipartide_Graph as bg
import Complete_graph as cg
import Dijkstra_HAU as dh
import Havel_Hakimi as hh
import Prims as pr
import Simple_graph as sg
import Tripartide as tr

def aug():
    au.main()


def dij():
    dh.main()

def havel():
    hh.main()


def prim():
    pr.main()

def bip():
    bg.main()

def com():
    cg.main()

def sim():
    sg.main()

def trip():
    tr.main()
# # Create the main window
root = tk.Tk()
root.title("Library Function Caller")

# Create and pack the buttons
button1 = tk.Button(root, text="Augmenting Flow", command=aug)
button1.pack(pady=5)

button2 = tk.Button(root, text="Dijkstra", command=dij)
button2.pack(pady=5)

button3 = tk.Button(root, text="Havel Hakimi", command=havel)
button3.pack(pady=5)

button4 = tk.Button(root, text="Prims", command=prim)
button4.pack(pady=5)

button5 = tk.Button(root, text="Bipartide Graph", command=bip)
button5.pack(pady=5)

button6 = tk.Button(root, text="Complete Graph", command=com)
button6.pack(pady=5)

button7 = tk.Button(root, text="Simple Graph", command=sim)
button7.pack(pady=5)

button8 = tk.Button(root, text="Tripartide Graph", command=trip)
button8.pack(pady=5)


root.mainloop()
