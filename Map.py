import Cube

size_cube = 57
size_line = 4
size_cube_and_line = size_cube + size_line
# the pixel number of the up left corner in every cube
up_limit = 84
left_limit = 91
# those are not existing cubes:
down_limit = 694
right_limit = 701


# arr map
def create_map():
    map = [[Cube.Cube(left_limit + x * size_cube_and_line, up_limit + y * size_cube_and_line, 0, False, 0) for x in
            range(10)]
           for y in range(10)]
    return map


def check_on_map(x, y):
    if 0 <= x < 10 and 0 <= y < 10:
        return True
    return False


if __name__ == '__main__':

    print(map)


# funcs
def update_all_ice():
    """
    get square - location
    get which direction -
        up(hight=hight-size_ice-size_line)
        down(hight=hight+size_ice+size_line)
        left(width=width-size_ice-size_line)
        right(width=width+size_ice+size_line)
    bool b = cube.is.ice(create/break)
    while hight/width != limit&&is.ice==b:
        func Cube.update_ice()
        update location
    """