import Tkinter as tk
import serial
from xbee import ZigBee
import urllib, urllib2
import json

def refresh(msg):
    global w
    #msg = xbee.wait_read_frame()
    q = msg['rf_data']
    w.configure(text=q)
    
    data = urllib.urlencode({ 'number': q })
    req = urllib2.Request('http://104.131.161.219/post')
    try:
        urllib2.urlopen(req, data)
    except IOError, e:
        print e.reason
    
    #root.after(100, refresh)

ser = serial.Serial('/dev/ttyACM0', 9600)
xbee = ZigBee(ser, callback=refresh)

root = tk.Tk()
root.attributes("-fullscreen", True)
w = tk.Label(root, text="0", font=("Helvetica", 32))
w.pack()
w.place(relx=.5, rely=.5, anchor=tk.CENTER)

#refresh()
root.mainloop()
