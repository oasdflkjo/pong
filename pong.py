import pygame
from pygame import mixer
import sys

# Constants
FPS = 160

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
SCREEN_WIDTH_CENTER = SCREEN_WIDTH // 2
SCREEN_HEIGHT_CENTER = SCREEN_HEIGHT // 2

BALL_SIZE = 20
BALL_BASE_SPEED = 3
BALL_SPEED_MULTIPLIER = 3.5
BALL_SPEED_DECAY = 0.98
BALL_SPEED_MULTIPLIER_INITIAL = 1

PADDLE_WIDTH = 20
PADDLE_HEIGHT = 100
BORDER_WIDTH = 10

COLOR_DRAW = (255, 0, 0)
COLOR_BACKGROUND = (0, 0, 0)


class Pong:
    def __init__(self):
        pygame.init()
        mixer.init()
        self.pop_sound = mixer.Sound("pop.wav")

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 50)

        self.ball = pygame.Rect(SCREEN_WIDTH_CENTER, SCREEN_HEIGHT_CENTER, BALL_SIZE, BALL_SIZE)
        self.ball_speed = [BALL_BASE_SPEED, BALL_BASE_SPEED]
        self.speed_multiplier = BALL_SPEED_MULTIPLIER_INITIAL
        self.speed_decay = BALL_SPEED_DECAY

        self.paddle1 = pygame.Rect(20, SCREEN_HEIGHT_CENTER, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.paddle2 = pygame.Rect(600, SCREEN_HEIGHT_CENTER, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.score1 = 0
        self.score2 = 0

    def ai_paddle(self, paddle, ball, paddle_speed):
        if paddle.centery < ball.centery and paddle.bottom < SCREEN_HEIGHT - BORDER_WIDTH:
            paddle.y += min(paddle_speed, ball.centery - paddle.centery)
        elif paddle.centery > ball.centery and paddle.top > BORDER_WIDTH:
            paddle.y -= min(paddle_speed, paddle.centery - ball.centery)

        if paddle.top < BORDER_WIDTH:
            paddle.y = BORDER_WIDTH
        elif paddle.bottom > SCREEN_HEIGHT - BORDER_WIDTH:
            paddle.y = SCREEN_HEIGHT - BORDER_WIDTH - PADDLE_HEIGHT

    # Check for ball collision with paddle top/bottom
        if ball.colliderect(paddle):
            if ball.bottom >= paddle.top and ball.top <= paddle.top:
                self.ball_speed[1] = -abs(self.ball_speed[1])
                self.ball.y = paddle.top - BALL_SIZE
            elif ball.top <= paddle.bottom and ball.bottom >= paddle.bottom:
                self.ball_speed[1] = abs(self.ball_speed[1])
                self.ball.y = paddle.bottom

    def reset_game(self):
        self.ball.x = SCREEN_WIDTH_CENTER
        self.ball.y = SCREEN_HEIGHT_CENTER
        self.paddle1.x = 20
        self.paddle1.y = SCREEN_HEIGHT_CENTER
        self.paddle2.x = 600
        self.paddle2.y = SCREEN_HEIGHT_CENTER
        self.speed_multiplier = BALL_SPEED_MULTIPLIER_INITIAL
    
    def lerp(self, a, b, t):
        x = int((1 - t) * a[0] + t * b[0])
        y = int((1 - t) * a[1] + t * b[1])
        return x, y

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.clock.tick(FPS)

            self.ai_paddle(self.paddle1, self.ball, 5)
            self.ai_paddle(self.paddle2, self.ball, 5)

            next_ball_pos = [self.ball.x + self.ball_speed[0] * self.speed_multiplier, self.ball.y + self.ball_speed[1] * self.speed_multiplier]
            self.ball.x, self.ball.y = self.lerp([self.ball.x, self.ball.y], next_ball_pos, 0.5)

            next_paddle1_pos = [self.paddle1.x, self.paddle1.y + min(5, self.paddle1.centery)]
            self.paddle1.x, self.paddle1.y = self.lerp([self.paddle1.x, self.paddle1.y], next_paddle1_pos, 0.5)

            next_paddle2_pos = [self.paddle2.x, self.paddle2.y + min(5, self.paddle2.centery)]
            self.paddle2.x, self.paddle2.y = self.lerp([self.paddle2.x, self.paddle2.y], next_paddle2_pos, 0.5)

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
                self.speed_multiplier *= BALL_SPEED_MULTIPLIER
                self.pop_sound.play()

            self.speed_multiplier = max(1, self.speed_multiplier * self.speed_decay)

            self.screen.fill(COLOR_BACKGROUND)
            pygame.draw.rect(self.screen, COLOR_DRAW, (0, 0, SCREEN_WIDTH, BORDER_WIDTH))  # Top border
            pygame.draw.rect(self.screen, COLOR_DRAW, (0, 0, BORDER_WIDTH, SCREEN_HEIGHT))  # Left border
            pygame.draw.rect(self.screen, COLOR_DRAW, (0, SCREEN_HEIGHT - BORDER_WIDTH, SCREEN_WIDTH, BORDER_WIDTH))  # Bottom border
            pygame.draw.rect(self.screen, COLOR_DRAW, (SCREEN_WIDTH - BORDER_WIDTH, 0, BORDER_WIDTH, SCREEN_HEIGHT))  # Right border

            pygame.draw.rect(self.screen, COLOR_DRAW, self.ball)
            pygame.draw.rect(self.screen, COLOR_DRAW, self.paddle1)
            pygame.draw.rect(self.screen, COLOR_DRAW, self.paddle2)

            score_text = self.font.render(str(self.score1), True, COLOR_DRAW)
            score_text2 = self.font.render(str(self.score2), True, COLOR_DRAW)
            self.screen.blit(score_text, (SCREEN_WIDTH_CENTER - 50, 20))
            self.screen.blit(score_text2, (SCREEN_WIDTH_CENTER + 20, 20))

            framerate_text = self.font.render(f"{self.clock.get_fps():.0f} FPS", True, COLOR_DRAW)
            self.screen.blit(framerate_text, (SCREEN_WIDTH - 170, 20))
            
            ball_speed_text = self.font.render(f"{self.ball_speed[0] * self.speed_multiplier.__abs__():.0f} px/s", True, COLOR_DRAW)
            self.screen.blit(ball_speed_text, (SCREEN_WIDTH - 170, 70))
            pygame.display.flip()



if __name__ == "__main__":
    pong = Pong()
    pong.run()
