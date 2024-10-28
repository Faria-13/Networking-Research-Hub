import capture
import cleaner2
import statmaker
import csvmaker

def main():
    print("\n\n Welcome to Faria's version of Wireshark \n\n")

    while True:
        if ask_user("Do you want to start the capture process? (y/n) Q to quit") == 'y':
            capture.main()
        elif ask_user("Do you want to start the capture process? (y/n) Q to quit") == 'q':
            break
        else:
            continue

        if ask_user("Do you want to clean the tcpdump output? (y/n) Q to quit") == 'y':
            cleaner2.process_tcpdump_output('foobar.txt', 'cleaned_foobar.txt')
        elif ask_user("Do you want to clean the tcpdump output? (y/n) Q to quit")  == 'q':
            break
        else:
            continue

        if ask_user("Do you want to see some stats? (y/n) Q to quit") == 'y':
            statmaker.analyze_packets_from_file("cleaned_foobar.txt")
        elif ask_user("Do you want to see some stats? (y/n) Q to quit") == 'q':
            break
        else:
            continue

        if ask_user("Do you want to parse packets into a CSV file? (y/n) Q to quit") == 'y':
            csvmaker.parse_packets("cleaned_foobar.txt", "foobar_csv.csv")
        elif ask_user("Do you want to parse packets into a CSV file? (y/n) Q to quit") == 'q':
            break
        else:
            continue
        
        # If all processes are completed, break the loop
        print("All processes completed. Exiting the program.")
        break

def ask_user(question):
    while True:
        response = input(question).strip().lower()
        if response in ['y', 'Y']:
            return response == 'y'
        elif response == 'Q':
            return response == 'q'
        print("Invalid input")
        return response =='y'
        

main()
