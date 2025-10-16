import pygame
from .paddle import Paddle
from .ball import Ball

# Game Engine

WHITE = (255, 255, 255)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)

        self.player_score = 0
        self.ai_score = 0
        self.font = pygame.font.SysFont("Arial", 30)

        # New: set default winning score
        self.target_score = 5

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)

    def update(self):
        self.ball.move()
        self.ball.check_collision(self.player, self.ai)

        if self.ball.x <= 0:
            self.ai_score += 1
            self.ball.reset()
        elif self.ball.x >= self.width:
            self.player_score += 1
            self.ball.reset()

        self.ai.auto_track(self.ball, self.height)

    # def check_game_over(self, screen):
    #     winner_text = None
    #     if self.player_score >= 5:
    #         winner_text = "Player Wins!"
    #     elif self.ai_score >= 5:
    #         winner_text = "AI Wins!"

    #     if winner_text:
    #         # Display winner text
    #         text_surface = self.font.render(winner_text, True, WHITE)
    #         text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 2))
    #         screen.blit(text_surface, text_rect)
    #         pygame.display.flip()

    #         # Wait a few seconds before closing
    #         pygame.time.delay(3000)
    #         pygame.quit()
    #         exit()
    def check_game_over(self, screen):
        winner_text = None
        if self.player_score >= self.target_score:
            winner_text = "Player Wins!"
        elif self.ai_score >= self.target_score:
            winner_text = "AI Wins!"

        if winner_text:
            # Display winner text
            text_surface = self.font.render(winner_text, True, WHITE)
            text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 2 - 40))
            screen.blit(text_surface, text_rect)

            # Display replay options
            options = [
                "Press 3 for Best of 3",
                "Press 5 for Best of 5",
                "Press 7 for Best of 7",
                "Press ESC to Exit"
            ]
            for i, option in enumerate(options):
                option_text = self.font.render(option, True, WHITE)
                screen.blit(option_text, (self.width // 2 - 120, self.height // 2 + i * 30))

            pygame.display.flip()

            # Wait for key input
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            exit()
                        elif event.key == pygame.K_3:
                            self.target_score = 3
                            waiting = False
                        elif event.key == pygame.K_5:
                            self.target_score = 5
                            waiting = False
                        elif event.key == pygame.K_7:
                            self.target_score = 7
                            waiting = False

            # Reset scores and ball for a new match
            self.player_score = 0
            self.ai_score = 0
            self.ball.reset()

    
    def render(self, screen):
        # Draw paddles and ball
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width//2, 0), (self.width//2, self.height))

        # Draw score
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width//4, 20))
        screen.blit(ai_text, (self.width * 3//4, 20))
        
        # Check for game over condition
        self.check_game_over(screen)
