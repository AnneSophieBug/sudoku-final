#!/usr/bin/env python
# coding: utf-8

# In[3]:


import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


# Connexion au serveur smtp et à l'adresse gmail, grâce à un mot de passe unique
server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
server.login("sudoku.python@gmail.com", "eaqh niof dvqv qjih")

## Création du mail
# Mise en forme du mail
expediteur = 'sudoku.python@gmail.com'
objet = 'Projet de programmation Master1 SE'
corps_message = 'Salut c\'est Ninho, \n\n\n\n\n...Et non c\'est pas lui.  \nMais c\'est Lisa, Julie et Anne-Sophie, étudiante en M1 Statistiques et Econométrie, qui vous invitent à jouer à une petite partie de Sudoku. Cela vous prendra entre 5 minutes et 118 jours selon votre niveau. \nPour ce faire, vous devez télécharger le fichier zip ci-joint et exécutez le code principal nommé "code_sudoku" via un interpréteur Python tel que Spyder. Vous pourrez choisir le niveau de difficulté entre facile (trop la honte), moyen et difficile. Un score sera calculé en fonction de votre performance. Vous pourrez retrouver plus de détails ainsi que les règles du sudoku en cliquant sur le bouton "Règles".\nEnjoy! \n\n\n Enfin, vous trouverez la totalité de notre code à l\'adresse suivante https://github.com/AnneSophieBug/sudoku-final'

# Création du message
message = MIMEMultipart()
message['From'] = expediteur
message['Subject'] = objet

# Ajout du corps du message
message.attach(MIMEText(corps_message, 'plain'))

## Traitement de la pièce jointe
# Chemin vers la pièce jointe que l'on renomme, par défaut le nom est le chemin d'accès
chemin_piece_jointe = 'C:/Users/annes/Downloads/sudoku.zip'
nom_piece_jointe = "Sudoku.zip"

# Lecture du fichier joint
with open(chemin_piece_jointe, 'rb') as piece_jointe:
    piece_jointe_mime = MIMEBase('application', 'octet-stream')
    piece_jointe_mime.set_payload(piece_jointe.read())

# Encodage de la pièce jointe en base64
encoders.encode_base64(piece_jointe_mime)

# Ajout de l'en-tête de la pièce jointe
piece_jointe_mime.add_header(
    'Content-Disposition', f'attachment; filename= {nom_piece_jointe}')

# Attache de la pièce jointe au message
message.attach(piece_jointe_mime)

## Envoi
# Envoi du mail en indiquant les destinataires
server.sendmail(expediteur, ["p.pelletier@unistra.fr","anne-sophie.bugeia@sfr.fr","julie.bailly2@etu.unistra.fr", "lisa.masson2@etu.unistra.fr", "anne-sophie.bugeia@etu.unistra.fr"], message.as_string())

# Déconnexion au serveur
server.quit()


# In[ ]:




