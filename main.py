#!/usr/bin/python3
import argparse, logging

def parse_line(line: str):
    sp = line.split(" ")
    return sp[0], " ".join(sp[1:])

def handle_line(line: str):
    logging.debug("Line: " + line)

if __name__ == "__main__":
    logging.basicConfig(format="[%(asctime)s] %(levelname)s: %(message)s", level=logging.DEBUG)

    parser = argparse.ArgumentParser()
    parser.add_argument("script", type=str,
                        help="input script file")
    args = parser.parse_args()

    logging.info(f"Opening file '{args.script}'")
    with open(args.script, "rt") as f:
        for line in f:
            line = line.rstrip()
            handle_line(line)
    logging.info("End of file")
