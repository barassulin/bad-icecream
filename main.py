# This is a sample Python script.
import time

import Map
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import move
import pygame
import Player
import socket
import select
import protocol
import random
import pickle

# constants

size_cube = 57
size_line = 4

# the pixel number of the up left corner in every cube
up_limit = 84
left_limit = 91
# those are not existing cubes:
down_limit = 694
right_limit = 701

window_width = 800
window_height = 775
PINK = (255, 146, 255)
WHITE = (255, 255, 255)
IMAGE = 'pics/screen1new.jpg'

REFRESH_RATE = 10

FRUITS = 7

SERVER_IP = '127.0.0.1'
SERVER_PORT = 20003

FILE_DICTIONARY = {
    '1': 'pics/probPL1.jpg',
    '2': 'pics/probPL2.jpg',
    '10': "pics/cherry.jpg",
    '20': "pics/strawberry.jpg",
    '30': "pics/blueberry.jpg",
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
    pic = pygame.image.load(file_name).convert()
    if key is not None:
        pic.set_colorkey(key)
    screen.blit(pic, [x, y])
    pygame.display.flip()


def print_map(map):
    for x in range(10):
        for y in range(10):
            print_pic(FILE_DICTIONARY[map[y][x].ice], map[y][x].pixelw, map[y][x].pixelh, None)
            if str(map[y][x].fruit) in FILE_DICTIONARY:
                print_pic(FILE_DICTIONARY[str(map[y][x].fruit)], map[y][x].pixelw, map[y][x].pixelh, None)
            if str(map[y][x].player) in FILE_DICTIONARY:
                print_pic(FILE_DICTIONARY[str(map[y][x].player)], map[y][x].pixelw, map[y][x].pixelh, None)


# init screen
pygame.init()
size = (window_width, window_height)
screen = pygame.display.set_mode(size)
img = pygame.image.load(IMAGE)
clock = pygame.time.Clock()


def main():
    screen.blit(img, (0, 0))
    pygame.display.flip()

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_IP, SERVER_PORT))
    client_socket.settimeout(20)
    # server sending starting map
    finish = False
    while not finish:
        message = 0
        # Handle Pygame events
        for event in pygame.event.get():
            print("check")
            if event.type == pygame.QUIT:
                finish = True
            elif event.type == pygame.KEYDOWN:
                message = event.key
                # client_socket.send(str(message).encode())
        # logging.debug("sending path as requested" + message)
        # client_socket.send(protocol.send_protocol(message).encode())
        client_socket.send(str(message).encode())

        response = client_socket.recv(1)

        if response == "":
            finish = True

        else:
            response = response + client_socket.recv(4096)
            try:
                print(response.decode())
                print_pic(FILE_DICTIONARY[response.decode()], 0, 0, None)
                time.sleep(5)
            except Exception:
                MAP = pickle.loads(response)
                print_map(MAP)
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

    client_socket.close()

    pygame.quit()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
