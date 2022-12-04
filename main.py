import badger2040
import time
import random
import io
from machine import Pin
from game_engine import *

badger2040.system_speed(badger2040.SYSTEM_FAST)

button_a = Pin(badger2040.BUTTON_A, Pin.IN, Pin.PULL_DOWN)
button_up = Pin(badger2040.BUTTON_UP, Pin.IN, Pin.PULL_DOWN)

display = badger2040.Badger2040()
display_width = badger2040.WIDTH
display_height = badger2040.HEIGHT

high_score_path = "/highscore.txt"
high_score = 0

dino_img = Image("/dino.pbm")
cactus_img = Image("/cactus.pbm")

player = MovingObject(10, display_height - dino_img.height, dino_img, display, ground=display_height, gravity=0.02)
cactus = MovingObject(display_width - cactus_img.width, display_height - cactus_img.height, cactus_img, display, ground=display_height)
cactus2 = MovingObject(4 * display_width - cactus_img.width, display_height - cactus_img.height, cactus_img, display, ground=display_height)

objects = [player, cactus, cactus2]
obstacles = [cactus, cactus2]

for o in obstacles:
    o.set_motion_vector(-1, 0)

def clear_screen():
    display.pen(15)
    display.clear()
    display.pen(0)

def game_loop():
    global score
    score = 0

    clear_screen()
    display.update_speed(badger2040.UPDATE_TURBO)
    display.update()

    now = time.ticks_ms()
    for o in objects:
        o.physics_tick(now)

    player.set_pos(10, display_height - dino_img.height)
    cactus.set_pos(display_width - cactus_img.width, display_height - cactus_img.height)
    cactus2.set_pos(4 * display_width - cactus_img.width, display_height - cactus_img.height)

    while True:
        clear_screen()
        now = time.ticks_ms()
        if display.pressed(badger2040.BUTTON_UP) and player.on_ground():
            player.set_motion_vector(0, -2)
        for o in obstacles:
            if o.x <= -cactus_img.width:
                o.set_pos(x=display_width + random.randint(0, display_width))
                score += 1
                o.set_motion_vector(-1 - score * 0.05, 0)
        for o in objects:
            o.physics_tick(now)
            o.draw()
        display.text("Score: " + str(score), 10, 10)
        display.update()
        if player.collision_test(obstacles) != None or display.pressed(badger2040.BUTTON_A):
            break

def start_text():
    clear_screen()
    display.font("bitmap14_outline")
    display.text("Dino Game", 20, 20, 2)
    display.font("bitmap8")
    display.text("Press UP to start, A to abort", 20, 60, 2)
    display.text("High score: " + str(high_score), 20, 80, 2)
    display.update_speed(badger2040.UPDATE_FAST)
    display.update()

try:
    with io.open(high_score_path, "r") as f:
        try:
            high_score = int(f.readline())
        except ValueError:
            print("Cannot read high score")
except OSError:
    print("High score file not found")

start_text()

while True:
    if display.pressed(badger2040.BUTTON_UP):
        game_loop()
        if score != None and score > high_score:
            high_score = score
            print("Saving new high score: " + str(high_score));
            with io.open(high_score_path, "w") as f:
                f.write(str(score))
        start_text()
    elif display.pressed(badger2040.BUTTON_A):
        clear_screen()
        display.update_speed(badger2040.UPDATE_FAST)
        display.update()
        display.halt()
