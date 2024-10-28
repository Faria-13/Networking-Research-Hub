import capture
import cleaner2
import statmaker
import csvmaker

def main():
    print("\n\n Welcome to Faria's version of Wireshark \n\n")

    while True:
        if ask_user("Do you want to start the capture process? (y/n)"):
            capture.main()
        else:
            continue

        if ask_user("Do you want to clean the tcpdump output? (y/n)"):
            cleaner2.process_tcpdump_output('foobar.txt', 'cleaned_foobar.txt')
        else:
            continue

        if ask_user("Do you want to see some stats? (y/n)"):
            statmaker.analyze_packets_from_file("cleaned_foobar.txt")
        else:
            continue

        if ask_user("Do you want to parse packets into a CSV file? (y/n)"):
            csvmaker.parse_packets("cleaned_foobar.txt", "foobar_csv.csv")
        else:
            continue
        
        # If all processes are completed, break the loop
        print("All processes completed. Exiting the program.")
        break

def ask_user(question):
    while True:
        response = input(question).strip().lower()
        if response in ['y', 'n']:
            return response == 'y'
        print("Invalid input. Please enter 'y' for yes or 'n' for no.")

main()
