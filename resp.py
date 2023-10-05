import asyncio
import sys
import time
from types import SimpleNamespace
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
        for _ in range(count):
            value, rel_offset = parse_command(cmd[offset:])
            values.append(value[0])
            offset += rel_offset
    elif cmd_type == "$":
        length = int(value)
        value = cmd[offset:offset+length]
        values.append(value)
        offset += length + LEN_CRLF
    elif cmd_type == '+' or cmd_type == ':' or cmd_type == '-':
        values.append(value)

    return (values, offset)


def get_simple_string_reply(text):
    return "+" + text + CRLF


def get_bulk_string_reply(text):
    return "$" + str(len(text)) + CRLF + text + CRLF


def get_empty_array_reply():
    return "*0" + CRLF


KV_STORE = {}


async def construct_reply(cmds, lock):
    resp = ""
    if cmds[0] == "PING":
        if len(cmds) == 1:
            resp = get_simple_string_reply("PONG")
        else:
            resp = get_bulk_string_reply(cmds[1])
    elif cmds[0] == "SET":
        key = cmds[1]
        val = cmds[2]
        sn = SimpleNamespace(val=val, expiry=-1)
        if len(cmds) > 3:
            sn.expiry = int(cmds[4]) + time.time()
        async with lock:
            KV_STORE[key] = sn
        resp = get_simple_string_reply("OK")
    elif cmds[0] == "GET":
        key = cmds[1]
        async with lock:
            sn = KV_STORE.get(key, "nil")
        resp = get_bulk_string_reply(sn.val if sn != "nil" else "nil")
    elif cmds[0] == "CONFIG":
        resp = get_empty_array_reply()
    return resp


async def handle_client(reader, writer, lock):
    while True:
        data = await reader.read(100)
        message = data.decode()
        cmds, _ = parse_command(message)
        print('commands: ', cmds)
        reply = await construct_reply(cmds, lock)
        if reply != "":
            data = bytes(reply, 'utf-8')
        else:
            print("Empty reply")
        writer.write(data)
        await writer.drain()


async def check_key_expiry(interval, lock):
    async def check(lock):
        async with lock:
            cur_time = time.time()
            for k in list(KV_STORE):
                v = KV_STORE[k]
                if v.expiry != -1 and v.expiry <= cur_time:
                    KV_STORE.pop(k)
    while True:
        await asyncio.gather(
            asyncio.sleep(interval),
            check(lock),
        )


async def listen(lock):
    HOST = '127.0.0.1'
    PORT = int(sys.argv[1])              # Arbitrary non-privileged port
    server = await asyncio.start_server(
            lambda r, w: handle_client(r, w, lock), HOST, PORT)
    async with server:
        await server.serve_forever()


async def main():
    lock = asyncio.Lock()
    await asyncio.gather(listen(lock), check_key_expiry(1, lock))


if __name__ == "__main__":
    # parse_command("+OK\r\n")
    # parse_command("-ERR unknown command 'asdf'\r\n")
    # parse_command(":1000\r\n")
    # parse_command("*2\r\n$4\r\necho\r\n$5\r\nhello\r\n")
    # parse_command("*3\r\n:1\r\n:2\r\n:3\r\n")
    # parse_command("$5\r\nworld\r\n")
    asyncio.run(main())
