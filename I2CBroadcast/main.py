# A compl�ter: limites �ventuelles des composants

#import
from Server.Listener import Listener
from Server.Handler import Handler
from Server.ClientHandler import ClientHandler
import socket
import i2clibraries
from time import *

#Initialisation de l'adresse du broadcaster et du pipe qu'il utilise
?
#Par quoi se caract�rise par d�faut un client => cr�er classe client?

#A-t-on des clients ready?

clientlisten= Listener(self, addr, pipe)
clientlisten.start(clientlisten)
clientlisten._serve(clientlisten)
clientlisten._free(clientlisten)
clients= clientlisten.clients
print clientlisten.clients

# identification des clients: qui est qui?
 for client in clients :
	if (client= accel.caracteristique?) :
			client = accel
	elif (client= magnet.caracteristique?) :
			client = magnet
	elif (client = gyro.caracteristique?) :
			client = gyro
	elif (client =filtre.caracteristique?):
			client = filtre

#cr�ation des 3 serveurs handler (1/capteur =>) et d'1 serveur client handlerclient(=> filtre)

accelhandler = ClientHandler(accelhandler,addr)  #remplacer addr par client et identifier les clients par leur adresse?
accelhandler.start(clienthandler)
accelhandler.run(accelhandler)
gyrohandler = ClientHandler(gyrohandler,addr)
gyrohandler.start(gyrohandler)
gyrohandler.run(gyrohandler)
magnethandler = ClientHandler(magnethandler,addr)  #remplacer addr par client et identifier les clients par leur adresse?
magnethandler.start(magnethandler)
magnethandler.run(magnethandler)
filtrehandler = Handler(filtrehandler, addr)
filtrehandler.run(filtrehandler)


#g�re la r�ception et l'envoi des donn�es de l'acc�l�rateur au filtre
#protection des donn�es en lecture et �criture par un cadenas
# m�thode send?

 def accelhandler._msgToSend: 
  data= input("Quel axe?)
	if (data=x) : send 0x3
					
				  send 





#g�re la r�ception et l'envoi des donn�es du magn�tom�tre au filtre


#g�re la r�ception et l'envoi des donn�es du gyroscope au filtre




#enslavement/start?
