Togetic
=======

![Togetic][]

Application utilisant une centrale inertiel pour récupérer la position d'un
objet et contrôler une caméra dans blender.  L'application est découpée en
différentes tâches permettant d'avoir des éléments dédiés communiquants par
IPC.  Les IPC utilisés sont des sockets sur le domaine UNIX.

L'architecture globale est la suivante :
- Demande et écoute des message I2C provenant des différents capteurs puis
  retransmission directe (sans modification des données récupérées) au PC via
  communication Serial (UBS).
- Ecoute des informations bruts sur le sérial et renvoie sur un socket.
- Ecoute des données sur le socket précédemment fait puis filtrage et calcul de
  la position relative puis renvoie sur un socket.
- Obtention de la position puis modification de la caméra principale d'une
  scène [Blender][] en utilisant le BGE.

Voici un schéma de l'architecture globale de l'application :
![Architecture][]

## Diffusion des messages I2C

## Filtrage des données et calcul de la position
![Filtre][]

## Affichage sur une courbe des données

## Blender
Cette partie écoute continuellement sur un socket dont l'adresse est passée en
paramètre. Les messages reçus sont alors vérifiés puis utilisés dans le cas où
ils ont un format valide (voir le protocole de communication utilisé en sortie
du filtre). Les autres messages sont tous ignorés. Les messages, lorsqu'ils
sont utilisés, modifient une données partagées correspondant à la position
relative de la personne. Pour éviter le blocage des appels systèmes pour lire
sur le socket de communication, cette partie est encapsulé dans un fil
d'exécution. La position relative qui est alors une mémoire partagé est
protégée par un verrou de mutex.

Un autre fil d'exécution est utilisé pour modifier la position de la caméra
principale d'une scène blender. La lecture de la donnée partagée est également
protégée par son mutex associé. Cette fonction est automatiquement appelé par
blender et représente un controller blender activé par un sensor always à une
fréquence prédéfinie. Lorsque cette fonction est appelé pour la première fois,
elle crée le fil d'exécution d'écoute sur le socket. Ce dernier doit alors
s'arreter lorsque le controller l'est.

Pour lancer cette partie, il faut d'abord lancer blender. Un script de
lancement est présent et permet également de controller l'adresse par paramètre
l'adresse du socket de communication. Ce script ouvrira la scène blender,
ajoutera un sensor always associé à un controlleur python exécutant la fonction
définie ci-dessus. Ensuite, il placera la fenetre en plein écran avec une vue
caméra sur la scène et lancera le moteur de jeu de blender.

Son utilisation est :

    ./runBlender.py --input=<socket_filename> --blender=<blender_filename>

Pour le moment, le lancement de blender n'est pas totalement géré. Il faut donc
exécuter manuellement le game engine de blender et préconfigurer la scène en
ajoutant le sensor associé au controlleur.

Il existe également un fichier contenant un serveur de test envoyant une
position suivant une trajectoire de cercle pour tester cette partie de
l'application. Il faut d'abord lancer le serveur puis blender :

    ./TestServer.py --output=<path_to_socket> &
    ./runBlender.py --input=<socket_filename> --blender=<blender_filename>

## Pourquoi Togetic ?
Le nom du projet est vraiment simple à retrouver et il suffit d'appliquer une
toute petite formule vraiment banale (en python) :

    N = sum(set(map(lambda x: ord(x.upper()) - ord('A') + 1, reduce(operator.add, L))))

- On considère une liste de mot L.
- On réduit cette liste à une chaîne de caractères contenant tous les mots.
- On calcul alors pour chaque lettre de cette chaîne sa position dans
  l'alphabet (A étant à la position 1).
- On retire ensuite les doublons.
- Puis on fait la sommes de la liste résultantes.

Lorsque la liste L contient la liste des prénoms des auteurs, on a alors N=176.
Ce nombre correspond au numéro du pokémon Togetic.

## Requis
- [Python 3.3][]
- [Matplotlib][]
- [Blender][] (utilisé avec la 2.69)

Bibliothèques Arduino :
- [ADXL345][]
- [HMC5883L][]
- [L3G4200D][]

## Auteurs
- [Franz Laugt][]
- [Matthieu Falce][]
- [Pierre Turpin][]
- [Sarah Leclerc][]
- [Stéphane Baudrand][]

[Architecture]: ../../blob/master/docs/Architecture.png?raw=true
[Filtre]: ../../blob/master/docs/Filter.png?raw=true
[Togetic]: ../../blob/master/assets/togetic.png?raw=true
[Python 3.3]: http://www.python.org/download/releases/3.3
[Matplotlib]: http://matplotlib.org
[Blender]: http://www.blender.org
[Pierre Turpin]: https://github.com/TurpIF
[Matthieu Falce]: https://github.com/ice3
[Sarah Leclerc]: https://github.com/SarahLeclerc
[Stéphane Baudrand]: https://github.com/Stefjeanne
[Franz Laugt]: https://github.com/znarf94
[Quick2wire]: https://github.com/quick2wire/quick2wire-python-api
[ADXL345]: http://code.google.com/p/adxl345driver/
[HMC5883L]: http://www.loveelectronics.co.uk/Tutorials/8/hmc5883l-tutorial-and-arduino-library
[L3G4200D]: http://bildr.org/2011/06/l3g4200d-arduino/
