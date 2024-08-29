######################################################################################
# Controls the ADLINK card
######################################################################################

from operator import truediv
import os
from tokenize import Double
import numpy as np
from ctypes import *
# import matplotlib.pyplot as plt  #used to pilot chart
# if not installed , use following command to install
# python -m pip install -U pip setuptools
# python -m pip install matplotlib
# also use python -m pip install pillow to save image
import time
import dask91xx

dask = dask91xx.Dask91xxLib()
card_num = 0

def ExitClear(var_card):
    if (var_card >= 0):
        dask.Release_Card(var_card)

    print("card release")


#############################################
# Open and Initialize Device
# Step1. Open and Initialize Device
#############################################

def set_voltage():
    err = 0
    Channel = 0  # AO channel to be written

    var_card = dask.Register_Card(52, card_num) # PCIe_9101 = 52, see dask91xx.py
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

    print("finish")

    #############################################
    # AOStart

    # Step 3. AO Start
    #############################################

    print("Start AO")
    Stopped = list()
    Stopped.append(False)

    HalfReady = list()
    VBuffer = list()
    AccessCnt = list()
    Startpos = c_uint32()

    while (True):

        Channel = int(input("AO Channel Number to be update: [0 or 1] "))
        if (Channel > 1):
            print(f"Invalid Channel Number... Set to Channel 0\n")
            Channel = 0

        Voltage = float(input("AO voltage to be updated: [-10 ~ 10]"))
        if (Voltage > 10 or Voltage < -10):
            print(f"Out of range, forcedly ouput 10V\n")
            Voltage = 0

        err = dask.AO_VWriteChannel(var_card, Channel, Voltage)
        if (err < 0):
            print(f"AO_VWriteChannel Error: %d\n", err)
            ExitClear(var_card)

        text = input("\n (C)ontinue?")
        if text != "C" and text != "c":
            break

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

def SetChipMap(channel, chipmap):
    row = 0
    column = 0
    status = 0
    address = 0x0
    value = 0
    wr = 0
    dataToWrite = 0x0000

    channel <<= 13

    for column in range(16):
        for row in range(64):
            value = chipmap[16 * row + column]
            value <<= 10

            address = column
            address <<= 6
            address |= row

            wr = 0x0
            wr <<= 12
            dataToWrite = address | value | wr | channel

            status = dask.DO_WritePort(card_num, 0, dataToWrite)
            wait(0.00002)

            wr = 0x1
            wr <<= 12
            dataToWrite = address | value | wr | channel

            status = dask.DO_WritePort(card_num, 0, dataToWrite)
            wait(0.00002)

            dataToWrite = 0
            address = 0

    return status


def GetChipMap(channel, chipmap):
    status = 0
    column = 0
    row = 0
    address = 0x0
    value = 0
    wr = 0x1
    dataToWrite = 0x0000
    dataRead = 0x0

    channel <<= 13
    value <<= 10
    wr <<= 12


    for column in range(16):
        for row in range(64):
            address = column
            address <<= 6
            address += row

            dataToWrite = address | value | wr | channel


            status = dask.DO_WritePort(card_num, 0, dataToWrite)
            wait(0.00002)
            status = dask.DI_ReadPort(card_num, 0, dataRead)
            wait(0.00002)


            dataRead >>= 14
            chipmap[16 * row + column] = dataRead

    return status


def SetChipState(channel, row, column, value):
    status = 0
    address = 0x0
    wr = 0
    dataToWrite = 0x0000

    channel <<= 13


    value <<= 10

    address = column
    address <<= 6
    address |= row

    wr = 0x0
    wr <<= 12
    dataToWrite = address | value | wr | channel

    status = dask.DO_WritePort(card_num, 0, dataToWrite)
    wait(0.00002)

    wr = 0x1
    wr <<= 12
    dataToWrite = address | value | wr | channel

    status = dask.DO_WritePort(card_num, 0, dataToWrite)
    wait(0.00002)

    dataToWrite = 0
    address = 0

    return status


def GetChipState(channel, row, column, value):
    status = 0
    address = 0x0
    wr = 0x1
    dataToWrite = 0x0000
    dataRead = 0x0

    channel <<= 13
    wr <<= 12


    address = column
    address <<= 6
    address += row

    dataToWrite = address | wr | channel


    status = dask.DO_WritePort(card_num, 0, dataToWrite)
    wait(0.00002)
    status = dask.DI_ReadPort(card_num, 0, dataRead)
    wait(0.00002)

    dataRead >>= 14
    value = dataRead

    return status

def wait(duration, get_now=time.perf_counter):
    now = get_now()
    end = now + duration
    while now < end:
        now = get_now()