# -*- coding: utf-8 -*-
"""
Created on Mon Aug  3 19:50:10 2020

@author: 25223
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Aug  1 16:54:04 2020

symmetry

@author: 25223
"""

import tkinter as tk
from tkinter import filedialog
import struct
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import cv2
import readtxt as t
import math
import bin
import writebin

defaultsize=512

def read_txt_file(path):
    import re
    file = open(path,'r',encoding='utf-8')
    list_arr = file.readlines()
    lists = []
    r = '[’!"#$%&\'()*+,/:;<=>?@[\\]^_`{|}~]'
    for index, x in enumerate(list_arr):
        a = re.sub(r,'',x)
        c = a.strip()
        c = c.split()
        lists.append(c)
    return np.array(lists)

def fft_topo():
    root=tk.Tk()
    root.withdraw()
    Filepath = filedialog.askopenfilename()
    # print(Filepath)
    # Filepath="D:/code/data/data/topo/200/200Z_flat_afterRegr.bin"
    # Filepath="D:/code/data/data/数据/QPI/Sr2RuO4/43meV/gLockin_Y_flat_afterFancy.bin"
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
    
    topo=topo-np.mean(topo)
    fftdata=np.fft.fft2(topo)
    fftdata=np.fft.fftshift(fftdata)
    fftmodu=abs(fftdata)
    # fftmodu=np.log(fftmodu)
    size=nx
    file.close()
    
    # fig,ax = plt.subplots(figsize =(10,10),constrained_layout =True)#绘制子图区域 size为5*5，constrained_layout =True避免子图重叠

    
    # ax.pcolormesh(fftmodu,cmap='Blues',vmin=np.min(fftmodu),vmax=np.max(fftmodu))#绘制边界图
    # # ax.imshow(field)
    # # psm = ax.contourf(field+1,cmap="Blues")#绘制边界图
    # ax.set_title('field')
    # plt.show()    
    # # print(nx)
    # print(count)
    # print(type(topo[0][0]))
    # topofinal=np.zeros((int(size/2),int(size/2)),dtype=np.float64)
    # reduce=False
    return[fftmodu,nx,ny,v,current,x,y,Filepath]

def main():
    fftinfo=fft_topo()
    [data,nx,ny,v,current,x,y,path]=fftinfo

    
    mean=np.mean(data)
    braggvec=t.read_txt()
    
    unitbraggvec=[0,0]
    unitbraggvec[0]=t.unitvector(braggvec[0][0],braggvec[0][1])
    unitbraggvec[1]=t.unitvector(braggvec[1][0],braggvec[1][1])
    
    print(unitbraggvec)
    
    Reflection_matrix=[0,0]
    Reflection_matrix[0]=t.getReflection_matrix(unitbraggvec[0][0],unitbraggvec[0][1])
    Reflection_matrix[1]=t.getReflection_matrix(unitbraggvec[1][0],unitbraggvec[1][1])
    
    print(Reflection_matrix)
    
    reflection=[0,0]
    reflection[0]=t.applyLinearTransformation(data,Reflection_matrix[0])
    reflection[1]=t.applyLinearTransformation(data,Reflection_matrix[1])
    # print(reflection)
    
    ans=np.zeros((3,len(data),len(data[0])))
    ans[0]=data+reflection[0]
    ans[1]=rotate_plus90_about_pixel(ans[0],round(len(ans[0])/2),round(len(ans[0][0])/2))
    ans[2]=ans[0]+ans[1]
    # ans[2]=np.fft.fftshift(ans[2])
    

    # print(ans[2])
    
    dx=(x[-1]-x[0])/(nx-1)
    dy=(y[-1]-y[0])/(ny-1)
    
    leng_x=dx*nx
    leng_y=dy*ny
    
    dx=2*math.pi/leng_x
    dy=2*math.pi/leng_y
    
    
    xnew=np.zeros(nx)
    ynew=np.zeros(ny)
    
    for i in range(nx):
        xnew[i]=(i-nx/2)*dx
    for i in range(ny):
        ynew[i]=(i-nx/2)*dy
        
    location=path.rfind("/")
    
    name=path[0:location+1]+"symm"
    writebin.write_bin(ans[2],nx,ny,current,v,xnew,ynew,name)
    
    
    # for i in range(3):
    #     name="ans"+str(i)+".bin"
    #     writebin.write_bin(ans[i],nx,ny,current,v,xnew,ynew,name)
        
    # for i in range(2):
    #     name="reflection"+str(i)+".bin"
    #     writebin.write_bin(reflection[i],nx,ny,current,v,xnew,ynew,name)   
        
    # name="rawdata.bin"
    # writebin.write_bin(data,nx,ny,current,v,xnew,ynew,name)
    
    
    

    # fig,ax = plt.subplots(figsize =(10,10),constrained_layout =True)#绘制子图区域 size为5*5，constrained_layout =True避免子图重叠

    
    # ax.pcolormesh(ans[2],cmap='Blues',vmin=np.min(ans[2]),vmax=np.max(ans[2]))#绘制边界图

    # ax.set_title('field')
    # plt.show()    

      
    
def rotate_plus90_about_pixel(field,cx,cy):
    result=np.zeros((len(field),len(field[0])))
    [x, y, xp, yp, ip, jp, nx] = [len(field)]*7
    ny=len(field[0])
    for i in range(len(field)):
        for j in range(len(field[0])):
            x=i-cx;y=j-cy
            yp=-x;xp=y
            ip=((xp+cx)+nx)%nx
            jp=((yp+cy)+ny)%ny
            
            result[i][j]=field[ip][jp]
            
    return result
            
            
            
#     data=np.random.rand(4,4)
#     braggvec=t.read_txt()
    
#     unitbraggvec=[0,0]
#     unitbraggvec[0]=t.unitvector(braggvec[0][0],braggvec[0][1])
#     unitbraggvec[1]=t.unitvector(braggvec[1][0],braggvec[1][1])
    
#     print(unitbraggvec)
    
#     Reflection_matrix=[0,0]
#     Reflection_matrix[0]=t.getReflection_matrix(unitbraggvec[0][0],unitbraggvec[0][1])
#     Reflection_matrix[1]=t.getReflection_matrix(unitbraggvec[1][0],unitbraggvec[1][1])
    
#     print(Reflection_matrix)
    
#     reflection=[0,0]
#     reflection[0]=t.applyLinearTransformation(data,Reflection_matrix[0])
#     reflection[1]=t.applyLinearTransformation(data,Reflection_matrix[1])
#     print(reflection)    
# main()
main()
    
    
 
    
    
    
    
    