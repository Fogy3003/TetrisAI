from grid import Grid
from blocks import *
import random
import pygame
from colors import Colors
import sys
class Game:
    def __init__(self):
        self.grid = Grid()
        self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.game_over = False
        self.score = 0
        pygame.init()

        self.title_font = pygame.font.Font(None, 40)
        self.score_surface = self.title_font.render("Score", True, Colors.white)
        self.next_surface = self.title_font.render("Next", True, Colors.white)
        self.game_over_surface = self.title_font.render("GAME OVER", True, Colors.white)

        self.score_rect = pygame.Rect(320, 55, 170, 60)
        self.next_rect = pygame.Rect(320, 215, 170, 180)

        self.screen = pygame.display.set_mode((500, 620))
        pygame.display.set_caption("Python Tetris")

        self.clock = pygame.time.Clock()

        self.GAME_UPDATE = pygame.USEREVENT
        pygame.time.set_timer(self.GAME_UPDATE, 200)

    def play_step(self, move=False):
        for event in pygame.event.get():
            reward = self.get_score()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if self.game_over == True:
                    self.game_over = False
                    self.reset()
                if event.key == pygame.K_LEFT and self.game_over == False:
                    self.move_left()
                if event.key == pygame.K_RIGHT and self.game_over == False:
                    self.move_right()
                if event.key == pygame.K_DOWN and self.game_over == False:
                    self.move_down()
                    self.update_score(0, 1)
                if event.key == pygame.K_UP and self.game_over == False:
                    self.rotate()

            if move == [1,0,0]:
                self.move_left()
            elif move == [0,1,0]:
                self.move_right()
            elif move == [0,0,1]:
                self.move_down()
                self.update_score(0, 1)
            else:
                pass

            if event.type == self.GAME_UPDATE and self.game_over == False:
                self.move_down()
        return self.game_over

    def update_score(self, lines_cleared, move_down_points):
        if lines_cleared == 1:
            self.score += 100
        elif lines_cleared == 2:
            self.score += 300
        elif lines_cleared == 3:
            self.score += 500
        self.score += move_down_points

    def get_score(self):
        return self.score

    def get_random_block(self):
        if len(self.blocks) == 0:
            self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        block = random.choice(self.blocks)
        self.blocks.remove(block)
        return block

    def move_left(self):
        self.current_block.move(0, -1)
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(0, 1)

    def move_right(self):
        self.current_block.move(0, 1)
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(0, -1)

    def move_down(self):
        self.current_block.move(1, 0)
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(-1, 0)
            self.lock_block()

    def lock_block(self):
        tiles = self.current_block.get_cell_positions()
        for position in tiles:
            self.grid.grid[position.row][position.column] = self.current_block.id
        self.current_block = self.next_block
        self.next_block = self.get_random_block()
        rows_cleared = self.grid.clear_full_rows()
        if rows_cleared > 0:
            self.update_score(rows_cleared, 0)
        if not self.block_fits():
            self.game_over = True

    def reset(self):
        self.grid.reset()
        self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.score = 0

    def block_fits(self):
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if not self.grid.is_empty(tile.row, tile.column):
                return False
        return True

    def rotate(self):
        self.current_block.rotate()
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.undo_rotation()
        else:
            pass

    def block_inside(self):
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if not self.grid.is_inside(tile.row, tile.column):
                return False
        return True

    def draw(self, screen):
        self.grid.draw(screen)
        self.current_block.draw(screen, 11, 11)

        if self.next_block.id == 3:
            self.next_block.draw(screen, 255, 290)
        elif self.next_block.id == 4:
            self.next_block.draw(screen, 255, 280)
        else:
            self.next_block.draw(screen, 270, 270)

    def update_ui(self):
        score_value_surface = self.title_font.render(str(self.score), True, Colors.white)

        self.screen.fill(Colors.dark_blue)
        self.screen.blit(self.score_surface, (365, 20, 50, 50))
        self.screen.blit(self.next_surface, (375, 180, 50, 50))

        if self.game_over == True:
            self.screen.blit(self.game_over_surface, (320, 450, 50, 50))
        pygame.draw.rect(self.screen, Colors.light_blue, self.score_rect, 0, 10)
        self.screen.blit(score_value_surface, score_value_surface.get_rect(centerx=self.score_rect.centerx,
                                                                      centery=self.score_rect.centery))
        pygame.draw.rect(self.screen, Colors.light_blue, self.next_rect, 0, 10)
        self.draw(self.screen)

        pygame.display.update()
        self.clock.tick(20)