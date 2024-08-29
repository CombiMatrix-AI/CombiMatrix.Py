######################################################################################
# Quick translation of digital adlink functions to python
# Needs work!!!
# Should eventually be folded into chip.py
######################################################################################

def SetChipMap(channel, map):
    row = 0
    column = 0
    status = 0
    address = 0x0
    value = 0
    wr = 0
    dataToWrite = 0x0000
    message = ""

    channel <<= 13

    for column in range(MAXIMUM_COLUMNS):
        for row in range(MAXIMUM_ROWS):
            value = map[MAXIMUM_COLUMNS * row + column]
            value <<= 10

            address = column
            address <<= 6
            address |= row

            wr = 0x0
            wr <<= 12
            dataToWrite = address | value | wr | channel
            if emulateChipHardware == 0:
                status = DO_WritePort(cardId, 0, dataToWrite)
                if chipHardwareDelay > 0:
                    Wait(chipHardwareDelay)

            else:
                address = (row * MAXIMUM_COLUMNS) + column
                emulatedChipMap[address] = map[address]

            wr = 0x1
            wr <<= 12
            dataToWrite = address | value | wr | channel

            if emulateChipHardware == 0:
                status = DO_WritePort(cardId, 0, dataToWrite)
                if chipHardwareDelay > 0:
                    Wait(chipHardwareDelay)

            dataToWrite = 0
            address = 0

    return status


def GetChipMap(channel, map):
    status = 0
    column = 0
    row = 0
    address = 0x0
    value = 0
    wr = 0x1
    dataToWrite = 0x0000
    dataRead = 0x0
    message = ""

    channel <<= 13
    value <<= 10
    wr <<= 12

    message = f"{TimeStr()} Reading chip map"
    AddToDebugOutput(message)

    for column in range(MAXIMUM_COLUMNS):
        for row in range(MAXIMUM_ROWS):
            address = column
            address <<= 6
            address += row

            dataToWrite = address | value | wr | channel

            if emulateChipHardware == 0:
                status = DO_WritePort(cardId, 0, dataToWrite)
                if chipHardwareDelay > 0:
                    Wait(chipHardwareDelay)
                status = DI_ReadPort(cardId, 0, dataRead)
                if chipHardwareDelay > 0:
                    Wait(chipHardwareDelay)

            else:
                address = (row * MAXIMUM_COLUMNS) + column
                dataRead = emulatedChipMap[address] << 14

            dataRead >>= 14
            map[MAXIMUM_COLUMNS * row + column] = dataRead

    return status


def SetChipState(channel, row, column, value):
    status = 0
    address = 0x0
    wr = 0
    dataToWrite = 0x0000
    message = ""

    channel <<= 13

    message = f"{TimeStr()} Setting chip state row {row} column {column} vline {value}"
    AddToDebugOutput(message)

    value <<= 10

    address = column
    address <<= 6
    address |= row

    wr = 0x0
    wr <<= 12
    dataToWrite = address | value | wr | channel
    if emulateChipHardware == 0:
        status = DO_WritePort(cardId, 0, dataToWrite)
        if chipHardwareDelay > 0:
            Wait(chipHardwareDelay)

    wr = 0x1
    wr <<= 12
    dataToWrite = address | value | wr | channel

    if emulateChipHardware == 0:
        status = DO_WritePort(cardId, 0, dataToWrite)
        if chipHardwareDelay > 0:
            Wait(chipHardwareDelay)

    dataToWrite = 0
    address = 0

    return status


def GetChipState(channel, row, column, value):
    status = 0
    address = 0x0
    wr = 0x1
    dataToWrite = 0x0000
    dataRead = 0x0
    message = ""

    channel <<= 13
    wr <<= 12


    address = column
    address <<= 6
    address += row

    dataToWrite = address | wr | channel

    if emulateChipHardware == 0:
        status = DO_WritePort(cardId, 0, dataToWrite)
        if chipHardwareDelay > 0:
            Wait(chipHardwareDelay)
        status = DI_ReadPort(cardId, 0, dataRead)
        if chipHardwareDelay > 0:
            Wait(chipHardwareDelay)

    dataRead >>= 14
    value = dataRead

    return status
