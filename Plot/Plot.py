import socket
from numpy import *
import pylab
import Tkinter as Tk
from Server import Server
import threading

global data

class Client(Server):
	global connexion_to_sever
	def __init__ (self):
		Server.__init__(self)
		connexion_to_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	def connect(self, addr, port):
		connexion_to_server.connect((addr, port))
			

class Courbe:
	global t                # Temps actuel
	global delta_t          # Pas de temps
	global retrace          # Retrace le graphique à chaque retrace millisecondes
	global temps, valeur    # Vecteurs temps et valeur de fonction pour graphique
	global courbe, etiquette, manager # Variables contenant les détails des graphiques


	# Cette méthode avance l'horloge, recalcule la fonction et retrace le tout

	def run(self) :
		# Liste des variables globales actives dans cette méthode
		global t, retrace, etiquette, manager
		global valeur, temps, courbe, delta_t, data

		# On calcule le nouveau temps et la valeur de la fonction associée
		t = t + delta_t

		# Puis on place ces données dans deux tableaux
		temps.append(t)
		valeur.append(data)

		# Met à jour les données dans le tableau associé avec le graphique
		courbe[0].set_data(temps,valeur)

		# On fait de même pour le texte et les axes
		etiquette.set_text('Retrace au temps %f '%( t ))

		# Cette commande s'applique au graphique actuel
		pylab.axis([min(temps)-0.1,max(temps)+0.1,min(valeur)-0.1,max(valeur)+0.1])

		# Redraws the figure
		manager.canvas.draw()

		# Puis, on attend 'retrace' ms avant de relancer run
		manager.window.after(retrace,self.run)

		
	def __init__(self, valeur_initiale):
		global t, retrace, etiquette, manager
		global valeur, temps, courbe, delta_t, data
		retrace =  100  # Temps en millisecondes 

		# On définit les paramètres du graphique; une seule figure
		fig = pylab.figure(1)
		manager = pylab.get_current_fig_manager()   

		# Initialise quelques variables
		t       = 0.0
		delta_t = 0.1
		data = valeur_initiale

		#De même que les tableaux
		temps = []
		valeur = []

		# Ajoute la première valeur à ces tableaux
		temps.append(t)
		valeur.append(data)

		# On crée le graphique
		courbe = pylab.plot(temps,valeur)

		# Définit le titre et xlabel 
		titre     = pylab.title("Sinus en fonction du temps")
		etiquette = pylab.xlabel("Retrace %f " % (t) )

		# On trace le tout
		manager.canvas.draw()

		# Puis on lance la méthode qui iterera 
		self.run()

		# Lancer le graphique avec show() et le maintenir actif avec mainloop.
		manager.show()
		Tk.mainloop()  # Nécessaire pour garder le programme actif
