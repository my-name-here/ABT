# Anything but That
# version 0.2

from turtle import *
from tkinter import *
import random
from Highscore_tools import *
from math import *
import ABTShapes
from time import time
import os
import gc


class bullet(Turtle):
    def __init__(self, direction, pos, color = (255, 0, 0), sp = 1.5, btype = 'regular'):
        Turtle.__init__(self)
        self.onscreen = False #Are you on the screen
        self.speed = sp #How fast you are (higher is faster)
        self.damage = 0 #How much damage a bullet deals
        self.radius = 40 #Used for the bomb
        self.up()
        self.btype = btype
        self.turtlesize(0.5, 0.5)
        self.goto(pos)
        self.color(color)
        self.direction = direction
        self.seth(self.direction)
        bullets.append(self) #Put yourself in the bullet list

    def move(self, enlist):
        if self.btype == 'homing': #Run homing missile code if this is a homing missile
            bestenemy = ''
            bestdistance = float('inf')
            for enemy in enlist:
                x = sqrt((self.xcor()-enemy.xcor())**2+(self.ycor()-enemy.ycor())**2)
                if x<bestdistance:
                    bestdistance = x
                    bestenemy = enemy
            if bestenemy != '':
                x = self.heading()-90
                self.seth(x+(self.towards(bestenemy)-90>x)-(self.towards(bestenemy)-90<x)+90)
            self.forward(self.speed)
        self.forward(self.speed)
        if self.ycor() < -300 or self.ycor() > 300:
            return True
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
            self.shape('circle')
            self.explode(1, self)
        else:
            self.delete()

    def explode(self, radius, turtle, hitenemies = []):
        damagedenemies = list(hitenemies)
        turtle.shapesize(radius/10)
        for enemy in enlist:
            if (not enemy in hitenemies) and sqrt(((enemy.xcor()-self.xcor())**2)+(enemy.ycor()-self.ycor())**2)<=radius:
                enemy.takeDamage()
                damagedenemies.append(enemy)
        if radius < self.radius:
            turtle.pencolor((0, int(sum(turtle.pencolor())/1.25), 0))
            root.after(50, lambda: self.explode(radius+4, turtle, damagedenemies))
        else:
            turtle.delete()

    def delete(self):
        bullets.remove(self)
        self.getscreen()._turtles.remove(self)
        del self
       
class enemy(Turtle):
    def __init__(self, level):
        Turtle.__init__(self)
        self.speed(0)
        self.pencolor(255, 0, 0)
        self.level = level
        self.up()
        self.health = level
        self.hideturtle()
        self.turtlesize(self.health, self.health, 2)
        self.right(90)
        self.goto(random.randint(-300, 300), 300)
        self.bullets = []
        self.going = 1
        for i in range(5):
            b = bullet(-90, self.pos())
            self.bullets.append(b)
        elist.append(self)

    def move(self, p):
        self.forward(0.5)
        if self.level == 5:
            self.shape('5enemy')
            self.setx(self.xcor() + self.going)
            if self.xcor() > 300:
                self.setx(-300)
            if self.xcor() < -300:
                self.setx(300)
        elif self.level >= 6:
            a = self.towards(p)
            
        for b in self.bullets:
            if b.onscreen:
                b.move()
                if b.ycor() < -300 or b.ycor() > 300:
                    b.takeOffScreen()

    def shoot(self):
        self.going = self.going * -1
        for b in self.bullets:
            if not b.onscreen:
                b.moveToPos(self.pos())
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
        elist.remove(self)
        self.getscreen()._turtles.remove(self)
        del self

class boss(Turtle):
    def __init__(self):
        Turtle.__init__(self)
        self.spot = 0
        self.bullets = []
        self.bossness = 0
        for i in range(20):
            b = bullet(-90, self.pos())
            self.bullets.append(b)
        self.health = 0
        self.keeper = Turtle()
        self.up()

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

class player(Turtle):
    def __init__(self, weapons):
        Turtle.__init__(self)
        self.weapons = weapons
        self.weapon = 0
        self.health = 20
        self.charge = 0
        self.chargespeed = 0
        self.chargemax = 5
        self.points = 0
        self.cap = 25 #Maximum number of bullets on the screen

    def fire(self):
        num = 0
        if len(bullets) < self.cap:
            if self.weapons[self.weapon] == 'blaster':
                b = bullet(90, p.pos(), (0, 255, 0))
                b.damage = 1
                b.speed = 1.5
                b.moveToPos(p.pos())
                b.reset()
                return
            elif self.weapons[self.weapon] == 'spreadshot' and charge >= 2:
                charge -= 2
                for i in range(3): #If the bullet cap is 2 more than the # of bullets, it will exceed that number i. e. 18+3 =21>20
                    b = bullet(90, p.pos(), (0, 255, 0))
                    b.damage = 1
                    b.speed = 1.5
                    b.moveToPos(p.pos())
                    b.direction = random.randint(80, 100)
                return
            elif self.weapons[self.weapon] == 'lazor' and charge >= 3:
                charge -= 3
                self.lazorgo()
                return
            elif self.weapons[self.weapon] == 'blaster_2.0' and charge >= 3:
                b = bullet(90, p.pos(), (0, 255, 0))
                charge -= 2
                b.damage = 2
                b.speed = 1
                b.moveToPos(p.pos())
                b.reset()
                return
            elif self.weapons[self.weapon] == 'homing_missile' and charge >= 2:
                b = bullet(90, p.pos(), (0, 255, 0), 1.5, 'homing')
                charge -= 2
                h.moveToPos(p.pos())
                h.seth(90)
                return
            elif self.weapons[self.weapon] == 'bombs' and charge >= 3:
                charge -= 1
                b = bullet(90, p.pos(), (0, 255, 0), 1.2, 'bomb')
                b.moveToPos(p.pos())
                b.seth(90)
                return
            elif self.weapons[self.weapon] == 'pentashot' and charge >= 3:
                charge -= 3
                for num in range(1, 6):
                    b = bullet(90, p.pos(), (0, 255, 0))
                    b.moveToPos(p.pos())
                    b.damage = 1
                    b.speed = 2.5
                    x = 40
                    b.direction = 90 + (2 - num)*x
                    b.seth(90 + (2 - num)*x)
                return
            elif self.weapons[self.weapon] == "machine_gun" and charge >= 4:
                charge -= 4
                for i in range(7):
                    b = bullet(90, p.pos(), (0, 255, 0))
                    b.moveToPos(p.pos())
                    b.damage = 1
                    b.speed = 2
                    b.direction = random.randint(70,110)
                    b.seth(b.direction)

    def move(self):
        pass

    def takeDamage(self):
        pass
    
    def buy(self, button, weapon, cost):
        button.forget()
        self.weapons.append(weapon)
        self.points -= cost

    def lazorgo(self):
        pass

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

    chargeb = Button(root, text = 'max charge + 2 [self explanatory] (5 pts)', command = chargeboost)
    chargeb.pack()
    f = open("HighScore.txt").read().split('\n')
    for weapond in f:
        weapon = weapond.spilt()
        if weapon[0] not in p.weapons and weapon[1] in p.weapons and n >= weapon[2]:
            button = Button(root, text = ' '.join(weapon[4:]), command = lambda: p.buy(button, weapon[0], weapon[3]))#button, weapon, cost
            button.pack()
    if k > 0:
        hb = Button(root, text = 'health + 1 [self explanatory] (10 pts)', command = lambda: p.health += 1)
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
bullets = [] #Holds the players bulletsd
elist = [] #Holds all the enemies

mov = 0
n = 1 #Progress for enemy level
distance = 0## 0
kdistance = 20## 0
fite = False
stopped = False
started = False
scoreboard = Tk()
root = 0
boss = boss()
boss.bossness = 2## 0
boss.hideturtle()
g = False

score = Label(scoreboard, text = 'points: ' + str(points), font = ('Monaco', 16))
score.pack()
hitpoints = Label(scoreboard, text = 'health: ' + str(health), font = ('Monaco', 16))
hitpoints.pack()
battery = Label(scoreboard, text = 'charge: ' + str(charge), font = ('Monaco', 16))
battery.pack()
weaponl = Label(scoreboard, text = 'weapon: ' + str(weapons[weapon]), font = ('Monaco', 16))
weaponl.pack()

def loop_iteration():
    '''Iterates once and returns whether you're done'''
    if charge < maxcharge and distance % 20 == 0:
        charge += chargespeed
        updatecharge()
    if p.xcor() > 300:
        p.setx(-300)
    if p.xcor() < -300:
        p.setx(300)
    if random.randint(0, 100) == 100 and not fite:
        x = enemy(random.randint(n, n+1))
    for i in range(len(elist)):
            e = elist[i]
            e.move(p) #p is Player
            if random.randint(0, 200) == 0:
                e.shoot()
            if enlist[i].ycor() < -300:
                e.delete()
                
    for b in bullets:
        b.move()
        for e in elist:
            if abs(b.ycor() - e.ycor()) < 20:
                if abs(b.xcor() - e.xcor()) < e.turtlesize()[0]*6:
                    if e.takeDamage(b.damage): #True if it dies
                        if random.randint(0, 1) == 0:
                            health += 1
                            updatescoreboard()
                    b.collide()
                    if random.randint(0, 1) == 0:
                        points += b.damage
                        updatescoreboard()

    for e i in elist:
        for b in e.bullets:
            if abs(b.ycor() - p.ycor()) < 20:
                if abs(b.xcor() - p.xcor()) < p.turtlesize()[0]*5:
                    b.delete()
                    p.health -= 1
                    updatescoreboard()
    if stopped:
        screen.onkey(loop, "e")
        screen.onkey(loop, "E")
        root = Tk()
        shop(root, boss.bossness)
        break
    if health < 1:
        print('you lose haha')
        print('points: ', points)
        print('distance: ', distance + 1000*kdistance)
        if points > get_highscore('Anything_But_That'):
            change_highscore('Anything_But_That', points)
            print('NEW POINTS HIGH SCORE!!!!')
        if distance + 1000*kdistance > get_highscore('Anything_But_Thatd'):
            change_highscore('Anything_But_Thatd', distance + 1000*kdistance)
            print('NEW DISTANCE HIGH SCORE!!!!')
        print('highscore: ', get_highscore('Anything_But_That'))
        print('distance highscore: ', get_highscore('Anything_But_Thatd'))
        return True
    return False
                        
def boss_iteration():
    if distance == 1000:
        kdistance += 1
        distance = 0
        print('1km')
        if kdistance % 10 == 0:
            fite = True
            print('ahh', kdistance)
    if not fite:
        distance += 1
    

def main():
    loop_iteration()
    boss_iteration()
    if root != 0:
        try:
            root.destroy()
        except:
            pass
    screen.onkey(stop, "e")
    stopped = False
    screen.update()

colormode(255)

