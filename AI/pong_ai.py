
class AiPlayer():
    #MAKES THE raquet FOLLOW THE ball
    def move_raquet_intelligent(raquet, ball, height, raquet_height):
        if ball.y >= height - raquet_height:
            raquet.y = height - raquet_height
        else:
            y_ball = ball.y
            raquet.y = y_ball
        