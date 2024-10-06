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

# def capture_traffic(interface, output_file):
#     """Runs tcpdump on the selected interface and writes the output to a file"""
#     try:
#         print(f"Capturing traffic on {interface}... Press Ctrl+C to stop.")
#         interface = interface.split()
#         with open(output_file, 'w') as file:
#             process = subprocess.Popen(['sudo', 'tshark', '-i', interface[0], '-x', '-t', 'a'], stdout=file, stderr=subprocess.PIPE)
#             process.wait()
#     except KeyboardInterrupt:
#         print("\nCapture stopped.")
#         process.terminate()

def capture_traffic(interface, output_file):
    """Captures traffic on the selected interface and writes the output to a file."""
    pcap_file = 'capture.pcap'  # Temporary PCAP file name
    try:
        print(f"Capturing traffic on {interface}... Press Ctrl+C to stop.")
        
        # Step 1: Capture traffic into a PCAP file
        interface = interface.split()
        capture_command = ['sudo', 'tshark', '-i', interface[0], '-t', 'a', '-w', pcap_file]
        
        # Start capturing packets
        process = subprocess.Popen(capture_command, stderr=subprocess.PIPE)
        try:
            process.wait()  # Wait for the process to complete
        except KeyboardInterrupt:
            print("\nCapture stopped.")
            process.terminate()
        
        # Step 2: Read the captured PCAP file and write to the output text file
        with open(output_file, 'w') as file:
            tshark_read_command = ['tshark', '-r', pcap_file, '-x', '-t', 'a']
            tshark_process = subprocess.Popen(tshark_read_command, stdout=file, stderr=subprocess.PIPE)
            tshark_process.communicate()  # Wait for TShark to finish
        
        print(f"Output saved to {output_file}.")
    
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Cleanup: Remove the temporary PCAP file if it exists
        if subprocess.call(['rm', '-f', pcap_file]) != 0:
            print("Failed to remove the temporary PCAP file.")

def main():
    print("Listing available network interfaces...\n")
    interfaces = list_interfaces()
    
    if not interfaces:
        print("No interfaces found or an error occurred.")
        return
    
    # Display options to the user
    for idx, iface in enumerate(interfaces):
        print(f"{idx + 1}: {iface}")
    
    try:
        # Ask the user to choose an interface
        choice = int(input("\nEnter the number of the interface to capture on: ")) - 1
        if choice < 0 or choice >= len(interfaces):
            print("Invalid choice. Exiting.")
            return
        
        # Ask the user for the output filename
        output_file = input("Enter the name of the output file (e.g., capture.txt): ")
        if not output_file:
            print("Invalid file name. Exiting.")
            return

        # Run the capture
        capture_traffic(interfaces[choice], output_file)

    except ValueError:
        print("Invalid input. Please enter a valid number.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
