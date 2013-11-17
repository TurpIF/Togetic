# A compléter: limites éventuelles des composants

#import
from Server.Listener import Listener
from Server.Handler import Handler
from Server.ClientHandler import ClientHandler
import socket
import i2clibraries
from time import *

#Initialisation de l'adresse du broadcaster et du pipe qu'il utilise
?
#Par quoi se caractérise par défaut un client => créer classe client?

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

#création des 3 serveurs handler (1/capteur =>) et d'1 serveur client handlerclient(=> filtre)

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


#gère la réception et l'envoi des données de l'accélérateur au filtre
#protection des données en lecture et écriture par un cadenas
# méthode send?

 def accelhandler._msgToSend: 
  data= input("Quel axe?)
	if (data=x) : send 0x3
					
				  send 





#gère la réception et l'envoi des données du magnétomètre au filtre


#gère la réception et l'envoi des données du gyroscope au filtre




#enslavement/start?
