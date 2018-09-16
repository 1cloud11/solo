from tkinter import *
import random
import time

class Game:
	def __init__(self):
		self.tk = Tk() # создали переменную и сохранили в ней обьект импортированного класса Tk модуля tkinter. Обьект создает пустое окно, в которое можно добавлять элементы.
		self.tk.title("Человечек спешит к выходу") # заголовок игрового окна
		self.tk.resizable(0, 0) # фиксируем размер окна (блокируем изменения)
		self.tk.wm_attributes("-topmost", 1) # функция модуля Tkinter. Параметр топмост отвечает за размещение окна поверх всех окон
		self.canvas = Canvas(self.tk, width=500, height=500, highlightthickness=0) # Создали холст, привязали его к обьекту tk с пустым окном, указали его размеры, а аргумент highlightthickness=0 удаляет рамку окна.
		self.canvas.pack() # команда pack() включает отображение добавленных элементов на холст
		self.tk.update() # Команда tk.update() подготавливает tkinter к игровой анимации. Без вызова update программа не будет работать так, как задумано.
		self.canvas_height = 500 # Мы создали переменную, которая будет одним из наследуемых свойств класса. В переменной хранится ссылка(референс) на обьект 500, который соответствует одному из параметров размера холста.
		self.canvas_width = 500 # --//--
		self.bg = PhotoImage(file="background.gif") # bg - ещё одно свойство класса Game. Свойство - это обьект из встроенного в tkinter класса PhotoImage, который отвечает за чтение картинок формата .gif и их размещение на холст (canvas). в аргументы передаем наш бекграунд.
		w = self.bg.width() # width и height - это функции класса PhotoImage, которые возвращают размер изображения (background в данном случае)
		h = self.bg.height() # --//--
# Размер холста 500х500. Размер background.gif 100x100. Следующий цикл заполняет холст изображением background.gif сначала по горизонтали, а затем - по вертикали.
		for x in range(0, 5): # создаем переменную x и перебираем ее 5 раз (0, 1, 2, 3, 4)
			for y in range(0, 5): # создаем переменную y и перебираем ее 5 раз (0, 1, 2, 3, 4) для каждого из x
				self.canvas.create_image(x * w, y * h, image=self.bg, anchor='nw') # функция create_image выводит наше изображение в определенной позиции на холсте, отмеряя отступ в каждй итерации цикла ( в цикле х=1 х*w = 100, изображение будет размещено с отступом 100px по оси х)
		self.sprites = [] # Спрайт - это графический обьект в игре, в нашей - человечек и платформы. Тут мы создали список наших спрайтов в игре.
		self.running =  True

	def mainloop(self):
		while 1: # цикл while будет работать до закрытия игрового окна.
			if self.running == True: # Проверяем значение running (строка 24)
				for sprite in self.sprites: # В цикле мы перебираем все спрайты из списка sprites[] (строка 23)
					sprite.move() # Для каждого спрайта списка sprites[] мы вызываем функцию move.
				self.tk.update_idletasks() #М ы перерисовываем отображение обьектов на холсте
				self.tk.update() #М ы перерисовываем отображение обьектов на холсте
				time.sleep(0.01) # Делаем паузу на 1 сотую секунды между итерациями в цикле while 1
class Coords:
	def __init__(self, x1=0, y1=0, x2=0, y2=0):
		self.x1 = x1 # Свойства класса Coords, в которых будут хранится координаты спрайтов.
		self.y1 = y1 #--//--
		self.x2 = x2 #--//--
		self.y2 = y2 #--//--

class Sprite:
	def __init__(self, game):
		self.game = game
		self.endgame = False
		self.coordinates = None
	def move(self):
		pass
	def coords(self):
		return self.coordinates

class PlatformSprite(Sprite):
	def __init__(self, game, photo_image, x, y, width, height):
		Sprite.__init__(self, game)
		self.photo_image = photo_image
		self.image = game.canvas.create_image(x, y, image=self.photo_image, anchor='nw')
		self.coordinates = Coords(x, y, x + width, y + height)

class StickFigureSprite(Sprite):
	def __init__(self, game):
		Sprite.__init__(self, game)
		self.images_left = [
			PhotoImage(file="figure-L1.gif"),
			PhotoImage(file="figure-L2.gif"),
			PhotoImage(file="figure-L3.gif")
		]
		self.images_right = [
			PhotoImage(file="figure-R1.gif"),
			PhotoImage(file="figure-R2.gif"),
			PhotoImage(file="figure-R3.gif")
		]
		self.image = game.canvas.create_image(200, 470, image=self.images_left[0], anchor='nw')
		self.x = -2
		self.y = 0
		self.current_image = 0
		self.current_image_add = 1
		self.jump_count = 0
		self.last_time = time.time()
		self.coordinates = Coords()
		game.canvas.bind_all('<KeyPress-Left>', self.turn_left)
		game.canvas.bind_all('<KeyPress-Right>', self.turn_right)
		game.canvas.bind_all('<Space>', self.jump)
	
	def turn_left(self, evt):
		if self.y == 0:
			self.x = -2
	
	def turn_right(self, evt):
		if self.y == 0:
			self.x = 2

	def jump(self, evt):
		if self.y == 0:
			self.y = -4
			self.jump_count = 0

	def animate(self):
		if self.x != 0 and self.y == 0:
			if time.time() - self.last_time > 0.1:
				self.last_time = time.time()
				self.current_image += self.current_image_add
				if self.current_image >= 2:
					self.current_image_add = -1
				if self.current_image <= 0:
					self.current_image_add = 1
		if self.x < 0:
			if self.y != 0:
				self.game.canvas.itemconfig(self.image, image=self.images_left[2])
			else:
				self.game.canvas.itemconfig(self.image, image=self.images_left[self.current_image])
		elif self.x > 0:
			if self.y != 0:
				self.game.canvas.itemconfig(self.image, image=self.images_right[2])
			else:
				self.game.canvas.itemconfig(self.image, image=self.images_right[self.current_image])

	def coords(self):
		xy = self.game.canvas.coords(self.image)
		self.coordinates.x1 = xy[0]
		self.coordinates.y1 = xy[1]
		self.coordinates.x2 = xy[0] + 27
		self.coordinates.y2 = xy[1] + 30
		return self.coordinates

	def move(self):
		self.animate()
		if self.y < 0:
			self.jump_count += 1
			if self.jump_count > 20:
				self.y = 4
		if self.y > 0:
			self.jump_count -= 1
		co = self.coords()
		left = True
		right = True
		bottom = True
		falling = True
		if self.y > 0 and co.y2 >= self.game.canvas_height:
			self.y = 0
			bottom = False
		elif self.y < 0 and co.y1 <= 0:
			self.y = 0
			top = False
		if self.x > 0 and co.x2 >= self.game.canvas_width:
			self.x = 0
			right = False
		elif self.x < 0 and co.x1 <= 0:
			self.x = 0
			left = False

def within_x(co1, co2):
	if (co1.x1 > co2.x1 and co1.x1 < co2.x2) \
			or (co1.x2 > co2.x1 and co1.x2 < co2.x2) \
			or (co2.x1 > co1.x1 and co2.x1 < co1.x2) \
			or (co2.x2 > co1.x1 and co2.x2 < co1.x2):
		return True
	else:
		return False

def within_y(co1, co2):
	if (co1.y1 > co2.y1 and co1.y1 < co2.y2) \
			or (co1.y2 > co2.y1 and co1.y2 < co2.y2) \
			or (co2.y1 > co1.y1 and co2.y1 < co1.y2) \
			or (co2.y2 > co1.y1 and co2.y2 < co1.y2):
		return True
	else:
		return False

def collided_left(co1, co2):
	if within_y(co1, co2):
		if co1.x1 <= co2.x2 and co1.x1 >= co2.x2:
			return True
	return False

def collided_right(co1, co2):
	if within_y(co1, co2):
		if co1.x2 >= co2.x1 and co1.x2 <= co2.x2:
			return True
	return False

def collided_top(co1, co2):
	if within_x(co1, co2):
		if co1.y1 >= co2.y2 and co1.y1 <= co2.y1:
			return True
	return False

def collided_bottom(co1, co2,):
	if within_x(co1, co2):
		y_calc = co1.y2 + y
		if y_calc >= co2.y1 and y_calc <= co2.y2:
			return True
	return False

g = Game() #мы создали обьект класса Game, и сохранили его в переменной g.

platform1 = PlatformSprite(g, PhotoImage(file="platform1.gif"), 0, 480, 100, 10)
platform2 = PlatformSprite(g, PhotoImage(file="platform1.gif"), 150, 440, 100, 10)
platform3 = PlatformSprite(g, PhotoImage(file="platform1.gif"), 300, 400, 100, 10)
platform4 = PlatformSprite(g, PhotoImage(file="platform1.gif"), 300, 160, 100, 10)
platform5 = PlatformSprite(g, PhotoImage(file="platform2.gif"), 175, 350, 66, 10)
platform6 = PlatformSprite(g, PhotoImage(file="platform2.gif"), 50, 300, 66, 10)
platform7 = PlatformSprite(g, PhotoImage(file="platform2.gif"), 170, 120, 66, 10)
platform8 = PlatformSprite(g, PhotoImage(file="platform2.gif"), 45, 60, 66, 10)
platform9 = PlatformSprite(g, PhotoImage(file="platform3.gif"), 170, 250, 32, 10)
platform10 = PlatformSprite(g, PhotoImage(file="platform3.gif"), 230, 200, 32, 10)
g.sprites.append(platform1)
g.sprites.append(platform2)
g.sprites.append(platform3)
g.sprites.append(platform4)
g.sprites.append(platform5)
g.sprites.append(platform6)
g.sprites.append(platform7)
g.sprites.append(platform8)
g.sprites.append(platform9)
g.sprites.append(platform10)
g.mainloop() #Вызываем функцию mainloop для для созданного обьекта g (строка 193), запуская этим гланый цикл игры.
