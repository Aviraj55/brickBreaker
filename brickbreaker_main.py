import time
from hw5_lib import *

PART1 = False
PART2 = False
PART3 = False
PART4 = False
PART5 = False


def setupButtons(window, botton_width, botton_height, space_from_side, space_from_bottom):
    win_width, win_height = window.getWidth(), window.getHeight()
    start_btn = Rectangle(Point(space_from_side, win_height - space_from_bottom - botton_height), Point(space_from_side + botton_width, win_height - space_from_bottom))
    start_btn.setFill("black")
    start_btn.setOutline("white")
    start_text = Text(Point(space_from_side + botton_width / 2, win_height - space_from_bottom - botton_height / 2), "START")
    start_text.setTextColor("white")

    quit_btn = Rectangle(Point(win_width - space_from_side - botton_width, win_height - space_from_bottom - botton_height), Point(win_width - space_from_side, win_height - space_from_bottom))
    quit_btn.setFill("black")
    quit_btn.setOutline("white")
    quit_text = Text(Point(win_width - space_from_side - botton_width / 2, win_height - space_from_bottom - botton_height / 2), "QUIT")
    quit_text.setTextColor("white")
    return start_btn, start_text, quit_btn, quit_text


def setupBricks(lines_of_words, window, pixel_btwn_layers, pixel_per_char, brick_height, pixel_btwn_word, color_palette):
   bricks = []
   init_y = pixel_btwn_layers
   win_width = window.getWidth()
   for line in lines_of_words:
      total_x_len = calcTotalPixelsLength(line, pixel_per_char, pixel_btwn_word)
      init_x = (win_width - total_x_len) / 2
      for w in line:
         brick_width = pixel_per_char*len(w)
         bricks.append(Brick(init_x, init_y, brick_width, brick_height, color_palette[len(w)-2], window, w))
         init_x += (pixel_per_char*len(w) + pixel_btwn_word)
      init_y += pixel_btwn_layers
   return bricks

def showAndWaitStartClick(window, start_btn, start_text):
   start_btn.draw(window)
   start_text.draw(window)
   while True:
      click = window.getMouse()
      if start_btn.getP1().getX() < click.getX() < start_btn.getP2().getX() and start_btn.getP1().getY() < click.getY() < start_btn.getP2().getY():
         start_btn.undraw()
         start_text.undraw()
         break

def showAndWaitQuitClick(window, quit_btn, quit_text):
   quit_btn.draw(window)
   quit_text.draw(window)
   while True:
      click = window.getMouse()
      if quit_btn.getP1().getX() < click.getX() < quit_btn.getP2().getX() and quit_btn.getP1().getY() < click.getY() < quit_btn.getP2().getY():
         break

def calcTotalPixelsLength(line, pixel_per_char, pixel_btwn_word):
   total_x_len  = 0
   for w in line:
      total_x_len += pixel_per_char * len(w) + pixel_btwn_word
   total_x_len -= pixel_btwn_word
   return total_x_len

def checkTermination(window, ball, bricks, life):
   if ball.circle.getP2().getY() >= window.getHeight(): return life - 1
   elif len(bricks) == 0: return 0
   return life

def isCollide(ball, window, bricks, paddle):
   if ball.checkHitWindow(window) or ball.checkHit(paddle.getRectangle()):
      return (1, None)

   for brick in bricks:
      if ball.checkHit(brick.getRectangle()):
         return (2, brick)

   return (0, None)

def moveBall(ball, window, bricks, paddle):
   tmp_direction = ball.getDirectionSpeed()

   ball.setDirectionSpeed([tmp_direction[0], 0])
   ball.moveIt()
   status, brick = isCollide(ball, window, bricks, paddle)
   if status > 0:
      ball.setDirectionSpeed([-tmp_direction[0], 0])
      ball.moveIt()
      ball.setDirectionSpeed(tmp_direction)
      ball.reverseX()
      ball.moveIt()
      if status == 2:
         brick.getRectangle().undraw()
         bricks.remove(brick)
         return brick.getScore()
   else:
      ball.setDirectionSpeed(tmp_direction)

   ball.setDirectionSpeed([0, tmp_direction[1]])
   ball.moveIt()
   status, brick = isCollide(ball, window, bricks, paddle)
   if status > 0:
      ball.setDirectionSpeed([0, -tmp_direction[1]])
      ball.moveIt()
      ball.setDirectionSpeed(tmp_direction)
      ball.reverseY()
      ball.moveIt()
      if status == 2:
         brick.getRectangle().undraw()
         bricks.remove(brick)
         return brick.getScore()
   else:
      ball.setDirectionSpeed(tmp_direction)

   return 0

def movePaddleBall(paddle, window, ball, bricks, move_offset):
   key = window.checkKey()
   if key == "":
      return False


   if not ball.checkHit(Rectangle(Point(0, paddle.getRectangle().getP1().getY()), Point(window.getWidth(), paddle.getRectangle().getP2().getY()))):
      paddle.moveByKey(key, window.getWidth(), move_offset)
      return

   for _ in range(move_offset):
      paddle.moveByKey(key, window.getWidth(), 1)
      tmp_direction = ball.getDirectionSpeed()
      ball.setDirectionSpeed([tmp_direction[0], 0])
      ball.moveIt()
      status, _ = isCollide(ball, window, [], paddle)
      ball.setDirectionSpeed([-tmp_direction[0], 0])
      ball.moveIt()
      ball.setDirectionSpeed(tmp_direction)
      if status:
         ball.reverseX()
         ball.moveIt()

      ball.setDirectionSpeed([0, tmp_direction[1]])
      ball.moveIt()
      status, _ = isCollide(ball, window, [], paddle)
      ball.setDirectionSpeed([0, -tmp_direction[1]])
      ball.moveIt()
      ball.setDirectionSpeed(tmp_direction)
      if status:
         ball.reverseY()
         ball.moveIt()

def setMessage(message_text, message):
   message_text.setText(message)

def clearMessage(message_text):
   message_text.setText("")

def clearKey(window):
   start_time = time.time()
   while time.time() < start_time + 0.05:
      window.checkKey()

def main():
   window = GraphWin("Brick Breaker", 800, 600, autoflush=False)
   window.setBackground("black")

   paddle = Paddle(window, space_from_bottom=100, paddle_width=100, paddle_height=10)

   ball = Ball(window, paddle, radius=5)
   ball.setRandomDirectionSpeed(min_speed=0.85, max_speed=2.0)

   start_btn, start_text, quit_btn, quit_text = setupButtons(window, botton_width=120, botton_height=30, space_from_side=60, space_from_bottom=30)

   message_text, score_num_text, life_text, life_input = setupMessageScoreAndLifeInput(window, offset_from_center_x=50, offset_from_bottom=30)

   while PART1:
      window.update()
      time.sleep(1)

   palette = [
      color_rgb(180,230,128),
      color_rgb(52,178,228),
      color_rgb(6,83,129),
      color_rgb(139,16,62),
      color_rgb(227,72,86),
      color_rgb(254,154,42),
      color_rgb(230, 209, 174)
   ]
   lines_of_words = getLinesOfWords("document.txt")

   if PART2:
      window.update()
      print(lines_of_words)
      while True: time.sleep(1)

   bricks = setupBricks(lines_of_words, window, pixel_btwn_layers=30, pixel_per_char=10, brick_height=10, pixel_btwn_word=4, color_palette=palette)

   setMessage(message_text, "Enter the LIFE and click START button to launch")
   showAndWaitStartClick(window, start_btn, start_text)

   life, life_num_text = makeLifeStatic(window, life_input)
   clearMessage(message_text)
   clearKey(window)

   while PART3:
      window.update()
      time.sleep(1)

   life_max = life
   while True:
      new_life = checkTermination(window, ball, bricks, life)
      life_num_text.setText(str(new_life))
      if new_life == 0:
         setMessage(message_text, "Game Over. Click QUIT button to close")
         showAndWaitQuitClick(window, quit_btn, quit_text)
         break
      elif new_life != life:
         life = new_life
         paddle.resetToCenter(window)
         ball.resetToPaddle(paddle)
         ball.setRandomDirectionSpeed(min_speed=min(0.85*life_max/life, 2.0), max_speed=max(0.9*life_max/life, 2.5))
         setMessage(message_text, "Click START button to relaunch")
         showAndWaitStartClick(window, start_btn, start_text)
         clearMessage(message_text)
         clearKey(window)

      movePaddleBall(paddle, window, ball, bricks, move_offset=25)
      if PART4: continue
      score_offset = moveBall(ball, window, bricks, paddle)
      if PART5: continue
      updateScore(score_offset, score_num_text)

main()
