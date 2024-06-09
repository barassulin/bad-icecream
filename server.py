"""
a select server - by Bar Assulin
Date: 31/5/24
"""
import select
import socket
import protocol
import pickle
import logging
import Map
import pygame
import Player
import random
import IceLoop

# constants
MAX_CLIENTS = 2
size_cube = 57
size_line = 4
up_limit = 84
left_limit = 91
down_limit = 694
right_limit = 701
LOG_FILE = 'server.log'
USERS_FILE = 'conf/users.txt'
ADMIN_ROLE = 'admin'
USER_ROLE = 'user'
USER_ROLE_SEPARATOR = ','
USERS_LINE_SEPARATOR = '\n'
SERVER_IP = '0.0.0.0'
SERVER_PORT = 20003
LISTEN_SIZE = 5
READ_SIZE = 1024
ADMIN_SIGN = '!'
AT_SIGN = ':'
FRUITS = 7
GAME_OVER = False

inputs = []
outputs = []
message_queues = {}
exceptional = []
finish = False

player1 = Player.Player(4, 4, 1, 0, [0, -1])
player2 = Player.Player(5, 5, 2, 0, [0, 1])
MAP = [], []

# players by index
SOURCE_DICTIONARY = {
    0: player1,
    1: player2
}

ICE_LOOP: list[IceLoop.IceLoop] = []


def send_message_to_all(message, open_client_sockets):
    """
    Sends the same message to all connected clients.
    :param message: The message to be sent.
    :param open_client_sockets: List of open client sockets.
    """
    for client_socket in open_client_sockets:
        client_socket.send(protocol.send_protocol(message))


def handle_new_connection(server_socket, open_client_sockets):
    client_socket, client_address = server_socket.accept()
    open_client_sockets.append(client_socket)


def handle_data(current_socket):
    data = current_socket.recv(1).decode()
    if data == "":
        data = None
    else:
        data = protocol.recv_protocol(current_socket, data)
        if data.isnumeric():
            data = int(data)
    """
    if data == '':
        # logout(current_socket, open_client_sockets)
        data = None
        return data
    else:
        data = data + current_socket.recv(4095).decode()
        print("data" + data)

    data = int(data)
        # data = protocol.recv_protocol(current_socket, data)
    # logging.log(data)
    """
    return data


def send_waiting_massages(list_of_messages, wlist):
    for message in list_of_messages:
        client_socket, msg = message
        if client_socket in wlist:
            client_socket.send(protocol.send_protocol(msg))
            # client_socket.send(msg.encode())
            list_of_messages.remove(message)


def is_ice_loop(x, y, is_ice):
    if Map.check_on_map(x, y):
        if is_ice == MAP[y][x].ice:
            if (x != player1.xcube or y != player1.ycube) and (x != player2.xcube or y != player2.ycube):
                return True
    return False


def try_move(player, player2):
    x = player.xcube
    y = player.ycube

    if player.move(player2, MAP):
        MAP[y][x].player = 0


def set_players():
    player1.set_player(4, 4, 1, 0, [0, -1])
    player2.set_player(5, 5, 2, 0, [0, 1])
    MAP[4][4].player = player1.number
    MAP[5][5].player = player2.number


def logout(current_socket, open_client_sockets):
    open_client_sockets.remove(current_socket)
    current_socket.close()


def create_all_fruits():
    counter = 0
    points = 5
    while counter < 7:
        if counter == 4:
            points = 7
        if counter == 6:
            points = 10
        numx = random.randint(0, 9)
        numy = random.randint(0, 9)
        while MAP[numy][numx].fruit != 0:
            numx = random.randint(0, 9)
            numy = random.randint(0, 9)
        MAP[numy][numx].create_fruit(points)
        counter = counter + 1


def set_map():
    global MAP
    MAP = Map.create_map()
    set_players()
    create_all_fruits()


def who_won(pl1, pl2):
    if pl1.score > pl2.score:
        return pl1
    elif pl1.score < pl2.score:
        return pl2
    else:
        return None


def update_map(data, client_index):
    print("client_index")
    print(client_index)
    player = SOURCE_DICTIONARY[client_index]
    print(player)

    if len(ICE_LOOP) < MAX_CLIENTS:
        ICE_LOOP.append(IceLoop.IceLoop(False, player1.xcube, player1.ycube, player1.direction[0],
                                        player1.direction[1], MAP[player1.ycube][player1.xcube].ice))
        ICE_LOOP.append(IceLoop.IceLoop(False, player2.xcube, player2.ycube, player2.direction[0],
                                        player2.direction[1], MAP[player2.ycube][player2.xcube].ice))

    if ICE_LOOP[client_index].is_working:
        MAP[ICE_LOOP[client_index].ycube][ICE_LOOP[client_index].xcube].update_ice()
        ICE_LOOP[client_index].xcube = ICE_LOOP[client_index].xcube + ICE_LOOP[client_index].xdir
        ICE_LOOP[client_index].ycube = ICE_LOOP[client_index].ycube + ICE_LOOP[client_index].ydir
        ICE_LOOP[client_index].is_working = is_ice_loop(ICE_LOOP[client_index].xcube, ICE_LOOP[client_index].ycube,
                                                        ICE_LOOP[client_index].is_ice)

    # if data == pygame.KEYDOWN:
    moved = True
    if data == pygame.K_SPACE:

        if not ICE_LOOP[client_index].is_working:
            ICE_LOOP[client_index].xdir = player.direction[0]
            ICE_LOOP[client_index].ydir = player.direction[1]
            ICE_LOOP[client_index].xcube = player.xcube + ICE_LOOP[client_index].xdir
            ICE_LOOP[client_index].ycube = player.ycube + ICE_LOOP[client_index].ydir
            if Map.check_on_map(ICE_LOOP[client_index].xcube, ICE_LOOP[client_index].ycube):
                ICE_LOOP[client_index].is_ice = MAP[ICE_LOOP[client_index].ycube][ICE_LOOP[client_index].xcube].ice
            ICE_LOOP[client_index].is_working = is_ice_loop(ICE_LOOP[client_index].xcube, ICE_LOOP[client_index].ycube,
                                                            ICE_LOOP[client_index].is_ice)
        moved = False
    if data == pygame.K_UP:
        print(pygame.K_UP)
        print("pygame.K_UP")
        player.direction = [0, -1]
    elif data == pygame.K_DOWN:
        print(pygame.K_DOWN)
        print("pygame.K_DOWN")
        player.direction = [0, 1]
    elif data == pygame.K_LEFT:
        print(pygame.K_LEFT)
        print("pygame.K_LEFT")
        player.direction = [-1, 0]
    elif data == pygame.K_RIGHT:
        print(pygame.K_RIGHT)
        print("pygame.K_RIGHT")
        player.direction = [1, 0]
    else:
        moved = False
    if moved:
        if client_index == 1:
            secoendplayer = SOURCE_DICTIONARY[0]
        else:
            secoendplayer = SOURCE_DICTIONARY[1]
        try_move(player, secoendplayer)

    if player.check_got_fruit(MAP):
        global FRUITS
        FRUITS = FRUITS - 1

    if FRUITS == 0:
        global finish
        finish = True


def receive_responses(server_socket, open_client_sockets):
    responses = {}
    # Loop until responses are received from all clients
    while len(responses) < MAX_CLIENTS:
        # Use select to monitor sockets for incoming data
        rlist, _, _ = select.select([server_socket] + open_client_sockets, [], [])
        # Iterate over sockets with incoming data

        for current_socket in rlist:
            if current_socket is server_socket:
                if len(open_client_sockets) >= MAX_CLIENTS:
                    client_socket, client_address = current_socket.accept()
                    client_socket.close()
                else:

                    client_socket, client_address = current_socket.accept()
                    # logging.log('received a new connection from '
                    # + str(client_address[0]) + ':'
                    # + str(client_address[1]))
                    open_client_sockets.append(client_socket)
                    # send starting map
            else:
                # Receive response from client
                response = handle_data(current_socket)
                # Check if response is empty, indicating client disconnected
                if response is not None:
                    client_index = open_client_sockets.index(current_socket)
                    responses[current_socket] = response
                    update_map(response, client_index)
                    """
                        else:
                            logout(current_socket, open_client_sockets)
                            open_client_sockets[0].send(protocol.send_protocol(msg))
                    """


def main_loop(server_socket):
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen(LISTEN_SIZE)
    global GAME_OVER
    global FRUITS
    global finish
    while True:
        print('setting game')
        FRUITS = 7
        finish = False
        set_map()
        messages_to_send = []
        open_client_sockets = []
        rlist, wlist, xlist = select.select([server_socket]
                                            + open_client_sockets,
                                            [], open_client_sockets)
        while not finish:
            for current_socket in xlist:
                # logging.log('handling exception socket')
                open_client_sockets.remove(current_socket)
                current_socket.close()
            receive_responses(server_socket, open_client_sockets)
            # message = protocol.send_protocol(pickle.dumps(MAP).decode())
            if not finish:
                message = pickle.dumps(MAP)
            else:
                if player1.score > player2.score:
                    message = "p1won".encode()
                else:
                    message = "p2won".encode()
            send_message_to_all(message, open_client_sockets)
        print("hi")
        for current_socket in open_client_sockets:
            if current_socket != server_socket:
                logout(current_socket, open_client_sockets)
        """
        #
        for current_socket in open_client_sockets:
            open_client_sockets.remove(current_socket)
            current_socket.close()
        
        """

        # send_message_to_all(GAME_OVER, open_client_sockets)


# except socket.error as err:
# logging.log('received socket error - exiting, ' + str(err))


def main():
    server_socket = socket.socket()

    main_loop(server_socket)

    server_socket.close()


if __name__ == '__main__':
    # logging.activate_log(LOG_FILE)
    main()
