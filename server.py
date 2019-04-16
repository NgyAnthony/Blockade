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
    conn.send(pickle.dumps(players[player]))
    while True:
        try:
            data = pickle.loads(conn.recv(2048*15))
            players[player] = data

            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = players[0]
                else:
                    reply = players[1]

                print("Received: ", data)
                print("Sending : ", reply)

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

#TODO : Send current-player back to the server AND send back the board but reverse the thing
#ねたい