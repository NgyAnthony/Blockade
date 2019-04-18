import socket
from _thread import *
from config import Config
from logic import *
import pickle
import random

server = "127.0.0.1"
port = 5550

# Create a new socket with TCP and IPv4
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))  # Bind a tuple with server and port as parameters to the socket.
except socket.error as e:
    str(e)

s.listen(2)  # 2 threads are expected.
print("Waiting for a connection, Server Started")

# Randomly pick the starting player
player_list = ["P1", "P2"]
random_player = random.choice(player_list)

# Set the board
board = Board()

# Create two Config instances which will serve as the databases used in our game
players = [Config("P1", board, random_player), Config("P2", board, random_player)]

# Keep track of the threads connected
currentPlayer = 0


def threaded_client(conn, player):
    global currentPlayer
    # Initially, send to the clients a copy of config
    conn.sendall(pickle.dumps(players[player]))
    while True:
        try:
            # Receive the data inside a pickle container
            data = pickle.loads(conn.recv(2048*30))

            # If there is not data being received, the connection is down.
            if not data:
                print("Disconnected")
                break

            # The received data wants us to send a copy of the board
            elif data.__class__.__name__ == "AskBoard":
                if player == 1:
                    reply = players[1]  # Give the client his updated board
                elif player == 0:
                    reply = players[0]

                print("Updating board...")
                print("- Received: ", data)
                print("- Sending : ", reply)
                conn.sendall(pickle.dumps(reply))

            else:
                # In this case, a move has been made by the client
                players[player] = data  # The old board stored on the server is replaced by the new board sent as data

                # Since a move has been made, we can assume that we can replace the other client's board and turn
                # by the new data collected.
                if player == 1:
                    players[0].TURN = players[1].TURN
                    players[0].BOARD = players[1].BOARD
                    reply = players[0]

                elif player == 0:
                    players[1].TURN = players[0].TURN
                    players[1].BOARD = players[0].BOARD
                    reply = players[1]

                print("Making a move...")
                print("- Received: ", data)
                print("- Sending : ", reply)
                # Send back a reply which won't actually be used, it's there to keep the connection going.
                conn.sendall(pickle.dumps(reply))

        # If this somehow fails or the client has been closed just break the thread.
        except:
            break

    # Close the connection
    print("Lost connection")
    conn.close()
    currentPlayer -= 1
    # Since the server will still be running, we keep a track of the number of opened connction
    # to make sure that we can re-assign our players.


while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1