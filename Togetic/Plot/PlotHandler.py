from numpy import *
import pylab

from Togetic.Server.AbstractServer import AbstractServer

class PlotHandler(AbstractServer):
    def __init__(self, input_queue):
        AbstractServer.__init__(self)
        self._input_queue = input_queue

# Init plotlib
        self.retrace = 0.1        # Temps en secondes, retrace le graphique à chaque retrace millisecondes
        # On définit les paramètres du graphique; une seule figure. Le programme ouvrira une fenêtre différente pour chaque courbe.
        fig = pylab.figure('Figure')
        self.manager = pylab.get_current_fig_manager()

        # Initialise quelques variables
        self.time = 0.0         # Temps actuel
        self.delta_t = 0.1      # Pas de temps

        #De même que les tableaux, vecteurs temps et valeur de fonction pour graphique
        self.temps = []
        self.valeur = []

        # On crée le graphique
        self.courbe = pylab.plot(self.temps, self.valeur)

        # Définit le titre et xlabel
        self.titre = pylab.title("X en fonction du temps")
        self.etiquette = pylab.xlabel("Retrace %f " % (self.time))

    def start(self):
        self.manager.show()
        AbstractServer.start(self)

    def _serve(self):
        # On calcule le nouveau temps et la valeur de la fonction associée
        self.time = self.time + self.delta_t

        # Puis on place ces données dans deux tableaux
        self.temps.append(self.time)
        self.valeur.append(self._queue.get()[0])

        # Met à jour les données dans le tableau associé avec le graphique
        self.courbe[0].set_data(self.temps,self.valeur)

        # On fait de même pour le texte et les axes
        self.etiquette.set_text('Retrace au temps %f '%( self.time ))

        # Cette commande s'applique au graphique actuel
        pylab.axis([min(self.temps)-0.1,max(self.temps)+0.1,min(self.valeur)-0.1,max(self.valeur)+0.1])

        # Redraws the figure
        self.manager.canvas.draw()

        #  Puis, on attend 'retrace' ms avant de relancer run
        time.sleep(self.retrace)
