def parse_packet_file(input_filename, output_filename):
    with open(input_filename, 'r') as infile, open(output_filename, 'w') as outfile:
        lines = infile.readlines()

    
        timestamp = None
        hex_data = ""

        for line in lines:
            line = line.strip()

            if line.startswith("+---------+"):
                continue  # Skip the separator lines

            # If a line contains a timestamp
            if "," in line and "ETHER" in line:
                if timestamp and hex_data:             # this becomes true after the program has read both the lines
                    # Clean up the hex data by removing spaces and '|'
                    clean_hex = hex_data.replace("|", "").replace(" ", "").lower()
                    if clean_hex.startswith('0'):
                        clean_hex = clean_hex[1:]
                    outfile.write(f"{timestamp}\n{clean_hex}\n")

                # Reset for the next packet
                timestamp = line.split()[0]
                hex_data = ""              # the loop goes again and reads the next line, enters the else segment and grabs the hex
            else:
                # Grab the hex data 
                hex_data += line

        # After the loop, ensure the last packet is saved
        if timestamp and hex_data:
            clean_hex = hex_data.replace("|", "").replace(" ", "").lower()
            outfile.write(f"{timestamp}\n{clean_hex}\n")

# Call the function with input and output file paths
parse_packet_file('trial1.txt', 'cleaned_trial.txt')
