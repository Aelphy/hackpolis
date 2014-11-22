import Tkinter as tk
import serial
from xbee import ZigBee
import urllib, urllib2
import json
from PIL import ImageTk, Image
import collections

global w
data = ''
path = 'icon.png'
cash = 'cash.png'
count = 0
average = 0

def refresh(partial_data):
    global data

    data = data + partial_data['rf_data']
    data = data.split('\n')

    buffer = ''

    if not partial_data['rf_data'].endswith('\n'):
        buffer = data[len(data) - 1]
        data = data[0:(len(data) - 1)]

    for msg in data:
      print msg
      if len(msg) > 0:
        w.configure(text=msg)

        info = urllib.urlencode({ 'number': msg })
        req = urllib2.Request('http://104.131.161.219/post')

        try:
          urllib2.urlopen(req, info)
          ncount = json.loads(msg)['Length']
          if ncount > count:
            for i in range(count, ncount):
              addBuyer()
          elif ncount < count:
            for i in range(ncount, count):
              delBuyer()
          count = ncount
        except IOError, e:
          print e.reason

    data = buffer

def initCanvas():
    global img, width, height
    global canvas, canvas_width
    global q
    img = ImageTk.PhotoImage(Image.open(path))
    width = img.width()
    height = img.height()
    canvas_width = width * 10
    canvas = tk.Canvas(root, width=canvas_width, height=height)
    canvas.pack()
    canvas.place(relx=.5, rely=.5, anchor=tk.CENTER)
    reg = ImageTk.PhotoImage(Image.open(cash))
    label = tk.Label(root, image=reg)
    label.image = reg
    label.place(y = 600, x = canvas_width)
    q = collections.deque()
    addButton = tk.Button(root, text ="Add", command=addBuyer)
    addButton.pack(side=tk.TOP)
    delButton = tk.Button(root, text ="Del", command=delBuyer)
    delButton.pack(side=tk.TOP)

def moveItem(item, s, f):
    for i in range((f - s) / 10):
        canvas.move(item, 10, 0)
        canvas.update()

def addBuyer():
    global q
    item = canvas.create_image(0, height / 2, image=img)
    q.append(item)
    k = (canvas_width - len(q) * width - width / 2)
    moveItem(item, 0, k)

def delBuyer():
    global q
    if len(q) == 0:
        return
    moveQueue()
    item = q.popleft()
    x = (canvas_width + len(q) * width) / 2
    moveItem(item, x, canvas_width + width)

def moveQueue():
    global q
    for i in range(len(q)):
        x = (canvas_width - i * width) / 2
        moveItem(q[i], x, x + width)

ser = serial.Serial('/dev/ttyACM0', 9600)
xbee = ZigBee(ser, callback=refresh)

root = tk.Tk()
root.attributes("-fullscreen", True)
w = tk.Label(root, text="0", font=("Helvetica", 32))
w.pack()
w.place(relx=.5, rely=.5, anchor=tk.CENTER)
initCanvas()
root.mainloop()
