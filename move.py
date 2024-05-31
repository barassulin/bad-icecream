EMPTY_CUBE = 'empty_cube.jpg'


def movep(player):
    b = True
    player.xcube = player.xcube+player.direction[0]
    player.ycube = player.ycube+player.direction[1]
    return b
