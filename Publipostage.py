{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 2,
   "id": "facafb9a",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "(221,\n",
       " b'2.0.0 closing connection n8-20020a5d6b88000000b0033ec8739918sm1418682wrx.41 - gsmtp')"
      ]
     },
     "execution_count": 2,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "import smtplib\n",
    "from email.mime.text import MIMEText\n",
    "from email.mime.multipart import MIMEMultipart\n",
    "from email.mime.base import MIMEBase\n",
    "from email import encoders\n",
    "\n",
    "\n",
    "# Connexion au serveur smtp et à l'adresse gmail, grâce à un mot de passe unique\n",
    "server = smtplib.SMTP_SSL('smtp.gmail.com', 465)\n",
    "server.login(\"sudoku.python@gmail.com\", \"eaqh niof dvqv qjih\")\n",
    "\n",
    "## Création du mail\n",
    "# Mise en forme du mail\n",
    "expediteur = 'sudoku.python@gmail.com'\n",
    "objet = 'Sudoku'\n",
    "corps_message = 'Salut c\\'est Ninho, \\n\\n\\n\\n\\n...Et non c\\'est pas lui.  \\nMais c\\'est Lisa, Julie et Anne-Sophie, étudiante en M1 Statistiques et Econométrie, qui vous invitent à jouer à une petite partie de Sudoku. Cela vous prendra entre 5 minutes et 118 jours selon votre niveau. \\nPour ce faire, ouvrez le fichier ci-joint et exécutez le code via un interpréteur Python. Vous pourrez choisir le niveau de difficulté entre facile (trop la honte), moyen et difficile. Un score sera calculé en fonction de votre performance. Vous pourrez retrouver plus de détails ainsi que les règles du sudoku en cliquant sur le bouton \"Règles\".\\nEnjoy !'\n",
    "\n",
    "# Création du message\n",
    "message = MIMEMultipart()\n",
    "message['From'] = expediteur\n",
    "message['Subject'] = objet\n",
    "\n",
    "# Ajout du corps du message\n",
    "message.attach(MIMEText(corps_message, 'plain'))\n",
    "\n",
    "## Traitement de la pièce jointe\n",
    "# Chemin vers la pièce jointe que l'on renomme, par défaut le nom est le chemin d'accès\n",
    "chemin_piece_jointe = 'C:/Users/annes/Downloads/pj_test.py'\n",
    "nom_piece_jointe = \"Sudoku.py\"\n",
    "\n",
    "# Lecture du fichier joint\n",
    "with open(chemin_piece_jointe, 'rb') as piece_jointe:\n",
    "    piece_jointe_mime = MIMEBase('application', 'octet-stream')\n",
    "    piece_jointe_mime.set_payload(piece_jointe.read())\n",
    "\n",
    "# Encodage de la pièce jointe en base64\n",
    "encoders.encode_base64(piece_jointe_mime)\n",
    "\n",
    "# Ajout de l'en-tête de la pièce jointe\n",
    "piece_jointe_mime.add_header(\n",
    "    'Content-Disposition', f'attachment; filename= {nom_piece_jointe}')\n",
    "\n",
    "# Attache de la pièce jointe au message\n",
    "message.attach(piece_jointe_mime)\n",
    "\n",
    "## Envoi\n",
    "# Envoi du mail en indiquant les destinataires\n",
    "server.sendmail(expediteur, [\"anne-sophie.bugeia@sfr.fr\", \"annesophie.bugeia@gmail.com\"], message.as_string())\n",
    "\n",
    "# Déconnexion au serveur\n",
    "server.quit()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "eccd817f",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
