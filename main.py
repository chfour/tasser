#!/usr/bin/python3
import argparse, logging, time

def parse_line(line: str):
    sp = line.split(" ")
    return sp[0], " ".join(sp[1:])

def handle_line(line: str):
    logging.debug(f"Line: {line!r}")
    # comment / empty line
    if line.startswith("//") or not line: return
    
    cmd, args = parse_line(line)
    cmd = cmd.lower()

    if cmd in ["title", "#"]: # title
        logging.info("Title: " + args)
    elif cmd in ["-", "sleep"]: # waiting
        try: to_sleep = float(args)
        except ValueError:
            logging.fatal(f"sleep: invalid duration {args!r}")
            return True
        logging.debug(f"wait {to_sleep}s")
        time.sleep(to_sleep)
    elif cmd in [">", "print"]: # keyboard text input
        logging.debug(f"write {args!r}")
    elif cmd in [".", "key", "combo"]: # pressing key combinations
        keys = args.split("+")
        logging.debug(f"key combo {keys!r}")
    elif cmd in ["kdown", "kdn", "hold"]: # holding down a key
        logging.debug(f"keydown {args!r}")
    elif cmd in ["kup", "release"]: # releasing a key
        logging.debug(f"keyup {args!r}")
    

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
            if handle_line(line): break
        else:
            logging.info("End of file")
