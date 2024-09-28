import configparser
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

CONFIG = configparser.ConfigParser()
CONFIG.read("config.ini")


# The below variables should be set once in the launch process and not changed again
PAR_ENABLED = False
def GET_PAR_ENABLED():
    return PAR_ENABLED

def SET_PAR_ENABLED(value):
    global PAR_ENABLED
    PAR_ENABLED = value

ROBOT_ENABLED = False
def GET_ROBOT_ENABLED():
    return ROBOT_ENABLED

def SET_ROBOT_ENABLED(value):
    global ROBOT_ENABLED
    ROBOT_ENABLED = value

COUNTER_ELECTRODE = ""
def GET_COUNTER_ELECTRODE():
    return COUNTER_ELECTRODE

def SET_COUNTER_ELECTRODE(value):
    global COUNTER_ELECTRODE
    COUNTER_ELECTRODE = value

REFERENCE_ELECTRODE = ""
def GET_REFERENCE_ELECTRODE():
    return REFERENCE_ELECTRODE

def SET_REFERENCE_ELECTRODE(value):
    global REFERENCE_ELECTRODE
    REFERENCE_ELECTRODE = value

WORKING_ELECTRODE = ""
def GET_WORKING_ELECTRODE():
    return WORKING_ELECTRODE

def SET_WORKING_ELECTRODE(value):
    global WORKING_ELECTRODE
    WORKING_ELECTRODE = value
