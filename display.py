import Tkinter as tk
import serial
from xbee import ZigBee
import urllib, urllib2
import json

w

data = ''

def refresh(partial_data):
    data = data + partial_data['rf_data']

    data = data.split('\n')

    buffer = ''

    if not partial_data['rf_data'].endswith('\n'):
        buffer = data[len(data) - 1]
        data = data[0:(len(data) - 1)]

    for msg in data:
        w.configure(text=msg)

        info = urllib.urlencode({ 'number': msg })
        req = urllib2.Request('http://104.131.161.219/post')

        try:
            urllib2.urlopen(req, info)
        except IOError, e:
            print e.reason

    data = buffer

ser = serial.Serial('/dev/ttyACM0', 9600)
xbee = ZigBee(ser, callback=refresh)

root = tk.Tk()
root.attributes("-fullscreen", True)
w = tk.Label(root, text="0", font=("Helvetica", 32))
w.pack()
w.place(relx=.5, rely=.5, anchor=tk.CENTER)

root.mainloop()
