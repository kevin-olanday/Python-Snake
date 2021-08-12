# Simple Snake game that runs in a terminal
# Code is a fork of https://github.com/Carla-Codes/simple-snake-game-python/

import curses
from curses import KEY_UP, KEY_DOWN, KEY_RIGHT, KEY_LEFT
from random import randint


# initialize the game window
curses.initscr()  # initialize screen
window = curses.newwin(20, 30, 0, 0)  # create new window
window.keypad(True)  # enable keypad
curses.noecho()  # turn off automatic echoing of keys
curses.curs_set(0)  # hide the cursor
window.nodelay(True)  # do not wait for the user input

# initialize global variables
key = KEY_RIGHT
score = 0

# initialize first food and snake coordinates
snake = [[5, 8], [5, 7], [5, 6]]
food = [10, 15]

# display the first food
window.addch(food[0], food[1], 'O')

while key != 27:  # While they Esc key is not pressed
    window.border(0)
    # display the score and title
    window.addstr(19, 11, 'Score: ' + str(score) + ' ')
    window.addstr(0, 11, ' SNAKE ')
    # make the snake faster as it eats more
    window.timeout(140 - (int(len(snake)/5) + int(len(snake)/10)) % 120)
    # refreshes the screen and then waits for the user to hit a key
    event = window.getch()
    key = key if event == -1 else event

    # Calculates the new coordinates of the head of the snake.
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
        food = []
        score += 1
        while food == []:
            # Generate coordinates for next food
            food = [randint(1, 18), randint(1, 28)]
            if food in snake:
                food = []
        window.addch(food[0], food[1], 'O')  # display the food
    else:
        last = snake.pop()
        window.addch(last[0], last[1], ' ')
    window.addch(snake[0][0], snake[0][1], '#')  # add food to snakes tail
curses.endwin()  # close the window and end the game
print("\nScore: " + str(score))
