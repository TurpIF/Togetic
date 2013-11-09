import socket
from numpy import *
import pylab
import Tkinter as Tk
from Server import Server
import threading

global data  #Tableau de données

class Client(Server):
	connexion_to_server=0
	def __init__ (self):
		Server.__init__(self)
		connexion_to_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	def connect(self, addr, port):
		connexion_to_server.connect((addr, port))
			

class Courbe:
	t=0                # Temps actuel
	delta_t=0          # Pas de temps
	retrace=0          # Retrace le graphique à chaque retrace millisecondes
	temps, valeur = 0,0   # Vecteurs temps et valeur de fonction pour graphique
	courbe, etiquette, manager = 0,0,0 # Variables contenant les détails des graphiques


	# Cette méthode avance l'horloge, recalcule la fonction et retrace le tout

	def run(self) :
		global data
		# On calcule le nouveau temps et la valeur de la fonction associée
		self.t = self.t + self.delta_t

		# Puis on place ces données dans deux tableaux
		self.temps.append(self.t)
		self.valeur.append(data)

		# Met à jour les données dans le tableau associé avec le graphique
		self.courbe[0].set_data(self.temps,self.valeur)

		# On fait de même pour le texte et les axes
		self.etiquette.set_text('Retrace au temps %f '%( self.t ))

		# Cette commande s'applique au graphique actuel
		pylab.axis([min(self.temps)-0.1,max(self.temps)+0.1,min(self.valeur)-0.1,max(self.valeur)+0.1])

		# Redraws the figure
		self.manager.canvas.draw()

		# Puis, on attend 'retrace' ms avant de relancer run
		self.manager.window.after(self.retrace,self.run)

		
	def __init__(self, valeur_initiale):
		global data
		self.retrace =  100  # Temps en millisecondes 

		# On définit les paramètres du graphique; une seule figure
		fig = pylab.figure(1)
		self.manager = pylab.get_current_fig_manager()   

		# Initialise quelques variables
		self.t       = 0.0
		self.delta_t = 0.1
		data = valeur_initiale

		#De même que les tableaux
		self.temps = []
		self.valeur = []

		# Ajoute la première valeur à ces tableaux
		self.temps.append(self.t)
		self.valeur.append(data)

		# On crée le graphique
		self.courbe = pylab.plot(self.temps,self.valeur)

		# Définit le titre et xlabel 
		self.titre     = pylab.title("Sinus en fonction du temps")
		self.etiquette = pylab.xlabel("Retrace %f " % (self.t) )

		# On trace le tout
		self.manager.canvas.draw()

		# Puis on lance la méthode qui iterera 
		self.run()

		# Lancer le graphique avec show() et le maintenir actif avec mainloop.
		self.manager.show()
		Tk.mainloop()  # Nécessaire pour garder le programme actif
