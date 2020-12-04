import tkinter as tk
from tkinter import filedialog
import struct
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

defaultsize = 512


def read_binfile():
    root = tk.Tk()
    root.withdraw()
    Filepath = filedialog.askopenfilename()
    # print(Filepath)
    # Filepath="D:/code/data/data/topo/200/200Z_flat_afterRegr.bin"
    file = open(Filepath, "rb")

    nx = struct.unpack(">i", file.read(4))[0]
    ny = struct.unpack(">i", file.read(4))[0]

    print(nx)
    print(ny)
    v = np.float64(struct.unpack(">d", file.read(8)))[0]
    current = np.float64(struct.unpack(">d", file.read(8)))[0]

    topo = np.zeros((nx, ny), dtype=np.float64)
    x = np.zeros(nx, dtype=np.float64)
    y = np.zeros(ny, dtype=np.float64)

    for i in range(nx):
        x[i] = np.float64(struct.unpack(">d", file.read(8)))[0]
    for j in range(nx):
        y[j] = np.float64(struct.unpack(">d", file.read(8)))[0]
    count = 0
    for i in range(nx):
        for j in range(ny):
            topo[i][j] = np.float64(struct.unpack(">d", file.read(8)))[0]
            c = topo[i][j]
            if c == "":
                count = count + 1



    return [topo,nx,ny,x,y,v,current]
lsit=read_binfile()
a=len(lsit[3])
print(lsit[3])
lenth=abs(np.max(lsit[3])-np.min(lsit[3]))
print(lenth)
