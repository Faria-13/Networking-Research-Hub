import capture
import cleaner2
import statmaker
import csvmaker

def main():
    print("\n\n Welcome to Faria's version of Wireshark \n\n")

    while True:
        res = ask_user("Do you want to start the capture process? (y/n) Q to quit ")
        if  res == True:
            capture.main()
        elif res == 'q':
            break
        else:
            continue
        
        res = ask_user("Do you want to clean the tcpdump output? (y/n) Q to quit")
        if res == True:
            cleaner2.process_tcpdump_output('foobar.txt', 'cleaned_foobar.txt')
        elif res == 'q':
            break
        else:
            continue
        res = ask_user("Do you want to see some stats? (y/n) Q to quit ")
        if res == True:
            statmaker.analyze_packets_from_file("cleaned_foobar.txt")
        elif res == 'q':
            break
        else:
            continue
        res = ask_user("Do you want to parse packets into a CSV file? (y/n) Q to quit ")
        if res == True:
            csvmaker.parse_packets("cleaned_foobar.txt", "foobar_csv.csv")
        elif res == 'q':
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
        elif response in ['Q', 'q']:
            return response == 'q'
        print("Invalid input")
        return response =='meh'


def ask_user(question):
    while True:
        response = input(question).strip().lower()
        if response in ['y', 'yes']:  # Adjusted to also accept 'yes'
            return True
        elif response in ['n', 'no']:  # Added option to return False for 'no'
            return False
        elif response in ['q', 'quit']:  # Adjusted to check for 'quit'
            return 'q'
        print("Invalid input. Please enter 'y', 'n', or 'q'.")


main()
