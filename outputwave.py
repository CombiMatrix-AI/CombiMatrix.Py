#####################################################################################
# FOR LATER INTEGRATION
#####################################################################################

from operator import truediv
import os
from tokenize import Double
import numpy as np
from ctypes import *
import matplotlib.pyplot as plt  # used to pilot chart
# if not installed , use following command to install
# python -m pip install -U pip setuptools
# python -m pip install matplotlib
# also use python -m pip install pillow to save image
import time
from msvcrt import kbhit, getch
import dask91xx

dask = dask91xx.Dask91xxLib()

WRITECOUNT = 256
TIMEBASE = 64000000
UPDATEINTRV = 10000

err = 0
card_num = 0
card_type = 0
ConfigCtrl = dask.P91xx_AO_TIMEBASE_EXT
TrigCtrl = dask.P91xx_AO_TRGMOD_POST | dask.P91xx_AO_TRGSRC_EXTD | dask.P91xx_AO_TrgPositive
TriggerCount = 1  # No retrigger mode
AutoResetBuf = True
WriteCount = WRITECOUNT

Channel = 0  # AO channel to be written
Iterations = 0  # 0: means infinite wave repeats    //repeate count
Interval = UPDATEINTRV
definite = 1  # finite
BufferId = list()

W_Buffer0 = (c_uint16 * WriteCount)()
cast(W_Buffer0, POINTER(c_uint16))

W_Buffer1 = (c_uint16 * WriteCount)()
cast(W_Buffer1, POINTER(c_uint16))

AccessCnt = (c_uint16 * WriteCount)()
cast(AccessCnt, POINTER(c_uint16))

Patten0 = (c_uint16 * WriteCount)()
x = np.linspace(0, 2 * np.pi, WriteCount)
y = np.sin(x) * 0x7fff
y1 = y.astype(c_int16)
for i in range(WriteCount):
    Patten0[i] = y1[i]
cast(Patten0, POINTER(c_uint16))

Patten1 = (c_uint16 * WriteCount)()
x = np.linspace(0, 2 * np.pi, WriteCount)
y = np.sin(x) * 0x7fff
y1 = y.astype(c_int16)
for i in range(WriteCount):
    Patten1[i] = y1[i]
cast(Patten1, POINTER(c_uint16))

W_Buffer0 = Patten0
W_Buffer1 = Patten1


def ExitClear():
    if (AutoResetBuf == False):
        dask.AO_ContBufferReset(var_card)

    dask.PCI_Buffer_Free(var_card, W_Buffer0)
    dask.PCI_Buffer_Free(var_card, W_Buffer1)

    if (var_card >= 0):
        dask.Release_Card(var_card)

    print("card release")


#############################################
# Open and Initialize Device
# Step1. Open and Initialize Device
#############################################

card_type = dask.PCIe_9101

card_num = 0
var_card = dask.Register_Card(card_type, card_num)
if var_card < 0:
    print(f"UD_Register_Card fail, error = {var_card}\n")
    exit()
print("Register card successfully")

#############################################
# AOConfig
# Configure DAQ
# Step 2.Configure AO
#############################################

dask.AO_relay_EN(var_card, 1)

err = dask.AO_Config(var_card, ConfigCtrl, TrigCtrl, TriggerCount, AutoResetBuf)

if err < 0:
    print(f"AO_Config Error: {err}\n")
    ExitClear()

# Enable Double Buffer Mode*/
err = dask.AO_AsyncDblBufferMode(var_card, 0)
if (err < 0):
    print(f"AO_AsyncDblBufferMode Error: {err}\n")
    ExitClear()

# Setup buffer*/
err = dask.AO_ContBufferSetup(var_card, W_Buffer0, WriteCount, BufferId)
if (err < 0):
    print(f"AO_ContBufferSetup0 Error: {err}\n")
    ExitClear()

print("finish")

#############################################
# AOStart

# Step 3. AO Start
#############################################

err = dask.AO_ContWriteChannel(var_card, Channel, BufferId[0], WriteCount, Iterations, Interval, definite,
                               dask.ASYNCH_OP)
if (err < 0):
    print(f"AO_ContWriteChannel Error: {err}\n")
    dask.AO_ContBufferReset(var_card)
    ExitClear()

print("Start AO")
Stopped = list()
Stopped.append(False)

HalfReady = list()
VBuffer = list()
AccessCnt = list()
Startpos = c_uint32()

RdyBufCnt = 0

while ((Stopped[0] == False) and (kbhit() == False)):

    err = dask.AO_AsyncCheck(var_card, Stopped, AccessCnt)
    if (err < 0):
        print(f"AO_AsyncCheck Error: {err}\n")
        ExitClear()

if (Stopped):
    print(f"\nAO Update Done...\n")
else:
    print(f"\nAO will be stopped...\n")

#############################################
# Stop AO
# Step 4.Stop AO
#############################################

var_ret = dask.AO_AsyncClear(var_card, AccessCnt, 0)
dask.Release_Card(var_card)
print("Release card successfully")









