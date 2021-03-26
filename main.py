#!/usr/bin/python3
import argparse, logging, time, json

def parse_line(line: str) -> tuple:
    sp = line.split(" ")
    return sp[0], " ".join(sp[1:])

def handle_line(line: str, lineno: int):
    line = line.strip() # lstrip for indents, rstrip for newline
    logging.debug(f"ln {lineno}: {line!r}")
    # comment / empty line
    if line.startswith("//") or not line: return
    
    cmd, args = parse_line(line)
    cmd = cmd.lower()

    if cmd in ["title", "#"]: # title
        logging.info("\x1B[1mTitle: " + args + "\x1B[0m")
    elif cmd in ["-", "sleep"]: # waiting
        try: to_sleep = float(args)
        except ValueError:
            logging.fatal(f"sleep: invalid duration {args!r}")
            return True
        logging.debug(f"wait {to_sleep}s")

        time.sleep(to_sleep)
    elif cmd in [">", "print"]: # keyboard text input
        try: args = json.loads(args)
        except json.JSONDecodeError:
            logging.fatal("print: json error")
            return True
        if type(args) != str:
            logging.fatal("print: argument is not a json string")
            return True
        logging.debug(f"write {args!r}")
    elif cmd in [".", "key", "combo"]: # pressing key combinations
        keys = args.split("+")
        logging.debug(f"key combo {keys!r}")
    elif cmd in ["kdown", "kdn", "hold"]: # holding down a key
        logging.debug(f"keydown {args!r}")
    elif cmd in ["kup", "release"]: # releasing a key
        logging.debug(f"keyup {args!r}")
    elif cmd in ["*", "times"]: # calling the same command multiple times
        try: to_repeat = args[args.index(" ")+1:]
        except ValueError:
            logging.fatal(f"times: invalid syntax on line {lineno}")
            return True
        repeats = args[:args.index(" ")]
        try: repeats = int(repeats)
        except ValueError:
            logging.fatal(f"times: invalid count {repeats!r}")
            return True
        logging.debug(f"{repeats} times do {to_repeat!r}")
        
        for _ in range(repeats):
            if handle_line(to_repeat, lineno): return True

if __name__ == "__main__":
    logging.basicConfig(format="[%(asctime)s] %(levelname)s: %(message)s", level=logging.DEBUG)

    parser = argparse.ArgumentParser()
    parser.add_argument("script", type=str,
                        help="input script file")
    args = parser.parse_args()

    logging.info(f"Opening file '{args.script}'")
    with open(args.script, "rt") as f:
        for lineno, line in enumerate(f):
            if handle_line(line, lineno + 1): break
        else:
            logging.info("End of file")
