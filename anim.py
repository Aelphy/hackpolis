import Tkinter as tk
import time
from PIL import ImageTk, Image
import collections

path = '/Users/vasart/Downloads/easter-egg.jpg'

root = tk.Tk()

def initCanvas():
	global canvas_width
	global img, width, height
	global canvas
	global q
	img = ImageTk.PhotoImage(Image.open(path))
	width = img.width()
	height = img.height()
	canvas_width = width * 5
	canvas = tk.Canvas(width=canvas_width, height=height)
	canvas.pack(expand=1, fill=tk.BOTH)
	q = collections.deque()

	addButton = tk.Button(root, text ="Add", command=addBuyer)
	addButton.pack()
	delButton = tk.Button(root, text ="Del", command=delBuyer)
	delButton.pack()

def moveItem(item, s, f):
	for i in range((f - s) / 5):
		canvas.move(item, 5, 0)
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

initCanvas()
root.mainloop()