
TERMINAL_CODES = {
    # Screen and cursor
    'CLEAR_SCREEN': '\x1b[2J',
    'CLEAR_LINE': '\x1b[2K',
    'HIDE_CURSOR': '\x1b[?25l',
    'SHOW_CURSOR': '\x1b[?25h',
    'MOVE_CURSOR_HOME': '\x1b[H',
    'MOVE_TO_START': '\x1b[0G',
    'CURSOR_UP': '\x1b[1A',
    'CURSOR_DOWN': '\x1b[1B',
    'CURSOR_FORWARD': '\x1b[1C',
    'CURSOR_BACKWARD': '\x1b[1D',
    'REMOVE_LAST_CHARACTER': '\x1b[K',

    # Text formatting
    'RESET': '\x1b[0m',
    'BOLD': '\x1b[1m',
    'DIM': '\x1b[2m',
    'UNDERLINE': '\x1b[4m',
    'BLINK': '\x1b[5m',
    'REVERSE': '\x1b[7m',
    'HIDDEN': '\x1b[8m',

    # Foreground
    'FG_BLACK': '\x1b[30m',
    'FG_RED': '\x1b[31m',
    'FG_GREEN': '\x1b[32m',
    'FG_YELLOW': '\x1b[33m',
    'FG_BLUE': '\x1b[34m',
    'FG_MAGENTA': '\x1b[35m',
    'FG_CYAN': '\x1b[36m',
    'FG_WHITE': '\x1b[37m',
    'FG_DEFAULT': '\x1b[39m',

    # Background
    'BG_BLACK': '\x1b[40m',
    'BG_RED': '\x1b[41m',
    'BG_GREEN': '\x1b[42m',
    'BG_YELLOW': '\x1b[43m',
    'BG_BLUE': '\x1b[44m',
    'BG_MAGENTA': '\x1b[45m',
    'BG_CYAN': '\x1b[46m',
    'BG_WHITE': '\x1b[47m',
    'BG_DEFAULT': '\x1b[49m',
    
    'REQUEST_TERMINAL_SIZE': '\x1b[18t',

    'CHANGE_WINDOW_SIZE': '\x1b[8;{rows};{cols}t',

    'FG_RGB': '\x1b[38;2;{r};{g};{b}m',
    'BG_RGB': '\x1b[48;2;{r};{g};{b}m',

    'FG_256': '\x1b[38;5;{n}m',
    'BG_256': '\x1b[48;5;{n}m',

}

SPECIAL_KEYS = {
    'ENTER': '\n',
    'BACKSPACE_KEY': '\x7f',  
    'BACKSPACE_CHAR': '\b', 
    'TAB': '\t',
    'SPACE': ' ',

    # Arrows
    'ARROW_LEFT': '\x1b[D',
    'ARROW_RIGHT': '\x1b[C',
    'ARROW_UP': '\x1b[A',
    'ARROW_DOWN': '\x1b[B',
    
    'F1': '\x1bOP',
    'F2': '\x1bOQ',
    'F3': '\x1bOR',
    'F4': '\x1bOS',
    'F5': '\x1b[15~',
    'F6': '\x1b[17~',
    'F7': '\x1b[18~',
    'F8': '\x1b[19~',
    'F9': '\x1b[20~',
    'F10': '\x1b[21~',
    'F11': '\x1b[23~',
    'F12': '\x1b[24~',

    # Others
    'ESC': '\x1b',
    'DELETE': '\x1b[3~',
    'HOME': '\x1b[H',
    'END': '\x1b[F',
    'PAGE_UP': '\x1b[5~',
    'PAGE_DOWN': '\x1b[6~',
    'INSERT': '\x1b[2~',
    
    
    # Example: \x1b[<0;X;Ym  => mouse down
    #           \x1b[<0;X;Yu  => mouse up
    #           \x1b[<64;X;Yt => scroll up
    'MOUSE_CLICK_SGR': '\x1b[<',  # prefix
}
