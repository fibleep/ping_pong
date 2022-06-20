from ursina import *
from HandTracker import HandTracker
app = Ursina()
hand_tracker = HandTracker()

window.color = rgb(29, 92, 47)

table = Entity(model='cube', scale=(10,.5,15),position=(0,0,0), color=rgb(20, 17, 92),texture='white_cube')
camera.position = (0,15,-25)
camera.rotation_x = 30

def update():
    lmList = hand_tracker.get_position_of_hand()
    if len(lmList) != 0:
        print(lmList)


app.run()
