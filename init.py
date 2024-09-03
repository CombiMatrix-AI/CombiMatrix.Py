import ke6485
import pcie9101
import block
import chipmap

# Holds important program variables
keithley = ke6485.Keithley()
adlink = pcie9101.Adlink()

blocks = block.Block.from_blocks_folder()
chipmap = chipmap.ChipMap()