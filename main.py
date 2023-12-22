from game import Game


game = Game()
while True:
    reward = game.get_score()
    game_over = game.play_step()
    game.update_ui()


