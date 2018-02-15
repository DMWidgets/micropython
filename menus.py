import machine, oled_ssd1306, menu_framework, network

# MENUS (menu requires nested list of options and call_function bool in matching index
# -----------------------------------------------------------------------------


main_menu = [
    ['system', 'mqtt', 'LED', 'stats', 'unused', 'unused2', 'credits'],
    [0, 0, 0, 0, 0, 0, 1]
             ]

system = [
    ['reboot', 'IP cfg', 'wifi scan'],
    [1, 1, 1]
            ]

# MENU FUNCTIONS (must match menu option string stripped of spaces + '_func' e.g. IP CFG > ipcfg_func
# ------------------------------------------------------------------------------


def reboot_func():
    # resets board
    machine.reset()


def ipcfg_func():
    # prints current station connection details
    oled_ssd1306.wipe()
    board_station = network.WLAN(network.STA_IF)
    conn = board_station.isconnected()
    ipcfg = board_station.ifconfig()
    if conn:
        oled_ssd1306.pt('wifi connected', noshow=1, centered=1)
    else:
        oled_ssd1306.pt('wifi unconnected', noshow=1, centered=1)
    for item in ipcfg:
        oled_ssd1306.pt(item, noshow=1, centered=1)
        oled_ssd1306.scr.show()
    while 1:
        if not menu_framework.b1.value():
            sleep_ms(200)
            menu_framework.show_menu(main_menu)
            return


def wifiscan_func():
    # scans available networks, prints first 7. returns all results in csv format in txt file
    import ubinascii
    res_file = open('results.txt', 'w')
    path = '/results.txt'
    board_station = network.WLAN(network.STA_IF)
    oled_ssd1306.wipe()
    results = board_station.scan()
    for ap in range(0, 7):
        oled_ssd1306.pt(results[ap][0], noshow=1)
    oled_ssd1306.scr.show()
    res_file.write('SSID,BSSID,CHANNEL,RSSI,AUTHMODE,Hidden?\n')
    for result in results:
        res_file.write(
            str(result[0].decode()) + ',' + str(ubinascii.hexlify(result[1]).decode()) + ',' + str(
                result[2]) + ',' + str(result[3]) + ',' + str(result[4]) + ',' + str(
                result[5]) + '\n')
    res_file.close()
    while 1:
        if not menu_framework.b1.value():
            sleep_ms(200)
            menu_framework.show_menu(main_menu)
            return


def credits_func():
    # does what it says on the tin
    credits = ['through many', 'frustratin hours', 'this code', 'brought to you', 'by kyle hurst']
    oled_ssd1306.wipe()
    for line in credits:
        oled_ssd1306.pt(line, noshow=1, centered=1)
    oled_ssd1306.scr.show()
    while 1:
        if not menu_framework.b1.value():
            sleep_ms(200)
            menu_framework.show_menu(main_menu)
            return
