"""
Author: Bar Assulin
Date: 11.12.2023
Description: server.py for cyber2.7
"""
END_SIGN = "!"


def send_protocol(message):
    """
    send a string with her length
    :param message: the string
    :return: a string with her length
    """
    length = str(len(message))
    message = length + END_SIGN + message
    return message


def recv_protocol(socket, message):
    """
    get from socket the length of the string and the string
    :param socket: the socket
    :return: the string
    """
    length = ""
    while message != END_SIGN:
        length = length + message
        message = socket.recv(1).decode()
    message = socket.recv(int(length)).decode()
    return message
