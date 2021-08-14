# Simple Snake game that runs in a terminal
# Code is a fork of https://github.com/Carla-Codes/simple-snake-game-python/

import curses
from curses import KEY_UP, KEY_DOWN, KEY_RIGHT, KEY_LEFT, wrapper
from random import randint


class Score:
    def __init__(self, value = 0):
        self.value = value
    
    def add(self, points):
        self.value += points
    
class Snake:
    def __init__(self, coordinates):
        self.coordinates = coordinates
        self.length = len(coordinates)
        self.head_coordinates = list(coordinates[0])
        self.speed = 1

    def __repr__(self):
        return f"Snake at coordinates {self.coordinates} with length {self.length}"

    def move(self, direction):
        self.head_coordinates[0] += (direction == "down" and 1) + (direction == "up" and -1)      
        self.head_coordinates[1] += (direction == "left" and -1) + (direction == "right" and 1)
        self.coordinates.insert(0, [self.head_coordinates[0], self.head_coordinates[1]])        
        if self.head_coordinates != food.coordinates:
            head = self.coordinates.pop()
            window.addch(head[0], head[1], ' ')
        window.addch(self.head_coordinates[0], self.head_coordinates[1], '#', curses.color_pair(1))

    def set_speed(self, speed = 1):
        print(speed)
        window.timeout(150 - speed)
        
    def eat_food(self, food):
        print("nom!")
        self.length += 1
        self.set_speed(self.length)
        if food.type == "Normal":
            window2.addch(12,19,">", curses.color_pair(1))

class Food:
    def __init__(self, coordinates, type = "Normal"):
        self.coordinates = coordinates
        self.type = type
        self.display()

    def __repr__(self):
        return f"{self.type} food at {self.coordinates}"

    def display(self):
        window.addch(self.coordinates[0], self.coordinates[1], '○', curses.color_pair(2)) 

    def respawn(self):
        while self.coordinates in snake.coordinates:
           self.coordinates = [randint(1, 18), randint(1, 28)]
        self.display()

# initialize the game window 
curses.initscr()  # initialize screen
curses.start_color()  # initialize colors
curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
curses.noecho()  # turn off automatic echoing of keys
curses.curs_set(0)  # hide the cursor
window = curses.newwin(20, 30, 0, 30)  # create game window
window.keypad(True)  # enable keypad
window.nodelay(True)  # do not wait for the user input
window.timeout(150)

# initialize the instructions window
window2 = curses.newwin(20, 30, 0, 0)  # create game window
window2.border(0)
window2.addstr(0, 10, '[ SNAKE ]',  curses.color_pair(1))
window2.addstr(5, 3,"Press ↑, ↓, →, ← to move")
window2.addstr(7, 3,"Press ENTER to start game")
window2.addstr(8, 4,"Press ESC to exit game")
window2.addstr(12,14,".'`_ o `;__,", curses.color_pair(1))
window2.addstr(13,4,".       .'.'` '---'  '", curses.color_pair(1))
window2.addstr(14,4,".`-...-'.'", curses.color_pair(1))
window2.addstr(15,4," `-...-'", curses.color_pair(1))

# initialize global variables
key = ""
score = Score()

# initialize first food and snake coordinates
snake = Snake([[5, 8], [5, 7], [5, 6]])
food = Food([18, 15])


while key != 10 and key != 27: # While the user hasn't started the game
     event = window2.getch()
     key = key if event == -1 else event
     window2.refresh()

key = KEY_RIGHT
  
while key != 27:  # While they Esc key is not pressed
    window.border(0)
    # display the score and title
    window2.addstr(19, 11, 'Score: ' + str(score.value) + ' ', curses.color_pair(2))
    window2.refresh()
    # refreshes the screen and then waits for the user to hit a key
    event = window.getch()
    key = key if event == -1 else event


    # Calculates the new coordinates of the head of the snake.
    if key == KEY_DOWN:
        direction = "down"
    elif key == KEY_UP:
        direction = "up"
    elif key == KEY_LEFT:
        direction = "left"
    elif key == KEY_RIGHT:
        direction = "right"
    
    snake.move(direction)

    # Exit if snake crosses the boundaries or runs over itself
    if snake.head_coordinates[0] == 0 or snake.head_coordinates[0] == 19 or snake.head_coordinates[1] == 0 or snake.head_coordinates[1] == 29 or snake.head_coordinates in snake.coordinates[1:]:
        window.addstr(9, 10,"GAME OVER!", curses.color_pair(3))
        while key != 27:
            event = window.getch()
            key = key if event == -1 else event
        break

    # If snake hits food
    if snake.head_coordinates == food.coordinates:
        snake.eat_food(food)
        score.add(1)
        food.respawn()
#curses.endwin()  # close the window and end the game
print("\nScore: " + str(score.value))
