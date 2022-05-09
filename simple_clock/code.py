# simple_clock_code.py -- Simple clock in using WorldTimeAPI in CircuitPython
# 6 May 2022 - @todbot / Tod Kurt
#
# Part of the CircuitPython Clock project: https://github.com/todbot/circuitpython_clock
#
# This example works on any native WiFI CircuitPython board with a built-in display.
# It can be easily modified for external display
# See http://worldtimeapi.org/pages/examples for info about the API. It's really easy!

import time
import board
import wifi, socketpool, ssl
import adafruit_requests

import displayio, terminalio
from adafruit_display_text import bitmap_label as label

from secrets import secrets

time_api_url = "http://worldtimeapi.org/api/ip"
myfont = terminalio.FONT

# set up display and on-screen text labels
display = board.DISPLAY
main_group = displayio.Group()
display.show(main_group)

date_label = label.Label(font=myfont, text="YYYY-MM-DD", scale=4, y=display.height//3)
time_label = label.Label(font=myfont, text="HH:MM:SS", scale=4, y=2*(display.height//3))
status_label = label.Label(font=myfont, text="connecting...", y=display.height-14) 
main_group.append(date_label)
main_group.append(time_label)
main_group.append(status_label)

print("Connecting to", secrets['ssid'])
wifi.radio.connect(ssid=secrets['ssid'],password=secrets['password'])
print("Connected!")

pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool, ssl.create_default_context())

last_check_time = 0 # when our last time check happened
update_rate = 10  # every N seconds, update clock

while True:
    status_label.text = f"connected. uptime:{int(time.monotonic())}"
    if time.monotonic() - last_check_time > update_rate:
        last_check_time = time.monotonic()
        print("fetching at", last_check_time)
        response = requests.get(time_api_url)
        time_data = response.json()
        print("time_data:",time_data) # debug
        datet = time_data['datetime']
        current_date = datet[0:10]
        current_time = datet[11:19]
        date_label.text = current_date
        time_label.text = current_time
        print("date:",current_date, "time:", current_time)
    time.sleep(1)
