import socket
import pickle


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "127.0.0.1"
        self.port = 5550
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def getP(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)  # Connect to the server
            return pickle.loads(self.client.recv(2048*30))  # Receive what the server has sent
        except:
            print("Connection failed.")

    def send(self, data):
        try:
            self.client.sendall(pickle.dumps(data))  # Send an object to the server
            return pickle.loads(self.client.recv(2048*30))  # Receive back what the server sent
        except socket.error as e:
            print(e)
