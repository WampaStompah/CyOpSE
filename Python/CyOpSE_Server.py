import socketserver
from xml.dom.minidom import parseString
import pymysql
import xmltodict

# EXERCISE INFORMATION
HIGH_VALUE_TARGETS = ["10.19.0.204", "10.19.0.199","10.19.0.155","10.19.0.201"]
ATTACKERS = ["10.19.0.201"]
Attacks = []
Objectives = []
Missions = []

# MySQL INFORMATION
"""
Be advised that the database must already exist before this script is run
"""
SQL_HOST = "127.0.0.1"
SQL_PORT = "3306"
SQL_USER = "root"
SQL_PASSWORD = ""
SQL_DB = "mydb"
SQL_CHARSET = "utf8"

def SQL_Connect(host, port, user, password, db, charset):
    """
    Create MySQL connection to Database and return the pymysql object to control that connection.
    :param host: ip address of the sever
    :param port: port the server is running on
    :param user: username to be used with the database
    :param password: password for the user above to access database
    :param db: the name of the database to be used from the server
    :param charset: the charset in use by the database
    :return: 
    """
    try:
        connector = pymysql.connect(host = host,
                                    user = user,
                                    password = password,
                                    db = db,
                                    charset = charset)
    except ConnectionError:
        print("Could not establish connection to sever. Please check the parameters and try again.")

    return connector


class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.
    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        length = self.request.recv(100).strip().decode()
        print ("Preparing to receive " + length + " bytes from " + self.client_address[0])
        self.request.sendall(length.encode())
        self.data = self.myreceive(int(length))
        """
        self.data = self.request.recv(2048).strip().decode()
        while len(self.data) <= int(length) - 2:
            self.data += self.request.recv(10240).strip().decode()
            print(len(self.data))
        """
        # Uncomment these lines to see the payload coming through
        print ("{} wrote:".format(self.client_address[0]))
        print (parseString(self.data).toprettyxml())


        self.data = xmltodict.parse(self.data)
        #print(self.data['root']['item'])

        for i in self.data['root']['item']:
            if i['id.orig_h']['#text'] in HIGH_VALUE_TARGETS:
                print(i['name']['#text'] + " detected on high value target: " + i['id.orig_h']['#text'])
            if i['id.resp_h']['#text'] in HIGH_VALUE_TARGETS:
                print(i['name']['#text'] + " detected on high value target: " +  i['id.resp_h']['#text'])
        
        #for i in self.data['root']['item']:
            #if i['id.orig_h']['#text'] in HIGH_VALUE_TARGETS and i['id.resp_h']['#text'] in ATTACKERS:
                #print("Attack detected on high value target: " + i['id.orig_h']['#text'])
            #if i['id.resp_h']['#text'] in HIGH_VALUE_TARGETS and i['id.orig_h']['#text'] in ATTACKERS:
                #print("Attack detected on high value target: " + i['id.resp_h']['#text'])

    def myreceive(self, MSGLEN):
        chunks = []
        bytes_recd = 0
        while bytes_recd < MSGLEN:
            chunk = self.request.recv(min(MSGLEN - bytes_recd, 2048))
            if chunk == b'':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
        return b''.join(chunks)

if __name__ == "__main__":
    HOST, PORT = "", 9999

    # Create the server, binding to localhost on port 9999
    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)

    # Connect to MqSQL DB
    sql_conection = SQL_Connect(SQL_HOST,SQL_PORT,SQL_USER,SQL_PASSWORD,SQL_DB,SQL_CHARSET)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
