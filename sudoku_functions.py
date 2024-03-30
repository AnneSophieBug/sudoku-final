import random
import tkinter as tk
from tkinter import Tk, Frame, Entry, Button, Label, Toplevel
import time

# Règles

def afficher_regles(root):
    rules_window = Toplevel(root)  # Nouvelle fenetre
    rules_window.title("Règles du Sudoku")
    rules_text = ("Règles : Le but du jeu est de remplir la grille avec les numéros de 1 à 9.\n"
                  "Chaque ligne, colonne et carré (qui comporte chacun 9 cases) doit être complété par les numéros SANS répétition.\n"
                  "Ainsi, on doit retrouver une fois chaque nombre dans toutes les lignes, colonnes et carrés.\n\n"
                  "Au début de la partie, quelques cases sont déjà complétées. La difficulté de la partie dépend du nombre de cases déjà complétées.\n"
                  "Il y a trois niveaux :\n"
                  "- Niveau 1 : 45% des cases initialement complétées.\n"
                  "- Niveau 2 : 40% des cases initialement complétées.\n"
                  "- Niveau 3 : 35% des cases initialement complétées.\n\n"
                  "Un système de score est mis en place. Le score initial en début de partie est de 100.\n"
                  "A chaque chiffre correctement placé, vous gagnez 30 points. A chaque erreur vous en perdez 10.\n"
                  "De plus, toutes les 30 secondes, le score diminue de 15 points (ne prenez pas trop votre temps!).\n"
                  "Lorsque la partie est terminée, si la partie jouée était de niveau moyen, le score est multiplié par deux. Si elle était de niveau difficile, par 3.")
    rules_label = Label(rules_window, text=rules_text)  # Mettez les règles du Sudoku ici
    rules_label.pack()

# Conception grille et niveaux de difficulté

def generer_grille_partielle_facile(self, first_time=False):
    self.generer_grille_partielle(0.45)  # 45% de cellules pré-remplies pour le niveau facile
    if first_time:
        self.disable_level_buttons()
    self.start_chronometer()  # Démarrer le chronomètre

def generer_grille_partielle_moyen(self, first_time=False):
    self.generer_grille_partielle(0.40)  # 40% de cellules pré-remplies pour le niveau moyen
    if first_time:
        self.disable_level_buttons()
    self.start_chronometer()  # Démarrer le chronomètre

def generer_grille_partielle_difficile(self, first_time=False):
    self.generer_grille_partielle(0.35)  # 35% de cellules pré-remplies pour le niveau difficile
    if first_time:
        self.disable_level_buttons()
    self.start_chronometer()  # Démarrer le chronomètre

def generer_grille_partielle(self, proportion):
    self.grille_partielle = [[0 for _ in range(9)] for _ in range(9)]
    for i in range(9):
        for j in range(9):
            if random.random() < proportion:
                self.grille_partielle[i][j] = self.grille_complete[i][j]
                self.cells[i][j].insert(0, str(self.grille_partielle[i][j]))
                self.cells[i][j].config(state='readonly')  # Verrouiller les champs d'entrée
            else:
                self.grille_partielle[i][j] = 0
                self.cells[i][j].delete(0, tk.END)  # Effacer la valeur précédente
                self.cells[i][j].config(state='normal')  # Assurez-vous que les autres champs sont éditables

# Conception du chronometre (activer, arreter, pause)

def start_chronometer(self):
    global timing_increment
    if not self.chronometer_running:
        timing_increment = -1
        self.chronometer_running = True
        self.start_time = time.time()
        self.update_chronometer()

def stop_chronometer(self):
    if self.chronometer_running:
        self.chronometer_running = False

def update_chronometer(self):
    if self.chronometer_running:
        elapsed_time = time.time() - self.start_time
        hours = int(elapsed_time // 3600)
        minutes = int((elapsed_time % 3600) // 60)
        seconds = int(elapsed_time % 60)
        time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        self.chronometer_label.config(text=time_str)
        self.root.after(1000, self.update_chronometer)  # Mettre à jour toutes les secondes
        global timing_increment
        timing_increment += 1
        if timing_increment == 30:
            self.lose_timing_point()
            timing_increment = 0

def pause_chronometer(self):
    if self.chronometer_running:
        self.chronometer_running = False
        self.pause_time = time.time()
        self.pause_button.config(state=tk.DISABLED)
        self.resume_button.config(state=tk.NORMAL)
        self.disable_sudoku_grid()
        self.cover_sudoku_grid()  # Masquer la grille de Sudoku

def resume_chronometer(self):
    if not self.chronometer_running:
        self.chronometer_running = True
        self.start_time += time.time() - self.pause_time
        self.pause_button.config(state=tk.NORMAL)
        self.resume_button.config(state=tk.DISABLED)
        self.enable_sudoku_grid()
        self.uncover_sudoku_grid()  # Révéler la grille de Sudoku
        self.update_chronometer()
