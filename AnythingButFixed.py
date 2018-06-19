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
        self.onscreen = False
        self.speed = sp
        self.damage = 0
        self.up()
        self.btype = btype
        self.turtlesize(0.5, 0.5)
        self.goto(pos)
        self.color(color)
        self.direction = direction
        self.seth(self.direction)
        self.hideturtle()

    def addToScreen(self):
        self.onscreen = True
        self.seth(self.direction)
        self.showturtle()

    def takeOffScreen(self):
        self.onscreen = False
        self.hideturtle()

    def move(self, enlist):
        if self.btype == 'homing':
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
            self.takeOffScreen()
        if self.xcor() < -300 or self.xcor() > 300:
            self.takeOffScreen()

    def moveToPos(self, pos):
        self.goto(pos)

    def resetvars(self):
        self.direction = 90
        self.seth(self.direction)

    def delete(self):
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
                b.addToScreen()
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
            self.delete()

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
                b.addToScreen()
                return
            
    def burst(self, angle, number, spread):
        num = 0
        for b in self.bullets:
            if not b.onscreen:
                b.direction = angle
                b.moveToPos((self.pos()[0] + ((num-((number+1)/2))*spread), self.pos()[1]))
                b.addToScreen()
                num += 1
                if num == number:
                    return
            
    def spreadshoot(self):
        num = 0
        for b in self.bullets:
            if not b.onscreen:
                b.direction = random.randint(-110, -70)
                b.moveToPos(self.pos())
                b.addToScreen()
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

    def fire(self):
        pass

    def move(self):
        pass

    def takeDamage(self):
        pass
    
    def buy():
        pass
    
t = Turtle()
s = t.getscreen()
m = Turtle()
t.hideturtle()
del t

print(s.getTurtles())
