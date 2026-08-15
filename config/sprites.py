SEAL_ART = r"""
                                                                   ,-,
                                                             _.-=;~ /_
                                                          _-~   '     ;.
                                                      _.-~     '   .-~-~`-._
                                                _.--~~:.             --.____88
                              ____.........--~~~. .' .  .        _..-------~~
                     _..--~~~~               .' .'             ,'
                 _.-~                        .       .     ` ,'
               .'                                    :.    ./
             .:     ,/          `                   ::.   ,'
           .:'     ,(            ;.                ::. ,-'
          .'     ./'.`.     . . /:::._______.... _/:.o/
         /     ./'. . .)  . _.,'               `88;?88|
       ,'  . .,/'._,-~ /_.o8P'                  88P ?8b
    _,'' . .,/',-~    d888P'                    88'  88|
 _.'~  . .,:oP'        ?88b              _..--- 88.--'8b.--..__
:     ...' 88o __,------.88o ...__..._.=~- .    `~~   `~~      ~-._ Seal _.
`.;;;:='    ~~            ~~~                ~-    -       -   -
"""


def shift_art(art: str, spaces: int = 0, vertical: int = 0) -> str:
    """Shift ASCII art horizontally and vertically."""

    horizontal = " " * spaces
    vertical_padding = "\n" * vertical

    lines = art.splitlines()

    shifted_lines = [
        horizontal + line if line.strip() else line
        for line in lines
    ]

    return vertical_padding + "\n".join(shifted_lines)


SEAL_FRAMES = [
    # Center
    shift_art(SEAL_ART, 0, 0),

    # Move slightly right
    shift_art(SEAL_ART, 1, 0),

    # Move right + slightly down
    shift_art(SEAL_ART, 2, 1),

    # Furthest point
    shift_art(SEAL_ART, 3, 0),

    # Move back
    shift_art(SEAL_ART, 2, 0),

    # Move slightly left
    shift_art(SEAL_ART, 1, 1),

    # Back to center
    shift_art(SEAL_ART, 0, 0),

    # Slightly left
    shift_art(SEAL_ART, 1, 0),

    # Slightly right
    shift_art(SEAL_ART, 2, 1),

    # Return
    shift_art(SEAL_ART, 1, 0),
]


MASCOTS = {
    "seal": SEAL_FRAMES,
}