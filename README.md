# tasser

a program to replay preprogrammed keystrokes from a file

## usage

```
python3 main.py [-h] [-t WAIT_TIME] [-w DEFAULTDELAY] [-d] [--sh] SCRIPTFILE
```
* `-h` - display help
* `-t WAIT_TIME` - time to wait before starting, default = 5
* `-w DEFAULTDELAY` - time between each action, default = 0.1
* `-d` - "fake mode", don't actually take control of the keyboard
* `--sh` - enable calling shell commands from scripts
* `SCRIPTFILE` - script to run

## scriptfile syntax

a scriptfile is a text file with commands (actions) to run

### commands

* `> str` / `print str` - type out text where `str` is a JSON string
* `# text` / `title text` - display text in the console
* `- time` / `sleep time` - wait `time` seconds
* `<` / `wait` - display popup and wait until `Ok` is pressed
* `. keys` / `key keys` - press `keys`, for example `return` or `ctrl+alt+t`
* `kdn key` / `hold key` - hold `key` until released
* `kup key` / `release key` - release `key`
* `* N command` - run `command` `N` times
* `( name` / `fn name` / `function name` - begin function `name`
* `)` / `endfn` / `endfunction` - end function
* `/ name` / `call name` / `jump name` - call function `name`
* `$ command` / `sh command` - run `command` in shell and wait until command finishes, requires `--sh`
* `% command` / `ash command` - run `command`, but don't wait until command finishes, requires `--sh`

### other

* `//` at the beginning of a line indicates a single-line comment
* `/*` at the beginning of a line starts a multi-line comment
* `*/` at the end of a line ends a multi-line comment

### examples

```
// this is a comment, it won't be treated as a command

// here we define a function, which we will call later
( type_aaaa
    > "aaaa\n"
)

# this will be printed to the terminal

// start a terminal
. ctrl+alt+t

// wait for it to open
- 1

// type "nano" and press enter
> "nano\n"

- 0.1

// here we call the function we defined earlier
/ type_aaaa

- 2

// we can also call a function (or command) multiple times:
* 5 / type_aaaa

- 1

// now we will exit nano
. ctrl+x
. n

// and the terminal
> "exit\n"

/*
// this code won't run
> "abcd\n"
> "efgh\n"
*/

// but this will, and will display a messagebox
<
```

you can also take a look at `test.txt`
