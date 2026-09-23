#  _   _                 _ 
# | \ | |               (_)
# |  \| | __ ___   __ _  _ 
# | . ` |/ _` \ \ / /(_)| |
# | |\  | (_| |\ V /  _ | |
# |_| \_|\__,_| \_/  (_)|_|
# 
# Navi Multitool - Developed by glockinhand
# GitHub: https://github.com/glockinhand/navi-multitool

from pystyle import Colors

THEMES = {
    "blue": {
        "banner": Colors.white_to_blue,
        "head": Colors.blue_to_cyan,
        "num": Colors.cyan_to_blue,
        "txt": Colors.white_to_blue,
        "sub": Colors.blue_to_cyan,
        "inp": Colors.blue_to_cyan
    },
    "red": {
        "banner": Colors.red_to_white,
        "head": Colors.white_to_red,
        "num": Colors.white_to_red,
        "txt": Colors.white,
        "sub": Colors.red_to_white,
        "inp": Colors.white_to_red
    },
    "purple": {
        "banner": Colors.blue_to_purple,
        "head": Colors.purple_to_blue,
        "num": Colors.purple_to_blue,
        "txt": Colors.white,
        "sub": Colors.purple_to_blue,
        "inp": Colors.purple_to_blue
    },
    "green": {
        "banner": Colors.green_to_white,
        "head": Colors.white_to_green,
        "num": Colors.white_to_green,
        "txt": Colors.white,
        "sub": Colors.green_to_white,
        "inp": Colors.white_to_green
    },
    "yellow": {
        "banner": Colors.yellow_to_red,
        "head": Colors.red_to_yellow,
        "num": Colors.yellow_to_red,
        "txt": Colors.white,
        "sub": Colors.red_to_yellow,
        "inp": Colors.red_to_yellow
    },
    "pink": {
        "banner": Colors.purple_to_red,
        "head": Colors.red_to_purple,
        "num": Colors.purple_to_blue,
        "txt": Colors.white,
        "sub": Colors.pink,
        "inp": Colors.pink
    },
    "cyan": {
        "banner": Colors.cyan_to_blue,
        "head": Colors.blue_to_cyan,
        "num": Colors.cyan,
        "txt": Colors.white,
        "sub": Colors.cyan,
        "inp": Colors.cyan
    },
    "gray": {
        "banner": Colors.black_to_white,
        "head": Colors.gray,
        "num": Colors.gray,
        "txt": Colors.white,
        "sub": Colors.gray,
        "inp": Colors.gray
    },
    "rainbow": {
        "banner": Colors.rainbow,
        "head": Colors.rainbow,
        "num": Colors.rainbow,
        "txt": Colors.white,
        "sub": Colors.rainbow,
        "inp": Colors.rainbow
    },
    "modern": {
        "banner": Colors.white_to_blue,
        "head": Colors.white,
        "num": Colors.white_to_blue,
        "txt": Colors.white,
        "sub": Colors.white_to_blue,
        "inp": Colors.white_to_blue
    },
    "modern_red": {
        "banner": Colors.white_to_red,
        "head": Colors.white,
        "num": Colors.white_to_red,
        "txt": Colors.white,
        "sub": Colors.white_to_red,
        "inp": Colors.white_to_red
    },
    "modern_purple": {
        "banner": Colors.blue_to_purple,
        "head": Colors.white,
        "num": Colors.blue_to_purple,
        "txt": Colors.white,
        "sub": Colors.blue_to_purple,
        "inp": Colors.blue_to_purple
    }
}
