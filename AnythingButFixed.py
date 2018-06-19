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
        self.radius = 40#Used for the bomb
        self.up()
        self.btype = btype
        self.turtlesize(0.5, 0.5)
        self.goto(pos)
        self.color(color)
        self.direction = direction
        self.seth(self.direction)

    def move(self, enlist):
        if self.btype == 'homing': #Run homing missile code uf this is a homing missile
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
        if self.ycor() < -300 or self.ycor() > 300: #Take yourself off the screen when you're off the screen
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
                bullets.append(b)
                b.damage = 1
                b.speed = 1.5
                b.moveToPos(p.pos())
                b.reset()
                return
            elif self.weapons[self.weapon] == 'spreadshot' and charge >= 2:
                charge -= 2
                for i in range(3): #If the bullet cap is 2 more than the # of bullets, it will exceed that number i. e. 18+3 =21>20
                    b = bullet(90, p.pos(), (0, 255, 0))
                    bullets.append(b)
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
                bullets.append(b)
                charge -= 2
                b.damage = 2
                b.speed = 1
                b.moveToPos(p.pos())
                b.reset()
                return
            elif self.weapons[self.weapon] == 'homingmissile' and charge >= 2:
                b = bullet(90, p.pos(), (0, 255, 0), 1.5, 'homing')
                bullets.append(b)
                charge -= 2
                h.moveToPos(p.pos())
                h.seth(90)
                return
            elif self.weapons[self.weapon] == 'bombs' and charge >= 3:
                charge -= 1
                b = bullet(90, p.pos(), (0, 255, 0), 1.2, 'bomb')
                bullets.append(b)
                b.moveToPos(p.pos())
                b.seth(90)
                return
            elif self.weapons[self.weapon] == 'pentashot' and charge >= 3:
                charge -= 3
                for num in range(1, 6):
                    b = bullet(90, p.pos(), (0, 255, 0))
                    bullets.append(b)
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
                    bullets.append(b)
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

bullets = []
elist = []
t = Turtle()
s = t.getscreen()
m = Turtle()
t.hideturtle()
del t

def loop():
    global p, ennum, stopped, screen, enlist, pbullets, mov, health, points, root
    global charge, maxcharge, weapons, weapon, distance, kdistance, fite, boss
    global bbullets
    distance += 1
    if root != 0:
        try:
            root.destroy()
        except:
            pass
    screen.onkey(stop, "e")
    stopped = False
    while True:
        distance += 1
        if fite:
            distance = distance % 20
        if distance == 1000:
            kdistance += 1
            distance = 0
            print('1km')
            if kdistance % 10 == 0:
                fite = True
                print('ahh', kdistance)
        screen.update()
        p.setx(p.xcor() + mov)

        if fite:
            global n
            if kdistance == 10 and boss.bossness == 0 and not boss.isvisible():
                boss.turtlesize(20, 20, 2)
                boss.pencolor(255, 0, 0)
                boss.seth(-90)
                boss.up()
                boss.goto(0, 300)
                boss.health = 200
                boss.showturtleandhealth()
                n = 1
                for i in range(200):
                    boss.forward(1)
                    screen.update()
                    
            elif kdistance == 20 and boss.bossness == 1 and not boss.isvisible():
                boss.turtlesize(2, 2, 2)
                boss.pencolor(255, 0, 0)
                boss.shape('boss2')
                boss.seth(-90)
                boss.up()
                boss.spot = 0
                boss.goto(0, 300)
                boss.health = 200
                boss.showturtleandhealth()
                n = 1
                for i in range(200):
                    boss.forward(1)
                    screen.update()

            elif kdistance == 30 and boss.bossness == 2 and not boss.isvisible():
                boss.turtlesize(10, 20, 2)
                boss.pencolor(255, 0, 0)
                boss.shape('classic')
                boss.seth(-90)
                boss.up()
                boss.goto(0, 300)
                boss.health = 300
                boss.showturtleandhealth()
                n = 1
                for i in range(200):
                    boss.forward(1)
                    screen.update()
            
            elif boss.isvisible() and kdistance == 10:
                try:
                    boss.moveBullets()
                    for b in boss.bullets:
                        if abs(b.ycor() - p.ycor()) < 20:
                            if abs(b.xcor() - p.xcor()) < p.turtlesize()[0]*5:
                                b.takeOffScreen()
                                b.moveToPos((0, 0))
                                health -= 1
                                updatescoreboard()
                    boss.setx(boss.xcor()+n)
                    if boss.xcor() > 300 or boss.xcor() < -300:
                        n = n*-1
                    if random.randint(0, 200) == 0 and ennum < len(enlist)-1:
                        ennum += 1
                        enlist[ennum].goto(boss.pos())
                    if random.randint(0, 50) == 0:
                        boss.spreadshoot()
                    for b in pbullets + hbullets + bbullets:
                        if b.onscreen:
                            if abs(b.ycor() - boss.ycor()) < 20:
                                if abs(b.xcor() - boss.xcor()) < boss.turtlesize()[0]*6:
                                    b.takeOffScreen()
                                    boss.takeDamage(b.damage)
                                    if random.randint(0, 1) == 0:
                                        points += 1
                                        updatescoreboard()
                                    if boss.health < 1 and fite:
                                        fite = False
                                        boss.hideturtle()
                                        for b in boss.bullets:
                                            b.takeOffScreen()
                                        boss.bossness += 1
                                        for e in enlist:
                                            e.level += 1
                                        for i in range(50):
                                            points += 1
                                            screen.update()
                                            updatescoreboard()
                                    else:
                                        continue
                except UnboundLocalError:
                    n = 1
            elif boss.isvisible() and kdistance == 20:
                try:
                    boss.forward(n)
                    boss.clear()
                    boss.moveBullets()
                    for b in boss.bullets:
                        if abs(b.ycor() - p.ycor()) < 20:
                            if abs(b.xcor() - p.xcor()) < p.turtlesize()[0]*5:
                                b.takeOffScreen()
                                b.moveToPos((0, 0))
                                health -= 1
                                updatescoreboard()
                    boss.setx(boss.xcor() + int(boss.spot > boss.xcor())*4-int(boss.spot < boss.xcor())*4)
                    if abs(boss.spot - boss.xcor()) < 10:
                        boss.dot(40)
                    if random.randint(0, 40) == 0 and abs(boss.spot - boss.xcor()) < 10:
                        if boss.health > 150:
                            if boss.lazershot(boss.pos(), -90):
                                health -= 2
                                updatescoreboard()
                        else:
                            if boss.lazershot(boss.pos(), -90) or boss.lazershot((boss.pos()[0]+100, boss.pos()[1]), -90) or boss.lazershot((boss.pos()[0]-100, boss.pos()[1]), -90):
                                health -= 2
                                updatescoreboard()
                        screen.update()
                        boss.spot = p.xcor()
                    for b in boss.bullets:
                            b.clear()
                    v = boss.bullets[1].pos()
                    boss.bullets[1].goto(boss.spot, -275)
                    boss.bullets[1].showturtle()
                    boss.bullets[1].dot(10, 'red')
                    boss.bullets[1].hideturtle()
                    boss.bullets[1].goto(v)
                    if boss.ycor() > 200 or boss.ycor() < 100:
                        n = n*-1
                    for b in pbullets + hbullets + bbullets:
                        if b.onscreen:
                            if abs(b.ycor() - boss.ycor()) < 20:
                                if abs(b.xcor() - boss.xcor()) < boss.turtlesize()[0]*60:
                                    b.takeOffScreen()
                                    boss.takeDamage(b.damage)
                                    if random.randint(0, 1) == 0:
                                        points += 1
                                        updatescoreboard()
                                    if boss.health < 1 and fite:
                                        fite = False
                                        boss.hideturtle()
                                        boss.clear()
                                        for b in boss.bullets:
                                            b.takeOffScreen()
                                        boss.bossness += 1
                                        for e in enlist:
                                            e.level += 1
                                        for i in range(50):
                                            points += 1
                                            screen.update()
                                            updatescoreboard()
                                    else:
                                        continue
                except UnboundLocalError:
                    n = 1

            elif boss.isvisible() and kdistance == 30:
                try:
                    boss.moveBullets()
                    for b in boss.bullets:
                        if abs(b.ycor() - p.ycor()) < 20:
                            if abs(b.xcor() - p.xcor()) < p.turtlesize()[0]*5:
                                b.takeOffScreen()
                                b.moveToPos((0, 0))
                                health -= 1
                                updatescoreboard()
                    x = 1 if boss.xcor() < p.xcor() else -1
                    boss.setx(boss.xcor()+(2*n)+x)
                    if random.randint(0, 20) == 0 or boss.xcor() > 300 or boss.xcor() < -300:
                        n = n*-1
                    if random.randint(0, 50) == 0 and ennum < len(enlist)-1:
                        ennum += 1
                        enlist[ennum].goto(boss.pos())
                        enlist[ennum].seth(random.randint(-120, -60))
                    if random.randint(0, 50) == 0:
                        boss.burst(boss.towards(p), 20, 20)
                        screen.update()
                    for b in boss.bullets:
                        b.clear()
                    for b in pbullets + hbullets + bbullets:
                        if b.onscreen:
                            if abs(b.ycor() - boss.ycor()) < 20:
                                if abs(b.xcor() - boss.xcor()) < boss.turtlesize()[0]*6:
                                    b.takeOffScreen()
                                    boss.takeDamage(b.damage)
                                    if random.randint(0, 1) == 0:
                                        points += 1
                                        updatescoreboard()
                                    if boss.health < 1 and fite:
                                        fite = False
                                        boss.hideturtle()
                                        for b in boss.bullets:
                                            b.takeOffScreen()
                                        boss.bossness += 1
                                        for e in enlist:
                                            e.level += 1
                                        for i in range(50):
                                            points += 1
                                            screen.update()
                                            updatescoreboard()
                                    else:
                                        continue
                except UnboundLocalError:
                    n = 1
                    print('shjfdk')

        if charge < maxcharge and distance % 20 == 0:
            charge += chargespeed
            updatecharge()

        if p.xcor() > 300:
            p.setx(-300)
        if p.xcor() < -300:
            p.setx(300)
        
        if random.randint(0, 100) == 100 and ennum < len(enlist) and not fite:
            ennum += 1

        for i in range(ennum):
            e = enlist[i]
            e.showturtle()
            e.move(p)
            if random.randint(0, 200) == 0:
                e.shoot()
            if enlist[i].ycor() < -300:
                e.resetstuff()
                enlist.remove(e)
                enlist.append(e)
                ennum -= 1

        for b in bullets:
            b.move()
            for i in range(len(elist))):#elist is the list of enemies
                e = enlist[i]
                if abs(b.ycor() - e.ycor()) < 20:
                    if abs(b.xcor() - e.xcor()) < e.turtlesize()[0]*6:
                        b.takeOffScreen()
                        e.takeDamage(b.damage)
                        if random.randint(0, 1) == 0:
                            points += b.damage
                            updatescoreboard()
                        if e.health <= 0:
                            e.resetstuff()
                            enlist.remove(e)
                            enlist.append(e)
                            ennum -= 1
                            if random.randint(0, 1) == 0:
                                health += 1
                                updatescoreboard()
                        else:
                            continue

        for e in enlist:
            for b in e.bullets:
                if abs(b.ycor() - p.ycor()) < 20:
                    if abs(b.xcor() - p.xcor()) < p.turtlesize()[0]*5:
                        b.takeOffScreen()
                        b.moveToPos((0, 0))
                        health -= 1
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
            break
