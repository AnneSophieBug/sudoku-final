# sudoku-final


## Prérequis 

1) Posséder un interpréteur python afin d'exécuter un code provenant d'un fichier .py
2) Savoir compter de 1 à 9


## Introduction   (manque à mieux expliquer le découpage du score)

Dans le cadre du projet de programmation de Master1, nous avons décidé de créer, grâce à python, un jeu de Sudoku. Le code est disponible dans ce repository actuel. Il a été découpé de la manière suivante : 

Dans le fichier "main" se trouve le code à exécuter afin de générer la grille.
Dans le fichier ......
Enfin, dans le fichier "Publipostage" se trouve un autre code sur lequel nous reviendrons un peu plus loin.

La finalité de notre projet est de pouvoir partager le jeu que nous avons créé à plusieurs personnes afin de se défier en tentant d'obtenir le meilleur score possible.


## 1) Fonctionnement de la grille 

Pour obtenir la grille du jeu, il suffit d'exécuter uniquement le code principal, à partir du fichier .py que nous aurons envoyé au préalable aux personnes invitées à jouer. Le jeu va alors s'afficher dans une fenêtre.
A gauche se trouve la grille à remplir et à droite, plusieurs boutons. Pour commencer une partie, il suffit de sélectionner "Nouvelle Partie" puis de choisir un niveau de difficulté. Le jeu ainsi que le chronomètre se lance. En fonction du niveau choisi, un nombre différent de chiffres sera déjà remplis : plus la partie est facile, plus il y aura de chiffres déjà placés. Pour remplir la grille, il faut sélectionner une case et ensuite le chiffre que l'on veut y inscrire. En cas de doute, les règles du jeu sont disponibles en haut à droite. Il est possible de mettre pause puis de reprendre le jeu, d'effacer le contenu de la case sélectionnée ainsi que de demander une aide qui donnera la réponse pour une case vide. A la fin de la partie, il faut cliquer sur "Résoudre", les chiffres n'ayant pas été placés correctement s'afficheront en rouge. Le score évolue au cours du jeu et est affiché en bas. Il est calculé de la manière suivante : En début de partie le score est de 100. Lorsque un nombre est placé correctement, il augmente de 30 et diminue de 10 en cas d'erreur. Toutes les 30 secondes, le score diminue de 15 points. A la fin de la partie, il est multiplié par 2 ou 3 en fonction de si la partie était de niveau moyen ou difficile.


## 2) Partage du jeu

Pour partager notre jeu, nous avons choisi de le faire par mail. Ainsi nous avons coder en python l'envoi de mails en masse (publipostage). Nous avons créé une adresse mail spécialement pour le projet : sudoku.python@gmail.com.
Fonctionnement : il faut tout d'abord se connecter au serveur smtp de gmail et à la messagerie (nom d'utilisateur, mot de passe) depuis le code. Pour des raisons de sécurité, le mot de passe à renseigner n'est plus, depuis début 2024, le mot de passe de la messagerie elle-même, mais un autre créé exprès depuis les paramètres de celle-ci et qui autorise l'exécuteur de code à se connecter. Il faut ensuite renseigner l'objet du mail, le contenu ainsi que les destinataires. Pour finir, le plus important est d'attacher la pièce jointe comportenant notre code sous la forme d'un fichier .py. Afin de faciliter le processus, nous sommes parties de l'hypothèse que les personnes qui recevront le code savent lancer son exécution et possèdent notamment python sur leur ordinateur. 
Ainsi, des mails sont envoyés comportant en pièce jointe le code que les personnes devront ouvrir afin de jouer.


## 3) Récupérer les scores (mettre plus de details)

Enfin, nous avons mis en place un système permettant de récupérer le score des personnes ayant joué afin de procéder à un classement.

