import socketserver
#from xml.dom.minidom import parseString
import pymysql
#import xmltodict
import re

#General Info
HOST = ""
PORT = 9999

# EXERCISE INFORMATION
HIGH_VALUE_TARGETS = ["10.19.0.204", "10.19.0.199","10.19.0.155","10.19.0.201"]
ATTACKERS = ["10.19.0.201"]
ATTACK_NAMES = []
OBJECTIVES = []
MISSIONS = []

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


        #get the Missions, Objectives, and Attacks from SQL Database
        try:
            att_query = 'SELECT DISTINCT Attack_Name From Attack;'
            obj_query = 'SELECT DISTINCT Objective_Name From Objective;'
            mis_query = 'SELECT DISTINCT Mission_Name From Mission_Set;'
            with connector.cursor() as cursor:
                #Attack Data
                cursor.execute(att_query)
                result = cursor.fetchall()
                names = re.split('\W+', str(result))
                ATTACK_NAMES = [x for x in names if x != ""]
                # Objectives Data
                cursor.execute(obj_query)
                result = cursor.fetchall()
                names = re.split('\W+', str(result))
                Objectives = [x for x in names if x != ""]
                # Mission Data
                cursor.execute(mis_query)
                result = cursor.fetchall()
                names = re.split('\W+', str(result))
                Missions = [x for x in names if x != ""]

        except Exception as e:
            print("Could not retrieve information from the sever. Please check your parameters and try again.", e)

        finally:
            connector.close()

    except ConnectionError:
        print("Could not establish connection to sever. Please check the parameters and try again.")

    return ATTACK_NAMES, Objectives, Missions


class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.
    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    
    ***THIS IS NOT USABLE OUTSIDE OF THIS FILE***
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        length = self.request.recv(100).strip().decode()
        #print ("Preparing to receive " + length + " bytes from " + self.client_address[0])
        self.request.sendall(length.encode())
        self.data = self.myreceive(int(length))

        # Uncomment these lines to see the payload coming through
        #print ("{} wrote:".format(self.client_address[0]))
        #print (parseString(self.data))

        array_data = re.split('\t+|\n+|\n#+|\t#+',self.data.decode())
        num_params = 0
        param_start = 0

        # Find attacks within the logs
        for param in range(len(array_data)):
            if array_data[param] == "#types":
                break
            elif array_data[param] == "#fields":
                param_start = param
                num_params = 0
            else:
                num_params += 1

        #print(str(num_params) + " parameters detected.")

        for i in range(param_start, param_start + num_params):
            if array_data[i] == "addl":
                    for x in range(len(array_data)//num_params - 1):
                        if array_data[i+num_params*x] in ATTACK_NAMES:
                            print(array_data[i+num_params*x] + " objective complete.")
                            try:
                                connector = pymysql.connect(host=SQL_HOST,
                                                            user=SQL_USER,
                                                            password=SQL_PASSWORD,
                                                            db=SQL_DB,
                                                            charset=SQL_CHARSET)

                                sql_query = "UPDATE Attack SET Attack_Status = 'Complete' WHERE Attack_Name = '" + array_data[i+num_params*x] + "';"
                                print(sql_query)
                                with connector.cursor() as cursor:
                                    cursor.execute(sql_query)
                                    connector.commit()
                            except Exception as E:
                                print("Unable to update database.", E)
                            finally:
                                connector.close()
                                ATTACK_NAMES.remove(array_data[i+num_params*x])


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

    # Connect to MqSQL DB
    # Create the server, binding to localhost on port 9999
    ATTACK_NAMES, OBJECTIVES, MISSIONS = SQL_Connect(SQL_HOST, SQL_PORT, SQL_USER, SQL_PASSWORD, SQL_DB, SQL_CHARSET)
    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
