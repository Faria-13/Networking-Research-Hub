import capture
import cleaner2
import statmaker
import csvmaker

def main():
    print(" \n\n Welcome to Faria's version of Wireshark \n\n")

    capture.main()
    cleaner2.process_tcpdump_output('foobar.txt','cleaned_foobar.txt')
    statmaker.analyze_packets_from_file("cleaned_foobar.txt")
    csvmaker.parse_packets("cleaned_foobar.txt", "foobar_csv.csv")

main()