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
	global n
	n = 0
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
	for i in range(s, f):
		canvas.move(item, 1, 0)
		canvas.update()

def addBuyer():
	global n
	global q
	n = n + 1
	item = canvas.create_image(0, height / 2, image=img)

	k = (canvas_width - width * n) / 2
	moveItem(item, 0, k)
	q.append(item)
	moveQueue()

def delBuyer():
	global n
	global q
	if n == 0:
		return
	moveQueue()
	item = q.popleft()
	x = (canvas_width + n * width) / 2
	moveItem(item, x, canvas_width + width)
	n = n - 1

def moveQueue():
	global n
	global q
	for i in range(n):
		direction = 1
		if i < n / 2:
			direction = -1
		x = (canvas_width + direction * i * width) / 2
		moveItem(q[i], x, x + width / 2)

initCanvas()
root.mainloop()