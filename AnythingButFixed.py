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
        else:
            elist.remove(self)
            self.delete() #Die if you're dead

    def delete(self):
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
            elif self.weapons[self.weapon] == 'blaster 2.0' and charge >= 3:
                b = bullet(90, p.pos(), (0, 255, 0))
                charge -= 2
                b.damage = 2
                b.speed = 1
                b.moveToPos(p.pos())
                b.reset()
                return
            elif self.weapons[self.weapon] == 'homingmissile' and charge >= 2:
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
            elif self.weapons[self.weapon] == "machine gun" and charge >= 4:
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
    
    def buy():
        pass

    def lazorgo(self):
        pass

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

<<<<<<< HEAD
def loop_iteration():
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
                e.resetstuff()
                enlist.remove(e)
                enlist.append(e)
                ennum -= 1
=======
colormode(255)

print(s.getTurtles())
>>>>>>> 57e5a639d6efcbfc138d9e1df6304a742a7dc9c6
