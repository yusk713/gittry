# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 10:09:31 2020

@author: 25223
"""


#sxm hahahahhahahhaha
#more change

import tkinter as tk
from tkinter import filedialog
import struct
import numpy as np
root=tk.Tk()
root.withdraw()

def main():
    # Filepath = filedialog.askopenfilename()
    Filepath=r"D:\code\dan Java\sxm\196.sxm"
    file=open(Filepath,"rb")
    print(Filepath)
    
    headlist=[]#记录数据的测量信息
    head=""
    
    while head.find("SCANIT_END")==-1:
    # for i in range(43):
        head=str(file.readline())
        # head=head[2:-3]
        # print(head)
        headlist.append(head)
    # headlist=headlist[0:-2]
    for i in range(len(headlist)):
        print(headlist[i])
    
    thing=""
    name=[]
    for i in range(len(headlist)):
        if headlist[i].find("SCAN_PIXELS")!=-1:
            thing=headlist[i+1][2:-3]
            scan_pixels=thing.split()
            nx=int(scan_pixels[0])
            ny=int(scan_pixels[1])
            print(type(nx))   
        if headlist[i].find("SCAN_RANGE")!=-1:    
            thing=headlist[i+1][2:-3]
            scan_range=thing.split()
            lx=np.float64(scan_range[0])
            ly=np.float64(scan_range[1])
            

        if headlist[i].find("SCAN_OFFSET")!=-1:
            thing=headlist[i+1][2:-3]
            scan_offset=thing.split()
            cx=np.float64(scan_offset[0])
            cy=np.float64(scan_offset[1])
            

        if headlist[i].find("SCAN_ANGLE")!=-1:    
            thing=headlist[i+1][2:-3]
            scan_angle=np.float64(thing.split()[0])
            
        if headlist[i].find("SCAN_DIR")!=-1:
            thing=headlist[i+1][2:-3]
            direction=thing
            # nchannels=len(headlist)-i-2
            # print(nchannels)
        
        if headlist[i].find(":BIAS:")!=-1:
            thing=headlist[i+1][2:-3]    
            bias=np.float64(thing)
            print(bias)
            
        if headlist[i].find("log Current")!=-1:
            thing=headlist[i][3:-3]   
            log_Cur=thing.split("\\")
            log_Current=np.float64(log_Cur[2][1:-2])
            # log_Current=np.float64(log_Current)
            print(log_Current)
            # print(thing)
            
           
        if headlist[i].find("DATA_INFO")!=-1:
            # thing=headlist[i+1][2:-3]   
            nchannels=int((len(headlist)-i-4)*2)

            for j in range (nchannels//2):
                thing=headlist[i+2+j][2:-3]
                info=thing.split("\\")

                name.append(info[2][1:])
                name.append(info[2][1:]+" back")
        
                
    x=np.linspace(cx-lx/2, cx+lx/2, nx)
    y=np.linspace(cy-ly/2, cy+ly/2, ny)
    # print(y)

    dataset=np.zeros((nchannels,nx,ny),dtype=np.float64)
    for i in range(2):
        head=str(file.readline())
        # print(head)#读取无效行，以下为二维数组信息
    # data=file.read(4)
    # print(data)
    for i in range(2):
        unknown=struct.unpack(">b",file.read(1))
        print(unknown)
    for i in range(nchannels):
        for j in range(nx):
            for k in range(ny):
                
                dataset[i][j][k]=np.float64(struct.unpack(">f",file.read(4)))
    
    print(name)
    # print(dataset)
    # for i in range(6):
    #     head=str(file.readline())
    #     print(1)
    #     print(head)#           
    # for i in range(5):
    #     for j in range(3):
    #         for k in range(3):
    #                print(dataset[i][j][k])
    # print("over")
    # for i in range(10):
        
    #     s=file.read(1)
    #     print(s)
    print(type(log_Current))
    print(type(bias))
    for i in range(len(name)):
        if name[i].find("\\")==1:
            name[i]=name[i].split("\\")[0]+name[i].split("\\")[1]
        if name[i].find("/")==1:
            name[i]=name[i].split("/")[0]+name[i].split("/")[1]
        binfile=open(name[i]+".bin","wb")
        data=struct.pack(">i",nx)
        binfile.write(data)
        data=struct.pack(">i",ny)
        binfile.write(data)  
        data=struct.pack(">d",log_Current)
        binfile.write(data)
        data=struct.pack(">d",bias)
        binfile.write(data)
        print(len(x))
        print(len(y))
        
        print(dataset.shape)
        for m in range(len(x)):
            data=struct.pack(">d",x[m])
            binfile.write(data)
        for n in range(len(y)):
            data=struct.pack(">d",y[n])
            binfile.write(data)
    
        
        for m in range(nx):
            for n in range(ny):
                data=struct.pack(">d",dataset[i][m][n])
                binfile.write(data)
        binfile.close()
                
           
            
            

            # print(thing)
            # print(1)
#     for i in range(len(headlist)):
#         if headlist[i].find("Scan>channels")!=-1:
#             thing = headerLines.get(i+1).trim()				
# 			nchannels = thing.split(";").length;
# 			names = new String [nchannels*2];
            
    
main()