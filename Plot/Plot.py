# -*- coding: utf-8 -*-
import socket
from numpy import *
import pylab
#import Tkinter as Tk
import ClientHandler
import threading
import Queue
import Tab_queue
import time
import sys
sys.path += ['..']
     
### C'est une mémoire partagé. Il faut un threading.Lock associé pour protéger les accès.
### Pour l'instant tu utilises une simple liste. Au début reste comme ça.
### Une fois que ça fonctionne, essaye de transformer ta liste en Queue. C'est fait exprès pour les threads.
### Seulement une fois que ça fonctionne


_queue = Tab_queue(6).getTab()  #Tableau de données
lock = threading.Lock()


     
class Receiver(ClientHandler):

	def __init__(self, addr):
		ClientHandler._init_(self, addr)
		
	def _msgToSend(self):
		pass
            	
	def _parseRecv(self, data_raw):
		global _queue

		data_line = data_raw.decode('utf-8').split('\n')
		for _data in data_line:
			data_array = _data.split(' ')
			# Read data parsed like 'TIME X Y Z THETA PHI PSY' to test
			if len(data_array) == 7 :
				try:
					# Get the position
					x = float(data_array[1])
					y = float(data_array[2])
					z = float(data_array[3])
					theta = float(data_array[4])
					phi = float(data_array[5])
					psy = float(data_array[6])
				except ValueError:
					 continue

				# Set the position
				_queue[0].put(x)
				_queue[1].put(y)
				_queue[2].put(z)
				_queue[3].put(theta)
				_queue[4].put(phi)
				_queue[5].put(psy)
                           
     
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
		global _queue
		while True:
			# On calcule le nouveau temps et la valeur de la fonction associée
			self.t = self.t + self.delta_t

			# Puis on place ces données dans deux tableaux
			self.temps.append(self.t)
			self.valeur.append(_queue[self.indice].get())

			# Met à jour les données dans le tableau associé avec le graphique
			self.courbe[0].set_data(self.temps,self.valeur)

			# On fait de même pour le texte et les axes
			self.etiquette.set_text('Retrace au temps %f '%( self.t ))

			# Cette commande s'applique au graphique actuel
			pylab.axis([min(self.temps)-0.1,max(self.temps)+0.1,min(self.valeur)-0.1,max(self.valeur)+0.1])

			# Redraws the figure
			self.manager.canvas.draw()
			
			#  Puis, on attend 'retrace' ms avant de relancer run
			time.sleep(self.retrace) 
				
     
    
    
### Ici tu as ton main
### Donne un cas d'utilisation avec lancement du serveur et de ton plot
### Tu pourras alors tester ton code
if __name__ == '__main__':
    receiver=Receiver(42000)
    ay = Courbe(2)
    receiver.start()
    ay.start()

