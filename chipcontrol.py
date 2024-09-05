######################################################################################
# Controls the ADLINK PCIe-9101 card
######################################################################################

import time
import random

import inc.adlink.dask91xx as dask91xx

class Adlink:
    def __init__(self):
        self.dask = dask91xx.Dask91xxLib()
        self.var_card = self.dask.Register_Card(52, 0)  # PCIe_9101 = 52, see dask91xx.py
        if self.var_card < 0:
            print(f"UD_Register_Card fail, error = {self.var_card}\n")
            exit()
        print("Register card successfully")

    def exit_clear(self):
        if self.var_card >= 0:
            self.dask.Release_Card(self.var_card)

        print("card release")

    def set_chip_map(self, channel, chipmap):
        for column in range(16):
            for row in range(64):
                value = chipmap[row][column]
                status = self.set_chip_state(channel, row, column, value)

                # Cause the old chips have problems double check setting was successful
                while self.get_chip_state(channel, row, column) != value:
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
        self.wait(0.00001)

        wr = 0x1
        wr <<= 12
        dataToWrite = address | value | wr | channel

        status = self.dask.DO_WritePort(self.var_card, 0, dataToWrite)
        self.wait(0.00001)

        return status

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

        status = self.dask.DO_WritePort(self.var_card, 0, dataToWrite)
        self.wait(0.00001)
        status = self.dask.DI_ReadPort(self.var_card, 0, dataRead)
        self.wait(0.00001)

        out = dataRead[0] >> 14

        return out

    def wait(self, duration, get_now=time.perf_counter):
        now = get_now()
        end = now + duration
        while now < end:
            now = get_now()

    def chip_test(self, channel):
        for i in range(7):
            if i == 0:
                chipmap_in = [[0] * 16 for _ in range(64)]
            elif i == 1:
                chipmap_in = [[1] * 16 for _ in range(64)]
            elif i == 2:
                chipmap_in = [[2] * 16 for _ in range(64)]
            elif i == 3:
                chipmap_in = [[3] * 16 for _ in range(64)]
            elif i == 4:
                chipmap_in = [[1 if (r + c) % 2 == 0 else 2 for c in range(16)] for r in range(64)]
            elif i == 5:
                chipmap_in = [[2 if (r + c) % 2 == 0 else 3 for c in range(16)] for r in range(64)]
            elif i == 6:
                chipmap_in = [[random.randint(0, 3) for _ in range(16)] for _ in range(64)]
            else: # Handle out of bounds cases
                break

            chipmap_out = [[0] * 16 for _ in range(64)]

            self.set_chip_map(channel, chipmap_in)
            self.get_chip_map(channel, chipmap_out)

            if chipmap_in == chipmap_out:
                print(f"Test {i} Passed")
            else:
                print(f"Test {i} Failed")
                differences = [
                    (r, c, chipmap_in[r][c], chipmap_out[r][c])
                    for r in range(len(chipmap_in))
                    for c in range(len(chipmap_in[r]))
                    if chipmap_in[r][c] != chipmap_out[r][c]
                ]
                # Print differences
                for row, col, value1, value2 in differences:
                    print(f"Row {row}, Col {col}: chipmap_in has {value1}, chipmap_out has {value2}")
