# Anything but That
# version 0.2

from tkinter import *
from turtle import *
import random
from Highscore_tools import *
from math import *
import ABTShapes
from time import time
import os
#import gc

class explosion(Turtle):
    def __init__(self, pos, fade, color = (255, 0, 0), radius = 40):
        Turtle.__init__(self)
        self.fade = fade
        self.up()
        self.goto(pos)
        self.pencolor((0, 255, 0))
        self.radius = radius
        self.shape('circle')
        self.explode(1)

    def explode(self, radius, hitenemies = []):
        damagedenemies = list(hitenemies)
        self.shapesize(radius/10)
        for enemy in elist:
            if (not enemy in hitenemies) and sqrt(((enemy.xcor()-self.xcor())**2)+(enemy.ycor()-self.ycor())**2)<=radius:
                enemy.takeDamage()
                damagedenemies.append(enemy)
        if radius < self.radius:
            self.pencolor((int(self.pencolor()[0]/self.fade), int(self.pencolor()[1]/self.fade), int(self.pencolor()[2]/self.fade)))
            scoreboard.after(50, lambda: self.explode(radius+4, damagedenemies))
        else:
            bullets.append(self)
            self.hideturtle()
            del self

    def move(self, x):
        pass
            

class bullet(Turtle):
    def __init__(self, direction, pos, color = (255, 0, 0), sp = 1.5, btype = 'regular'):
        Turtle.__init__(self)
        self.movespeed = sp #How fast you are (higher is faster)
        self.damage = 0 #How much damage a bullet deals
        self.radius = 40 #Used for the bomb
        
        self.up()
        self.btype = btype
        self.turtlesize(0.5, 0.5)
        self.goto(pos)
        self.color(color)
        self.direction = direction
        self.seth(self.direction)
        #self.start(direction, pos, color)

    def start(self):
        self.up()
        self.turtlesize(0.5, 0.5)
        self.goto(pos)
        self.color((0, 255, 0))
        self.seth(self.direction)

    def move(self, elist):
        if self.btype == 'homing': #Run homing missile code if this is a homing missile
            bestenemy = ''
            bestdistance = float('inf')
            for enemy in elist:
                x = sqrt((self.xcor()-enemy.xcor())**2+(self.ycor()-enemy.ycor())**2)
                if x<bestdistance:
                    bestdistance = x
                    bestenemy = enemy
            if bestenemy != '':
                x = self.heading()-90
                self.seth(x+(self.towards(bestenemy)-90>x)-(self.towards(bestenemy)-90<x)+90)
            self.forward(self.movespeed)
        else:
            self.forward(self.movespeed)
        if self.ycor() < -300 or self.ycor() > 300: #Take yourself off the screen when you're off the screen
            self.delete()
        if self.xcor() < -300 or self.xcor() > 300:
            self.delete()

    def moveToPos(self, pos):
        self.goto(pos)

    def resetvars(self):
        self.direction = 90
        self.seth(self.direction)

    def collide(self):
        if self.btype == 'bomb':
            t = explosion(self.pos(), 1.2, radius = self.radius)
        self.delete()

    def explode(self, radius, turtle, hitenemies = []):
        damagedenemies = list(hitenemies)
        turtle.shapesize(radius/10)
        for enemy in elist:
            if (not enemy in hitenemies) and sqrt(((enemy.xcor()-self.xcor())**2)+(enemy.ycor()-self.ycor())**2)<=radius:
                enemy.takeDamage()
                damagedenemies.append(enemy)
        if radius < self.radius:
            turtle.pencolor((0, int(sum(turtle.pencolor())/1.25), 0))
            root.after(50, lambda: self.explode(radius+4, turtle, damagedenemies))
        else:
            turtle.delete()

    def delete(self):
        self.hideturtle()
        del self

def garbage_collect(bullets):
    '''Takes in turtles and deletes them'''
    for b in bullets:
        bullets.remove(b)
        screen._turtles.remove(b)

       
class enemy(Turtle):
    def __init__(self, level):
        Turtle.__init__(self)
        self.speed(0)
        self.pencolor(255, 0, 0)
        self.level = level
        self.up()
        self.health = level
        self.turtlesize(self.health, self.health, 2)
        self.right(90)
        self.goto(random.randint(-300, 300), 300)
        self.going = 1
        elist.append(self)

    def move(self, p):
        self.forward(0.5)
        if self.ycor() < -300 or self.ycor() > 300:
            self.delete()
        if self.level == 5:
            self.shape('5enemy')
            self.setx(self.xcor() + self.going)
            if self.xcor() > 300:
                self.setx(-300)
            if self.xcor() < -300:
                self.setx(300)
        elif self.level >= 6:
            a = self.towards(p)
        if not random.randint(0, 100):
            self.shoot()

    def shoot(self):
        self.going = self.going * -1
        b = bullet(-90, self.pos(), (255, 0, 0))
        ebullets.append(b)
        return

    def resetstuff(self):
        for b in self.bullets:
            b.takeOffScreen()
        self.health = self.level
        self.hideturtle()
        self.turtlesize(self.health, self.health, 2)
        self.goto(random.randint(-300, 300), 300)
        self.seth(-90)

    def takeDamage(self, damage = 1):
        self.health -= damage
        if self.health > 0:
            self.turtlesize(self.health, self.health, 2)
            return False #Youre alive
        else:
            self.delete() #Die if you're dead
            return True

    def delete(self):
        self.hideturtle()
        del self

class boss(Turtle):
    def __init__(self):
        Turtle.__init__(self)
        self.spot = 0
        self.bullets = []
        self.bossness = 0
        self.health = 0
        self.keeper = Turtle()
        self.up()

    def setup(self, level):
        pass

    def showturtleandhealth(self):
        self.showturtle()
        self.keeper.seth(0)
        self.keeper.fillcolor('red')
        self.keeper.hideturtle()
        self.keeper.goto(0, 300)
        self.keeper.begin_fill()
        self.keeper.forward(self.health/2)
        self.keeper.left(90)
        self.keeper.forward(10)
        self.keeper.left(90)
        self.keeper.forward(self.health)
        self.keeper.left(90)
        self.keeper.forward(10)
        self.keeper.left(90)
        self.keeper.forward(self.health/2)
        self.keeper.backward(self.health/2)
        self.keeper.left(90)
        self.keeper.end_fill()

    def takeDamage(self, damage):
        self.keeper.clear()
        self.health -= damage
        self.keeper.begin_fill()
        self.keeper.forward(10)
        self.keeper.right(90)
        self.keeper.forward(self.health)
        self.keeper.right(90)
        self.keeper.forward(10)
        self.keeper.right(90)
        self.keeper.forward(self.health)
        self.keeper.right(90)
        self.keeper.end_fill()
        if self.health <= 0:
            self.keeper.clear()
            return True
        return False
    
    def moveBullets(self):
        for b in self.bullets:
            if b.onscreen:
                b.move()
                if b.ycor() < -300 or b.ycor() > 300:
                    b.takeOffScreen()
                    
    def shoot(self):
        for b in self.bullets:
            if not b.onscreen:
                b.seth(-90)
                b.moveToPos(self.pos())
                return
            
    def burst(self, angle, number, spread):
        num = 0
        for b in self.bullets:
            if not b.onscreen:
                b.direction = angle
                b.moveToPos((self.pos()[0] + ((num-((number+1)/2))*spread), self.pos()[1]))
                num += 1
                if num == number:
                    return
            
    def spreadshoot(self):
        num = 0
        for b in self.bullets:
            if not b.onscreen:
                b.direction = random.randint(-110, -70)
                b.moveToPos(self.pos())
                num += 1
                if num == 3:
                    return

    def lazershot(self, start, direction):
        for b in self.bullets:
            if not b.onscreen:
                b.goto(start)
                b.color('red')
                b.down()
                b.width(5)
                b.seth(direction)
                while b.ycor() > -290:
                    b.forward(5)
                if abs(b.xcor() - p.xcor()) < p.turtlesize()[0]*5:
                    b.up()
                    b.width(1)
                    b.getscreen().update()
                    return True
                b.up()
                b.width(1)
                b.getscreen().update()
                return False

def stop():
    global stopped, root
    stopped = True
    screen.onkey(main, "e")
    screen.onkey(main, "E")
    root = Tk()
    shop(root, n)#boss.bossness

def movel():
    global mov
    mov = -2

def stopmovel():
    global mov
    if mov == -2:
        mov = 0

def mover():
    global mov
    mov = 2

def stopmover():
    global mov
    if mov == 2:
        mov = 0

class player(Turtle):
    def __init__(self, weapons):
        Turtle.__init__(self)
        self.weapons = weapons
        self.weapon = 0
        self.health = 20
        self.charge = 0
        self.chargespeed = 1
        self.maxcharge = 5
        self.points = 1000000
        self.cap = 25 #Maximum number of bullets on the screen
        self.up()
        self.pencolor(color)

    def spray(self, num, charge, damage, speed, spread = 10, regular = False):
        self.charge -= charge
        for i in range(1, num+1): #If the bullet cap is 2 more than the # of bullets, it will exceed that number i. e. 18+3 =21>20
            b = bullet(90, p.pos(), (0, 255, 0))
            bullets.append(b)
            b.damage = 1
            b.speed = 1.5
            b.moveToPos(p.pos())
            if regular:
                b.direction = 90 + (floor(num/2) - i)*regular
                b.seth(b.direction)
            else:
                b.direction = random.randint(90 - spread, 90 + spread)
                b.seth(b.direction)

    def fire(self):
        if len(bullets) < self.cap:
            if self.weapons[self.weapon] == 'blaster':
                b = bullet(90, self.pos(), (0, 255, 0))
                bullets.append(b)
                b.damage = 1
                b.speed = 1.5
                b.moveToPos(p.pos())
            elif self.weapons[self.weapon] == 'spreadshot' and self.charge >= 2:
                self.spray(3, 2, 1, 1.5)
            elif self.weapons[self.weapon] == 'lazor' and self.charge >= 3:
                self.charge -= 3
                self.lazorgo()
            elif self.weapons[self.weapon] == 'blaster_2.0' and self.charge >= 3:
                b = bullet(90, p.pos(), (0, 255, 0))
                bullets.append(b)
                self.charge -= 2
                b.damage = 2
                b.speed = 1
                b.moveToPos(p.pos())
            elif self.weapons[self.weapon] == 'homing_missile' and self.charge >= 2:
                b = bullet(90, p.pos(), (0, 255, 0), 1.5, 'homing')
                bullets.append(b)
                self.charge -= 2
                b.damage = 1
                b.moveToPos(p.pos())
                b.seth(90)
            elif self.weapons[self.weapon] == 'bombs' and self.charge >= 3:
                self.charge -= 1
                b = bullet(90, p.pos(), (0, 255, 0), 1.2, 'bomb')
                b.damage = 1
                bullets.append(b)
                b.moveToPos(p.pos())
                b.seth(90)
            elif self.weapons[self.weapon] == 'pentashot' and self.charge >= 3:
                self.spray(5, 3, 1, 2.5, regular = 40)
            elif self.weapons[self.weapon] == "machine_gun" and self.charge >= 4:
                self.spray(7, 4, 1, 2, spread = 20)
        updatecharge()
        return
    
    def move(self):
        pass

    def takeDamage(self):
        pass

    def changeWeapon(self):
        self.weapon += 1
        self.weapon %= len(self.weapons)
        updatescoreboard()
    
    def buy(self, button, weapon, cost):
        if self.points >= cost:
            button.forget()
            self.weapons.append(weapon)
            self.points -= cost

    def lazorgo(self):
        pass

def chargeboost():
    global p
    if p.points >= 5:
        p.points -= 5
        p.maxcharge += 2
        updatescoreboard()

def healthboost():
    global p
    if p.points >= 10:
        p.points -= 10
        p.health += 1
        updatescoreboard()

def csboost():
    global p
    if p.points >= 10:
        p.points -= 10
        p.chargespeed += 0.2
        updatescoreboard()

def shop(root, k):
    global weapons
    c = Canvas(root)
    c.pack()
    root.title("turtle man's shop :D")
    rt = RawTurtle(c)
    bg = rt.getscreen()
    bg.bgcolor('black')
    bg.colormode(255)
    rt.shape('turtle')
    rt.turtlesize(3, 3, 2)
    rt.right(90)
    rt.pencolor(0, 255, 0)

    
    f = open("Weapons.txt").read().split('\n')
    for weapond in f:
        weapon = weapond.split()
        if weapon[0] not in p.weapons and weapon[1] in p.weapons and n >= int(weapon[2]):
            button = Button(root, text = ' '.join(weapon[4:]), command = lambda: 1+1)
            button.configure(command=lambda b=button, weapon=weapon[0], cost=int(weapon[3]): p.buy(b, weapon, cost))
            #button = Button(root, text = ' '.join(weapon[4:]), command = lambda b=button, weapon=weapon[0], cost=int(weapon[3]): p.buy(b, weapon, cost))#button, weapon, cost
            button.pack()
    chargeb = Button(root, text = 'max charge + 2 [self explanatory] (5 pts)', command = chargeboost)
    chargeb.pack()
    if k > 0:
        hb = Button(root, text = 'health + 1 [self explanatory] (10 pts)', command = healthboost)
        hb.pack()
    if k > 1:
        hb = Button(root, text = 'increase charge speed [self explanatory] (10 pts)', command = csboost)
        hb.pack()

def updatescoreboard():
    global scoreboard, score, hitpoints, battery, weaponl
    try:
        score.forget()
        hitpoints.forget()
        weaponl.forget()
        battery.forget()
        score = Label(scoreboard, text = 'points: ' + str(p.points), font = ('Monaco', 16))
        score.pack()
        hitpoints = Label(scoreboard, text = 'health: ' + str(p.health), font = ('Monaco', 16))
        hitpoints.pack()
        weaponl = Label(scoreboard, text = 'weapon: ' + str(p.weapons[p.weapon]), font = ('Monaco', 16))
        weaponl.pack()
        battery = Label(scoreboard, text = 'charge: ' + str(int(p.charge)), font = ('Monaco', 16))
        battery.pack()
    except TclError:
        scoreboard = Tk()
        score = Label(scoreboard, text = 'points: ' + str(points), font = ('Monaco', 16))
        score.pack()
        hitpoints = Label(scoreboard, text = 'health: ' + str(p.health), font = ('Monaco', 16))
        hitpoints.pack()
        weaponl = Label(scoreboard, text = 'weapon: ' + str(p.weapons[p.weapon]), font = ('Monaco', 16))
        weaponl.pack()
        battery = Label(scoreboard, text = 'charge: ' + str(int(p.charge)), font = ('Monaco', 16))
        battery.pack()

def updatecharge(): #Delete if this doesn't make things faster
    global scoreboard, battery
    try:
        battery.forget()
        battery = Label(scoreboard, text = 'charge: ' + str(int(p.charge)), font = ('Monaco', 16))
        battery.pack()
    except TclError:
        scoreboard = Tk()
        score = Label(scoreboard, text = 'points: ' + str(p.points), font = ('Monaco', 16))
        score.pack()
        hitpoints = Label(scoreboard, text = 'health: ' + str(p.health), font = ('Monaco', 16))
        hitpoints.pack()
        weaponl = Label(scoreboard, text = 'weapon: ' + str(p.weapons[p.weapon]), font = ('Monaco', 16))
        weaponl.pack()
        battery = Label(scoreboard, text = 'charge: ' + str(int(p.charge)), font = ('Monaco', 16))
        battery.pack()

def start_tutorial():
    screen.onkey(first_loop, "e")
    screen.onkey(first_loop, "E")
    turtor = Turtle()
    turtor.up()
    turtor.seth(-90)
    turtor.shapesize(2)
    turtor.shape('turtle')
    turtor.pencolor('green')
    turtor.goto(20, 20)
    turtor.write('Hi there', font=("Ariel", 10, "normal"))
    turtor.goto(0, 0)
    screen.update()
    canvas.after(1500, lambda: speech(turtor, 'Press space to shoot.'))
    canvas.after(3500, lambda: speech(turtor, 'Press w to cycle through your weapons.'))
    canvas.after(5500, lambda: speech(turtor, 'You can press e to pause the game.\nIt will also open the shop.'))
    canvas.after(8500, lambda: speech(turtor, "I'll be in there to sell you weapons for the\npoints you get from hitting enemies."))
    canvas.after(11500, lambda: speech(turtor, "When you kill an enemy you may be able to use\ntheir scrap to fix your ship and get more health."))
    canvas.after(14500, lambda: speech(turtor, "Here's a blaster. Use it safely."))
    canvas.after(16500, lambda: speech(turtor, "I almost forgot, arrow keys to move."))
    canvas.after(18500, lambda: speech(turtor, "Bye bye"))
    canvas.after(20500, lambda: turtor.hideturtle())
    canvas.after(20500, lambda: speech(turtor, ''))
    canvas.after(20500, first_loop)

def speech(turtor, words):
    if not started:
        turtor.clear()
        turtor.goto(20, 20)
        turtor.write(words, font=("Ariel", 10, "normal"))
        turtor.goto(0, 0)
        screen.update()
    else:
        turtor.hideturtle()
        turtor.clear()

def first_loop():
    global started
    if not started:
        started = True
        main()

colormode(255)
color = (0, 255, 0)

p = player(['blaster'])
screen = p.getscreen()
screen.colormode(255)
screen.tracer(0)
canvas = screen.getcanvas()
ABTShapes.registerABTShapes(screen)
screen.bgcolor(0, 0, 0)
p.turtlesize(3, 4, 2)
p.left(90)
p.back(275)
#p.pencolor(color)


bullets = [] #Holds the players bulletsd
ebullets = [] #Holds the enemy bullets
elist = [] #Holds all the enemies
garbage = []

mov = 0
n = 3 #Progress for enemy level
distance = 0## 0
kdistance = 20## 0
fight = False
stopped = False
started = False
scoreboard = Tk()
root = 0
'''boss = boss()
boss.bossness = 2## 0
boss.hideturtle()'''
g = False

screen.listen()
screen.onkeypress(movel, "Left")
screen.onkey(stopmovel, "Left")
screen.onkeypress(mover, "Right")
screen.onkey(stopmover, "Right")
screen.onkey(p.changeWeapon, "w")
screen.onkey(p.changeWeapon, "W")
screen.onkeypress(p.fire, "space")
screen.title('Anything but That')
os.system('xset r off')

score = Label(scoreboard, text = 'points: ' + str(p.points), font = ('Monaco', 16))
score.pack()
hitpoints = Label(scoreboard, text = 'health: ' + str(p.health), font = ('Monaco', 16))
hitpoints.pack()
battery = Label(scoreboard, text = 'charge: ' + str(p.charge), font = ('Monaco', 16))
battery.pack()
weaponl = Label(scoreboard, text = 'weapon: ' + str(p.weapons[p.weapon]), font = ('Monaco', 16))
weaponl.pack()

def loop_iteration():
    '''Iterates once and returns whether you're done'''
    p.setx(p.xcor() + mov)
    if p.charge < p.maxcharge and distance % 20 == 0:
        p.charge += p.chargespeed
        updatecharge()
    if p.xcor() > 300:
        p.setx(-300)
    if p.xcor() < -300:
        p.setx(300)
    if random.randint(0, 100) == 100 and not fight:
        x = enemy(random.randint(n, n+1))
    for i in range(len(elist)):
        try:
            e = elist[i]
            e.move(p) #p is Player
            if elist[i].ycor() < -300:
                e.delete()
        except:
            pass
                
    for b in bullets:
        b.move(elist)
        for e in elist:
            if abs(b.ycor() - e.ycor()) < 20:
                if abs(b.xcor() - e.xcor()) < e.turtlesize()[0]*6:
                    if e.takeDamage(b.damage): #True if it dies
                        if random.randint(0, 1) == 0:
                            p.health += 1
                            updatescoreboard()
                    b.collide()
                    if random.randint(0, 1) == 0:
                        p.points += b.damage
                        updatescoreboard()

    for b in ebullets:
        b.move(elist)
        if abs(b.ycor() - p.ycor()) < 20:
            if abs(b.xcor() - p.xcor()) < p.turtlesize()[0]*5:
                b.delete()
                p.health -= 1
                updatescoreboard()
    if stopped:
        screen.onkey(main, "e")
        screen.onkey(main, "E")
        root = Tk()
        shop(root, boss.bossness)
    if p.health < 1:
        print('you lose haha')
        print('points: ', p.points)
        print('distance: ', distance + 1000*kdistance)
        if p.points > get_highscore('Anything_But_That'):
            change_highscore('Anything_But_That', p.points)
            print('NEW POINTS HIGH SCORE!!!!')
        if distance + 1000*kdistance > get_highscore('Anything_But_Thatd'):
            change_highscore('Anything_But_Thatd', distance + 1000*kdistance)
            print('NEW DISTANCE HIGH SCORE!!!!')
        print('highscore: ', get_highscore('Anything_But_That'))
        print('distance highscore: ', get_highscore('Anything_But_Thatd'))
        raise done 
    return False
                        
def boss_iteration():
    pass
    
def main():
    global distance, kdistance, root, stopped, fight
    stopped = False
    if distance % 40 == 10:
        garbage_collect(garbage)
    for b in bullets:
        if not b.isvisible():
            garbage.append(b)
            bullets.remove(b)
    for b in ebullets:
        if not b.isvisible():
            garbage.append(b)
            ebullets.remove(b)
    for e in elist:
        if not e.isvisible():
            garbage.append(e)
            elist.remove(e)
    if fight:
        boss_iteration()
    loop_iteration()
    if root != 0:
        try:
            root.destroy()
        except:
            pass
    screen.onkey(stop, "e")
    screen.update()

try:
    while True:
        if not stopped:
            main()
        else:
            screen.update()
except:
    pass
