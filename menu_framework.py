import machine, oled_ssd1306
from utime import sleep_ms
from menus import *

line_y = {1: 3, 2: 12, 3: 21, 4: 30, 5: 39, 6: 48, 7: 57}
cursor_pos = 1
b1 = machine.Pin(4, machine.Pin.IN, machine.Pin.PULL_UP)
b2 = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP)

options = ('1', '2', '3', '4', '5', '6', '7')


def draw_marker(x, o=1):
    # draws cursor along left side of screen for current selection
    oled_ssd1306.scr.pixel(3, x, o)
    oled_ssd1306.scr.pixel(4, x, o)
    oled_ssd1306.scr.pixel(5, x, o)
    oled_ssd1306.scr.pixel(3, x + 1, o)
    oled_ssd1306.scr.pixel(4, x + 1, o)
    oled_ssd1306.scr.pixel(5, x + 1, o)


def show_menu(menu):
    # prints to screen <menu> list, justified left 9 pixels to fit cursor
    global cursor_pos
    cursor_pos = 1
    oled_ssd1306.active_line = 0
    oled_ssd1306.wipe()
    for s in menu[0]:
        oled_ssd1306.pt(s, x=9, noshow=1)
    draw_marker(line_y[cursor_pos])
    oled_ssd1306.scr.show()
    nav(menu)


def select(x):
    # either loads new menu based on selection or runs function related to selection if any
    selection = x[0][cursor_pos - 1]
    if x[1][cursor_pos -1]:
        globals()[selection.replace(' ', '').lower() + '_func']()
    else:
        show_menu(globals()[selection])


def nav(x):
    while 1:
        if not b1.value():
            sleep_ms(200)
            select(x)
            continue
        if not b2.value():
            sleep_ms(200)
            cursor_move(x)
            continue


def cursor_move(x):
    # moves cursor down menu entries. round robins when reaching end
    global cursor_pos
    if cursor_pos + 1 > len(x[0]):
        draw_marker(line_y[cursor_pos], 0)
        cursor_pos = 1
        draw_marker(line_y[cursor_pos])
        oled_ssd1306.scr.show()
    else:
        draw_marker(line_y[cursor_pos], 0)
        cursor_pos += 1
        draw_marker(line_y[cursor_pos])
        oled_ssd1306.scr.show()
    sleep_ms(150)