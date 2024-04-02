import tkinter as tk 
from tkinter import Tk, Frame, Entry, Button, Label, Toplevel
from tkinter import ttk
import random
import time
import datetime

class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")
        self.grille_complete = [[0 for _ in range(9)] for _ in range(9)]
        self.grille_partielle = [[0 for _ in range(9)] for _ in range(9)]
        self.cells = [[None for _ in range(9)] for _ in range(9)]
        self.selected_cell = None
        self.chronometer_running = False
        global score # rend accessible la variable score
        score = 100 # score initilalise à 100
        self.create_widgets()
        
    def afficher_regles(self):
        # Créer une nouvelle fenêtre pour afficher les règles du Sudoku
        rules_window = Toplevel(self.root)
        rules_window.title("Règles du Sudoku")
        
        # Afficher les regles
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
        
    def create_widgets(self):
        # Créer des cadres pour les régions 3x3 sans marges
        self.frames = [[None for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.frames[i][j] = tk.Frame(self.root, borderwidth=2, relief="ridge")
                self.frames[i][j].grid(row=i*4, column=j*1, rowspan=4, columnspan=1, padx=1, pady=1, sticky="nsew")
        # Créer les entrées pour chaque cellule avec un espacement réduit
        for i in range(9):
            for j in range(9):
                frame_row = i // 3
                frame_col = j // 3
                self.cells[i][j] = tk.Entry(self.frames[frame_row][frame_col], width=2, font=('Arial', 18))
                self.cells[i][j].grid(row=i%3, column=j%3)
                self.cells[i][j].bind("<Button-1>", lambda event, i=i, j=j: self.update_selected_cell(i, j))
        # Créer les boutons pour les chiffres de 1 à 9
        self.number_buttons = []
        for num in range(1, 10):
            button = tk.Button(self.root, text=str(num), command=lambda n=num: self.place_number(n))
            button.grid(row=5, column=num+5, pady=5)
            self.number_buttons.append(button)   
        self.number_buttons_label = tk.Label(self.root, text="Clavier numérique :")
        self.number_buttons_label.grid(row=5, column=3, columnspan=3, pady=5)
        
        # Boutons pour les niveaux de difficulté
        self.difficulty_label = tk.Label(self.root, text="Niveau de difficulté :")
        self.difficulty_label.grid(row=0, column=3, columnspan=3, pady=5)
        self.easy_button = tk.Button(self.root, text="Facile", command=lambda: self.generer_grille_partielle_facile(True))
        self.easy_button.grid(row=1, column=4, columnspan=3, pady=5)
        self.medium_button = tk.Button(self.root, text="Moyen", command=lambda: self.generer_grille_partielle_moyen(True))
        self.medium_button.grid(row=1, column=7, columnspan=3, pady=5)
        self.hard_button = tk.Button(self.root, text="Difficile", command=lambda: self.generer_grille_partielle_difficile(True))
        self.hard_button.grid(row=1, column=11, columnspan=3, pady=5)
        
        # Bouton "Nouvelle partie"
        self.new_game_button = tk.Button(self.root, text="Nouvelle partie", command=self.nouvelle_partie)
        self.new_game_button.grid(row=8, column=3, columnspan=3, pady=5)
        
        # Bouton "Resoudre"
        self.solve_button = tk.Button(self.root, text="Résoudre", command=self.resoudre_sudoku)
        self.solve_button.grid(row=10, column=3, columnspan=3, pady=5)
        
        # Boutons pour le chronomètre
        ## Affichage du chronometre
        self.chronometer_label = tk.Label(self.root, text="00:00:00", font=("Arial", 16))
        self.chronometer_label.grid(row=4, column=5, columnspan=3, pady=5)
        self.chrono_label = tk.Label(self.root, text="Chronomètre : ")
        self.chrono_label.grid(row=3, column=3, columnspan=3, pady=5)
        self.disable_level_buttons()
        
        ## Mettre en pause et reprendre le chronometre
        self.pause_button = tk.Button(self.root, text="Pause", command=self.pause_chronometer)
        self.pause_button.grid(row=3, column=7, columnspan=3, pady=5)
        self.resume_button = tk.Button(self.root, text="Reprendre", command=self.resume_chronometer, state=tk.DISABLED)
        self.resume_button.grid(row=3, column=11, columnspan=3, pady=5)
        
        # Bouton "Règles"
        self.rules_button = Button(self.root, text="Règles", command=self.afficher_regles)
        self.rules_button.grid(row=0, column=12, columnspan=3, pady=5)  # Vous pouvez ajuster la position et le padding
        
        # Bouton "Effacer"
        self.clear_button = Button(self.root, text="Effacer", command=self.effacer_case)
        self.clear_button.grid(row=6, column=12, columnspan=3, pady=5)  # Vous pouvez ajuster la position et le padding
        
        # Affichage et bouton pour le score
        self.score_label = tk.Label(self.root, text="Score : "+str(score), font=("Arial, 13"))
        self.score_label.grid(row=12, column=4, columnspan=3, pady=5)
        
        self.scores_button = tk.Button(self.root, text="Afficher les scores", command=self.display_scores)
        self.scores_button.grid(row=13, column=3, columnspan=3, pady=5)  # Placez le bouton dans la grille

        # Attribut pour stocker la case actuellement sélectionnée
        self.selected_cell = None
        
        
        # Bouton "AIde"
        self.hint_button = tk.Button(self.root, text="Aide", command=self.show_hint)
        self.hint_button.grid(row=10, column=7, columnspan=3, pady=5)
    
    def disable_level_buttons(self): # Desactive les boutons de niveau de difficulté
        self.easy_button.config(state=tk.DISABLED)
        self.medium_button.config(state=tk.DISABLED)
        self.hard_button.config(state=tk.DISABLED)
    
    def enable_level_buttons(self): # Active les boutons de niveau de difficulté
        self.easy_button.config(state=tk.NORMAL)
        self.medium_button.config(state=tk.NORMAL)
        self.hard_button.config(state=tk.NORMAL)
    
    def place_number(self, num): # Place un chiffre dans la case sélectionné
        if self.selected_cell:
            row, col = self.selected_cell
            self.cells[row][col].delete(0, tk.END)
            self.cells[row][col].insert(0, str(num))
            self.grille_partielle[row][col] = num
    
    def update_selected_cell(self, row, col): # Met à jour la case sélectionné
        self.selected_cell = (row, col)
    
    def generer_grille_complete(self):
        def remplir_grille(grille):
            row, col = self.trouver_case_vide(grille)
            if row is None:
                return True
            chiffres = list(range(1, 10))
            random.shuffle(chiffres)
            for num in chiffres:
                if self.est_valide(grille, num, (row, col)):
                    grille[row][col] = num
                    if remplir_grille(grille):
                        return True
                    grille[row][col] = 0
            return False
        remplir_grille(self.grille_complete)
    
    # Les niveaux de difficultés de la grille
    def generer_grille_partielle_facile(self, first_time=False):
        self.generer_grille_partielle(0.45)  # 45% de cellules pré-remplies pour le niveau facile
        if first_time:
            self.disable_level_buttons()
        # Démarrer le chronomètre
        self.start_chronometer()
    
    def generer_grille_partielle_moyen(self, first_time=False):
        self.generer_grille_partielle(0.40)  # 40% de cellules pré-remplies pour le niveau moyen
        if first_time:
            self.disable_level_buttons()
        self.start_chronometer()
    
    def generer_grille_partielle_difficile(self, first_time=False):
        self.generer_grille_partielle(0.35)  # 35% de cellules pré-remplies pour le niveau difficile
        if first_time:
            self.disable_level_buttons()
        self.start_chronometer()
    
    def generer_grille_partielle(self, proportion):
        self.grille_partielle = [[0 for _ in range(9)] for _ in range(9)]
        for i in range(9):
            for j in range(9):
                if random.random() < proportion:
                    self.grille_partielle[i][j] = self.grille_complete[i][j]
                    self.cells[i][j].insert(0, str(self.grille_partielle[i][j]))
                    self.cells[i][j].config(state='readonly')  # Verrouille les champs d'entrée
                else:
                    self.grille_partielle[i][j] = 0
                    self.cells[i][j].delete(0, tk.END)  # Efface la valeur précédente
                    self.cells[i][j].config(state='normal') 
    
    def corriger_grille(self): # Corrige la grille en fonction de la grille complète
        global score # accede à la varaible globale score
        for i in range(9):
            for j in range(9):
                cell_value = self.cells[i][j].get()
                if cell_value=="" :
                    pass
                elif not cell_value.isdigit() or int(cell_value) not in range(1, 10):
                    self.cells[i][j].config(fg="red")  # Mettre en rouge si la valeur n'est pas un chiffre entre 1 et 9
                    score -= 10 # erreur donc -10 points
                    self.score_label.config(text="Score : "+str(score)) # affichage du score actualise
                elif int(cell_value) != self.grille_complete[i][j] :
                    self.cells[i][j].config(fg="red")  # Mettre en rouge si la valeur est incorrecte
                    score -= 10 # erreur donc -10 points
                    self.score_label.config(text="Score : "+str(score)) # affichage du score actualise
                elif int(cell_value) == self.grille_complete[i][j] and self.grille_partielle[i][j]==0:
                    self.cells[i][j].config(fg="green")  # Mettre en vert si la valeur est correcte
                    score += 30 # juste donc -10 points
                    self.score_label.config(text="Score : "+str(score)) # affichage du score actualise
                
    def remplir_grille(self):
        for i in range(9):
            for j in range(9):
                if self.cells[i][j].get() == "":
                    self.cells[i][j].insert(0, str(self.grille_complete[i][j]))
                    self.cells[i][j].config(fg="blue")  # Mettre en bleu les valeurs entrees par l'ordinateur
    
    def resoudre_sudoku(self):
        self.stop_chronometer()
        self.corriger_grille()
        self.remplir_grille()
          
    def check_solution(self):
        for i in range(9):
            for j in range(9):
                if self.grille_partielle[i][j] != self.grille_complete[i][j]:
                    print(f"Erreur à la position ({i}, {j}): attendu {self.grille_complete[i][j]}, trouvé {self.grille_partielle[i][j]}.")
    
    def trouver_case_vide(self, grille):
        for i in range(9):
            for j in range(9):
                if grille[i][j] == 0:
                    return i, j
        return None, None
    
    def est_valide(self, grille, num, position): #Verifie si un numero est valide dans une position donnée
        row, col = position
        for i in range(9):
            if grille[row][i] == num and col != i:
                return False
        for i in range(9):
            if grille[i][col] == num and row != i:
                return False
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if grille[i][j] == num and (i, j) != position:
                    return False
        return True
    
    def nouvelle_partie(self):
        self.enable_level_buttons()
    # Effacer toutes les valeurs des cases et réinitialiser la couleur du texte
        for i in range(9):
            for j in range(9):
                self.cells[i][j].delete(0, tk.END)
                self.cells[i][j].config(fg="black")  
                self.cells[i][j].config(state='normal')  
                self.cells[i][j].delete(0, tk.END)  # Effacer à nouveau pour s'assurer que la case est vide
    
    # Réinitialiser la grille partielle
        self.grille_partielle = [[0 for _ in range(9)] for _ in range(9)]
    # Remettre le score à 100
        global score
        score = 100
        self.score_label.config(text="Score : "+str(score))  
    
    # Fonction pour le chronometre
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
            self.root.after(1000, self.update_chronometer)  
            global timing_increment
            timing_increment += 1
            if timing_increment == 30 :
                self.lose_timing_point()
                timing_increment = 0
    
    def pause_chronometer(self):
        if self.chronometer_running:
            self.chronometer_running = False
            self.pause_time = time.time()
            self.pause_button.config(state=tk.DISABLED)
            self.resume_button.config(state=tk.NORMAL)
            self.disable_sudoku_grid()
            self.cover_sudoku_grid()  
    
    def resume_chronometer(self):
        if not self.chronometer_running:
            self.chronometer_running = True
            self.start_time += time.time() - self.pause_time
            self.pause_button.config(state=tk.NORMAL)
            self.resume_button.config(state=tk.DISABLED)
            self.enable_sudoku_grid()
            self.uncover_sudoku_grid()  
            self.update_chronometer()
    
    # Calcul de score
    def lose_timing_point(self):
        global score
        score -= 15
        self.score_label.config(fg="red", text="Score : "+str(score))
        self.root.after(800, self.change_score_color)
    
    def change_score_color(self):
        self.score_label.config(fg="black")
    
    def disable_sudoku_grid(self):
        for row in self.cells:
            for cell in row:
                cell.config(state=tk.DISABLED)
    
    def enable_sudoku_grid(self):
        for row in self.cells:
            for cell in row:
                cell.config(state=tk.NORMAL)
            
    def cover_sudoku_grid(self):
        canvas_width = 320
        canvas_height = 325
        self.cover = tk.Canvas(self.root, bg="light gray", width=canvas_width, height=canvas_height)
        self.cover.place(x=0, y=0) 
    
    def uncover_sudoku_grid(self):
        self.cover.destroy()
    
    def effacer_case(self):
        if self.selected_cell is not None:
            row, col = self.selected_cell
            # Efface le contenu de la case sélectionnée
            self.cells[row][col].delete(0, tk.END)
            
    def show_hint(self):
        if not self.chronometer_running:
            return  # Ne pas montrer d'aide si le chronomètre n'est pas en cours
        empty_cells = [(i, j) for i in range(9) for j in range(9) if self.grille_partielle[i][j] == 0]
        while empty_cells:
            row, col = random.choice(empty_cells)
            if self.cells[row][col].get() == '':  
                self.cells[row][col].insert(0, str(self.grille_complete[row][col]))
                break
            else:
                empty_cells.remove((row, col))
                
    def display_scores(self):
        global score
        self.save_score_with_timestamp(score)
        try:
            # Lire les scores à partir du fichier et les ajouter à la liste
            with open('scores.txt', 'r') as file:
                scores = [line.strip() for line in file.readlines()]
                print(scores)
        except FileNotFoundError:
            # Si le fichier n'existe pas ou s'il est vide, afficher un message approprié
            print("Aucun score n'est enregistré.")
            return
        dernier=scores[-1]
        # Trier les scores dans l'ordre décroissant
        scores.sort(reverse=True,key=triD)
        print(dernier)
        # Créer une nouvelle fenêtre pour afficher les scores
        scores_window = Toplevel(self.root)
        scores_window.title("Scores")
        
        
        compteur=0
        dernier_trouve=False
        # Afficher les scores dans la fenêtre
        for i, score in enumerate(scores):
            if score==dernier:
                label = Label(scores_window, text=f"{i+1}. Dernière partie{score[19:]}")
                dernier_trouve=True
            elif compteur<5:
                label = Label(scores_window, text=f"{i+1}. {score}")
                compteur+=1
            label.pack()
            if compteur==5 and dernier_trouve:
                break
            
    def save_score_with_timestamp(self, score):
        # Obtenir la date et l'heure actuelles
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Écrire le score et le timestamp dans le fichier
        with open('scores.txt', 'a') as file:
            print(file.write(f"{timestamp}: Score - {score}\n"))


def triD(elem):
    if len(elem) < 4:
        return -100
    
    elem = elem[-4:]
    
    if elem[0] == '-':
        if elem[1] == ' ':
            elem = elem[2:]
        else:
            return -100
            
    return int(elem)

root = tk.Tk()
app = SudokuGUI(root)
app.generer_grille_complete()  
root.mainloop()
