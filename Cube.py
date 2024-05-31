"""
Cubes of map - by Bar Assulin
Date: 31/5/24
"""
window_width = 800
window_height = 775
PINK = (255, 146, 255)
IMAGE = 'screen1new.jpg'
ICE = 'ice.jpg'
EMPTY_CUBE = 'empty_cube.jpg'
PLAYER1_PIC = 'probPL1.jpg'
PLAYER2_PIC = 'probPL2.jpg'
REFRESH_RATE = 10
FRUIT1 = "cherry.jpg"
FRUIT2 = "strawberry.jpg"
FRUIT3 = "blueberry.jpg"


class Cube:
    def __init__(self, pixelw, pixelh, fruit, ice, player):
        self.pixelw = pixelw
        self.pixelh = pixelh
        self.fruit = fruit
        self.ice = ice
        self.player = player

    def update_ice(self):
        if self.ice:
            self.ice = False
        else:
            self.ice = True

    def got_fruit(self):
        score = self.fruit
        self.fruit = 0
        return score

    def create_fruit(self, points):
        self.fruit = points

    def update_player(self, player):
        self.player = player.number

