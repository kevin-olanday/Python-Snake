# Simple Snake game that runs in a terminal
# Code is a fork of https://github.com/Carla-Codes/simple-snake-game-python/

import curses
from curses import KEY_UP, KEY_DOWN, KEY_RIGHT, KEY_LEFT, wrapper
from random import randint



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

# initialize the instructions window
window2 = curses.newwin(20, 30, 0, 0)  # create game window
window2.border(0)
window2.addstr(0, 11, ' SNAKE ',  curses.color_pair(1))
window2.addstr(5, 3,"Press ↑, ↓, →, ← to move")
window2.addstr(7, 3,"Press ENTER to start game")
window2.addstr(8, 4,"Press ESC to exit game")
window2.addstr(12,14,".'`_ o `;__,", curses.color_pair(1))
window2.addstr(13,4,".       .'.'` '---'  '", curses.color_pair(1))
window2.addstr(14,4,".`-...-'.'", curses.color_pair(1))
window2.addstr(15,4," `-...-'", curses.color_pair(1))

# initialize global variables
key = ""
score = 0

# initialize first food and snake coordinates
snake = [[5, 8], [5, 7], [5, 6]]
food = [10, 15]

# display the first food
window.addch(food[0], food[1], '○', curses.color_pair(2) | curses.A_BLINK)

class Snake:
    def __init__(self, coordinates):
        self.coordinates = coordinates
        self.length = len(coordinates)
        self.head_coordinates = list(coordinates[0])

    def __repr__(self):
        return f"Snake at coordinates {self.coordinates} with length {self.length}"

    def move_snake(self, direction):
        self.head_coordinates[0] += (direction == "down" and 1) + (direction == "up" and -1)      
        self.head_coordinates[1] += (direction == "left" and -1) + (direction == "right" and 1)
        self.coordinates.insert(0, [self.head_coordinates[0], self.head_coordinates[1]])
        
        if self.head_coordinates != food2.coordinates:
            head = self.coordinates.pop()
            window.addch(head[0], head[1], ' ')
        window.addch(snake2.head_coordinates[0], snake2.head_coordinates[1], '#', curses.color_pair(1))


class Food:
    def __init__(self, coordinates, type = "Normal"):
        self.coordinates = coordinates
        self.type = type
        window.addch(self.coordinates[0], self.coordinates[1], '○', curses.color_pair(2)) 

    def __repr__(self):
        return f"{self.type} food at {self.coordinates}"

snake2 = Snake([[10, 8], [10, 7], [10, 6]])
food2 = Food([18, 15])


while key != 10 and key != 27: # While the user hasn't started the game
     event = window2.getch()
     key = key if event == -1 else event
     window2.refresh()

key = KEY_RIGHT
  
counter = 0
while key != 27:  # While they Esc key is not pressed

    window.border(0)
    # display the score and title
    window2.addstr(19, 11, 'Score: ' + str(score) + ' ', curses.color_pair(2))
    window2.refresh()
    # make the snake faster as it eats more
    window.timeout(140 - (int(len(snake)/5) + int(len(snake)/10)) % 120)
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
    
    snake2.move_snake(direction)

    snake.insert(0, [snake[0][0] + (key == KEY_DOWN and 1) + (key == KEY_UP and -1),
                 snake[0][1] + (key == KEY_LEFT and -1) + (key == KEY_RIGHT and 1)])
    # Exit if snake crosses the boundaries (Uncomment to enable)
    if snake[0][0] == 0 or snake[0][0] == 19 or snake[0][1] == 0 or snake[0][1] == 29:
        break
    # Exit if snake runs over itself
    if snake[0] in snake[1:]:
        break

    # When snake eats the food
    if snake[0] == food:
        counter = 0
        food = []
        score += 1
        while food == []:
            # Generate coordinates for next food
            food = [randint(1, 18), randint(1, 28)]
            if food in snake:
                food = []
        window.addch(food[0], food[1], '○', curses.color_pair(2))  # display the food
        window2.addch(12,19,">", curses.color_pair(1))
    else:
        counter += 1
        if(counter > 2): window2.addch(12,19,"○", curses.color_pair(1))
        last = snake.pop()
        window.addch(last[0], last[1], ' ')
    window.addch(snake[0][0], snake[0][1], '#', curses.color_pair(1))  # add food to snakes tail
curses.endwin()  # close the window and end the game
print("\nScore: " + str(score))
