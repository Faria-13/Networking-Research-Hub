import capture
import cleaner
import statmaker
import csvmaker

def main():
    print(" \n\n Welcome to Faria's version of Wireshark \n\n")

    capture.main()
    cleaner.parse_packet_file('foobar.txt', 'cleaned_foobar.txt')
    statmaker.analyze_packets_from_file("cleaned_foobar.txt")
    csvmaker.parse_packets("cleaned_foobar.txt", "foobar_csv.csv")

main()