# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 20:10:51 2020

@author: 25223
"""


#read_bin.py
import tkinter as tk
from tkinter import filedialog
import struct
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

defaultsize=512

def read_binfile():
    root=tk.Tk()
    root.withdraw()
    Filepath = filedialog.askopenfilename()
    # print(Filepath)
    # Filepath="D:/code/data/data/topo/200/200Z_flat_afterRegr.bin"
    file=open(Filepath,"rb")
         
    nx=struct.unpack(">i",file.read(4))[0]
    ny=struct.unpack(">i",file.read(4))[0]
    
    print(nx)
    print(ny)
    v=np.float64(struct.unpack(">d",file.read(8)))[0]
    current=np.float64(struct.unpack(">d",file.read(8)))[0]
         
         
         
    topo=np.zeros((nx,ny),dtype=np.float64)
    x=np.zeros(nx,dtype=np.float64)
    y=np.zeros(ny,dtype=np.float64)
         
    for i in range (nx):
        x[i]=np.float64(struct.unpack(">d",file.read(8)))[0]
    for j in range (nx):
        y[i]=np.float64(struct.unpack(">d",file.read(8)))[0]
    count=0    
    for i in range(nx):
        for j in range(ny):
            topo[i][j]=np.float64(struct.unpack(">d",file.read(8)))[0]
            c=topo[i][j]
            if c=="":
                count=count+1
    print(topo)           
    # topo=np.log(topo)
    
    fftdata=np.fft.fft2(topo)
    fftdata=np.fft.fftshift(fftdata)
    fftmodu=abs(fftdata)
    size=nx
    print(nx)
    print(count)
    print(type(topo[0][0]))
    topofinal=np.zeros((int(size/2),int(size/2)),dtype=np.float64)
    reduce=False
    
    # while size>defaultsize and size/2>=defaultsize:
    #     reduce=True
    #     count=count+1
    #     size=int(size/2)
    #     print(count)
    #     for i in range(len(topofinal)):
    #         for j in range(len(topofinal[0])):
    #             for m in range(2):
    #                 for n in range(2):
    #                     topofinal[i][j]=topo[2*i+m][2*j+n]+topofinal[i][j]
        
       
    file.close()
    if reduce:
        return topofinal
    else:
        return topo
        # return fftmodu
    
def draw_2D(field):
    fig,ax = plt.subplots(figsize =(10,10),constrained_layout =True)#绘制子图区域 size为5*5，constrained_layout =True避免子图重叠
    # print(np.max(field))
    # print(np.min(field))
    #
    # ax.pcolormesh(field,cmap=plt.cm.RdBu,vmin=np.min(field),vmax=np.max(field))#绘制边界图
    ax.pcolormesh(field,cmap="Blues",vmin=np.min(field),vmax=np.max(field))
    # ax.imshow(field)
    # psm = ax.contourf(field+1,cmap="Blues")#绘制边界图
    print("输入标题")
    title=input()
    ax.set_title(title)
    print(np.shape(field))
    plt.savefig('test3.jpg',dpi=np.shape(field)[0])
    plt.show()
data=read_binfile()
fftdata=np.fft.fft2(data)
fftdata=np.fft.fftshift(fftdata)
fftdata=abs(fftdata)
fftdata=np.log(fftdata)
# data=np.log(data)
# print(np.shape(data))
# print(type(data[0][0]))
draw_2D(fftdata)
     
         
    
    