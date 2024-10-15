from configparser import ConfigParser
from pathlib import Path

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
