#!/usr/bin/python3

def parse_line(line: str):
    sp = line.split(" ")
    return sp[0], " ".join(sp[1:])

if __name__ == "__main__":
    print(parse_line("kb shift+F10 asd"))