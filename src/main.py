from game import Game
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    juego = Game()
    juego.run()
