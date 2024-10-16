import tkinter as tk

class GameUI:
    def __init__(self, game):
        self.game = game
        self.master = game.master
        self.answer_buttons = []
        self.next_round_button = None
        self.strike_labels = {"Equipo 1": None, "Equipo 2": None}
        self.round_points_label = None
        self.current_team_label = None

    def welcome_screen(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        welcome_label = tk.Label(self.master, text="¡Bienvenidos a Cien Mexicanos Dijeron!", font=("Helvetica", 16))
        welcome_label.pack(pady=10)

        self.team1_entry = tk.Entry(self.master)
        self.team1_entry.pack(pady=5)
        self.team1_entry.insert(0, "Equipo 1")

        self.team2_entry = tk.Entry(self.master)
        self.team2_entry.pack(pady=5)
        self.team2_entry.insert(0, "Equipo 2")

        start_button = tk.Button(self.master, text="Iniciar Juego", command=self.start_game)
        start_button.pack(pady=10)

    def start_game(self):
        team1 = self.team1_entry.get()
        team2 = self.team2_entry.get()
        self.game.start_game(team1, team2)

    def setup_ui(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        # Mostrar la pregunta actual
        self.question_label = tk.Label(self.master, text=f"Ronda {self.game.current_round + 1}: {self.game.questions[self.game.current_round]['question']}")
        self.question_label.pack()

        # Crear botones para las respuestas
        self.answer_buttons = []
        for index, (answer, points) in enumerate(self.game.questions[self.game.current_round]['answers']):
            button = tk.Button(self.master, text="??", command=lambda i=index: self.game.reveal_answer(i))
            button.pack()
            self.answer_buttons.append(button)

        # Mostrar puntajes de los equipos
        self.update_scores()

        # Mostrar equipo actual
        self.current_team_label = tk.Label(self.master, text=f"Turno de: {self.game.team_names[self.game.current_team]}")
        self.current_team_label.pack()

        # Mostrar strikes para cada equipo
        self.strike_labels["Equipo 1"] = tk.Label(self.master, text=f"Strikes {self.game.team_names['Equipo 1']}: {self.game.strikes['Equipo 1']}/3")
        self.strike_labels["Equipo 1"].pack()
        self.strike_labels["Equipo 2"] = tk.Label(self.master, text=f"Strikes {self.game.team_names['Equipo 2']}: {self.game.strikes['Equipo 2']}/3")
        self.strike_labels["Equipo 2"].pack()

        # Puntos acumulados en la ronda
        self.round_points_label = tk.Label(self.master, text=f"Puntos en la ronda: {self.game.round_points}")
        self.round_points_label.pack()

        # Botón para cambiar de equipo
        switch_team_button = tk.Button(self.master, text="Cambiar Equipo", command=self.game.switch_team)
        switch_team_button.pack(pady=10)

        # Botón para agregar un strike (falla)
        strike_button = tk.Button(self.master, text="Agregar Strike", command=self.game.incorrect_guess)
        strike_button.pack(pady=10)

        # Botón de "Siguiente Ronda"
        self.next_round_button = tk.Button(self.master, text="Siguiente Ronda", command=self.game.next_round)
        self.next_round_button.pack_forget()

    def update_scores(self):
        score_text = f"{self.game.team_names['Equipo 1']}: {self.game.scores['Equipo 1']} - {self.game.team_names['Equipo 2']}: {self.game.scores['Equipo 2']}"
        self.score_label = tk.Label(self.master, text=score_text)
        self.score_label.pack()

    def update_round_points(self, points):
        self.round_points_label.config(text=f"Puntos en la ronda: {points}")

    def show_strike(self, team, strikes):
        self.strike_labels[team].config(text=f"Strikes {self.game.team_names[team]}: {strikes}/3")

    def update_current_team(self, team):
        self.current_team_label.config(text=f"Turno de: {self.game.team_names[team]}")

    def enable_steal(self):
        steal_label = tk.Label(self.master, text=f"¡{self.game.team_names['Equipo 2']} puede intentar robar!")
        steal_label.pack()

        steal_button = tk.Button(self.master, text="Intentar Robo", command=lambda: self.game.steal_attempt(correct=True))  # Modifica para manejar el intento
        steal_button.pack()

    def show_game_over(self):
        self.question_label.config(text="¡Juego terminado!")
        for button in self.answer_buttons:
            button.config(state="disabled")
        self.next_round_button.pack_forget()
