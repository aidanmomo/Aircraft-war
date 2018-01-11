#*****************************************
#作者(Author)：Zhou Aolong
#时间(Time)：2018年1月11日
#邮箱(email)：zhouaolong2017@gmail.com
#*****************************************
import pygame,sys
from pygame.locals import *
import time
import random

#Game level，0 is the initial screen
level = 0
#mouse motion
flag_mouse = 0
#a label / whether the plane explode
flag_plane_blast = 0

#base class of plane
class BasePlane(object):
	def __init__(self, screen_temp, x, y, image_name):
		self.x = x#initial location
		self.y = y
		self.screen = screen_temp
		self.image = pygame.image.load(image_name)
		self.bullet_list = []#store bullets

	#display image
	def display(self):
		self.screen.blit(self.image,(self.x,self.y))#display plane

		for bullet in self.bullet_list:
			bullet.display()#display plane
			bullet.move()
			if bullet.judge():#judge whether the bullet is out of the boundary
				self.bullet_list.remove(bullet)

#hero class
class HeroPlane(BasePlane):
	def __init__(self, screen_temp):
		BasePlane.__init__(self, screen_temp, 220, 700, "./Resource/hero1.png")

	def move_left(self):
		if self.x > 0:#left boundary
			self.x -= 5
	def move_right(self):
		if self.x < 410:#right boundary
			self.x += 5

	def fire(self):
		if len(self.bullet_list) < 3:#limit the number of the bullet
			self.bullet_list.append(Bullet(self.screen,self.x, self.y))

	def delay(self):
		num = 1
		for i in range(10000):
			num = num+1

	def blast_image_load(self):
		self.image = pygame.image.load("./Resource/hero_blowup_1.png")
		self.delay()
		self.image = pygame.image.load("./Resource/hero_blowup_2.png")
		self.delay()
		self.image = pygame.image.load("./Resource/hero_blowup_3.png")
		self.delay()
		self.image = pygame.image.load("./Resource/hero_blowup_4.png")

	#judge whether the plane is hited
	def blast(self, enemy):
		global flag_plane_blast, level
		for enemybullet in enemy.bullet_list:
			if enemybullet.y > self.y and enemybullet.y < self.y+82:
				if level == 2:#在第二关被摧毁
					if (enemybullet.x1 > self.x and enemybullet.x1 < self.x+66) or (enemybullet.x2 > self.x and enemybullet.x2 < self.x+66):
						self.blast_image_load()
						flag_plane_blast = 1
				elif level == 1:#在第一关被摧毁
					if (enemybullet.x > self.x and enemybullet.x < self.x+66):
						self.blast_image_load()
						flag_plane_blast = 1
				elif level == 3:#在第三关被摧毁
					if (enemybullet.x1 > self.x and enemybullet.x1 < self.x+66) or (enemybullet.x2 > self.x and enemybullet.x2 < self.x+66) or (enemybullet.x3 > self.x and enemybullet.x3 < self.x+66):
						self.blast_image_load()
						flag_plane_blast = 1



class EnemyPlane(BasePlane):
	global level
	def __init__(self, screen_temp):
		BasePlane.__init__(self, screen_temp, 0, 0, "./Resource/enemy0.png")
		self.direction = "right"#store the initial direction
		self.flag = True#用来记录敌机是否存活

	#自动移动auto move
	def move(self):
		if self.direction == "right":	
			self.x += 3
		elif self.direction == "left":
			self.x -= 3

		if self.x > 430:
			self.direction = "left"
		elif self.x < 0:
			self.direction = "right"
	#自动射击 auto fire
	def fire(self):
		if self.flag:#只有在敌机未被消灭的情况下才会随机产生子弹
			random_num = random.randint(1,50)
			if random_num == 7:#控制子弹出现的频率
				self.bullet_list.append(EnemyBullet(self.screen,self.x, self.y))

	def delay(self):
		num = 1
		for i in range(10000):
			num = num+1
	#飞机爆炸
	def blast(self, hero_temp):
		global level,flag_plane_blast
		for herobullet in hero_temp.bullet_list:
			if herobullet.y >= self.y and herobullet.y <= self.y+24:
				if herobullet.x >= self.x and herobullet.x <= self.x+34:
					self.direction = None#敌机不再移动
					self.flag = False#控制敌机不发出子弹
					self.image = pygame.image.load("./Resource/enemy1_blowup_1.png")
					self.delay()
					self.image = pygame.image.load("./Resource/enemy1_blowup_2.png")
					self.delay()
					self.image = pygame.image.load("./Resource/enemy1_blowup_3.png")
					self.delay()
					self.image = pygame.image.load("./Resource/enemy1_blowup_4.png")
					flag_plane_blast = 2

#小boss的类
class MiniBoss(BasePlane):
	def __init__(self, screen_temp):
		#初始化
		BasePlane.__init__(self, screen_temp, 0, 0, "./Resource/enemy3.png")
		self.direction = "right"#用来存储飞机默认的显示方向
		self.flag = True#用来记录敌机是否存活
		self.miniboss_hp = 3#血量

	def move(self):
		if self.direction == "right":	
			self.x += 3
		elif self.direction == "left":
			self.x -= 3

		if self.x > 430:
			self.direction = "left"
		elif self.x < 0:
			self.direction = "right"

	def fire(self):
		if self.flag:#只有在敌机未被消灭的情况下才会随机产生子弹
			random_num = random.randint(1,40)
			if random_num == 7:#控制子弹出现的频率
				self.bullet_list.append(MiniBossBullet(self.screen,self.x, self.y))

	def delay(self):
		num = 1
		for i in range(10000):
			num = num+1
	#飞机爆炸
	def blast(self, hero_temp):
		global level, flag_plane_blast
		for herobullet in hero_temp.bullet_list:
			if herobullet.y >= self.y and herobullet.y <= self.y+60:
				if herobullet.x >= self.x and herobullet.x <= self.x+46:
					self.miniboss_hp = self.miniboss_hp-1#被击中一次，血量减一
					if self.miniboss_hp == 2:
						hero_temp.bullet_list.remove(herobullet)#子弹命中目标后，就将目标移除
						self.image = pygame.image.load("./Resource/enemy3_blowup_1.png")
					elif self.miniboss_hp ==1:
						hero_temp.bullet_list.remove(herobullet)
						self.image = pygame.image.load("./Resource/enemy3_blowup_2.png")
					else:
						self.direction = None#敌机不再移动
						self.flag = False#控制敌机不发出子弹
						self.image = pygame.image.load("./Resource/enemy3_blowup_3.png")
						self.delay()
						self.image = pygame.image.load("./Resource/enemy3_blowup_4.png")
						flag_plane_blast = 3

#大boss的类
class FinalBoss(BasePlane):
	def __init__(self, screen_temp):
		#初始化
		BasePlane.__init__(self, screen_temp, 0, 0, "./Resource/enemy2.png")
		self.direction = "right"#用来存储飞机默认的显示方向
		self.flag = True#用来记录敌机是否存活
		self.finalboss_hp = 5#血量

	def move(self):
		if self.direction == "right":	
			self.x += 3
		elif self.direction == "left":
			self.x -= 3

		if self.x > 370:
			self.direction = "left"
		elif self.x < 0:
			self.direction = "right"

	def fire(self):
		if self.flag:#只有在敌机未被消灭的情况下才会随机产生子弹
			random_num = random.randint(1,20)
			if random_num == 7:#控制子弹出现的频率
				self.bullet_list.append(FinalBossBullet(self.screen,self.x, self.y))

	def delay(self):
		num = 1
		for i in range(10000):
			num = num+1
	#飞机爆炸
	def blast(self, hero_temp):
		global level, flag_plane_blast
		for herobullet in hero_temp.bullet_list:
			if herobullet.y >= self.y and herobullet.y <= self.y+164:
				if herobullet.x >= self.x and herobullet.x <= self.x+110:
					self.finalboss_hp = self.finalboss_hp-1
					if self.finalboss_hp == 4:
						hero_temp.bullet_list.remove(herobullet)#子弹命中目标后就将子弹移除
						self.image = pygame.image.load("./Resource/enemy2_blowup_1.png")
					elif self.finalboss_hp == 3:
						hero_temp.bullet_list.remove(herobullet)
						self.image = pygame.image.load("./Resource/enemy2_blowup_2.png")
					elif self.finalboss_hp == 2:
						hero_temp.bullet_list.remove(herobullet)
						self.image = pygame.image.load("./Resource/enemy2_blowup_3.png")
					elif self.finalboss_hp == 1:
						hero_temp.bullet_list.remove(herobullet)
						self.image = pygame.image.load("./Resource/enemy2_blowup_4.png")
					else:
						self.direction = None#敌机不再移动
						self.flag = False#控制敌机不发出子弹
						self.bullet_list = []
						self.image = pygame.image.load("./Resource/enemy2_blowup_5.png")
						self.delay()
						self.image = pygame.image.load("./Resource/enemy2_blowup_6.png")
						self.delay()
						self.image = pygame.image.load("./Resource/enemy2_blowup_7.png")
						flag_plane_blast = 4

#子弹基类
class BaseBullet(object):
	def __init__(self, screen_temp, x, y, image_name):
		self.x = x
		self.y = y
		self.screen = screen_temp
		self.image = pygame.image.load(image_name)

	#显示子弹
	def display(self):
		self.screen.blit(self.image,(self.x,self.y))

#hero子弹类
class Bullet(BaseBullet):
	def __init__(self, screen_temp, x, y):
		#初始化
		BaseBullet.__init__(self, screen_temp, x+30, y-15, "./Resource/bullet2.png")
  	
  	#子弹移动
	def move(self):
		self.y -= 15

	#判断是否越界
	def judge(self):
		if self.y < 0:
			return True
		else:
			return False

#enemy子弹类
class EnemyBullet(BaseBullet):
	def __init__(self, screen_temp, x, y):
		BaseBullet.__init__(self, screen_temp, x+15, y+20, "./Resource/bullet1.png")

	def move(self):
		self.y += 7#子弹速度

	#判断子弹是否越界
	def judge(self):
		if self.y > 750:
			return True
		else:
			return False

#小boss子弹类
class MiniBossBullet(object):
	def __init__(self, screen_temp, x, y):
		#初始化，每次发射两发子弹
		self.x1 = x+3
		self.y = y+40
		self.x2 = x+43
		self.screen = screen_temp
		self.image = pygame.image.load("./Resource/bullet1.png")


	def move(self):
		self.y += 10#子弹速度

	#显示子弹，每次发射两发子弹
	def display(self):
		self.screen.blit(self.image,(self.x1,self.y))
		self.screen.blit(self.image,(self.x2,self.y))

	def judge(self):
		if self.y > 750:
			return True
		else:
			return False

#大boss子弹类
class FinalBossBullet(object):
	def __init__(self, screen_temp, x, y):
		#初始化，每次发射三发子弹
		self.x1 = x+3
		self.y = y+160
		self.x2 = x+52
		self.x3 = x+107
		self.screen = screen_temp
		self.image = pygame.image.load("./Resource/bullet1.png")


	def move(self):
		self.y += 15#子弹速度

	#每次发射三发子弹
	def display(self):
		self.screen.blit(self.image,(self.x1,self.y))
		self.screen.blit(self.image,(self.x2,self.y))
		self.screen.blit(self.image,(self.x3,self.y))

	def judge(self):
		if self.y > 750:
			return True
		else:
			return False

#鼠标键盘事件处理函数
def key_control(hero_temp):
	global flag_mouse, level, flag_plane_blast

	#获取事件
	for event in pygame.event.get():
		#判断是否点击了退出按钮
		if event.type == QUIT:
			print("exit")
			exit()
		elif event.type == pygame.KEYDOWN:#控制子弹发射
			if event.key == K_SPACE:
				print('space')
				hero_temp.fire()
		pos = pygame.mouse.get_pos()#鼠标位置（x，y）
		if pos[0]>90 and pos[0]<390:#判断鼠标是否在开始图标或者退出游戏的位置点击左键
			if pos[1]>600 and pos[1]<640:
				if event.type == MOUSEBUTTONDOWN:
					pressed_mouse = pygame.mouse.get_pressed()
					if pressed_mouse[0]:
						print('Pressed LEFT Button!')
						flag_mouse = 1
						if flag_plane_blast > 0:#如果在有战机毁坏的情况下点击结束游戏图标，则退出游戏
							print("exit")
							exit()
		if pos[0]>90 and pos[0]<390:#判断鼠标是否在下一关或者重新开始（hero战机摧毁）或者游戏说明和返回按键的位置点击左键
			if pos[1]>450 and pos[1]<490:
				if event.type == MOUSEBUTTONDOWN:
					pressed_mouse = pygame.mouse.get_pressed()
					if pressed_mouse[0]:
						print('Pressed LEFT Button!')
						flag_mouse = 2
		
	#方向键采用这种方法可以连续移动，子弹不采取连续发射的方式
	pressed_keys = pygame.key.get_pressed()
	if pressed_keys[K_a] or pressed_keys[K_LEFT]:
		print('left')
		hero_temp.move_left()
	elif pressed_keys[K_d] or pressed_keys[K_RIGHT]:
		print('right')
		hero_temp.move_right()


def main():
	global level, flag_mouse, flag_plane_blast

	pygame.init()

	#创建一个窗口，窗口大小和选择的图片大小相同，用来显示内容
	screen = pygame.display.set_mode((480,852),0,32)#0和32是固定写法

	#创建一个和窗口大小的图片，用来充当背景
	background = pygame.image.load("./Resource/background.png")
	win_background = pygame.image.load("./Resource/win.png")
	hero_blast_background = pygame.image.load(r"./Resource/hero_blast_backgroud.png")
	introduction_background = pygame.image.load(r"./Resource/introduction.png")
	icon1 = pygame.image.load(r"./Resource/shoot_copyright.png")#图标
	#按钮
	start_icon_button = pygame.image.load(r"./Resource/game_start.png")
	next_level_button = pygame.image.load(r"./Resource/new_level.png")
	game_over_button = pygame.image.load(r"./Resource/game_over.png")
	restart_button = pygame.image.load(r"./Resource/game_Reagain.png")
	return_button = pygame.image.load(r"./Resource/return.png")
	introduction_button = pygame.image.load(r"./Resource/introduction_button.png")
	


	#创建一个飞机对象
	hero = HeroPlane(screen)

	#创建一个敌机
	enemy = EnemyPlane(screen)

	#创建一个小boss
	miniboss = MiniBoss(screen)

	#创建一个大boss
	finalboss = FinalBoss(screen)

	#把背景图片放到窗口中显示，持续刷新
	while True:
		#设定需要显示的背景图
		#(0,0)表示将图片的左上角贴到窗口的（0，0）点
		screen.blit(background,(0,0))
		if level == 0:
			screen.blit(icon1,(20,100))
			screen.blit(introduction_button,(90,450))
			screen.blit(start_icon_button,(90,600))
		if level == 1:
			hero.display()
			hero.blast(enemy)#检测战机爆炸
			enemy.display()
			enemy.move()#调用敌机的移动方法
			enemy.fire()#敌机开火
			enemy.blast(hero)#检测敌机爆炸
		if level == 2:
			hero.display()
			hero.blast(miniboss)#战机爆炸
			miniboss.display()
			miniboss.move()#调用敌机的移动方法
			miniboss.fire()#敌机开火
			miniboss.blast(hero)#敌机爆炸
		if level == 3:
			hero.display()
			hero.blast(finalboss)#检测战机爆炸
			finalboss.display()
			finalboss.move()#调用敌机的移动方法
			finalboss.fire()#敌机开火
			finalboss.blast(hero)#检测敌机爆炸
		key_control(hero)
		if flag_mouse == 1 and level == 0:#用于判断鼠标是否点击了开始按钮
			level = 1
			flag_mouse = 0
		if flag_mouse == 2 and level == 0:#用于判断鼠标是否点击了游戏说明
			level = 99
			flag_mouse = 0
		if level == 99:#界面切换到游戏说明界面
			screen.blit(introduction_background,(0,0))
			screen.blit(return_button,(90,450))
			if flag_mouse == 2:#用于判断鼠标是否在游戏说明界面点击了返回按钮
				level = 0
				flag_mouse = 0
		if level == 1 and flag_plane_blast == 2:#第一关结束，且enemy敌机摧毁，显示切换图案
			screen.blit(next_level_button,(90,450))
			screen.blit(game_over_button,(90,600))
			if flag_mouse == 2:#点击下一关
				level = 2
				flag_mouse = 0
				flag_plane_blast = 0
		if level == 2 and flag_plane_blast == 3:#第二关结束，且miniboss敌机摧毁，显示切换图案
			screen.blit(next_level_button,(90,450))
			screen.blit(game_over_button,(90,600))
			if flag_mouse == 2:#点击下一关
				level = 3
				flag_mouse = 0
				flag_plane_blast = 0
		if level == 3 and flag_plane_blast == 4:#第三关结束，如果finalboss敌机摧毁，显示win图案
			screen.blit(win_background,(0,0))
			screen.blit(game_over_button,(90,600))
		if flag_plane_blast == 1:#如果hero战机摧毁，则切换图案
			screen.blit(hero_blast_background,(0,0))
			screen.blit(restart_button,(90,450))
			screen.blit(game_over_button,(90,600))
			if flag_mouse == 2:#点击重新开始
				level = 1
				flag_mouse = 0
				flag_plane_blast = 0
				hero = HeroPlane(screen)
				enemy = EnemyPlane(screen)
				miniboss = MiniBoss(screen)
				finalboss = FinalBoss(screen)

		#更新需要显示的内容
		pygame.display.update()
		#控制刷新频率
		time.sleep(0.01)

if __name__ == '__main__':

	main()