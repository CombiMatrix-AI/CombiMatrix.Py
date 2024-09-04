""" Bio-Logic OEM package python API.

Script shown as an example of how to run an experiment with a Biologic instrument
using the EC-Lab OEM Package library.

The script uses parameters which are provided below.

"""

import os
import sys
import time

import inc.kbio.kbio_types as KBIO
from inc.kbio.kbio_api import KBIO_api
from inc.kbio.kbio_tech import ECC_parm
from inc.kbio.kbio_tech import get_experiment_data
from inc.kbio.kbio_tech import get_info_data
from inc.kbio.kbio_tech import make_ecc_parm
from inc.kbio.kbio_tech import make_ecc_parms
from inc.kbio.utils import exception_brief

# ------------------------------------------------------------------------------#

# Test parameters, to be adjusted

verbosity = 1

address = "USB0" # ethernet ex. "10.100.19.1"
channel = 0

binary_path = os.path.join(os.path.dirname(__file__), "lib", "kbio")
DLL_path = os.path.join(binary_path, "EClib64.dll")

force_load_firmware = True

# OCV parameter values
cv_tech_file = "cv.ecc"

duration = 10.0  # seconds
record_dt = 0.1  # seconds
e_range = "E_RANGE_10V"

# dictionary of OCV parameters (non exhaustive)

OCV_parms = {
    "duration": ECC_parm("Rest_time_T", float),
    "record_dt": ECC_parm("Record_every_dT", float),
    "record_dE": ECC_parm("Record_every_dE", float),
    "E_range": ECC_parm("E_Range", int),
    "timebase": ECC_parm("tb", int),
}

def newline():
    print()

"""

Example main :

  * open the DLL,
  * connect to the device using its address,
  * retrieve the device channel info,
  * test whether the proper firmware is running,
  * create an OCV parameter list (a subset of all possible parameters),
  * load the OCV technique into the channel,
  * start the technique,
  * in a loop :
      * retrieve and display experiment data,
      * stop when channel reports it is no longer running

Note: for each call to the DLL, the base API function is shown in a comment.

"""

try:
    newline()

    # API initialize
    api = KBIO_api(DLL_path)

    # BL_GetLibVersion
    version = api.GetLibVersion()
    print(f"> EcLib version: {version}")
    newline()

    # BL_Connect
    id_, device_info = api.Connect(address)
    print(f"> device[{address}] info :")
    print(device_info)
    newline()

    # based on board_type, determine firmware filenames
    board_type = api.GetChannelBoardType(id_, channel)
    firmware_path = "kernel.bin"
    fpga_path = "Vmp_ii_0437_a6.xlx"

    # Load firmware
    print(f"> Loading {firmware_path} ...")
    # create a map from channel set
    channel_map = api.channel_map({channel})
    # BL_LoadFirmware
    api.LoadFirmware(id_, channel_map, firmware=firmware_path, fpga=fpga_path, force=force_load_firmware)
    print("> ... firmware loaded")
    newline()

    # BL_GetChannelInfos
    channel_info = api.GetChannelInfo(id_, channel)
    print(f"> Channel {channel} info :")
    print(channel_info)
    newline()

    if not channel_info.is_kernel_loaded:
        print("> kernel must be loaded in order to run the experiment")
        sys.exit(-1)


    tech_file = cv_tech_file

    # BL_Define<xxx>Parameter
    p_duration = make_ecc_parm(api, OCV_parms["duration"], duration)
    p_record = make_ecc_parm(api, OCV_parms["record_dt"], record_dt)
    p_erange = make_ecc_parm(api, OCV_parms["E_range"], KBIO.E_RANGE[e_range].value)
    ecc_parms = make_ecc_parms(api, p_duration, p_record, p_erange)

    # BL_LoadTechnique
    api.LoadTechnique(id_, channel, tech_file, ecc_parms, first=True, last=True, display=(verbosity > 1))

    # BL_StartChannel
    api.StartChannel(id_, channel)

    # experiment loop
    csvfile = open("cv.csv", "w")
    csvfile.write("t (s),I (A)\n")
    count = 0
    print("> Reading data ", end="", flush=True)
    while True:
        # BL_GetData
        data = api.GetData(id_, channel)
        status, tech_name = get_info_data(api, data)
        print(".", end="", flush=True)

        for output in get_experiment_data(api, data, tech_name, board_type):
            csvfile.write(f"{output['t']},{output['I']}\n")
            csvfile.flush()
            count += 1

        if status == "STOP":
            break

        time.sleep(1)

    csvfile.close()
    print()
    print(f"> {count} data have been written into cv.csv")
    print("> experiment done")
    newline()

    # BL_Disconnect
    api.Disconnect(id_)

except KeyboardInterrupt:
    print(".. interrupted")

except Exception as e:
    print(exception_brief(e, verbosity >= 1))

# ==============================================================================#
