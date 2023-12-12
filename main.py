from game import Game


game = Game()
while True:
    reward = game.get_score()
    game_over = game.play_step()
    if game_over:
        reward -= 10
    game.update_ui()
    print(game.grid.grid)


