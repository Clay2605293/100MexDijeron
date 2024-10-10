import tkinter as tk
import json
import random

class CienMexDij:
    def __init__(self, master):
        self.master = master
        self.master.title("Cien Mexicanos Dijeron")
        self.current_round = 0
        self.scores = {"Equipo 1": 0, "Equipo 2": 0}
        self.questions = self.load_questions()
        self.revealed_answers = 0  

        self.setup_ui()

    def load_questions(self):
        try:
            with open('preguntas.json', 'r', encoding='utf-8') as file:
                all_questions = json.load(file)
            selected_questions = random.sample(all_questions, k=min(len(all_questions), 5))
            return selected_questions
        except FileNotFoundError:
            print("El archivo 'preguntas.json' no se encontró.")
            return []
        except json.JSONDecodeError:
            print("Error al decodificar el archivo JSON.")
            return []

    def setup_ui(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        if not self.questions:
            self.question_label = tk.Label(self.master, text="No hay preguntas disponibles.")
            self.question_label.pack()
            return

        self.question_label = tk.Label(self.master, text=f"Ronda {self.current_round + 1}: {self.questions[self.current_round]['question']}")
        self.question_label.pack()

        self.answer_buttons = []
        self.revealed_answers = 0  
        for index, (answer, points) in enumerate(self.questions[self.current_round]['answers']):
            button = tk.Button(self.master, text="?????", command=lambda i=index: self.reveal_answer(i))
            button.pack()
            self.answer_buttons.append(button)

        self.score_label = tk.Label(self.master, text=f"Equipo 1: {self.scores['Equipo 1']} - Equipo 2: {self.scores['Equipo 2']}")
        self.score_label.pack()

        self.next_round_button = tk.Button(self.master, text="Siguiente Ronda", command=self.next_round)
        self.next_round_button.pack()
        self.next_round_button.pack_forget()  

    def reveal_answer(self, index):
        answer, points = self.questions[self.current_round]['answers'][index]
        if self.answer_buttons[index]['text'] == "?????": 
            self.answer_buttons[index].config(text=f"{answer} - {points}")
            self.revealed_answers += 1

        if self.revealed_answers == len(self.questions[self.current_round]['answers']):
            self.next_round_button.pack() 

    def next_round(self):
        if self.current_round < len(self.questions) - 1:
            self.current_round += 1
            self.setup_ui()
        else:
            self.question_label.config(text="¡Juego terminado!")
            for button in self.answer_buttons:
                button.config(state="disabled")
            self.next_round_button.pack_forget()

if __name__ == "__main__":
    root = tk.Tk()
    app = CienMexDij(root)
    root.mainloop()
