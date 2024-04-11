import pygame
import random

""" Screen Size """
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 720

""" RGB VALUES FOR COLOURS """
COLOUR_BLACK = (0, 0, 0)
COLOUR_WHITE = (255, 255, 255)

""" Main Function """
def main():
  
  # Initialise pygame lib 
  pygame.init()

   # this creates the window for the game
  screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

  # set the window's title
  pygame.display.set_caption("Pong")

  """
  these are the players' game paddles
  the pygame.Rect function need the x, y, width and height
  of the rectangles we will be drawing (rects represent 
  sprites)
  """
  paddle_1_rect = pygame.Rect(30, 0, 7, 100)
  paddle_2_rect = pygame.Rect(SCREEN_WIDTH - 50, 0, 7, 100)

  # this is to track by how much the players' paddles will move per frame
  paddle_1_move = 0
  paddle_2_move = 0

  # this is the rectangle that represents the ball
  ball_rect = pygame.Rect(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 25, 25)

  # determine the x and y speed of the ball (0.1 is just to scale the speed down)
  ball_accel_x = random.randint(2, 4) * 0.1
  ball_accel_y = random.randint(2, 4) * 0.1

  # randomise the direction of the ball
  if random.randint(1, 2) == 1:
    ball_accel_x *= -1
  if random.randint(1, 2) == 1:
    ball_accel_y *= -1

  # create the clock object to keep track of the time
  clock = pygame.time.Clock()

  """
  this is to check whether or not to move the ball
  we will make it move after 3 seconds
  """
  started = False

  """
  get the time elapse between now and the last frame
  60 is an arbitrary number but the game runs smooth at 60 FPS
  """
  delta_time = clock.tick(60)

  # Game Loop 
  while True:
    """ Set the screen to black on default """
    screen.fill(COLOUR_BLACK)

    # make the ball move after 3 seconds
    if not started:
      # load the Consolas font
      font = pygame.font.SysFont('Consolas', 30)

      # draw some text to the center of the screen
      text = font.render('Press Space to Start', True, COLOUR_WHITE)
      text_rect = text.get_rect()
      text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
      screen.blit(text, text_rect)

      # update the display
      pygame.display.flip()

      clock.tick(60)

      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          return
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_SPACE:
            started = True

        continue

     # Checking for events
    for event in pygame.event.get():

      # if the user exits the window
      if event.type == pygame.QUIT:

        # exit the function, to finish the game
        return
      
      # if the user is pressing a key
      if event.type == pygame.KEYDOWN:

        # PLAYER 1
        # if the key is W, set the movement of paddle_1 to go up
        if event.key == pygame.K_w:
          paddle_1_move = -0.5

        # if the key is S, set the movement of paddle_1 to go down
        if event.key == pygame.K_s:
          paddle_1_move = 0.5

        # PLAYER 2
        # if the key is the up arrow, set the movement of paddle_2 to go up
        if event.key == pygame.K_UP:
          paddle_2_move = -0.5
        # if the key is the down arrow, set the movement of paddle_2 to go down
        if event.key == pygame.K_DOWN:
          paddle_2_move = 0.5

      # if the player released a key
      if event.type == pygame.KEYUP:
        # if the key released is w or s, stop the movement of paddle_1
        if event.key == pygame.K_w or event.key == pygame.K_s:
          paddle_1_move = 0.0

        # if the key released is the up or down arrow, stop the movement of paddle_2
        if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
          paddle_2_move = 0.0
      
      # draw player 1 and player 2's paddle rects with the white color
      pygame.draw.rect(screen, COLOUR_WHITE, paddle_1_rect)
      pygame.draw.rect(screen, COLOUR_WHITE, paddle_2_rect)

      # draw the ball with the white color
      pygame.draw.rect(screen, COLOUR_WHITE, ball_rect)

      # update the display (this is necessary for Pygame)
      pygame.display.update()

      # if the ball goes out of bounds, end the game
      if ball_rect.left <= 0 or ball_rect.left >= SCREEN_WIDTH:
        return

      # if the ball is getting close to the top (15 is an arbitrary number, but I found that it worked great)
      if ball_rect.top < 0:
        # invert its vertical velocity
        ball_accel_y *= -1
        # add a bit of y to it to not trigger the above code again
        ball_rect.top = 0
      # do the same thing with the bottom
      if ball_rect.bottom > SCREEN_HEIGHT - ball_rect.height:
        ball_accel_y *= -1
        ball_rect.top = SCREEN_HEIGHT - ball_rect.heigh

      """
      if paddle_1_rect collides with the ball and the ball is in front of it,
      change the speed of the ball and make it move a little in the other way
      """
      if paddle_1_rect.colliderect(ball_rect) and paddle_1_rect.left < ball_rect.left:
        ball_accel_x *= -1
        ball_rect.left += 5
      # do the same with paddle_2_rect
      if paddle_2_rect.colliderect(ball_rect) and paddle_2_rect.left > ball_rect.left:
        ball_accel_x *= -1
        ball_rect.left -= 5

      # if the game is started (after 3 seconds this is true)
      if started:
        # move the ball
        ball_rect.left += ball_accel_x * delta_time
        ball_rect.top += ball_accel_y * delta_time
    
    """
    move paddle_1 and paddle_2 according to their `move` variables
    we also multiply the `move` variable by the delta time to keep movement consistent through frames
    """
    paddle_1_rect.top += paddle_1_move * delta_time
    paddle_2_rect.top += paddle_2_move * delta_time

    if paddle_1_rect.top < 0:
      paddle_1_rect.top = 0
    if paddle_1_rect.bottom > SCREEN_HEIGHT:
      paddle_1_rect.bottom = SCREEN_HEIGHT
    if paddle_2_rect.top < 0:
      paddle_2_rect.top = 0
    if paddle_2_rect.bottom > SCREEN_HEIGHT:
      paddle_2_rect.bottom = SCREEN_HEIGHT

""" Wrap the main function """
if __name__ == '__main__':
  main()