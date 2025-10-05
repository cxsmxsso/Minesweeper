import pygame
import random
import sys

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
DARK_GRAY = (120, 120, 120)
LIGHT_GRAY = (230, 230, 230)
RED = (255, 0, 0)
DARK_RED = (200, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 128, 0)
DARK_GREEN = (0, 100, 0)

COLORS = {
    1: BLUE,
    2: GREEN,
    3: RED,
    4: (0, 0, 128),
    5: (128, 0, 0),
    6: (0, 128, 128),
    7: BLACK,
    8: DARK_GRAY
}

CELL_SIZE = 30
MARGIN = 1
HEADER_HEIGHT = 80

class Minesweeper:
    def __init__(self, difficulty=1):
        self.difficulty = difficulty
        self.set_difficulty()
        self.reset_game()
        
    def set_difficulty(self):
        if self.difficulty == 1:
            self.n, self.m, self.k = 9, 9, 10
        elif self.difficulty == 2:
            self.n, self.m, self.k = 16, 16, 40
        else:
            self.n, self.m, self.k = 16, 30, 99
            
        self.width = self.m * (CELL_SIZE + MARGIN) + MARGIN
        self.height = self.n * (CELL_SIZE + MARGIN) + MARGIN + HEADER_HEIGHT
        
    def reset_game(self):
        self.board = [[0 for _ in range(self.m)] for _ in range(self.n)]
        self.visible = [['hidden' for _ in range(self.m)] for _ in range(self.n)]
        self.flags = [[False for _ in range(self.m)] for _ in range(self.n)]
        
        all_positions = [(i, j) for i in range(self.n) for j in range(self.m)]
        mine_positions = random.sample(all_positions, self.k)
        
        for x, y in mine_positions:
            self.board[x][y] = -1
            
        for i in range(self.n):
            for j in range(self.m):
                if self.board[i][j] == -1:
                    continue
                count = 0
                for di in (-1, 0, 1):
                    for dj in (-1, 0, 1):
                        ni, nj = i + di, j + dj
                        if 0 <= ni < self.n and 0 <= nj < self.m and self.board[ni][nj] == -1:
                            count += 1
                self.board[i][j] = count
        
        self.game_over = False
        self.win = False
        self.mines_left = self.k
        
    def open_cell(self, x, y):
        if self.visible[x][y] != 'hidden' or self.flags[x][y]:
            return
            
        if self.board[x][y] == -1:
            self.visible[x][y] = 'mine'
            self.game_over = True
            self.reveal_all_mines()
            return
            
        self.visible[x][y] = 'revealed'
        
        if self.board[x][y] == 0:
            for di in (-1, 0, 1):
                for dj in (-1, 0, 1):
                    ni, nj = x + di, y + dj
                    if 0 <= ni < self.n and 0 <= nj < self.m:
                        self.open_cell(ni, nj)
        
        self.check_win()
    
    def reveal_all_mines(self):
        for i in range(self.n):
            for j in range(self.m):
                if self.board[i][j] == -1:
                    self.visible[i][j] = 'mine'
        
    def toggle_flag(self, x, y):
        if self.visible[x][y] == 'hidden':
            self.flags[x][y] = not self.flags[x][y]
            if self.flags[x][y]:
                self.mines_left -= 1
            else:
                self.mines_left += 1
        
    def check_win(self):
        hidden_count = 0
        for i in range(self.n):
            for j in range(self.m):
                if self.visible[i][j] == 'hidden':
                    hidden_count += 1
        if hidden_count == self.k:
            self.win = True

    def draw(self, screen):
        screen.fill(DARK_GRAY)
        
        header_rect = pygame.Rect(0, 0, self.width, HEADER_HEIGHT)
        pygame.draw.rect(screen, LIGHT_GRAY, header_rect)
        
        title_font = pygame.font.Font(None, 48)
        title = title_font.render("САПЕР", True, BLACK)
        screen.blit(title, (10, 10))
        
        mines_font = pygame.font.Font(None, 36)
        mines_text = mines_font.render(f"{self.mines_left}", True, RED)
        screen.blit(mines_text, (self.width - 50, 15))
        
        button_font = pygame.font.Font(None, 28)
        
        new_game_text = button_font.render("Новая игра (R)", True, BLUE)
        screen.blit(new_game_text, (self.width // 2 - new_game_text.get_width() + 5, 45))
        
        exit_text = button_font.render("Выход (Esc)", True, BLACK)
        screen.blit(exit_text, (self.width // 2 + 10, 45))
        
        field_bg = pygame.Rect(0, HEADER_HEIGHT, self.width, self.height - HEADER_HEIGHT)
        pygame.draw.rect(screen, DARK_GRAY, field_bg)
        
        for i in range(self.n):
            for j in range(self.m):
                x = j * (CELL_SIZE + MARGIN) + MARGIN
                y = i * (CELL_SIZE + MARGIN) + MARGIN + HEADER_HEIGHT
                
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                
                if self.visible[i][j] == 'revealed':
                    pygame.draw.rect(screen, LIGHT_GRAY, rect)
                    
                    if self.board[i][j] > 0:
                        number_font = pygame.font.Font(None, 24)
                        number_text = number_font.render(str(self.board[i][j]), True, COLORS.get(self.board[i][j], BLACK))
                        text_rect = number_text.get_rect(center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2))
                        screen.blit(number_text, text_rect)
                        
                elif self.visible[i][j] == 'mine':
                    pygame.draw.rect(screen, RED, rect)
                    
                    star_font = pygame.font.Font(None, 24)
                    star_text = star_font.render("#", True, WHITE)
                    star_rect = star_text.get_rect(center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2))
                    screen.blit(star_text, star_rect)
                    
                    pygame.draw.rect(screen, DARK_RED, rect, 2)
                    
                else:
                    pygame.draw.rect(screen, DARK_GRAY, rect)
                    
                    pygame.draw.line(screen, WHITE, (x, y), (x + CELL_SIZE, y), 2)
                    pygame.draw.line(screen, WHITE, (x, y), (x, y + CELL_SIZE), 2)
                    pygame.draw.line(screen, BLACK, (x + CELL_SIZE, y), (x + CELL_SIZE, y + CELL_SIZE), 2)
                    pygame.draw.line(screen, BLACK, (x, y + CELL_SIZE), (x + CELL_SIZE, y + CELL_SIZE), 2)
                    
                    if self.flags[i][j]:
                        flag_font = pygame.font.Font(None, 20)
                        flag_text = flag_font.render("F", True, RED)
                        flag_rect = flag_text.get_rect(center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2))
                        screen.blit(flag_text, flag_rect)
        
        if self.game_over:
            overlay = pygame.Surface((self.width, self.height - HEADER_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))
            screen.blit(overlay, (0, HEADER_HEIGHT))
            
            game_over_font = pygame.font.Font(None, 48)
            game_over_text = game_over_font.render("ИГРА ОКОНЧЕНА!", True, RED)
            screen.blit(game_over_text, (self.width // 2 - game_over_text.get_width() // 2, 
                                       HEADER_HEIGHT + (self.height - HEADER_HEIGHT) // 2 - 30))
            
            restart_font = pygame.font.Font(None, 36)
            restart_text = restart_font.render("Новая игра - R", True, WHITE)
            screen.blit(restart_text, (self.width // 2 - restart_text.get_width() // 2, 
                                     HEADER_HEIGHT + (self.height - HEADER_HEIGHT) // 2 + 20))
        
        elif self.win:
            overlay = pygame.Surface((self.width, self.height - HEADER_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))
            screen.blit(overlay, (0, HEADER_HEIGHT))
            
            win_font = pygame.font.Font(None, 48)
            win_text = win_font.render("ПОБЕДА!", True, GREEN)
            screen.blit(win_text, (self.width // 2 - win_text.get_width() // 2, 
                                 HEADER_HEIGHT + (self.height - HEADER_HEIGHT) // 2 - 30))
            
            restart_font = pygame.font.Font(None, 36)
            restart_text = restart_font.render("Новая игра - R", True, WHITE)
            screen.blit(restart_text, (self.width // 2 - restart_text.get_width() // 2, 
                                     HEADER_HEIGHT + (self.height - HEADER_HEIGHT) // 2 + 20))

def draw_menu(screen, width, height):
    screen.fill(LIGHT_GRAY)
    
    title_font = pygame.font.Font(None, 72)
    title = title_font.render("САПЕР", True, BLACK)
    screen.blit(title, (width // 2 - title.get_width() // 2, 50))
    
    option_font = pygame.font.Font(None, 36)
    options = [
        "1 - ЛЕГКИЙ   (9x9, 10 мин)",
        "2 - СРЕДНИЙ  (16x16, 40 мин)", 
        "3 - СЛОЖНЫЙ  (16x30, 99 мин)"
    ]
    
    for i, option in enumerate(options):
        text = option_font.render(option, True, BLUE)
        screen.blit(text, (width // 2 - text.get_width() // 2, 150 + i * 50))
    
    hint_font = pygame.font.Font(None, 24)
    hint = hint_font.render("Нажмите цифру для выбора уровня сложности", True, DARK_GRAY)
    screen.blit(hint, (width // 2 - hint.get_width() // 2, height - 50))

def main():
    initial_width, initial_height = 400, 500
    screen = pygame.display.set_mode((initial_width, initial_height))
    pygame.display.set_caption("Сапер")
    
    clock = pygame.time.Clock()
    game = None
    in_menu = True
    
    running = True
    while running:
        if in_menu:
            draw_menu(screen, initial_width, initial_height)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                        difficulty = event.key - pygame.K_0
                        game = Minesweeper(difficulty)
                        screen = pygame.display.set_mode((game.width, game.height))
                        in_menu = False
                    elif event.key == pygame.K_ESCAPE:
                        running = False
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
                elif event.type == pygame.MOUSEBUTTONDOWN and not game.game_over and not game.win:
                    pos = pygame.mouse.get_pos()
                    if pos[1] > HEADER_HEIGHT:
                        col = pos[0] // (CELL_SIZE + MARGIN)
                        row = (pos[1] - HEADER_HEIGHT) // (CELL_SIZE + MARGIN)
                        
                        if 0 <= row < game.n and 0 <= col < game.m:
                            if event.button == 1:
                                game.open_cell(row, col)
                            elif event.button == 3:
                                game.toggle_flag(row, col)
                
                elif event.type == pygame.KEYDOWN:
                    if event.key ==  pygame.K_r:
                        game.reset_game()
                    elif event.key == pygame.K_ESCAPE:
                        in_menu = True
                        screen = pygame.display.set_mode((initial_width, initial_height))
            
            game.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()