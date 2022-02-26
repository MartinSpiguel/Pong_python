import pygame
from AI.pong_ai import AiPlayer

pygame.init()

#Define constants
PLAYER1, PLAYER2 = True, True #True if a human is playing, false if the ai is playing
WIDTH, HEIGHT = 900, 500
RAQUET_WIDTH, RAQUET_HEIGHT = 5, 90
BACKGROUND_COLOR = (60, 60, 255) #LIGHT BLUE
RAQUET_COLOR = (255, 255, 255) #WHITE
BALL_COLOR = (255, 127, 0) #ORANGE
RAQUET_VEL = 9
NET = pygame.Rect(WIDTH//2 - 2, 0, 5, HEIGHT)
BALL_DIMENSION = 15
SCORE_FONT = pygame.font.SysFont('comicsans', 40)
FPS = 60
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pong')

#Define variables
raquet_1 = pygame.Rect(0, HEIGHT//2 - RAQUET_HEIGHT//2, RAQUET_WIDTH, RAQUET_HEIGHT)
raquet_2 = pygame.Rect(WIDTH - RAQUET_WIDTH, HEIGHT//2 - RAQUET_HEIGHT//2, RAQUET_WIDTH, RAQUET_HEIGHT)
raquet_1_points = 0 
raquet_2_points = 0 
ball = pygame.Rect(WIDTH//2 - 5, HEIGHT//2 - 5, BALL_DIMENSION, BALL_DIMENSION)
y_vel = x_vel = RAQUET_VEL

def draw_ball():
    pygame.draw.rect(WIN, BALL_COLOR, ball)

def draw_raquets():
    pygame.draw.rect(WIN, RAQUET_COLOR, raquet_1)
    pygame.draw.rect(WIN, RAQUET_COLOR, raquet_2)

def draw_net():
    pygame.draw.rect(WIN, RAQUET_COLOR, NET)

def ball_movement():
    global x_vel
    global y_vel
    global raquet_1_points
    global raquet_2_points
    if ball.y + BALL_DIMENSION > HEIGHT or ball.y < 0:
        y_vel *= -1
    if raquet_1.colliderect(ball) or raquet_2.colliderect(ball):
        x_vel *= -1
    if ball.x > WIDTH:
        raquet_1_points += 1
        ball.x = WIDTH//2 - 5
        ball.y = HEIGHT//2 - 5
        pygame.time.delay(1000)
    if ball.x + BALL_DIMENSION < 0:
        raquet_2_points += 1
        ball.x = WIDTH//2 - 5
        ball.y = HEIGHT//2 - 5
        pygame.time.delay(1000)
    ball.x += x_vel
    ball.y += y_vel

def draw_winner(text):
    game_over = SCORE_FONT.render(text, 1, RAQUET_COLOR)
    WIN.blit(game_over, (WIDTH//2 - game_over.get_width()//2, HEIGHT//2 - game_over.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)

def draw_score():
    raquet1_score = SCORE_FONT.render(str(raquet_1_points), 1, RAQUET_COLOR)
    raquet2_score = SCORE_FONT.render(str(raquet_2_points), 1, RAQUET_COLOR)
    WIN.blit(raquet1_score, (WIDTH//2 - raquet1_score.get_width() - 10, 10))
    WIN.blit(raquet2_score, (WIDTH//2 + 10, 10))

def draw_window():
    WIN.fill(BACKGROUND_COLOR)
    draw_raquets()
    draw_net()
    draw_score()
    draw_ball()
    ball_movement()
    pygame.display.update()

def main():
    global RAQUET_VEL
    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        #RAQUETS MOVEMENT
        if PLAYER1 and PLAYER2: #No AI
            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_UP] and raquet_2.y > 0:
                raquet_2.y -= RAQUET_VEL
            elif keys_pressed[pygame.K_DOWN] and raquet_2.y + RAQUET_HEIGHT < HEIGHT:
                raquet_2.y += RAQUET_VEL
            if keys_pressed[pygame.K_w] and raquet_1.y > 0:
                raquet_1.y -= RAQUET_VEL
            elif keys_pressed[pygame.K_s] and raquet_1.y + RAQUET_HEIGHT < HEIGHT:
                raquet_1.y += RAQUET_VEL

        elif not PLAYER1 and PLAYER2: #Player1 AI
            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_UP] and raquet_2.y > 0:
                raquet_2.y -= RAQUET_VEL
            elif keys_pressed[pygame.K_DOWN] and raquet_2.y + RAQUET_HEIGHT < HEIGHT:
                raquet_2.y += RAQUET_VEL
            AiPlayer.move_raquet_intelligent(raquet_1, ball, HEIGHT, RAQUET_HEIGHT) #AI that follows the ball
        
        elif PLAYER1 and not PLAYER2: #Player2 AI
            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_w] and raquet_1.y > 0:
                raquet_1.y -= RAQUET_VEL
            elif keys_pressed[pygame.K_s] and raquet_1.y + RAQUET_HEIGHT < HEIGHT:
                raquet_1.y += RAQUET_VEL
            AiPlayer.move_raquet_intelligent(raquet_2, ball, HEIGHT, RAQUET_HEIGHT) #AI that follows the ball
        
        elif not PLAYER1 and not PLAYER2: #Two AI
            AiPlayer.move_raquet_intelligent(raquet_1, ball, HEIGHT, RAQUET_HEIGHT)
            AiPlayer.move_raquet_intelligent(raquet_2, ball, HEIGHT, RAQUET_HEIGHT)

        winner_text = ''
        if raquet_1_points == 5:
            winner_text = 'Player 1 wins'
        elif raquet_2_points == 5:
            winner_text = 'Player 2 wins'
        if winner_text != '':
            draw_winner(winner_text)
            break

        draw_window()
        
    pygame.quit()

if __name__ == '__main__':
    main()