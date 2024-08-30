######################################################################################
# Controls the ADLINK PCIe-9101 card
######################################################################################

import time
import dask91xx

class Adlink:
    def __init__(self):
        self.dask = dask91xx.Dask91xxLib()
        self.var_card = self.dask.Register_Card(52, 0)  # PCIe_9101 = 52, see dask91xx.py
        if self.var_card < 0:
            print(f"UD_Register_Card fail, error = {self.var_card}\n")
            exit()
        print("Register card successfully")

    def set_voltage(self):
        self.dask.AO_relay_EN(self.var_card, 1)

        print("Start AO")

        stopped = list()
        stopped.append(False)

        access_cnt = list()

        while (True):

            channel = 0 # 0 or 1
            voltage = 0 # -10 to 10

            err = self.dask.AO_VWriteChannel(self.var_card, channel, voltage)
            if (err < 0):
                print(f"AO_VWriteChannel Error: %d\n", err)
                self.exit_clear(self.var_card)

            text = input("\n (C)ontinue?")
            if text != "C" and text != "c":
                break

        if (stopped):
            print(f"\nAO Update Done...\n")
        else:
            print(f"\nAO will be stopped...\n")

        var_ret = self.dask.AO_AsyncClear(self.var_card, access_cnt, 0)
        self.dask.Release_Card(self.var_card)
        print("Release card successfully")

    def exit_clear(self):
        if (self.var_card >= 0):
            self.dask.Release_Card(self.var_card)

        print("card release")

    def set_chip_map(self, channel, chipmap):
        for column in range(16):
            for row in range(64):
                value = chipmap[16 * row + column]
                status = self.set_chip_state(channel, row, column, value)
        return status

    def set_chip_state(self, channel, row, column, value):
        channel <<= 13

        value <<= 10

        address = column
        address <<= 6
        address |= row

        wr = 0x0
        wr <<= 12
        dataToWrite = address | value | wr | channel

        status = self.dask.DO_WritePort(self.var_card, 0, dataToWrite)
        self.wait(0.00002)

        wr = 0x1
        wr <<= 12
        dataToWrite = address | value | wr | channel

        status = self.dask.DO_WritePort(self.var_card, 0, dataToWrite)
        self.wait(0.00002)

        return status

    def get_chip_map(self, channel, chipmap):
        for column in range(16):
            for row in range(64):
                chipmap[16 * row + column] = self.get_chip_state(channel, row, column)

        return chipmap

    def get_chip_state(self, channel, row, column):
        wr = 0x1
        dataRead = []

        channel <<= 13
        wr <<= 12

        address = column
        address <<= 6
        address += row

        dataToWrite = address | wr | channel

        status = self.dask.DO_WritePort(self.var_card, 0, dataToWrite)
        self.wait(0.00002)
        status = self.dask.DI_ReadPort(self.var_card, 0, dataRead)
        self.wait(0.00002)

        out = dataRead[0] >> 14

        return out

    def wait(self, duration, get_now=time.perf_counter):
        now = get_now()
        end = now + duration
        while now < end:
            now = get_now()
