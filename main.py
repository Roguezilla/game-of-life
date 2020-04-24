from os import system
from copy import deepcopy
import platform
import keyboard
import sys

gen = 0

cells = []
try:
	with open(input('Filename: ')) as textFile:
		cells = [line.split() for line in textFile]
except FileNotFoundError:
	print('No such file in directory.')
	sys.exit(0)

def alive(x,y):
	num_of_neighbours = 0
	neighbours = ((1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,-1),(1,-1),(-1,1))
	for xx,yy in neighbours:
		if x+xx >= 0 and x+xx < len(cells) and y+yy > 0 and y+yy < len(cells[0]) - 1:
			if cells[x+xx][y+yy] == '@':
				num_of_neighbours += 1
	return num_of_neighbours

system('cls' if platform.system() == 'Windows' else 'clear')
print('__'*len(cells[0]))
for i in range(len(cells)):
	print(*cells[i], end='')
	print('|')
print('‾‾'*len(cells[0]))
print('Generation: {}'.format(gen))
system('pause')

while True:
	dc_cells = deepcopy(cells)
	for x in range(len(dc_cells)):
		for y in range(len(dc_cells[0])):
			live = alive(x,y)
			if dc_cells[x][y] == '@' and live < 2:
				dc_cells[x][y] = '.'
			elif dc_cells[x][y] == '@' and (live == 2 or live == 3):
				dc_cells[x][y] = '@'
			elif dc_cells[x][y] == '@' and live > 3:
				dc_cells[x][y] = '.'

			if dc_cells[x][y] == '.' and live == 3:
				dc_cells[x][y] = '@'

	cells = dc_cells

	system('cls' if platform.system() == 'Windows' else 'clear')
	print('__'*len(cells[0]))
	for i in range(len(cells)):
		print(*cells[i], end='')
		print('|')
	print('‾‾'*len(cells[0]))
	
	gen += 1
	print('Generation: {}'.format(gen))
	if keyboard.is_pressed('space'):
		system('pause')	