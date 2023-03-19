import pygame
from pygame import mixer
import sys

# Constants
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
BALL_SIZE = 20
PADDLE_WIDTH = 20
PADDLE_HEIGHT = 100
FPS = 165
BORDER_WIDTH = 10
SPEED_MULTIPLIER_INITIAL = 1


class Pong:
    def __init__(self):
        pygame.init()
        mixer.init()
        self.pop_sound = mixer.Sound("pop.wav")

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 50)

        self.ball = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, BALL_SIZE, BALL_SIZE)
        self.ball_speed = [3, 3]
        self.speed_multiplier = SPEED_MULTIPLIER_INITIAL
        self.speed_decay = 0.98

        self.paddle1 = pygame.Rect(20, SCREEN_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.paddle2 = pygame.Rect(600, SCREEN_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.score1 = 0
        self.score2 = 0

    def ai_paddle(self, paddle, ball, paddle_speed):
        if paddle.centery < ball.centery and paddle.bottom < SCREEN_HEIGHT - BORDER_WIDTH:
            paddle.y += min(paddle_speed, ball.centery - paddle.centery)
        elif paddle.centery > ball.centery and paddle.top > BORDER_WIDTH:
            paddle.y -= min(paddle_speed, paddle.centery - ball.centery)

        if paddle.top < BORDER_WIDTH:
            paddle.y = BORDER_WIDTH
        if paddle.bottom > SCREEN_HEIGHT - BORDER_WIDTH:
            paddle.y = SCREEN_HEIGHT - BORDER_WIDTH - PADDLE_HEIGHT

    def reset_game(self):
        self.ball.x = SCREEN_WIDTH // 2
        self.ball.y = SCREEN_HEIGHT // 2
        self.paddle1.x = 20
        self.paddle1.y = SCREEN_HEIGHT // 2
        self.paddle2.x = 600
        self.paddle2.y = SCREEN_HEIGHT // 2
        self.speed_multiplier = SPEED_MULTIPLIER_INITIAL

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.clock.tick(FPS)

            self.ai_paddle(self.paddle1, self.ball, 5)
            self.ai_paddle(self.paddle2, self.ball, 5)

            self.ball.x += self.ball_speed[0] * self.speed_multiplier
            self.ball.y += self.ball_speed[1] * self.speed_multiplier

            if self.ball.top <= BORDER_WIDTH:
                self.ball_speed[1] *= -1
                self.ball.y = BORDER_WIDTH + 1 # +1 to prevent the ball from getting stuck in the border
            elif self.ball.bottom >= SCREEN_HEIGHT - BORDER_WIDTH:
                self.ball_speed[1] *= -1
                self.ball.y = SCREEN_HEIGHT - BORDER_WIDTH - BALL_SIZE - 1 # -1 to prevent the ball from getting stuck in the border

            if self.ball.left <= BORDER_WIDTH:
                self.ball_speed[0] *= -1
                self.score1 += 1
                self.reset_game()
            if self.ball.right >= SCREEN_WIDTH - BORDER_WIDTH:
                self.ball_speed[0] *= -1
                self.score2 += 1
                self.reset_game()

            if self.ball.colliderect(self.paddle1) or self.ball.colliderect(self.paddle2):
                self.ball_speed[0] *= -1
                self.speed_multiplier *= 3.5
                self.pop_sound.play()

            self.speed_multiplier = max(1, self.speed_multiplier * self.speed_decay)

            self.screen.fill((0, 0, 0))
            pygame.draw.rect(self.screen, (255, 255, 255), (0, 0, SCREEN_WIDTH, BORDER_WIDTH))  # Top border
            pygame.draw.rect(self.screen, (255, 255, 255), (0, 0, BORDER_WIDTH, SCREEN_HEIGHT))  # Left border
            pygame.draw.rect(self.screen, (255, 255, 255), (0, SCREEN_HEIGHT - BORDER_WIDTH, SCREEN_WIDTH, BORDER_WIDTH))  # Bottom border
            pygame.draw.rect(self.screen, (255, 255, 255), (SCREEN_WIDTH - BORDER_WIDTH, 0, BORDER_WIDTH, SCREEN_HEIGHT))  # Right border

            pygame.draw.rect(self.screen, (255, 255, 255), self.ball)
            pygame.draw.rect(self.screen, (255, 255, 255), self.paddle1)
            pygame.draw.rect(self.screen, (255, 255, 255), self.paddle2)

            score_text = self.font.render(str(self.score1), True, (255, 255, 255))
            score_text2 = self.font.render(str(self.score2), True, (255, 255, 255))
            self.screen.blit(score_text, (SCREEN_WIDTH // 2 - 50, 20))
            self.screen.blit(score_text2, (SCREEN_WIDTH // 2 + 20, 20))

            framerate_text = self.font.render(f"{self.clock.get_fps():.0f} FPS", True, (255, 255, 255))
            self.screen.blit(framerate_text, (SCREEN_WIDTH - 170, 20))
            
            ball_speed_text = self.font.render(f"{self.ball_speed[0] * self.speed_multiplier.__abs__():.0f} px/s", True, (255, 255, 255))
            self.screen.blit(ball_speed_text, (SCREEN_WIDTH - 170, 70))
            pygame.display.flip()


if __name__ == "__main__":
    pong = Pong()
    pong.run()
