import json
import random
from ui import GameUI

class CienMexDij:
    def __init__(self, master):
        self.master = master
        self.current_round = 0
        self.scores = {"Equipo 1": 0, "Equipo 2": 0}  # Puntajes iniciales
        self.team_names = {"Equipo 1": "Equipo 1", "Equipo 2": "Equipo 2"}  # Nombres de los equipos
        self.questions = []
        self.revealed_answers = 0
        self.current_team = "Equipo 1"  # Equipo que está jugando actualmente
        self.strikes = {"Equipo 1": 0, "Equipo 2": 0}  # Strikes de cada equipo
        self.round_points = 0  # Puntos acumulados en la ronda

        self.ui = GameUI(self)
        self.ui.welcome_screen()

    def start_game(self, team1, team2):
        # Guardar los nombres de los equipos ingresados
        self.team_names["Equipo 1"] = team1
        self.team_names["Equipo 2"] = team2

        # Cargar preguntas y configurar la interfaz de juego
        self.questions = self.load_questions()
        self.setup_next_round()

    def load_questions(self):
        # Leer preguntas desde el archivo JSON
        try:
            with open('preguntas.json', 'r', encoding='utf-8') as file:
                all_questions = json.load(file)
            # Seleccionar aleatoriamente un subconjunto de preguntas
            selected_questions = random.sample(all_questions, k=min(len(all_questions), 5))
            return selected_questions
        except FileNotFoundError:
            print("El archivo 'preguntas.json' no se encontró.")
            return []
        except json.JSONDecodeError:
            print("Error al decodificar el archivo JSON.")
            return []

    def setup_next_round(self):
        self.revealed_answers = 0
        self.round_points = 0  # Reiniciar puntos de la ronda
        self.current_team = "Equipo 1"  # Comenzar la ronda con el Equipo 1
        self.ui.setup_ui()

    def reveal_answer(self, index):
        answer, points = self.questions[self.current_round]['answers'][index]
        if self.ui.answer_buttons[index]['text'] == "??":
            self.ui.answer_buttons[index].config(text=f"{answer} - {points}")
            self.revealed_answers += 1
            self.round_points += points  # Sumar puntos a la ronda
            if self.revealed_answers == len(self.questions[self.current_round]['answers']):
                self.end_round()
            else:
                self.ui.update_round_points(self.round_points)

    def incorrect_guess(self):
        # Agregar un strike al equipo actual
        self.strikes[self.current_team] += 1
        self.ui.show_strike(self.current_team, self.strikes[self.current_team])  # Mostrar los strikes en la interfaz
        if self.strikes[self.current_team] == 3:
            self.ui.enable_steal()  # Permitir que el otro equipo robe los puntos

    def switch_team(self):
        # Alternar entre Equipo 1 y Equipo 2
        self.current_team = "Equipo 2" if self.current_team == "Equipo 1" else "Equipo 1"
        self.ui.update_current_team(self.current_team)

    def steal_attempt(self, correct):
        if correct:
            # El equipo contrario roba los puntos
            other_team = "Equipo 2" if self.current_team == "Equipo 1" else "Equipo 1"
            self.scores[other_team] += self.round_points
            self.ui.update_scores()
        self.end_round()

    def end_round(self):
        # Asignar puntos al equipo actual si no hubo robo
        self.scores[self.current_team] += self.round_points
        self.ui.update_scores()
        if self.current_round < len(self.questions) - 1:
            self.current_round += 1
            self.setup_next_round()
        else:
            self.ui.show_game_over()

    def next_round(self):
        self.current_round += 1
        self.setup_next_round()
