import machine, ssd1306
i2c = machine.I2C(-1, machine.Pin(0), machine.Pin(2))
scr = ssd1306.SSD1306_I2C(128, 64, i2c)
active_line = 0

def wipe():
    # wipes screen black
    global active_line
    active_line = 0
    scr.fill(0)
    scr.show()


def pt(s, x=0, noshow=0, centered=0):
    # prints string to display, keeping track of current line. allows for not updating display and centering text
    global active_line
    if centered == 1:
        scr.text(s, int(64 - len(s) * 8 / 2), active_line)
    else:
        scr.text(s, x, active_line)
    if noshow == 0:
        scr.show()
    active_line += 9