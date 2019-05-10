from _thread import *  # Librairie standard python
import socket  # Librairie standard python
import pickle  # Librairie standard python
import random  # Librairie standard python
from config import Config  # Importer une class "config" de config.py
from logic import *  # Importer logic.py

# IP : localhost
server = "127.0.0.1"

# Port : identique à celui du client
port = 5550

# Création d'un nouveau socket avec le protocole TCP et IPv4
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Lier un tuple avec l'adresse et le port au socket
    s.bind((server, port))
except socket.error as e:
    # Si il y a une erreur, retourner l'erreur
    str(e)

s.listen(2)  # 2 threads/clients sont attendus
print("En attente d'une connection, serveur démarré.")

# Choisir aléatoirement un joueur
player_list = ["P1", "P2"]
random_player = random.choice(player_list)

# Créer une instance de la class Board()
board = Board()

# Créer deux instances de Config qui serviront de base de données
players = [Config("P1", board, random_player, 0, 0), Config("P2", board, random_player, 0, 0)]

# Garder une trace du nombre de clients/thread connectés
currentPlayer = 0


def threaded_client(conn, player):
    global currentPlayer
    # Au début, envoyer aux clients une copie de leur Config (sous forme d'objet)
    conn.sendall(pickle.dumps(players[player]))  # Pickle permet d'envoyer des objets
    while True:
        try:
            # Recevoir les données dans un container pickle
            data = pickle.loads(conn.recv(2048*30))

            # Si aucune donnée n'est reçue, la connection est coupée.
            if not data:
                print("Déconnecté")
                break

            # On reçoit une classe qui à le nom AskBoard, on envoie une copie de board
            elif data.__class__.__name__ == "AskBoard":
                if player == 1:
                    reply = players[1]  # Donner au client son board mis à jour
                elif player == 0:
                    reply = players[0]

                print("Mise à jour du board...")
                print("- Reçu: ", data)
                print("- Envoi : ", reply)
                conn.sendall(pickle.dumps(reply))

            # On reçoit une classe qui à le nom ResetBoard, on réinitiallise tout
            elif data.__class__.__name__ == "ResetBoard":
                new_board = Board()  # Créer une nouvelle instance de board
                new_random = random.choice(player_list)  # Choisir aléatoirement un nouveau joueur
                # Créer de nouvelles config
                new_players = [Config("P1", new_board, new_random, 0, 0), Config("P2", new_board, new_random, 0, 0)]
                board = new_board
                players[0] = new_players[0]
                players[1] = new_players[1]

                if player == 1:
                    reply = players[1]  # Give the client his updated board
                elif player == 0:
                    reply = players[0]

                print("Reset de la partie...")
                print("- Reçu: ", data)
                print("- Envoi : ", reply)
                conn.sendall(pickle.dumps(reply))

            else:
                # Dans ce cas, un mouvement a été effecuté par le joueur
                # L'ancien board stocké sur le serveur et remplacé par le nouveau board reçu par le client
                players[player] = data

                # Comme un mouvement à été effectué, on peut assumer qu'on peut remplacer le board de l'autre client
                # et le tour actuel par les données reçues.
                if player == 1:  # Les données sont reçues par le joueur 1
                    players[0].TURN = players[1].TURN  # Update du tour du joueur 0
                    players[0].BOARD = players[1].BOARD  # Update du board du joueur 0
                    reply = players[0]

                elif player == 0:
                    players[1].TURN = players[0].TURN
                    players[1].BOARD = players[0].BOARD
                    reply = players[1]

                print("Déplacement en cours...")
                print("- Reçu: ", data)
                print("- Envoi : ", reply)
                # Envoyer une réponse "board" qui ne va pas être utilisé sauf pour garder la connection.
                conn.sendall(pickle.dumps(reply))

        # Si il y a une erreur ou si le client est fermé, annuler le thread
        except:
            break

    # Fermer la connection
    print("Connection perdue.")
    conn.close()
    currentPlayer -= 1
    # Étant donné que le serveur reste allumé, on garde une trace du nombre connections
    # pour pouvoir s'assurer qu'on peut re-assigner nos joueurs si ils se reconnectent.


while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))  # Création d'un nouveau thread
    currentPlayer += 1  # Ajout du nombre de joueur