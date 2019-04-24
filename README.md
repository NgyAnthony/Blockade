# Blockade
- Développeur: NGUYEN Anthony
- Designer : reddit.com/user/elheber
- E-Mail: nguyen.anthony.dev@gmail.com

## Préambule
Blockade est un prototype conçu pour le projet d'ISN de fin d'année 2019. <br>
Toute la progression du jeu peut être suivie dans "Commits". <br>

Le jeu et le code sont entièrement en anglais afin de respecter un assignement constant des variables. <br>


Environnement : Ce jeu a été crée sous macOS Mojave(10.14.4 (18E226)), il est probable que des bugs soient présents sous Windows.<br>


![Jeu](https://i.imgur.com/mPBBeFC.png)
### Nécéssaire:
	Global :
    - Python 3.0+
    - Pygame
    - sys
    - os
    - webbrowser
    - random
    - numpy
    
    Serveur :
    - socket
    - thread
    - pickle

    
### Contenu:
    - /server.py    | Programme à exécuter : lance le serveur
    - /main.py 	    | Programme à exécuter : lance le jeu
   	  - /network.py   | Permet la liaison entre le serveur et le client
   	  - /Assets 	  | Dossier contenant les cartes pour les joueurs bleu et rouge.
      - /Other_assets | Dossier contenant les cartes de dos
      - /base.py 	  | Exécute le main loop pygame
      - /config.py    | Contient les paramètres globaux
      - /logic.py     | Créer un objet "board" avec des objets "cards" choisis aléatoirement

## Règles du jeu et fonctionnement:
### Règles du jeu:
L'objectif du jeu est d'établir une "route" de votre camp au camp adverse. A chaque tour, le nombre de routes que vous avez établi est rajouté au score. <br>
Afin d'établir une route, vous devez utiliser les cartes sur le plateau en partant de votre camp jusqu'au camp adverse. <br>
![Jeu](https://i.imgur.com/JRnpShJ.png
)

### Fonctionnement:

Les cartes sont composées de flèches qui indiquent la direction dans laquelle le chemin peut être crée ainsi qu'un nombre qui indique la distance à laquelle le chemin peut aller.
![Jeu](https://i.imgur.com/jLvRvFV.png)

Dans cet exemple, la carte qui est tout à gauche peut accéder à la case qui est tout à droite car elle à une distance de 2 et elle a une flèche qui va à droite. Par contre, elle ne peut pas accéder à la cause juste à côté avec le symbole infini car elle est à une distance de 1.
![Jeu](https://i.imgur.com/tClpd50.png)

Il existe des cases spéciales, comme les cases infini et les cases 1-2 et 1-3. Les cases 1-2 et 1-3 ont comme leur nombre l'indique, une distance qui va de 1 à x. Dans l'exemple en dessous, la carte du bas peut accéder aux deux cartes du haut car elle possède une distance de 1 et de 2 ainsi que d'une direction qui va vers le haut.

![Jeu](https://i.imgur.com/nK9eGYp.png)

En pratique, il suffit de cliquer sur une première carte dans votre camp puis de cliquer sur une deuxième carte qui est accessible, et ainsi de suite pour pouvoir établir une route. Si il n'est pas possible de construire, cliquez autre part ou bien l'algorithme va automatiquement rejetter la construction si il n'y a pas de case accessible ou si la carte sur laquelle vous avez cliqué est invalide (par exemple cliquer sur une carte ennemie).<br>

Vous pouvez voir ici qu'un chemin à été établi en passant par la flêche jaune.

![Jeu](https://i.imgur.com/TVoyKFk.png)
