# -*- coding: utf-8 -*-
import sys
sys.path += ['..']

import socket
from numpy import *
import pylab
#import Tkinter as Tk
# from Server import AbstractServer
import threading
import time

### C'est une mémoire partagé. Il faut un threading.Lock associé pour protéger les accès.
### Pour l'instant tu utilises une simple liste. Au début reste comme ça.
### Une fois que ça fonctionne, essaye de transformer ta liste en Queue. C'est fait exprès pour les threads.
### Seulement une fois que ça fonctionne

global data  #Tableau de données
lock = threading.Lock()

# class Client(AbstractServer):
#     def __init__ (self):
#         Server.__init__(self)
#         ### Utilise le fichier Server.py que j'ai mis dans le dossier Blender. Je le modifie cette aprem (jeudi aprem).
#         ### Tu peux t'inspirer du code de PositionController.py qui utilise ce fichier.
#         ### Copie le et utilise la version que tu as. Si tu travailles dessus avant que je modifie, c'est pas trop grave.
#         ### Il faudra juste readapter le code. Mais c'est pas compliquer
#         connexion_to_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 
#     def connect(self, addr, port):
#         connexion_to_server.connect((addr, port))

class Courbe(threading.Thread):
    def __init__(self, grandeur):
        threading.Thread.__init__(self)
        self.retrace =  0.1        # Temps en secondes, retrace le graphique à chaque retrace millisecondes
        self.indice = grandeur     #Indice de la valeur à lire dans data

        # On définit les paramètres du graphique; une seule figure. Le programme ouvrira une fenêtre différente pour chaque courbe.
        fig = pylab.figure(self.indice)
        self.manager = pylab.get_current_fig_manager()  

        # Initialise quelques variables
        self.t       = 0.0	       # Temps actuel
        self.delta_t = 0.1         # Pas de temps

        #De même que les tableaux, vecteurs temps et valeur de fonction pour graphique
        self.temps = []
        self.valeur = []

        # On crée le graphique
        self.courbe = pylab.plot(self.temps,self.valeur)

        # Définit le titre et xlabel
        self.titre     = pylab.title("X en fonction du temps")
        self.etiquette = pylab.xlabel("Retrace %f " % (self.t) )

        # Lancer le graphique avec show() et le maintenir actif avec mainloop.
        self.manager.show()
        #Tk.mainloop()  # Nécessaire pour garder le programme actif

    # Cette méthode avance l'horloge, recalcule la fonction et retrace le tout
    def run(self) :
        global data
        while True:
            # On calcule le nouveau temps et la valeur de la fonction associée
            self.t = self.t + self.delta_t

            # Puis on place ces données dans deux tableaux
            self.temps.append(self.t)

            ### C'est une variable partagé. Il faut lock puis release l'utilisation
            with lock:
                self.valeur.append(data[self.indice])

            # Met à jour les données dans le tableau associé avec le graphique
            self.courbe[0].set_data(self.temps,self.valeur)

            # On fait de même pour le texte et les axes
            self.etiquette.set_text('Retrace au temps %f '%( self.t ))

            # Cette commande s'applique au graphique actuel
            pylab.axis([min(self.temps)-0.1,max(self.temps)+0.1,min(self.valeur)-0.1,max(self.valeur)+0.1])

            # Redraws the figure
            self.manager.canvas.draw()

            #   Puis, on attend 'retrace' ms avant de relancer run
            time.sleep(self.retrace) 

### Ici tu as ton main
### Donne un cas d'utilisation avec lancement du serveur et de ton plot
### Tu pourras alors tester ton code
if __name__ == '__main__':
    data=[0, 2, 3, 5]
    a = Courbe(2)
    a.start()
    for i in xrange(5):
        data[2] += 1
        time.sleep(3)
    # Do things

