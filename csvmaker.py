import csv
from datetime import datetime
import time

# Protocol number to name mapping
PROTOCOLS = {
    1: "ICMP",
    6: "TCP",
    17: "UDP"
}

def extract_packet_info(packet_hex):
    ethernet_header_length = 14 * 2  # 14 bytes, each byte is 2 hex characters

    # IP header starts at byte 14 (i.e., at hex index 28)
    ip_header_start = ethernet_header_length 

    # Total length field in the IP header (2 bytes, 4 hex digits)
    total_length_hex = packet_hex[ip_header_start + 4:ip_header_start + 8]
    total_length = int(total_length_hex, 16)  # Convert hex string to integer

    # Protocol field (1 byte, 2 hex digits) is at byte 9 of the IP header
    protocol_hex = packet_hex[ip_header_start + 18:ip_header_start + 20]
    protocol = int(protocol_hex, 16)  # Convert hex string to integer (protocol number)

    # Convert protocol number to protocol name
    protocol_name = PROTOCOLS.get(protocol, "Unknown")

    return protocol_name, total_length

def parse_packets(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        csv_writer = csv.writer(outfile)
        csv_writer.writerow(['timestamp', 'epoch time', 'delta since last frame','protocol name', 'source port', 'packet size'])
        lines = infile.readlines()
        last_timestamp = None
        last_epoch = None

        for i in range(0, len(lines), 2):
            timestamp = lines[i].strip()  # First line is the timestamp
            packet_hex = lines[i + 1].strip()  # Second line is the hex data

            #timestamp 
            timestamp_without_microseconds, milliseconds, microseconds = timestamp.split(',') 
            current_date = datetime.now().strftime('%Y-%m-%d')      # if i dont do this, the calculation starts at 2000

            # Combine the current date with the timestamp time part
            full_timestamp = f"{current_date} {timestamp_without_microseconds}"    
            time_struct = time.strptime(full_timestamp, '%Y-%m-%d %H:%M:%S')
            #print(time_struct)
            epoch_time = time.mktime(time_struct) + int(milliseconds)/1000 + int(microseconds)/1000000

            #delta calculation
            if last_epoch is not None:
                delta = epoch_time - last_epoch
            else:
                delta = 0  # First frame, no previous delta

            # Extract protocol and size from the packet hex string
            protocol, packet_size = extract_packet_info(packet_hex)
            
            
            #source port shenanigan
            source_port_hex = packet_hex[68:72]
            source_port = int(source_port_hex, 16)

            csv_writer.writerow([timestamp, epoch_time, delta, protocol, source_port, packet_size])
            last_epoch = epoch_time

# Call the function
parse_packets('cleaned_foobar.txt', 'foobar_csv.csv')
