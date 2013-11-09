Togetic
=======

Application utilisant une centrale inertiel pour récupérer la position d'un
objet et contrôler une caméra dans blender.  L'application est découpée en
différentes tâches permettant d'avoir des éléments dédiés communiquants par
IPC.  Les IPC utilisés sont des sockets sur le domaine UNIX.

L'architecture globale est la suivante :
- Demande et écoute des message I2C provenant des différents capteurs puis
  retransmission directe (sans modification des données récupérées) avec un
  socket.
- Ecoute des données sur le socket précédemment fait puis filtrage puis calcul
  de la position relative puis renvoie sur un socket.
- Obtention de la position puis modification de la caméra principale d'une
  scène [Blender][] en utilisant le BGE.

## Diffusion des messages I2C

## Filtrage des données et calcul de la position

## Affichage sur une courbe des données

## Blender

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
- [Python 2.7][]
- [Matplotlib][]
- [Blender][] (utilisé avec la 2.69)

## Auteurs
- [Pierre Turpin][]
- [Matthieu Falce][]
- [Sarah Leclerc][]
- [Stéphane Baudrand][]
- [Franz Laugt][]

[Python 2.7]: http://www.python.org/download/releases/2.7
[Matplotlib]: http://matplotlib.org
[Blender]: http://www.blender.org
[Pierre Turpin]: https://github.com/TurpIF
[Matthieu Falce]: #
[Sarah Leclerc]: https://github.com/SarahLeclerc
[Stéphane Baudrand]: https://github.com/Stefjeanne
[Franz Laugt]: https://github.com/znarf94
