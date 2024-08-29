######################################################################################
# Controls the Keithley 8465
######################################################################################

import pyvisa
import time
import matplotlib.pyplot as plt

class Keithley:
    def __init__(self):
        self.keithley = pyvisa.ResourceManager().open_resource('GPIB0::14::INSTR')

    def zero_keithley(self):
        self.keithley.write('*RST')  # Return 6485 to RST defaults.
        self.keithley.write('SYST:ZCH ON')  # Enable zero check.
        self.keithley.write('CURR:RANG 2e-9')  # Select the 2nA range.
        self.keithley.write('INIT')  # Trigger reading to be used as zero correction.

        self.keithley.write('SYST:ZCOR:ACQ')  # Use last reading taken as zero correct value

        self.keithley.write('SYST:ZCOR ON')  # Perform zero correction
        self.keithley.write('CURR:RANG:AUTO ON')  # Auto range
        self.keithley.write('SYST:ZCH OFF')  # disable zero check

    def run_keithley(self):
        measurements = []
        timestamps = []

        start_time = time.time()
        while time.time() - start_time < 30: # TODO: MAKE it read for entire experiment
            # Read the output
            measurement = self.keithley.query('READ?').split(',')[0][1:-1]
            measurements.append(float(measurement))
            timestamps.append(time.time() - start_time)
            time.sleep(0.25)  # Adjust the sleep time as necessary

        # Plot the measurements
        plt.plot(timestamps, measurements)
        plt.xlabel('Time (seconds)')
        plt.ylabel('Current (amps)')
        plt.title('Current Response')
        plt.show()


    def close_keithley(self):
        # Close the connection
        self.keithley.close()
