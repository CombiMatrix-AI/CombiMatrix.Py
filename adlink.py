######################################################################################
# Controls the ADLINK PCIe-9101 card
######################################################################################

import time

import inc.adlink.dask91xx as dask91xx


def wait(duration, get_now=time.perf_counter):
    now = get_now()
    end = now + duration
    while now < end:
        now = get_now()


class Adlink:
    def __init__(self):
        self.dask = dask91xx.Dask91xxLib()
        self.var_card = self.dask.Register_Card(52, 0)  # PCIe_9101 = 52, see dask91xx.py
        if self.var_card < 0:
            print(f"UD_Register_Card fail, error = {self.var_card}\n")
            exit()
        print("Register card successfully")

    def release_adlink(self):
        if self.var_card >= 0:
            self.dask.Release_Card(self.var_card)

        print("Card release")

    def set_chip_map(self, channel, chipmap):
        for column in range(16):
            for row in range(64):
                value = chipmap[row][column]
                self.set_chip_state(channel, row, column, value)

                # Cause the old chips have problems double check setting was successful
                while self.get_chip_state(channel, row, column) != value:
                    self.set_chip_state(channel, row, column, value)


    def set_chip_state(self, channel, row, column, value):
        channel <<= 13

        value <<= 10

        address = column
        address <<= 6
        address |= row

        wr = 0x0
        wr <<= 12
        dataToWrite = address | value | wr | channel

        self.dask.DO_WritePort(self.var_card, 0, dataToWrite)
        wait(0.00001)

        wr = 0x1
        wr <<= 12
        dataToWrite = address | value | wr | channel

        self.dask.DO_WritePort(self.var_card, 0, dataToWrite)
        wait(0.00001)


    def get_chip_map(self, channel, chipmap):
        for column in range(16):
            for row in range(64):
                chipmap[row][column] = self.get_chip_state(channel, row, column)

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

        self.dask.DO_WritePort(self.var_card, 0, dataToWrite)
        wait(0.00001)
        self.dask.DI_ReadPort(self.var_card, 0, dataRead)
        wait(0.00001)

        value = dataRead[0] >> 14

        return value

