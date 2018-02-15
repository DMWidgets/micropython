import network, machine, ssd1306, test, oled_ssd1306, time, menu_framework
import uasyncio as asyncio
loop = asyncio.get_event_loop()
board_station = network.WLAN(network.STA_IF)
board_AP = network.WLAN(network.AP_IF)


def reboot():
    machine.reset()


async def ipcfg():
    # allows easy setting of AP connection via terminal
    ssid = board_AP.config('essid')
    print('current connection AP setting: ' + ssid)
    ssid = input('enter ssid of wifi connection')
    pw = input('enter password of connection')
    board_station.connect(ssid, pw)
    print('connecting...')
    await asyncio.sleep(10)
    if board_station.isconnected():
        print('connected!...rebooting')
        board_AP.active(False)
        time.sleep(2)
        reboot()
    else:
        print('connection failed')
        ipcfg()


async def wifi_status():
    # ensures wifi connection, otherwise turns on AP so user can connect via term and set connection
    x = 0
    while not board_station.isconnected():
        oled_ssd1306.scr.text('.', x, oled_ssd1306.active_line)
        oled_ssd1306.scr.show()
        x += 8
        await asyncio.sleep_ms(500)
        if x > 88:
            oled_ssd1306.wipe()
            oled_ssd1306.pt('no con. X\'ing AP')
            time.sleep(2)
            oled_ssd1306.wipe()
            oled_ssd1306.pt('ssid: <ssid>')
            oled_ssd1306.pt('pw: <password>')
            oled_ssd1306.pt('connect to')
            oled_ssd1306.pt('web REPL')
            board_AP.active(True)
            await asyncio.sleep(10)
            loop.create_task(ipcfg())
        if board_station.isconnected():
            oled_ssd1306.wipe()
            oled_ssd1306.pt('wifi connected')
            time.sleep(1)
            board_AP.active(False)
            break


oled_ssd1306.pt('connecting wifi')
loop.create_task(wifi_status())
loop.run_forever()
while 1:
    # loads the main menu once the board has connected to the wifi
    if board_station.isconnected():
        oled_ssd1306.wipe()
        menu_framework.show_menu(menu_framework.main_menu)