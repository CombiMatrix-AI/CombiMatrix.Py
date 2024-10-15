import json
import platform
import time
from configparser import ConfigParser
from pathlib import Path
from PyQt6.QtWidgets import QApplication
from grbl_streamer import GrblStreamer
from qt_material import apply_stylesheet

if platform.system() != 'Darwin':
    from utils.par import PAR
    from utils.adlink import Adlink
from utils.step import Block, Vcfg

ROOT_DIR = Path(__file__).parent / '..'

def config_init():
    # Correct path to the configuration file
    config_path = ROOT_DIR / 'config.ini'

    # Read the configuration file
    config = ConfigParser()
    if config_path.exists():
        config.read(config_path)
    else:
        print(f"Config file not found at: {config_path}")

    return config

def change_theme(theme):
    extra = {
        'font_family': 'Courier New',
    }

    config = config_init()
    config.set('General', 'theme', theme)
    with open(ROOT_DIR / 'config.ini', 'w') as configfile:
        config.write(configfile)
    apply_stylesheet(QApplication.instance(), theme=theme, extra=extra, css_file='view/stylesheet.css')

def init_adlink():
    adlink_card = Adlink()
    print("DEBUG MESSAGE: Adlink Card Initialized")
    return adlink_card

def init_par():
    config = config_init()
    kbio_port = config.get('Ports', 'par_port')
    par = PAR(kbio_port)
    print("DEBUG MESSAGE: EC-Lab PAR Initialized")
    return par

def init_robot():
    grbl = GrblStreamer(grbl_callback)
    grbl.setup_logging()
    config = config_init()
    grbl_port = config.get('Ports', 'robot_port')
    grbl.cnect(grbl_port, 115200)
    print("DEBUG MESSAGE: GRBL Connected")
    time.sleep(1)  # Let grbl connect
    grbl.killalarm()  # Turn off alarm on startup
    print("DEBUG MESSAGE: GRBL Alarm Turned off")
    return grbl

def grbl_callback(eventstring, *data):
    args = []
    for d in data:
        args.append(str(d))
    print("GRBL CALLBACK: event={} data={}".format(eventstring.ljust(30), ", ".join(args)))

def load_block_dict():
    blocks_dir = ROOT_DIR / 'blocks'
    blocks = {}

    for filename in blocks_dir.iterdir():
        if filename.suffix == ".block":  # Use your custom extension here
            with open(filename, 'r') as file:
                try:
                    data = json.load(file)
                    blocks[filename.stem] = Block(filename.stem, **data)  # Store the data in the list
                except json.JSONDecodeError:
                    print(f"Error decoding JSON from file: {filename}")
                except Exception as e:
                    print(f"Error processing file {filename}: {e}")

    return blocks

def load_vcfg_dict():
    vcfgs_dir = ROOT_DIR / 'vcfgs'
    vcfgs = {}

    for filename in vcfgs_dir.iterdir():
        if filename.suffix == ".vcfg":  # Use your custom extension here
            technique = filename.stem.rsplit('.', 1)[-1].upper()
            with open(filename, 'r') as file:
                try:
                    data = json.load(file)
                    vcfgs[filename.stem] = Vcfg(filename.stem, technique, data)  # Store the data in the list
                except json.JSONDecodeError:
                    print(f"Error decoding JSON from file: {filename}")
                except Exception as e:
                    print(f"Error processing file {filename}: {e}")

    return vcfgs

# The below variables should be set once in the launch process and not changed again
robot_enabled = False
par_enabled = False
counter_electrode = ''
working_electrode = ''
reference_electrode = ''

