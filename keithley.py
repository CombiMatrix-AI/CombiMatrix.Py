######################################################################################
# Controls the Keithley 8465
######################################################################################

import pyvisa
import time
import matplotlib.pyplot as plt


def startup_keithley():
    # Open a GPIB connection to the Keithley 6485
    return pyvisa.ResourceManager().open_resource('GPIB0::14::INSTR')

def zero_keithley(keithley):
    keithley.write('*RST')  # Return 6485 to RST defaults.
    keithley.write('SYST:ZCH ON')  # Enable zero check.
    keithley.write('CURR:RANG 2e-9')  # Select the 2nA range.
    keithley.write('INIT')  # Trigger reading to be used as zero correction.

    keithley.write('SYST:ZCOR:ACQ')  # Use last reading taken as zero correct value

    keithley.write('SYST:ZCOR ON')  # Perform zero correction
    keithley.write('CURR:RANG:AUTO ON')  # Auto range
    keithley.write('SYST:ZCH OFF')  # disable zero check

def run_keithley(keithley):
    measurements = []
    timestamps = []

    start_time = time.time()
    while time.time() - start_time < 30:
        # Read the output
        measurement = keithley.query('READ?').split(',')[0]
        measurements.append(float(measurement))
        timestamps.append(time.time() - start_time)
        time.sleep(0.25)  # Adjust the sleep time as necessary

    # Plot the measurements
    plt.plot(timestamps, measurements)
    plt.xlabel('Time (seconds)')
    plt.ylabel('Current (amps)')
    plt.title('Current Response')
    plt.show()


def close_keithley(keithley):
    # Close the connection
    keithley.close()
