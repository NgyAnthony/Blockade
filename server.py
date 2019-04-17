import socket
from _thread import *
from config import Config
from logic import *
import pickle
import random

server = "127.0.0.1"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

player_list = ["P1", "P2"]
random_player = random.choice(player_list)
board = Board()

players = [Config("P1", board, random_player), Config("P2", board, random_player)]

currentPlayer = 0


def threaded_client(conn, player):
    global currentPlayer
    conn.sendall(pickle.dumps(players[player]))
    while True:
        try:
            data = pickle.loads(conn.recv(2048*20))

            if not data:
                print("Disconnected")
                break

            elif data.__class__.__name__ == "AskBoard":
                if player == 1:
                    reply = players[1]
                elif player == 0:
                    reply = players[0]

                print("Updating board...")
                print("- Received: ", data)
                print("- Sending : ", reply)
                conn.sendall(pickle.dumps(reply))

            else:
                players[player] = data

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
                conn.sendall(pickle.dumps(reply))


        except:
            break

    print("Lost connection")
    conn.close()
    currentPlayer -= 1


while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1