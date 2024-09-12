import os
import sys
import time

from inc.kbio.kbio_api import KBIO_api
from inc.kbio.kbio_tech import ECC_parm
from inc.kbio.kbio_tech import get_experiment_data
from inc.kbio.kbio_tech import get_info_data
from inc.kbio.kbio_tech import make_ecc_parm
from inc.kbio.kbio_tech import make_ecc_parms

class KBio:
    def __init__(self, address):
        self.api = KBIO_api(os.path.join(os.path.dirname(__file__), "lib", "kbio", "EClib64.dll"))  # Init self.api
        self.channel = 5 # TODO: GENERALIZE LATER

        self.id, device_info = self.api.Connect(address)   # BL_Connect
        print(f"> device[{address}] info :")
        print(device_info)

        self.board_type = self.api.GetChannelBoardType(self.id, self.channel)

        print("> Loading firmware ...")         # Load firmware
        channel_map = self.api.channel_map({self.channel})        # create a map from channel set
        self.api.LoadFirmware(self.id, channel_map, firmware="kernel.bin", fpga="Vmp_ii_0437_a6.xlx", force=True) # BL_LoadFirmware
        print("> ... firmware loaded")

        # BL_GetChannelInfos
        channel_info = self.api.GetChannelInfo(self.id, self.channel)
        print(f"> Channel {self.channel} info :")
        print(channel_info)

        if not channel_info.is_kernel_loaded:
            print("> kernel must be loaded in order to run the experiment")
            sys.exit(-1)

    def cyclic_voltammetry(self, cv, index):
        vs_init = cv.vs_init
        v_step = cv.v_step
        scan_rate = cv.scan_rate
        scan_number = 2 # constant according to manual, can change later
        record_de = cv.record_de
        average_de = cv.average_de
        n_cycles = cv.n_cycles
        begin_i = cv.begin_i
        end_i = cv.end_i

        cv_parms = {
            "vs_initial": ECC_parm("vs_initial", bool),
            "Voltage_step": ECC_parm("Voltage_step", float),
            "Scan_Rate": ECC_parm("Scan_Rate", float),
            "Scan_number": ECC_parm("Scan_number", int),
            "Record_every_dE": ECC_parm("Record_every_dE", float),
            "Average_over_dE": ECC_parm("Average_over_dE", bool),
            "N_Cycles": ECC_parm("N_Cycles", int),
            "Begin_measuring_I": ECC_parm("Begin_measuring_I", float),
            "End_measuring_I": ECC_parm("End_measuring_I", float),
        }

        p_steps = list()         # BL_Define<xxx>Parameter

        for i in range(5):
            parm = make_ecc_parm(self.api, cv_parms["vs_initial"], vs_init[i], i)
            p_steps.append(parm)
            parm = make_ecc_parm(self.api, cv_parms["Voltage_step"], v_step[i], i)
            p_steps.append(parm)
            parm = make_ecc_parm(self.api, cv_parms["Scan_Rate"], scan_rate[i], i)
            p_steps.append(parm)

        p_scan_num = make_ecc_parm(self.api, cv_parms["Scan_number"], scan_number)
        p_record = make_ecc_parm(self.api, cv_parms["Record_every_dE"], record_de)
        p_average = make_ecc_parm(self.api, cv_parms["Average_over_dE"], average_de)
        p_cycles = make_ecc_parm(self.api, cv_parms["N_Cycles"], n_cycles)
        p_begin = make_ecc_parm(self.api, cv_parms["Begin_measuring_I"], begin_i)
        p_end = make_ecc_parm(self.api, cv_parms["End_measuring_I"], end_i)
        ecc_parms = make_ecc_parms(self.api, *p_steps, p_scan_num,
                                   p_record, p_average, p_cycles, p_begin, p_end)

        self.api.LoadTechnique(self.id, self.channel, "cv.ecc", ecc_parms, first=True, last=True, display=False)

        self.api.StartChannel(self.id, self.channel)

        # experiment loop # TODO: FIX PRINTING
        filename = "cv" + index
        csvfile = open(f"{filename}.csv", "w")
        csvfile.write("t (s),I (A)\n")
        count = 0
        print("Reading data")
        while True:
            # BL_GetData
            data = self.api.GetData(self.id, self.channel)
            status, tech_name = get_info_data(self.api, data)
            print(".")

            for output in get_experiment_data(self.api, data, tech_name, self.board_type):
                csvfile.write(f"{output}")
                count += 1

            if status == "STOP":
                break

            time.sleep(1)

        csvfile.close()
        print()
        print(f"> {count} data have been written into {filename}.csv")
        print("> experiment done")

    def release_kbio(self):
        self.api.Disconnect(self.id)        # BL_Disconnect
        