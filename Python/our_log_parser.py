from bro_log_reader import BroLogReader

def main(logfile):
    log = BroLogReader()
    records = log.read_log(logfile)
    print("Welcome to the Log Parser.")
    print("""Type "QUIT" to quit at any time.""")
    print()
    i = 0
    while 1 == 1:
        search_cat = input("Enter Search Field:")
        search_value = input("Enter the Search Value in that field:")
        if search_cat == "QUIT" or search_value == "QUIT":
            print("Thanks for using the parser...")
            print("Goodbye")
            return 0
        for row in records:
            if row[search_cat] == search_value:
                print(row)
                i = 1
        if i == 0:
            print("Unable to find the value " + search_value + " in " + search_cat + ".")
            print("Please try again.")
        i = 0
                
            

if __name__ == "__main__":
    main("conn.log")
