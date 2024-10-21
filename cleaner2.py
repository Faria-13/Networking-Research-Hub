def process_tcpdump_output(input_filename, output_filename):
    with open(input_filename, 'r') as infile, open(output_filename, 'w') as outfile:
        lines = infile.readlines()
        timestamp = None
        hex_data = ""

        for line in lines:
            line = line.strip()

            # Check if the line starts with a timestamp (starts with a date-like format)
            if len(line) > 24 and line[4] == '-' and line[7] == '-' and line[10] == ' ':
                if timestamp and hex_data:
                    # Write the previous packet's timestamp and hex data
                    formatted_hex = format_hex_data(hex_data)
                    outfile.write(f"{timestamp}\n{formatted_hex}\n")

                # Grab the new timestamp and reset hex data
                timestamp = format_timestamp(line[:26])  # First 26 characters are the timestamp
                hex_data = ""  # Reset hex data for the new packet

            # grab the hex
            elif line.startswith('0x'):
                hex_data += line[7:].replace(' ', '')  # Remove the offset and colon and replace spaces

        # Write the last packet if it exists
        if timestamp and hex_data:
            formatted_hex = format_hex_data(hex_data)
            outfile.write(f"{timestamp}\n{formatted_hex}\n")


def format_timestamp(timestamp):
    # Convert '2024-10-20 20:33:11.440718' to '20:33:11,440,718'
    print(timestamp)
    date_time, microseconds = timestamp.split('.')
    time_part = date_time.split()[1]  # '20:33:11'
    print(microseconds)
    formatted_timestamp = time_part + ',' + microseconds[:3] + ',' + microseconds[3:]
    return formatted_timestamp


def format_hex_data(hex_data):
    # Return the hex data as a continuous string
    return hex_data.lower()


# Call the function with the input and output file paths
process_tcpdump_output('foobar.txt', 'cleaned_foobar.txt')
