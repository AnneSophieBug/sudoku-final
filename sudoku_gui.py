import random
import tkinter as tk
from tkinter import Toplevel, Frame, Entry, Button, Label
import time
from sudoku_functions import afficher_regles, pause_chronometer, resume_chronometer, \
                              generer_grille_partielle_facile, generer_grille_partielle_moyen, \
                              generer_grille_partielle_difficile

class SudokuGUI:
    def __init__(self, root): 
        self.root = root
        self.root.title("Sudoku Solver")
        self.grille_complete = [[0 for _ in range(9)] for _ in range(9)]
        self.grille_partielle = [[0 for _ in range(9)] for _ in range(9)]
        self.cells = [[None for _ in range(9)] for _ in range(9)]
        self.selected_cell = None
        self.chronometer_running = False
        global score
        score = 100

        self.create_widgets()
        self.generer_grille_complete() 
        
    def create_widgets(self): 
        self.frames = [[None for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.frames[i][j] = tk.Frame(self.root, borderwidth=2, relief="ridge")
                self.frames[i][j].grid(row=i*4, column=j*1, rowspan=4, columnspan=1, padx=1, pady=1, sticky="nsew")

        for i in range(9):
            for j in range(9):
                frame_row = i // 3
                frame_col = j // 3
                self.cells[i][j] = tk.Entry(self.frames[frame_row][frame_col], width=2, font=('Arial', 18))
                self.cells[i][j].grid(row=i%3, column=j%3)
                self.cells[i][j].bind("<Button-1>", lambda event, i=i, j=j: self.update_selected_cell(i, j))

        self.number_buttons = []
        for num in range(1, 10):
            button = tk.Button(self.root, text=str(num), command=lambda n=num: self.place_number(n))
            button.grid(row=5, column=2+num, pady=5)
            self.number_buttons.append(button)

        self.number_buttons_label = tk.Label(self.root, text="Clavier numérique :")
        self.number_buttons_label.grid(row=4, column=3, columnspan=3, pady=5)

        self.difficulty_label = tk.Label(self.root, text="Niveau de difficulté :")
        self.difficulty_label.grid(row=0, column=3, columnspan=3, pady=5)
        self.easy_button = tk.Button(self.root, text="Facile", command=lambda: self.generer_grille_partielle_facile(True))
        self.easy_button.grid(row=1, column=3, columnspan=3, pady=5)
        self.medium_button = tk.Button(self.root, text="Moyen", command=lambda: self.generer_grille_partielle_moyen(True))
        self.medium_button.grid(row=1, column=5, columnspan=3, pady=5)
        self.hard_button = tk.Button(self.root, text="Difficile", command=lambda: self.generer_grille_partielle_difficile(True))
        self.hard_button.grid(row=1, column=7, columnspan=3, pady=5)

        self.new_game_button = tk.Button(self.root, text="Nouvelle partie", command=self.nouvelle_partie)
        self.new_game_button.grid(row=7, column=5, columnspan=3, pady=5)

        self.solve_button = tk.Button(self.root, text="Résoudre", command=self.resoudre_sudoku)
        self.solve_button.grid(row=8, column=5, columnspan=3, pady=5)

        self.chronometer_label = tk.Label(self.root, text="00:00:00", font=("Arial", 16))
        self.chronometer_label.grid(row=3, column=5, columnspan=3, pady=5)
        self.chrono_label = tk.Label(self.root, text="Chronomètre : ")
        self.chrono_label.grid(row=3, column=3, columnspan=3, pady=5)

        self.rules_button = Button(self.root, text="Règles", command=lambda: afficher_regles(self.root))
        self.rules_button.grid(row=0, column=10, columnspan=3, pady=5)

        self.clear_button = Button(self.root, text="Effacer", command=self.effacer_case)
        self.clear_button.grid(row=4, column=10, columnspan=3, pady=5)

        self.score_label = tk.Label(self.root, text="Score : "+str(score), font=("Arial, 13"))
        self.score_label.grid(row=10, column=5, columnspan=3, pady=5)

        self.pause_button = tk.Button(self.root, text="Pause", command=pause_chronometer)
        self.pause_button.grid(row=3, column=7, columnspan=3, pady=5)

        self.resume_button = tk.Button(self.root, text="Reprendre", command=resume_chronometer, state=tk.DISABLED)
        self.resume_button.grid(row=3, column=10, columnspan=3, pady=5)

        self.hint_button = tk.Button(self.root, text="Aide", command=self.show_hint)
        self.hint_button.grid(row=9, column=5, columnspan=3, pady=5)

    def place_number(self, num): 
        if self.selected_cell:
            row, col = self.selected_cell
            self.cells[row][col].delete(0, tk.END)
            self.cells[row][col].insert(0, str(num))
            self.grille_partielle[row][col] = num

    def update_selected_cell(self, row, col): 
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

    def resoudre_sudoku(self): 
        self.stop_chronometer()
        self.corriger_grille()
        self.remplir_grille()
        self.check_solution()

    def nouvelle_partie(self): 
        self.enable_level_buttons()
        self.effacer_grille()

    def stop_chronometer(self): 
        if self.chronometer_running:
            self.chronometer_running = False

    def corriger_grille(self): 
        global score
        for i in range(9):
            for j in range(9):
                cell_value = self.cells[i][j].get()
                if cell_value == "":
                    pass
                elif not cell_value.isdigit() or int(cell_value) not in range(1, 10):
                    self.cells[i][j].config(fg="red")
                    score -= 10
                    self.score_label.config(text="Score : "+str(score))
                elif int(cell_value) != self.grille_complete[i][j]:
                    self.cells[i][j].config(fg="red")
                    score -= 10
                    self.score_label.config(text="Score : "+str(score))
                elif int(cell_value) == self.grille_complete[i][j] and self.grille_partielle[i][j] == 0:
                    self.cells[i][j].config(fg="green")
                    score += 30
                    self.score_label.config(text="Score : "+str(score))

    def effacer_grille(self): 
        for i in range(9):
            for j in range(9):
                self.cells[i][j].delete(0, tk.END)
                self.cells[i][j].config(fg="black")
                self.cells[i][j].config(state='normal')

    def effacer_case(self): 
        if self.selected_cell is not None:
            row, col = self.selected_cell
            self.cells[row][col].delete(0, tk.END)

    def check_solution(self): 
        for i in range(9):
            for j in range(9):
                if self.grille_partielle[i][j] != self.grille_complete[i][j]:
                    print(f"Erreur à la position ({i}, {j}): attendu {self.grille_complete[i][j]}, trouvé {self.grille_partielle[i][j]}.")

    def show_hint(self): 
        if not self.chronometer_running:
            return
        empty_cells = [(i, j) for i in range(9) for j in range(9) if self.grille_partielle[i][j] == 0]
        while empty_cells:
            row, col = random.choice(empty_cells)
            if self.cells[row][col].get() == '':
                self.cells[row][col].insert(0, str(self.grille_complete[row][col]))
                break
            else:
                empty_cells.remove((row, col))

    def trouver_case_vide(self, grille):  
        for i in range(9):
            for j in range(9):
                if grille[i][j] == 0:
                    return i, j
        return None, None

    def est_valide(self, grille, num, position): 
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

    def enable_level_buttons(self):  
        self.easy_button.config(state=tk.NORMAL)
        self.medium_button.config(state=tk.NORMAL)
        self.hard_button.config(state=tk.NORMAL)

    def disable_level_buttons(self): 
        self.easy_button.config(state=tk.DISABLED)
        self.medium_button.config(state=tk.DISABLED)
        self.hard_button.config(state=tk.DISABLED)

root = tk.Tk()
app = SudokuGUI(root)
app.generer_grille_complete()  
root.mainloop()
