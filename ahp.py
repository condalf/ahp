from game import Game

N_GAMES = 10

print("Starting {} games of Auntie Hannie's Patience...".format(N_GAMES))

for i in range(N_GAMES):
    print("Starting game #{}...".format(i))
    game = Game()
    game.play()

    print("Game #{} finished.".format(i))

print("All games finished.")
