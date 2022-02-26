
class AiPlayer():
    #MOVES RAQUET UP AND DOWN (naive AI)
    def move_raquet(RAQUET_1, RAQUET_VEL):
        RAQUET_1.y += RAQUET_VEL

    #MAKES THE RAQUET FOLLOW THE BALL
    def move_raquet_intelligent(RAQUET, BALL, HEIGHT, RAQUET_HEIGHT):
        if BALL.y >= HEIGHT - RAQUET_HEIGHT:
            RAQUET.y = HEIGHT - RAQUET_HEIGHT
        else:
            y_ball = BALL.y
            RAQUET.y = y_ball
        