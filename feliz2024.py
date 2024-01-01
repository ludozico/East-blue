import time
import sys

class NewYearCountdown:
    def __init__(self, year):
        self.year = year

    def countdown(self):
        for i in reversed(range(1, 11)):
            sys.stdout.write("\rContagem Regressiva... " + str(i) + " ")
            sys.stdout.flush()
            time.sleep(1)
        print("\n🎆🎇 Um Feliz " + str(self.year) + "! 🎇🎆")

class Celebration:
    def __init__(self, celebrations):
        self.celebrations = celebrations

    def party_elements(self):
        return "🎉 " + " 🎈 ".join(self.celebrations) + " 🎉"

class Friends:
    def __init__(self, names):
        self.names = names

    def celebrate(self, countdown, celebration):
        names_str = ", ".join(self.names)
        print(f"{names_str}, que este ano\nwhile 2024 == True:\n    Muitas alegrias e sucessos!")
        countdown.countdown()
        print(celebration.party_elements())

# Usage
countdown = NewYearCountdown(2024)
celebration = Celebration(["Esse ano", "a Bruna", "vai formar"])

# Lista de nomes dos amigos
friends_names = ["Mateus", "Katy", "João", "Joca", "e Ben"]

# Criando um objeto Friends com todos os nomes
friends = Friends(friends_names)

# Celebrando com todos os amigos
friends.celebrate(countdown, celebration)
