from pathlib import Path
import serial
import re
import time

# Constants
RX_BUFFER_SIZE = 128
BAUD_RATE = 115200
ENABLE_STATUS_REPORTS = True
REPORT_INTERVAL = 1.0  # seconds
is_run = True  # Controls query timer

device_port = "COM3"

# Used to find port device information - deletable
import serial.tools.list_ports
ports = serial.tools.list_ports.comports()
for port in ports:
    print(f"Device: {port.device}, Description: {port.description}, HWID: {port.hwid}")


def initialize_serial(stream):
    s = serial.Serial(stream.device, BAUD_RATE)
    with open(stream.gcode, 'r') as f:
        
        # Wake up grbl
        print("Initializing Grbl...")
        # Two newlines wakes up machine
        s.write(b"\r\n\r\n")

        # Wait for grbl to initialize and flush startup text in serial input
        time.sleep(2)
        s.flushInput()
    return s , f


def enable_check(s, stream):
    print("Enabling Grbl Check-Mode: SND: [$C]", end='')
    s.write(b"$C\n")
    while True:
        grbl_out = s.readline().strip().decode()  # Wait for grbl response with carriage return
        if grbl_out.find('error') >= 0:
            print("REC:", grbl_out)
            print(" Failed to set Grbl check-mode. Aborting...")
            quit()
        elif grbl_out.find('ok') >= 0:
            if stream.stream.verbose:
                print('REC:', grbl_out)
            break
    return


def enable_setting( s , f , stream):
    print("SETTINGS MODE: Streaming", stream.gcode, "to", stream.device)
    for line in f:
        l_count += 1  # Iterate line counter
        l_block = line.strip()  # Strip all EOL characters for consistency
        if stream.stream.verbose:
            print("SND>" + str(l_count) + ": \"" + l_block + "\"")
        s.write((l_block + '\n').encode())  # Send g-code block to grbl
        while True:
            grbl_out = s.readline().strip().decode()  # Wait for grbl response with carriage return
            if grbl_out.find('ok') >= 0:
                if stream.stream.verbose:
                    print(" REC<" + str(l_count) + ": \"" + grbl_out + "\"")
                break
            elif grbl_out.find('error') >= 0:
                if stream.stream.verbose:
                    print(" REC<" + str(l_count) + ": \"" + grbl_out + "\"")
                error_count += 1
                break
            else:
                print(" MSG: \"" + grbl_out + "\"")
'''
Func:   stream_gcode

Desc:   Streams specified gcode to COM3 port

Params:
        gcode_file:     G code file that will be parsed and fed to robot via the COM3 port.
        device_file:    Device/port where the code is being fed, default is COM3.
        quiet:          Determines whether the code will output more prints.
        settings:       Determines whether settings will be fed to the port rather than normal G code.
        check:          Determines whether check mode is activated.


'''
def stream_gcode(gcode_file, device_file=device_port, quiet=True, settings=False, check=False):
    # Globalize variable so that all threads can clearly communicate about the state and use of the periodic timer
    global is_run

    stream = StreamInfo(gcode_file, device_file , quiet , settings, check)

    s = serial.Serial(stream.device, BAUD_RATE)
    with open(stream.gcode, 'r') as f:
        
        # Wake up grbl
        print("Initializing Grbl...")
        # Two newlines wakes up machine
        s.write(b"\r\n\r\n")

        # Wait for grbl to initialize and flush startup text in serial input
        time.sleep(2)
        s.flushInput()
        if stream.check:
            enable_check(s, stream)

        start_time = time.time()

        # if stream.setting:
        #     enable_setting(s, f, stream)

        # Stream g-code to grbl
        l_count = 0
        error_count = 0

        g_count = 0
        c_line = []
        for line in f:
            l_count += 1  # Iterate line counter
            l_block = re.sub(r'\s|\(.*?\)', '', line).upper()  # Strip comments/spaces/new line and capitalize
            c_line.append(len(l_block) + 1)  # Track number of characters in grbl serial read buffer
            grbl_out = ''
            while sum(c_line) >= RX_BUFFER_SIZE - 1 or s.inWaiting():
                out_temp = s.readline().strip().decode()  # Wait for grbl response
                if out_temp.find('ok') < 0 and out_temp.find('error') < 0:
                    print(" MSG: \"" + out_temp + "\"")  # Debug response
                else:
                    if out_temp.find('error') >= 0:
                        error_count += 1
                    g_count += 1  # Iterate g-code counter
                    if stream.verbose:
                        print(" REC<" + str(g_count) + ": \"" + out_temp + "\"")
                    del c_line[0]  # Delete the block character count corresponding to the last 'ok'
            s.write((l_block + '\n').encode())  # Send g-code block to grbl
            if stream.verbose:
                print("SND>" + str(l_count) + ": \"" + l_block + "\"")

        # Wait until all responses have been received.
        while l_count > g_count:
            out_temp = s.readline().strip().decode()  # Wait for grbl response
            if out_temp.find('ok') < 0 and out_temp.find('error') < 0:
                print(" MSG: \"" + out_temp + "\"")  # Debug response
            else:
                if out_temp.find('error') >= 0:
                    error_count += 1
                g_count += 1  # Iterate g-code counter
                del c_line[0]  # Delete the block character count corresponding to the last 'ok'
                if stream.verbose:
                    print(" REC<" + str(g_count) + ": \"" + out_temp + "\"")

        # Ensure all commands are processed before closing
        while s.inWaiting():
            print("Waiting for remaining responses...")
            out_temp = s.readline().strip().decode()
            if out_temp:
                print(" MSG: \"" + out_temp + "\"")

        # Wait for user input after streaming is completed
            print("\nG-code streaming finished!")
            end_time = time.time()
            is_run = False
            print(" Time elapsed: ", end_time - start_time, "\n")

            if stream.check:
                if error_count > 0:
                    print("CHECK FAILED:", error_count, "errors found! See output for details.\n")
                else:
                    print("CHECK PASSED: No errors found in g-code program.\n")
            else:
                print("WARNING: Wait until Grbl completes buffered g-code blocks before exiting.")
                input(" Press Enter to exit and disable Grbl.")

        # Close file and serial port
        s.close()

def generate_file_paths():
    # Define the rows and columns
    rows = 'ABCDEFGH'
    columns = range(1, 13)
    
    # Initialize an empty dictionary to store the file paths
    file_paths = {}
    
    # Populate the dictionary
    for row in rows:
        for column in columns:
            key = f"{row}{column}"
            value = Path(__file__).parents[0] / "gcode_files" / f"{key}.gcode"
            file_paths[key] = value
    
    return file_paths

# Example usage
file_paths_dict = generate_file_paths()
print(file_paths_dict)

def run_stream(position, sleep_time=10, com_port="COM3"):
    # Get file paths 
    file_dict = generate_file_paths()
    print("Position: ", position)
    file_path = file_dict[position]
    print(file_path)
    stream_gcode(file_path , com_port, True)
    # in the case that the user would just like to remain in the same position
    # until instructed otherwise
    if sleep_time is not None:
        time.sleep(sleep_time)
        stream_gcode(Path(__file__).parents[0] / "gcode_files" / "return.gcode", com_port, False)
    return 0

def main():
    stream_gcode('gcode_files/A1.gcode', 'COM3', quiet=False)

class StreamInfo:

    def __init__(self, gcode_file, device_file, quiet, settings, check):
        self.gcode = gcode_file
        self.device = device_file
        self.quiet = quiet
        self.setting = settings
        self.check = check
        self.verbose = not quiet


if __name__ == "__main__":
    main()

