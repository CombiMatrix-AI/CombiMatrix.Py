#####################################################################################
# ADLINK PCIe-9101 to acquire/measure DATA  
# This sample program shows how to import DLL
# AI One shot acquisition for PCIe-9101
# This sample program run on Python 3.x
# ADLINK Technologies 2023.08.4
#####################################################################################

from operator import truediv
import os
from tokenize import Double
import numpy as np
from ctypes import *
#import matplotlib.pyplot as plt  #used to pilot chart
#if not installed , use following command to install
#python -m pip install -U pip setuptools
#python -m pip install matplotlib
#also use python -m pip install pillow to save image
import time
from msvcrt import kbhit, getch
import dask91xx 


dask=dask91xx.Dask91xxLib()




err=0
card_num=0
card_type=0
Channel = 0  #AO channel to be written


def ExitClear():

    if (var_card >= 0):
        dask.Release_Card(var_card)

    print("card release")
    

#############################################
#Open and Initialize Device
#Step1. Open and Initialize Device
#############################################

type=int(input("Card Type: (0) PCIe_9101 (1) PCIe_9121 (2) PCIe_9141 (3) PCIe_9103? (4) PCIe_9147"))
if type==0:
    card_type=dask.PCIe_9101
elif type==1:
    card_type = dask.PCIe_9121
elif type==2:
    card_type = dask.PCIe_9141
elif type==3:
    card_type = dask.PCIe_9103
elif type==4:
    card_type = dask.PCIe_9147
else :
    print("Invalid parameter")

card_num=0
var_card =dask.Register_Card(card_type, card_num)
if var_card < 0:
	print(f"UD_Register_Card fail, error = {var_card}\n")
	exit()
print("Register card successfully")


#############################################
# AOConfig
#Configure DAQ   
#Step 2.Configure AO
#############################################

dask.AO_relay_EN(var_card, 1)

print("finish")

#############################################
# AOStart

#Step 3. AO Start
#############################################

print("Start AO")
Stopped =list() 
Stopped.append(False)

HalfReady =list() 
VBuffer=list()
AccessCnt  =list()
Startpos = c_uint32()


while (True) :
   
    Channel=int(input("AO Channel Number to be update: [0 or 1] "))
    if (Channel > 1) :
        print(f"Invalid Channel Number... Set to Channel 0\n")
        Channel = 0

    Voltage=float(input("AO voltage to be updated: [-10 ~ 10]"))
    if (Voltage > 10 or Voltage < -10) :
        print(f"Out of range, forcedly ouput 10V\n")
        Voltage = 0


    err = dask.AO_VWriteChannel(var_card, Channel, Voltage)
    if (err < 0) :
        print(f"AO_VWriteChannel Error: %d\n", err)
        ExitClear()

    text=input("\n (C)ontinue?")
    if text!="C" and text!="c":
        break
        

if (Stopped):
    print(f"\nAO Update Done...\n")
else:
    print(f"\nAO will be stopped...\n")

    
#############################################
#Stop AO
#Step 4.Stop AO
#############################################

var_ret = dask.AO_AsyncClear(var_card, AccessCnt, 0)
dask.Release_Card(var_card)
print("Release card successfully")
