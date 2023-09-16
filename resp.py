
# Redis Serialization Protocol - RESP
# https://redis.io/docs/reference/protocol-spec/
# - Simple to implement, fast to parse, human readable
# TCP - 6379, or Unix sockets

CRLF = 2


def parse_value(cmd):
    parts = []
    i = 0
    while cmd[i] != '\r':
        parts += cmd[i]
        i += 1
    return ("".join(parts), i+CRLF)


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
        offset += length + CRLF
        print(value)
        print(offset)
    elif cmd_type == '+' or cmd_type == ':' or cmd_type == '-':
        values.append(value)
        print(value)

    return (values, offset)


if __name__ == "__main__":
    parse_command("+OK\r\n")
    parse_command("-ERR unknown command 'asdf'\r\n")
    parse_command(":1000\r\n")
    parse_command("*2\r\n$4\r\necho\r\n$5\r\nhello\r\n")
    parse_command("*3\r\n:1\r\n:2\r\n:3\r\n")
    parse_command("$5\r\nworld\r\n")
