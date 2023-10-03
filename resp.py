import socket
import sys
import threading
# Redis Serialization Protocol - RESP
# https://redis.io/docs/reference/protocol-spec/
# - Simple to implement, fast to parse, human readable
# TCP - 6379, or Unix sockets

CRLF = "\r\n"
LEN_CRLF = len(CRLF)


def parse_value(cmd):
    parts = []
    i = 0
    while cmd[i] != '\r':
        parts += cmd[i]
        i += 1
    return ("".join(parts), i+LEN_CRLF)


def parse_command(cmd):
    values = []
    offset = 0
    cmd_type = cmd[offset]
    offset += 1
    value, pos = parse_value(cmd[offset:])
    offset += pos
    if cmd_type == '*':
        count = int(value)
        print(count, pos)
        for _ in range(count):
            value, rel_offset = parse_command(cmd[offset:])
            values.append(value[0])
            offset += rel_offset
        print(values)
    elif cmd_type == "$":
        length = int(value)
        print(length)
        value = cmd[offset:offset+length]
        values.append(value)
        offset += length + LEN_CRLF
        print(value)
        print(offset)
    elif cmd_type == '+' or cmd_type == ':' or cmd_type == '-':
        values.append(value)
        print(value)

    return (values, offset)


def get_simple_string_reply(text):
    return "+" + text + CRLF


def get_bulk_string_reply(text):
    return "$" + str(len(text)) + CRLF + text + CRLF


def get_empty_array_reply():
    return "*0" + CRLF


KV_STORE = {}


def construct_reply(cmds, lock):
    resp = ""
    if cmds[0] == "PING":
        if len(cmds) == 1:
            resp = get_simple_string_reply("PONG")
        else:
            resp = get_bulk_string_reply(cmds[1])
    elif cmds[0] == "SET":
        key = cmds[1]
        val = cmds[2]
        with lock:
            KV_STORE[key] = val
        resp = get_simple_string_reply("OK")
    elif cmds[0] == "GET":
        key = cmds[1]
        with lock:
            val = KV_STORE.get(key, "nil")
        resp = get_bulk_string_reply(val)
    elif cmds[0] == "CONFIG":
        resp = get_empty_array_reply()
    return resp


def handle_client(conn, addr, lock):
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            print(data, type(data))
            if not data:
                print("Exiting client")
                break
            cmds, _ = parse_command(str(data, encoding='utf-8'))
            print('commands: ', cmds)
            reply = construct_reply(cmds, lock)
            if reply != "":
                data = bytes(reply, 'utf-8')
            else:
                print("Empty reply")
            conn.sendall(data)


def listen():
    HOST = '127.0.0.1'
    PORT = int(sys.argv[1])              # Arbitrary non-privileged port
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(1)
        while True:
            conn, addr = s.accept()
            lock = threading.Lock()
            thread = threading.Thread(target=handle_client, args=(conn,addr,lock))
            thread.start()
            print("number of threads: ", threading.active_count() - 1)


if __name__ == "__main__":
    # parse_command("+OK\r\n")
    # parse_command("-ERR unknown command 'asdf'\r\n")
    # parse_command(":1000\r\n")
    # parse_command("*2\r\n$4\r\necho\r\n$5\r\nhello\r\n")
    # parse_command("*3\r\n:1\r\n:2\r\n:3\r\n")
    # parse_command("$5\r\nworld\r\n")
    listen()
