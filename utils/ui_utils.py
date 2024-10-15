import json
from configparser import ConfigParser
from pathlib import Path
from PyQt6.QtWidgets import QApplication
from qt_material import apply_stylesheet

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
PAR_ENABLED = False
def get_par_enabled():
    return PAR_ENABLED

def set_par_enabled(value):
    global PAR_ENABLED
    PAR_ENABLED = value

ROBOT_ENABLED = False
def get_robot_enabled():
    return ROBOT_ENABLED

def set_robot_enabled(value):
    global ROBOT_ENABLED
    ROBOT_ENABLED = value

COUNTER_ELECTRODE = ""
def get_counter_electrode():
    return COUNTER_ELECTRODE

def set_counter_electrode(value):
    global COUNTER_ELECTRODE
    COUNTER_ELECTRODE = value

REFERENCE_ELECTRODE = ""
def get_reference_electrode():
    return REFERENCE_ELECTRODE

def set_reference_electrode(value):
    global REFERENCE_ELECTRODE
    REFERENCE_ELECTRODE = value

WORKING_ELECTRODE = ""
def get_working_electrode():
    return WORKING_ELECTRODE

def set_working_electrode(value):
    global WORKING_ELECTRODE
    WORKING_ELECTRODE = value
