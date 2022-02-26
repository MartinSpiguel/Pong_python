import pygame
from AI.pong_ai import AiPlayer

#Initialize pygame
pygame.init()

#Define constants
PLAYER1, PLAYER2 = False, True #True if a human is playing, false if the ai is playing
WIDTH, HEIGHT = 900, 500
RAQUET_WIDTH, RAQUET_HEIGHT = 5, 90
RAQUET_VEL = 9
BALL_DIMENSION = 15

NET = pygame.Rect(WIDTH//2 - 2, 0, 5, HEIGHT)

LIGHT_BLUE = (60, 60, 255)
WHITE = (255, 255, 255) 
ORANGE = (255, 127, 0) 

SCORE_FONT = pygame.font.SysFont('comicsans', 40)

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pong')

def draw_ball(surface, color, ball):
    pygame.draw.rect(surface, color, ball)

def draw_raquets(surface, color, raquet_1, raquet_2):
    pygame.draw.rect(surface, color, raquet_1)
    pygame.draw.rect(surface, color, raquet_2)

def draw_net(surface, color, net):
    pygame.draw.rect(surface, color, net)

def ball_movement(x_vel, y_vel, raquet_1_points, raquet_2_points, ball, raquet_1, raquet_2, width, height, ball_dimension):
    if ball.y + ball_dimension > height or ball.y < 0:
        y_vel *= -1
    if ball.colliderect(raquet_1) or ball.colliderect(raquet_2):
        x_vel *= -1
    if ball.x > width:
        raquet_1_points += 1
        ball.x = width//2 - 5
        ball.y = height//2 - 5
        pygame.time.delay(1000)
    if ball.x + ball_dimension < 0:
        raquet_2_points += 1
        ball.x = width//2 - 5
        ball.y = height//2 - 5
        pygame.time.delay(1000)
    ball.x += x_vel
    ball.y += y_vel

def draw_winner(surface, font, color, width, height, text):
    game_over = font.render(text, 1, color)
    surface.blit(game_over, (width//2 - game_over.get_width()//2, height//2 - game_over.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)

def draw_score(surface, font, color, width, raquet_1_points, raquet_2_points):
    raquet1_score = font.render(str(raquet_1_points), 1, color)
    raquet2_score = font.render(str(raquet_2_points), 1, color)
    surface.blit(raquet1_score, (width//2 - raquet1_score.get_width() - 10, 10))
    surface.blit(raquet2_score, (width//2 + 10, 10))

def update_window():
    pygame.display.update()

def main():
    #Define pygame Rect objects for raquets and ball
    raquet_1 = pygame.Rect(0, HEIGHT//2 - RAQUET_HEIGHT//2, RAQUET_WIDTH, RAQUET_HEIGHT)
    raquet_2 = pygame.Rect(WIDTH - RAQUET_WIDTH, HEIGHT//2 - RAQUET_HEIGHT//2, RAQUET_WIDTH, RAQUET_HEIGHT)
    ball = pygame.Rect(WIDTH//2 - 5, HEIGHT//2 - 5, BALL_DIMENSION, BALL_DIMENSION)

    #Define the score
    raquet_1_points = 0
    raquet_2_points = 0 

    #Define the x and y velocity of the ball. Set it equal to the raquets velocity.
    y_vel = x_vel = RAQUET_VEL

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

        #Check if someone won and draw winner if someone had
        winner_text = ''
        if raquet_1_points == 5:
            winner_text = 'Player 1 wins'
        elif raquet_2_points == 5:
            winner_text = 'Player 2 wins'
        if winner_text != '':
            draw_winner(WIN, SCORE_FONT, WHITE, WIDTH, HEIGHT, winner_text)
            break

        #Draw everithing in the window
        WIN.fill(LIGHT_BLUE)
        draw_raquets(WIN, WHITE, raquet_1, raquet_2)
        draw_net(WIN, WHITE, NET)
        draw_score(WIN, SCORE_FONT, WHITE, WIDTH, raquet_1_points, raquet_2_points)
        draw_ball(WIN, ORANGE, ball)
        #Handle the ball's movement 
        ball_movement(x_vel, y_vel, raquet_1_points, raquet_2_points, ball, raquet_1, raquet_2, WIDTH, HEIGHT, BALL_DIMENSION)
        #Updates the window every loop
        update_window()
    
    #Quit pygame
    pygame.quit()

if __name__ == '__main__':
    main()