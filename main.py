from ursina import *

from game_logic import GameLogic
from hand_tracker import HandTracker

app = Ursina()
window.fullscreen_resolution = (1920, 1080)
window.fullscreen = True

hand_tracker = HandTracker()
game_logic = GameLogic()

window.color = rgb(29, 92, 47)

# Initializing the entities

table = Entity(model='cube', scale=(15, .5, 20), position=(0, 0, 0), color=rgb(20, 17, 92), texture='white_cube')
net = Entity(parent=table, model='quad', scale=(.98, 3, .5), position=(0, .5, 0), color=color.white,
             texture='white_cube')
ball = Entity(model='sphere', color=color.white, collider='sphere', position=(5, 0.5, 10))
racket = Entity(model='sphere', scale=(2, 0.5, 3), color=color.red, collider='sphere', position=(5, 0.5, -10))

# adjusting the camera

camera.position = (0, 15, -30)
camera.rotation_x = 30

served = False


def update():
    lmList = hand_tracker.get_position_of_hand()
    if len(lmList) != 0:
        racket.position = game_logic.calculate_position_of_racket(lmList[9], 1.6)
    if hand_tracker.get_gesture(lmList) == 'fist' and not served:
        ball.position = racket.position
    ball.z = ball.z + 0.1


app.run()
