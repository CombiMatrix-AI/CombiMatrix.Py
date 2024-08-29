import pyvisa
import configparser


def main():
    print("Begin")

    config = configparser.ConfigParser()
    config.read('config.ini')

    # Access values from the configuration file
    keithley_port = config.get('General', 'keithley_port')

    # Open a GPIB connection to the Keithley 6485
    keithley = pyvisa.ResourceManager().open_resource(keithley_port)

    keithley.write('*RST') #Return 6485 to RST defaults.
    keithley.write('SYST:ZCH ON') #Enable zero check.
    keithley.write('CURR:RANG 2e-9') #Select the 2nA range.
    keithley.write('INIT') #Trigger reading to be used as zero correction.
    
    keithley.write('SYST:ZCOR:ACQ') # Use last reading taken as zero correct value
    
    keithley.write('SYST:ZCOR ON') #Perform zero correction
    keithley.write('CURR:RANG:AUTO ON') #Auto range
    keithley.write('SYST:ZCH OFF') #disable zero check


    # Read the output
    measurement = keithley.query('READ?')

    # Print the measurement
    print(measurement)

    # Close the connection
    keithley.close()

if __name__ == "__main__":
    main()
