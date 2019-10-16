from graphics import *
import string
import random
import math


class Paddle:
    def __init__(self, window, space_from_bottom, paddle_width, paddle_height):
        self.paddle_width = paddle_width
        self.paddle_height = paddle_height
        self.paddle_x = (window.getWidth() - paddle_width) / 2
        self.paddle_y = window.getHeight() - space_from_bottom
        self.rectangle = Rectangle(Point(self.paddle_x, self.paddle_y), Point(self.paddle_x + paddle_width, self.paddle_y + paddle_height))
        self.rectangle.setFill("light green")
        self.rectangle.setOutline("white")
        self.rectangle.draw(window)

    def moveByKey(self, key, win_width, offset):
        if key == "Left" and self.rectangle.p1.getX() > 0:
            self.rectangle.move(-1 * offset, 0)
        elif key == "Right" and self.rectangle.p2.getX() < win_width:
            self.rectangle.move(offset, 0)

    def getSurfaceCenter(self):
        surface_center = Point(self.rectangle.getCenter().getX(), self.rectangle.p1.getY())
        return surface_center

    def resetToCenter(self, window):
        self.rectangle.undraw()
        self.rectangle = Rectangle(Point(self.paddle_x, self.paddle_y), Point(self.paddle_x + self.paddle_width, self.paddle_y + self.paddle_height))
        self.rectangle.setFill("light green")
        self.rectangle.setOutline("white")
        self.rectangle.draw(window)

    def getRectangle(self):
        return self.rectangle


class Brick:
    def __init__(self, x, y, width, height, color, window, text):
        self.rectangle = Rectangle(Point(x, y), Point(x+width, y+height))
        self.rectangle.setFill(color)
        self.rectangle.draw(window)
        self.text = text

    def getRectangle(self):
        return self.rectangle

    def getScore(self):
        sum = 0
        for i in self.text:
            for character in i:
                character_value = ord(character) - ord("a")
            sum += character_value
        return sum


class Ball:
    def __init__(self, window, paddle, radius):
        p = paddle.getSurfaceCenter()
        self.circle = Circle(Point(p.getX(), p.getY() - radius), radius)
        self.circle.setFill("yellow")
        self.circle.draw(window)
        self.direction_list = [0,0]

    def moveIt(self):
        self.circle.move(self.direction_list[0], self.direction_list[1])

    def resetToPaddle(self, paddle):
        p = paddle.getSurfaceCenter()
        center_x = self.circle.getCenter().getX()
        center_y = self.circle.getCenter().getY()
        self.circle.move(-1 * (center_x - p.getX()), p.getY() - center_y - self.circle.getRadius() )


    def setRandomDirectionSpeed(self, min_speed=0.85, max_speed=3.0):
        horizontal_speed = (max_speed - min_speed) * random.random() + min_speed
        left_or_right = random.randint(1, 100) % 2 == 0 # Randomly applies negation to speed to make direction left or right
        if left_or_right:
            horizontal_speed *= -1
        vertical_speed = (max_speed - min_speed) * random.random() - max_speed
        self.direction_list[0] = horizontal_speed
        self.direction_list[1] = vertical_speed

    def getDirectionSpeed(self):
        return self.direction_list

    def setDirectionSpeed(self, d):
        self.direction_list = d

    def reverseX(self):
        self.direction_list[0] *= -1

    def reverseY(self):
        self.direction_list[1] *= -1

    def checkHitWindow(self, window):
        if self.circle.getP2().getX() >= window.getWidth():
            return True
        elif self.circle.getP1().getX() <= 0:
            return True
        elif self.circle.getP1().getY() <= 0:
            return True
        else:
            return False

    def checkHit(self, rectangle):
        rectangle_height = rectangle.getCenter().getY() - rectangle.getP1().getY()  # Half the height of the rectangle
        rectangle_width = rectangle.getP2().getX() - rectangle.getCenter().getX()  # Half the width of the rectangle
        distance = math.sqrt((abs(self.circle.getCenter().getX() - rectangle.getCenter().getX()) - rectangle_width) ** 2 + (abs(self.circle.getCenter().getY() - rectangle.getCenter().getY()) - rectangle_height) ** 2)

        if abs(self.circle.getCenter().getX() - rectangle.getCenter().getX()) > abs(rectangle_width + self.circle.getRadius()) \
                or abs(self.circle.getCenter().getY() - rectangle.getCenter().getY()) > abs(rectangle_height + self.circle.getRadius()):  # Checks if ball is in green zone
            return False

        elif abs(self.circle.getCenter().getX() - rectangle.getCenter().getX()) < rectangle_width:
            return True

        elif abs(self.circle.getCenter().getY() - rectangle.getCenter().getY()) < rectangle_height:
            return True

        elif distance < self.circle.getRadius():
            return True
        else:
            return False


def setupMessageScoreAndLifeInput(window, offset_from_center_x, offset_from_bottom):
    score_text = Text(Point(window.getWidth() / 2 + offset_from_center_x, window.getHeight() - offset_from_bottom), "SCORE: ")
    score_text.setTextColor("white")
    score_text.draw(window)
    score_number = Text(Point(window.getWidth() / 2 + 2 * offset_from_center_x, window.getHeight() - offset_from_bottom), "0")
    score_number.setTextColor("white")
    score_number.draw(window)
    life_text = Text(Point(window.getWidth() / 2 - 2 * offset_from_center_x, window.getHeight() - offset_from_bottom), "LIFE: ")
    life_text.setTextColor("white")
    life_text.draw(window)
    life_entry = Entry(Point(window.getWidth() / 2 - offset_from_center_x, window.getHeight() - offset_from_bottom), 3)
    life_entry.setTextColor("white")
    life_entry.draw(window)
    red_message = Text(Point(window.getWidth() / 2, window.getHeight() - 2 * offset_from_bottom),"")
    red_message.setTextColor("red")
    red_message.draw(window)

    return red_message, score_number, life_text, life_entry


def getLinesOfWords(filename):
    infile = open(filename, "r")
    line_list = infile.readlines()
    line_list = [line.rstrip().lower() for line in line_list]  # Removes every newline and lowers every character
    for temp in range(len(line_list)):
        # Replaces every non alphanumeric character within each line with a whitespace character
        for character in line_list[temp]:  # line_list is still a list of strings
            if character in string.punctuation:
                line_list[temp] = line_list[temp].replace(character, " ")

    for temp in range(len(line_list)):  # Splits each string within line_list into a list of words
        line_list[temp] = line_list[temp].split()

    good_list = []
    for line in line_list:  # Line is a list of words, removes the word if it's not within 2 and 8 characters
        list_per_line = []
        for word in line:  # line_list is now a two-dimensional list of words in the given range
            if 2 <= len(word) <= 8:
                list_per_line.append(word)
        good_list.append(list_per_line)

    return good_list


def makeLifeStatic(window, life_input):
    lives = int(life_input.getText())
    location = life_input.getAnchor()
    lives_text = Text(location, "")
    lives_text.setText(lives)
    lives_text.setTextColor("white")
    life_input.undraw()
    lives_text.draw(window)

    return lives, lives_text


def updateScore(score_offset, score_num_text):
    initial_score = int(score_num_text.getText())
    new_score = str(initial_score + score_offset)
    score_num_text.setText(new_score)
