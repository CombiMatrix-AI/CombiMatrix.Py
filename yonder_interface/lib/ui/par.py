import sys
import time
import matplotlib.pyplot as plt
import pandas as pd

from ..kbio.kbio_api import KBIO_api
from ..kbio.kbio_tech import ECC_parm
from ..kbio.kbio_tech import get_experiment_data
from ..kbio.kbio_tech import get_info_data
from ..kbio.kbio_tech import make_ecc_parm
from ..kbio.kbio_tech import make_ecc_parms
from . import ROOT_DIR


class PAR:
    def __init__(self, address):
        self.api = KBIO_api(str(ROOT_DIR / 'resources' / 'kbio' / 'EClib64.dll'))  # Init self.api
        self.channel = 4 # TODO: GENERALIZE LATER

        self.id, device_info = self.api.Connect(address)   # BL_Connect
        print(f"> device[{address}] info :")
        print(device_info)

        plugged_channels = list(self.api.PluggedChannels(self.id))
        print("> Plugged channels ...")
        print(plugged_channels)

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

    def create_parameters(self, configs):
        # Convert to dictionary and iterate through key-value pairs
        parameter_steps = list()
        for key, value in configs.items():
            if isinstance(value, list):
                for i in range(len(value)):
                    parameter = make_ecc_parm(self.api, ECC_parm(key, type(value[i])), value[i], i)
                    parameter_steps.append(parameter)
                    print(f"{key}, {i}: {value[i]}")
            else:
                parameter = make_ecc_parm(self.api, ECC_parm(key, type(value)), value)
                parameter_steps.append(parameter)
                print(f"{key}: {value}")

        ecc_parms = make_ecc_parms(self.api, *parameter_steps)
        return ecc_parms

    def cyclic_voltammetry(self, cv, index): #TODO: GENERALIZE
        vs_init = [False, False, False, False, False] # TODO: fix CV data object = cv.vs_init
        v_step = [0.0, 1.3, 0.0, 0.0, 0.6] # TODO: fix CV data object = cv.v_step
        scan_rate = [200, 200, 200, 200, 200] ## TODO: fix CV data object =  cv.scan_rate
        scan_number = 2 # constant according to manual, can change later
        record_de = 0.001 # TODO: fix CV data object = cv.record_de
        average_de = True # TODO: fix CV data object = cv.average_de
        n_cycles = 10 # TODO: fix CV data object = cv.n_cycles
        begin_i = 0.98 # TODO: fix CV data object = cv.begin_i
        end_i = 1 # TODO: fix CV data object = cv.end_i

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

        # experiment loop
        filename = "cv" + str(index)
        output_path = ROOT_DIR / 'data' / 'outputs' / f"{filename}.csv"

        csvfile = open(output_path, "w")
        csvfile.write("t (s),Ece (V),Iwe (A),Ewe (V),cycle\n")
        count = 0
        print("Reading data")
        while True:
            # BL_GetData
            data = self.api.GetData(self.id, self.channel)
            status, tech_name = get_info_data(self.api, data)
            print(".")

            for output in get_experiment_data(self.api, data, tech_name, self.board_type):
                csvfile.write(f"{output['t']},{output['Ece']},{output['Iwe']},{output['Ewe']},{output['cycle']}\n")
                count += 1

            if status == "STOP":
                break

            time.sleep(1)

        # pop open a matplotlib window with the Iwe against the Ewe
        try:
            df = pd.read_csv(output_path)
            plt.plot(df['Ewe (V)'], df['Iwe (A)'])
            plt.xlabel('Ewe (V)')
            plt.ylabel('Iwe (A)')
            plt.show()
        except (pd.errors.EmptyDataError, ValueError):
            print("No data found")

        csvfile.close()
        print()
        print(f"> {count} data points have been written into {filename}.csv")
        print("> experiment done")

    def release_kbio(self):
        self.api.Disconnect(self.id)        # BL_Disconnect
        