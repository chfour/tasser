#!/usr/bin/python3
import argparse, logging, time, json
import pyautogui

logging.basicConfig(format="[%(asctime)s] %(levelname)s: %(message)s", level=logging.DEBUG)

def parse_line(line: str) -> tuple:
    sp = line.split(" ")
    return sp[0], " ".join(sp[1:])

def handle_line(line: str, lineno: int, functions: dict, run=True):
    # comment / empty line
    if line.startswith("//") or not line: return
    
    cmd, args = parse_line(line)
    cmd = cmd.lower()

    if cmd in ["title", "#"]: # title
        logging.info("\x1B[1m" + args + "\x1B[0m")
    elif cmd in ["-", "sleep"]: # waiting
        try: to_sleep = float(args)
        except ValueError:
            logging.fatal(f"ln {lineno}: sleep: invalid duration {args!r}")
            return True
        logging.debug(f"wait {to_sleep}s")

        time.sleep(to_sleep)
    
    elif cmd in [">", "print"]: # keyboard text input
        try: args = json.loads(args)
        except json.JSONDecodeError:
            logging.fatal(f"ln {lineno}: print: json error")
            return True
        if type(args) != str:
            logging.fatal(f"ln {lineno}: print: argument is not a json string")
            return True
        logging.debug(f"write {args!r}")

        if run: pyautogui.typewrite(args, interval=0.01)
    
    elif cmd in [".", "key", "combo"]: # pressing key combinations
        keys = args.split("+")
        logging.debug(f"key combo {keys!r}")

        if run: pyautogui.hotkey(*keys)
    
    elif cmd in ["kdown", "kdn", "hold"]: # holding down a key
        logging.debug(f"keydown {args!r}")

        if run: pyautogui.keyDown(args)
    
    elif cmd in ["kup", "release"]: # releasing a key
        logging.debug(f"keyup {args!r}")

        if run: pyautogui.keyUp(args)
    
    elif cmd in ["*", "times"]: # calling the same command multiple times
        try: to_repeat = args[args.index(" ")+1:]
        except ValueError:
            logging.fatal(f"ln {lineno}: times: invalid syntax")
            return True
        repeats = args[:args.index(" ")]
        try: repeats = int(repeats)
        except ValueError:
            logging.fatal(f"ln {lineno}: times: invalid count {repeats!r}")
            return True
        logging.debug(f"{repeats} times do {to_repeat!r}")
        
        for _ in range(repeats):
            if handle_line(to_repeat, lineno, functions, run): return True
    
    elif cmd in ["/", "call", "jump"]:
        func = functions.get(args, None)
        if not func:
            logging.fatal(f"ln {lineno}: call: no such function {args!r}")
            return
        logging.debug(f"call function {args!r}, {len(func)} lines")

        for lineno, line in func:
            logging.debug(f"fncall {args!r}: ln {lineno}: {line!r}")
            if handle_line(line, lineno, functions, run): return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("script", type=str,
                        help="input script file")
    parser.add_argument("-t", "--wait-time", type=float, default=5,
                        help="time to wait before starting in seconds, default=5")
    parser.add_argument("-w", "--defaultdelay", type=float, default=0.1,
                        help="time to wait between each input action, default=0.1")
    parser.add_argument("-d", "--dry-run", action="store_true",
                        help="'fake mode' - don't make calls to pyautogui")
    args = parser.parse_args()
    pyautogui.PAUSE = args.defaultdelay

    logging.info(f"Waiting {args.wait_time} seconds...")
    logging.info(f"Opening file '{args.script}'")
    with open(args.script, "rt") as f:
        in_function = False
        functions = {}
        for lineno, line in enumerate(f, 1):
            line = line.strip()
            logging.debug(f"ln {lineno}: {line!r}")
            if in_function:
                if line.startswith(("endfn", "endfunction", ")")):
                    in_function = False
                    logging.debug(f"end new function {this_func!r}")
                else:
                    functions[this_func].append((lineno, line))
            else:
                if line.startswith(("fn ", "function ", "( ")):
                    in_function = True
                    _, args = parse_line(line)
                    args = args.strip()
                    if not args:
                        logging.fatal(f"ln {lineno}: function: invalid syntax")
                        break
                    this_func = args
                    logging.debug(f"begin new function {this_func!r}")
                    functions[this_func] = []
                else:
                    if handle_line(line, lineno, functions, not args.dry_run): break
        else:
            logging.info("End of file")
