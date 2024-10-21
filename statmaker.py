from collections import defaultdict

def extract_packet_info(packet_hex):
    
    
    ethernet_header_length = 14 * 2  # 14 bytes, each byte is 2 hex characters
    
    # IP header starts at byte 14 (i.e., at hex index 28)
    ip_header_start = ethernet_header_length

    
    # The total length field in IPv4 is 2 bytes (4 hex digits) after the differenciated services field
    # so to get that we start at IP header + 4 hex characters, and then add 4 more characters laters
    total_length_hex = packet_hex[ip_header_start + 4:ip_header_start + 8]
    total_length = int(total_length_hex, 16)  # Convert hex string to integer

    # Protocol field (1 byte, 2 hex digits) is at byte 9 of the IP header
    protocol_hex = packet_hex[ip_header_start + 18:ip_header_start + 20]      
    protocol = int(protocol_hex, 16)  # Convert hex string to integer (protocol number)

    return protocol, total_length

def analyze_packets_from_file(filename):
    protocol_distribution = defaultdict(int)
    packet_sizes = []
    
    # Read the file
    with open(filename, 'r') as file:
        lines = file.readlines()
    
    # Iterate over the file, two lines at a time (timestamp and packet hex)
    for i in range(0, len(lines), 2):
        timestamp = lines[i].strip()  # First line is the timestamp
        packet_hex = lines[i + 1].strip()  # Second line is the hex data

        # Extract protocol and size from the packet hex string
        protocol, packet_size = extract_packet_info(packet_hex)
        
        # Count protocol occurrences
        protocol_distribution[protocol] += 1
        
        # Collect packet sizes
        packet_sizes.append(packet_size)
    
    # Calculate basic statistics for packet sizes
    total_packets = len(packet_sizes)
    total_size = sum(packet_sizes)
    avg_packet_size = total_size / total_packets if total_packets > 0 else 0
    max_packet_size = max(packet_sizes, default=0)
    min_packet_size = min(packet_sizes, default=0)

    # Protocol mapping for human-readable output
    protocol_map = {
        1: "ICMP",
        6: "TCP",
        17: "UDP"
    }
    
    # Calculate protocol distribution percentages
    protocol_percentage = {
        protocol_map.get(proto, f"Unknown({proto})"): (count / total_packets) * 100
        for proto, count in protocol_distribution.items()
    }

    # Print the results
    print(f"Total Packets: {total_packets}")
    print(f"Average Packet Size: {avg_packet_size:.2f} bytes")
    print(f"Max Packet Size: {max_packet_size} bytes")
    print(f"Min Packet Size: {min_packet_size} bytes")
    print("Protocol Distribution (percentage):")
    for proto, percent in protocol_percentage.items():
        print(f"  {proto}: {percent:.2f}%")

# Call the function with the path to your file
analyze_packets_from_file('cleaned_foobar.txt')
