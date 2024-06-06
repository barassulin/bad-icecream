import Map


class Player:
    def __init__(self, xcube, ycube, number, score, direction):
        self.xcube = xcube
        self.ycube = ycube
        self.number = number
        self.score = score
        self.direction = direction

    def set_player(self, xcube, ycube, number, score, direction):
        self.xcube = xcube
        self.ycube = ycube
        self.number = number
        self.score = score
        self.direction = direction

    def check_got_fruit(self, MAP):
        b = False
        specific_cube = MAP[self.ycube][self.xcube]
        if specific_cube.fruit > 0:
            self.score = self.score + specific_cube.got_fruit()
            b = True
        return b

    def move(self, player, MAP):
        x = self.xcube + self.direction[0]
        y = self.ycube + self.direction[1]
        if Map.check_on_map(x, y) and not MAP[y][x].ice:
            if x != player.xcube or y != player.ycube:
                self.xcube = self.xcube + self.direction[0]
                self.ycube = self.ycube + self.direction[1]
                MAP[self.ycube][self.xcube].player = self.number
                return True
        return False

