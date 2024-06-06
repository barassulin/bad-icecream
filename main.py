"""
a client - by Bar Assulin
Date: 31/5/24
"""
import time
import pygame
import socket
import protocol
import pickle

# constants
size_cube = 57
size_line = 4
up_limit = 84
left_limit = 91
down_limit = 694
right_limit = 701
window_width = 800
window_height = 775
PINK = (255, 146, 255)
WHITE = (255, 255, 255)
START_SCREEN = 'pics/START_SCREEN.jpg'
END_SCREEN = 'pics/END_SCREEN.jpg'
IMAGE = 'pics/screen1new.jpg'
REFRESH_RATE = 10
# SERVER_IP = '172.16.6.65'
SERVER_IP = '127.0.0.1'
SERVER_PORT = 20003

# dict for files
FILE_DICTIONARY = {
    '1': 'pics/probPL1.jpg',
    '2': 'pics/probPL2.jpg',
    '5': "pics/cherry.jpg",
    '6': "pics/icedcherry.jpg",
    '7': "pics/strawberry.jpg",
    '8': "pics/icedberry.jpg",
    '10': "pics/blueberry.jpg",
    '11': "pics/icedblub.jpg",
    True: 'pics/ice.jpg',
    False: 'pics/empty_cube.jpg',
    "p1won": 'pics/PINK.jpg',
    "p2won": 'pics/PURPLE.jpg'
}


"""
checks if ice got to the limit: 
    
    if up_limit != down_limit:
        screen.blit(ice, [left_limit, up_limit])
        pygame.display.flip()
        up_limit = up_limit+61
"""


# funcs
def print_pic(file_name, x, y, key):
    """
    prints pics
    :param file_name: the pics file name
    :param x: x pixel on screen
    :param y: y pixel on screen
    :param key: the background color
    :return: nothing
    """
    pic = pygame.image.load(file_name).convert()
    if key is not None:
        pic.set_colorkey(key)
    screen.blit(pic, [x, y])
    pygame.display.flip()


def print_map(map):
    """
    prints all the cubes on the map
    :param map: cube list
    :return: nothing
    """
    for x in range(10):
        for y in range(10):
            if not map[y][x].ice:
                if str(map[y][x].player) not in FILE_DICTIONARY and str(map[y][x].fruit) not in FILE_DICTIONARY:
                    print_pic(FILE_DICTIONARY[map[y][x].ice], map[y][x].pixelw, map[y][x].pixelh, None)
            else:
                if str(map[y][x].fruit) in FILE_DICTIONARY:
                    print_pic(FILE_DICTIONARY[str(map[y][x].fruit + 1)], map[y][x].pixelw, map[y][x].pixelh, None)
                else:
                    print_pic(FILE_DICTIONARY[map[y][x].ice], map[y][x].pixelw, map[y][x].pixelh, None)
            if str(map[y][x].fruit) in FILE_DICTIONARY and not map[y][x].ice:
                print_pic(FILE_DICTIONARY[str(map[y][x].fruit)], map[y][x].pixelw, map[y][x].pixelh, None)
            if str(map[y][x].player) in FILE_DICTIONARY:
                print_pic(FILE_DICTIONARY[str(map[y][x].player)], map[y][x].pixelw, map[y][x].pixelh, None)


# init screen

pygame.init()
size = (window_width, window_height)
screen = pygame.display.set_mode(size)
GAME_OVER = False


def main():
    global GAME_OVER
    clock = pygame.time.Clock()
    global finish
    while not GAME_OVER:
        # server sending starting map
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((SERVER_IP, SERVER_PORT))
        client_socket.settimeout(20)
        img = pygame.image.load(START_SCREEN)
        screen.blit(img, (0, 0))
        print_pic(START_SCREEN, 0, 0, None)
        pygame.display.flip()
        finish = False
        while not finish:
            message = 0
            # Handle Pygame events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    finish = True
                elif event.type == pygame.KEYDOWN:
                    message = event.key
                    # client_socket.send(str(message).encode())
            # logging.debug("sending path as requested" + message)
            # client_socket.send(protocol.send_protocol(message).encode())
            client_socket.send(protocol.send_protocol(message))
            # client_socket.send(str(message).encode())

            response = client_socket.recv(1)
            if img != IMAGE:
                img = IMAGE
                print_pic(img, 0, 0, None)
                pygame.display.flip()
            if response == "":
                finish = True
                GAME_OVER = True

            else:
                response = protocol.recv_protocol(client_socket, response.decode())
                # response = response + client_socket.recv(4096)
                try:
                    print_pic(FILE_DICTIONARY[response], 0, 0, None)
                    time.sleep(5)
                    finish = True
                except Exception:
                    map = pickle.loads(response)
                    print_map(map)
            """
                # response = protocol.recv_protocol(client_socket, response)
            # logging.debug("getting msg request" + response)
            if response in FILE_DICTIONARY:
                print_pic(FILE_DICTIONARY[response], 0, 0, None)
                finish = True
            else:
                response = response
                MAP = pickle.loads(response)
                print("MAP")
                print_map(MAP)
            """
            # Tick the clock
            clock.tick(REFRESH_RATE)
        print_pic(END_SCREEN, 0, 0, None)
        time.sleep(1)

        b = True
        while b:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    GAME_OVER = True
                    message = pygame.K_UP
                    b = False
                    break
                elif event.type == pygame.KEYDOWN:
                    message = event.key
                    b = False
                    break
                clock.tick(REFRESH_RATE)
        if message != pygame.K_SPACE:
            GAME_OVER = True
            """
        if GAME_OVER != True:

            response = client_socket.recv(1).decode()
            response = protocol.recv_protocol(client_socket, response)
            if response.isnumeric():
                response = int(response)
            if response == "":
                GAME_OVER = True
            else:
                GAME_OVER = bool(response)
            """
        clock.tick(REFRESH_RATE)
        client_socket.close()
        print(finish)

    pygame.quit()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
