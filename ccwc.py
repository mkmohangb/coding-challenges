import sys
import click


@click.command()
@click.option('-c','bytes',is_flag=True, default=False, help="number of bytes")
@click.option('-l','lines',is_flag=True, default=False, help="number of lines")
@click.option('-w','words',is_flag=True, default=False, help="number of words")
@click.argument('filename', required=False)
def ccwc(bytes, lines, words, filename):
    print(bytes, lines, words, filename)
    if filename is None:
        filename = sys.stdin.fileno()
    with open(filename, mode='br') as f:
        bdata = f.read()
    if bytes or lines or words:
        if bytes:
            print(len(bdata))
        if lines or words:
            text = bdata.decode('utf-8')
            if words:
                print(len(text.split()))
            else:
                print(text.count('\n'))
    else:
        text = bdata.decode('utf-8')
        print(text.count('\n'), len(text.split()), len(bdata))


if __name__ == '__main__':
    ccwc()
