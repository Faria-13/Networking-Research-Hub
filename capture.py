import os
import subprocess

def list_interfaces():
    """Lists network interfaces using tcpdump -D command"""
    try:
        result = subprocess.run(['tcpdump', '-D'], capture_output=True, text=True)
        if result.returncode != 0:
            print("Error fetching interfaces")
            return []
        
        # Parse and display interfaces
        interfaces = []
        for line in result.stdout.splitlines():
            parts = line.split(".")
            if len(parts) > 1:
                interfaces.append(parts[1].strip())
        return interfaces

    except Exception as e:
        print(f"Error: {e}")
        print("OOPS")
        return []

import subprocess

def capture_traffic(interface, output_file, num_of_packets):
    try:
        print(f"Capturing traffic on {interface}... Press Ctrl+C to stop.")
        
        # Split the interface string to handle multiple words if necessary
        interface = interface.split()
        
        # Define the tcpdump capture command
        capture_command = ['sudo', 'tcpdump', '-xx', '-tttt', '-i', interface[0], '-c', str(num_of_packets)]
        
        # Open the output file in write mode to save the tcpdump output
        with open(output_file, 'w') as file:
            # Start the tcpdump process and redirect stdout to the file
            process = subprocess.Popen(capture_command, stdout=file, stderr=subprocess.PIPE)
            
            try:
                # Wait for the process to finish or until keyboard interrupt (Ctrl+C)
                process.wait()
            except KeyboardInterrupt:
                print("\nCapture stopped.")
                process.terminate()
        
        print(f"Output saved to {output_file}.")
    
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
# capture_traffic('eth0', 'captured_output.txt', '10')


def main():
    print("Listing available network interfaces...\n")
    interfaces = list_interfaces()
    
    if not interfaces:
        print("No interfaces found or an error occurred.")
        return
    
    # Display options to the user
    for index, iface in enumerate(interfaces):
        print(f"{index + 1}: {iface}")
    
    try:
        
        choice = int(input("\nEnter the number of the interface to capture on: ")) - 1
        if choice < 0 or choice >= len(interfaces):
            print("Invalid choice. Exiting.")
            return
        
        # Ask the user for the output filename
        # output_file = input("Enter the name of the output file (e.g., foobar.txt): ")
        output_file = 'foobar.txt'
        if not output_file:
            print("Invalid file name. Exiting.")
            return

        num_of_packets = input ("How many packets do you want captured?")

        # function call
        capture_traffic(interfaces[choice], output_file, num_of_packets)

    except ValueError:
        print("Invalid input. Please enter a valid number.")
    except Exception as e:
        print(f"An error occurred: {e}")


