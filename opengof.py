import sys
import pyglet
import ctypes
from pyglet.gl import *
from OpenGL.GLUT import *
from copy import deepcopy

cells = []
try:
	with open(input('Filename: ')) as txt:
		cells = [line.split() for line in txt]
		for x in range(len(cells)):
			for y in range(len(cells[0])):
				if cells[x][y] == '.':
					cells[x][y] = ' '
				elif cells[x][y] == 'o':
					cells[x][y] = '■'
except FileNotFoundError:
	print('No such file in directory.')
	sys.exit(0)

def alive(x,y):
	num_of_neighbours = 0
	neighbours = ((1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,-1),(1,-1),(-1,1))
	for xx,yy in neighbours:
		try:
			if cells[x+xx][y+yy] == '■' and x+xx in range(len(cells)) and y+yy in range(len(cells[0])):
				num_of_neighbours += 1
		except IndexError: None
	return num_of_neighbours

def string(x, y, text, color=(1.0, 1.0, 1.0)):
	glutInit()
	glColor3f(color[0], color[1], color[2])
	glRasterPos2f(x,y)
	for ch in text:
		glutBitmapCharacter(GLUT_BITMAP_9_BY_15, ctypes.c_int(ord(ch)))

def outline_rect(x, y, mult, add, color=(0.0, 0.0, 0.0)):
	glPushAttrib(GL_CURRENT_BIT)
	glBegin(GL_LINE_LOOP)
	glColor3f(color[0], color[1], color[2])
	glVertex2f(x*mult, y*mult)
	glVertex2f(x*mult, y*mult+10)
	glVertex2f(x*mult+add, y*mult+add)
	glVertex2f(x*mult+add, y*mult)
	glEnd()
	glPopAttrib()

def rect(x, y, mult, add, color=(1.0, 1.0, 1.0)):
	glPushAttrib(GL_CURRENT_BIT)
	glBegin(GL_QUADS)
	glColor3f(color[0], color[1], color[2])
	glVertex2f(x*mult, y*mult)
	glVertex2f(x*mult, y*mult+10)
	glVertex2f(x*mult+add, y*mult+add)
	glVertex2f(x*mult+add, y*mult)
	glEnd()
	glPopAttrib()

gen = 0
def update(dt):
	global cells, gen
	dc_cells = deepcopy(cells)
	for x in range(len(dc_cells)):
		for y in range(len(dc_cells[0])):
			live = alive(x,y)
			if dc_cells[x][y] == '■' and live < 2:
				dc_cells[x][y] = ' '
			elif dc_cells[x][y] == '■' and (live == 2 or live == 3):
				dc_cells[x][y] = '■'
			elif dc_cells[x][y] == '■' and live > 3:
				dc_cells[x][y] = ' '

			if dc_cells[x][y] == ' ' and live == 3:
				dc_cells[x][y] = '■'
	cells = dc_cells
	gen += 1

window = pyglet.window.Window(width=len(cells[0])*10, height=len(cells)*10+10, caption='Game Of Life')
@window.event
def on_draw():
	global cells, gen
	pyglet.clock.schedule_once(update, .00001)
	glClear(GL_COLOR_BUFFER_BIT)
	glLoadIdentity()
	string(0, 0, 'Generation: {}'.format(gen))
	glTranslatef(0, window.height, 0)
	glRotatef(-90.0, 0.0, 0.0, 1.0)
	for x in range(len(cells)):
		for y in range(len(cells[0])):
			if cells[x][y] == ' ':
				outline_rect(x, y, 10, 10, color=(0.0, 0.0, 0.0))
				rect(x, y, 10, 10, color=(1.0, 1.0, 1.0))
			elif cells[x][y] == '■':
				outline_rect(x, y, 10, 10, color=(0.0, 0.0, 0.0))
				rect(x, y, 10, 10, color=(0.0, 1.0, 0.0))
	
pyglet.app.run()