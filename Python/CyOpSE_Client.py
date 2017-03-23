import socket, sys, time
from bro_log_reader import BroLogReader
from dicttoxml import dicttoxml

MY_ADDR = "192.168.1.20"
SERVER_ADDR, SERVER_PORT = "192.168.1.216", 9999
LOGFILE = "/usr/local/bro/spool/wired/weird.log"

def log_to_stix(file):
    """ Take a log file created by bro and convert it to a STIX compliant
    XML document."""
    log = BroLogReader()
    records = log.read_log(file)
    xml = dicttoxml(records)
    return xml

def mysend(socket, msg):
        totalsent = 0
        while totalsent < len(msg):
            sent = socket.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent
    


if __name__ == "__main__":
    # Create a socket (SOCK_STREAM means a TCP socket)
    
    try:
        while True:
            try:
                #resend any new data every 10 seconds
                data = log_to_stix(LOGFILE)
                data_len = len(data)
                print("sending " + str(data_len) + " bytes.")
                # Connect to server and send data
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((SERVER_ADDR, SERVER_PORT))
                sock.sendall(str(data_len).encode())
                print(sock.recv(100).strip().decode())
                mysend(sock, data)
            

                # Receive data from the server and shut down
                #received = sock.recv(1024)
                sock.close()
               
            except Exception :
                 print()            
             
            time.sleep(10)
            
    except OSError as e:
        print("Error Connecting. Check Parameters and try again.")
        print(e)


