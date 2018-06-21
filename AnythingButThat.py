# Anything but That
# version 0.1
# we reached 1100 lines!
# yay!

from turtle import *
from tkinter import *
import random
from Highscore_tools import *
from math import *
import ABTShapes
from time import time
import os


class bullet(Turtle):
    def __init__(self, direction, pos, color = (255, 0, 0), sp = 1.5, damage = 1):
        Turtle.__init__(self)
        self.speed = sp
        self.onscreen = False
        self.damage = 0
        self.up()
        self.turtlesize(0.5, 0.5)
        self.goto(pos)
        self.color(color)
        self.direction = direction
        self.seth(self.direction)

    def addToScreen(self):
        self.onscreen = True
        self.seth(self.direction)
        self.showturtle()

    def takeOffScreen(self):
        self.onscreen = False
        self.speed = 1.5
        self.hideturtle()

    def move(self):
        self.forward(self.speed)
        if self.ycor() < -300 or self.ycor() > 300:
            self.takeOffScreen()
        if self.xcor() < -300 or self.xcor() > 300:
            self.takeOffScreen()

    def moveToPos(self, pos):
        self.goto(pos)

    def reset(self):
        self.direction = 90
        self.seth(self.direction)

class bomb(Turtle):
    def __init__(self, direction, pos, color = (255, 0, 0), radius=5, damage = 1):
        Turtle.__init__(self)
        self.onscreen = False
        self.speed = 1.4
        self.damage = 1
        self.radius = radius
        self.up()
        self.turtlesize(0.5, 0.5)
        self.goto(pos)
        self.color(color)
        self.seth(direction)
        self.hideturtle()
        self.exploder = Turtle()
        self.exploder.hideturtle()
        self.exploder.up()
        self.exploder.shape('circle')

    def addToScreen(self, radius):
        self.onscreen = True
        self.radius = radius
        self.showturtle()

    def takeOffScreen(self):
        self.onscreen = False
        self.speed = 1.5
        self.hideturtle()
        self.exploder.showturtle()
        self.exploder.goto(self.xcor(), self.ycor())
        self.exploder.pencolor((0, 255, 0))
        self.explode(1, self.exploder)

    def move(self):
        self.forward(self.speed)
        if self.ycor() < -300 or self.ycor() > 300:
            self.takeOffScreen()
        if self.xcor() < -300 or self.xcor() > 300:
            self.takeOffScreen()

    def moveToPos(self, pos):
        self.goto(pos)
    
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
            turtle.hideturtle()

class homingmissile(Turtle):
    def __init__(self, direction, pos, color = (255, 0, 0), sp = 1.5, damage = 1):
        Turtle.__init__(self)
        self.onscreen = False
        self.speed = sp
        self.damage = damage
        self.up()
        self.turtlesize(0.5, 0.5)
        self.goto(pos)
        self.color(color)
        self.seth(direction)
        self.hideturtle()

    def addToScreen(self):
        self.onscreen = True
        self.showturtle()

    def takeOffScreen(self):
        self.onscreen = False
        self.speed = 1.5
        self.hideturtle()

    def move(self):
        global enlist
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
        if self.ycor() < -300 or self.ycor() > 300:
            self.takeOffScreen()
        if self.xcor() < -300 or self.xcor() > 300:
            self.takeOffScreen()

    def moveToPos(self, pos):
        self.goto(pos)


       
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

def lazorgo():
    global screen, enlist, ennum, points, health, fite, boss
    hitlist = []
    for b in pbullets:
        if not b.onscreen:
            b.moveToPos(p.pos())
            b.seth(90)
            b.damage = 1
            b.down()
            b.speed = 1.5
            b.width(3)
            b.write("blap", font = ("Comic Sans MS", 20, "normal"))
            for i in range(150):
                b.forward(5)
                for i in range(ennum):
                    e = enlist[i]
                    if abs(b.ycor() - e.ycor()) < 20 and e not in hitlist:
                        if abs(b.xcor() - e.xcor()) < e.turtlesize()[0]*6:
                            e.takeDamage()
                            hitlist.append(e)
                            if random.randint(0, 1) == 0:
                                points += 1
                                updatescoreboard()
                            if e.health == 0:
                                e.resetstuff()
                                enlist.remove(e)
                                enlist.append(e)
                                ennum -= 1
                                if random.randint(0, 1) == 0:
                                    health += 1
                                    updatescoreboard()
                if fite:
                    if abs(b.ycor() - boss.ycor()) < 20 and boss not in hitlist:
                        if abs(b.xcor() - boss.xcor()) < boss.turtlesize()[0]*6:
                            boss.takeDamage(1)
                            hitlist.append(boss)
                            if random.randint(0, 1) == 0:
                                points += 1
                                updatescoreboard()
                            if boss.health == 0:
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
            b.up()
            screen.update()
            b.clear()
            b.width(1)
            return

def fireBullet():
    global weapon, charge, screen, enlist, ennum
    num = 0
    if weapons[weapon] == 'blaster':
        for b in pbullets:
            if not b.onscreen:
                b.damage = 1
                b.speed = 1.5
                b.moveToPos(p.pos())
                b.reset()
                b.addToScreen()
                return
    elif weapons[weapon] == 'spreadshot' and charge >= 2:
        charge -= 2
        for b in pbullets:
            if not b.onscreen:
                b.damage = 1
                b.speed = 1.5
                b.moveToPos(p.pos())
                b.direction = random.randint(80, 100)
                b.addToScreen()
                num += 1
                if num == 3:
                    return
    elif weapons[weapon] == 'lazor' and charge >= 3:
        charge -= 3
        lazorgo()
    elif weapons[weapon] == 'blaster 2.0' and charge >= 3:
        for b in pbullets:
            if not b.onscreen:
                charge -= 2
                b.damage = 2
                b.speed = 1
                b.moveToPos(p.pos())
                b.reset()
                b.addToScreen()
                return
    elif weapons[weapon] == 'homingmissile' and charge >= 2:
        for h in hbullets:
            if not h.onscreen:
                charge -= 2
                h.moveToPos(p.pos())
                h.seth(90)
                h.addToScreen()
                return
    elif weapons[weapon] == 'bombs' and charge >= 3:####
        charge -= 0
        radius = 40
        for b in bbullets:
            if not b.onscreen:
                b.moveToPos(p.pos())
                b.seth(90)
                b.addToScreen(min(radius, 100))
                return
##        global firing
##        #global startofbullet
##        charge -= 0
##        if firing:
##            firing = False
##            radius = 10#int(startofbullet-time())*10
##            for b in bbullets:
##                if not b.onscreen:
##                    b.moveToPos(p.pos())
##                    b.seth(90)
##                    b.addToScreen(100-(abs(-100+radius)/2-(-100+radius)/2))
##                    return
##        if not firing:
##            startofbullet = time()
##            firing = True
##            return
    elif weapons[weapon] == 'pentashot' and charge >= 3:
        charge -= 3
        for b in pbullets:
            if not b.onscreen:
                b.moveToPos(p.pos())
                b.damage = 1
                b.speed = 2.5
                x = 40
                b.direction = 90 + (2 - num)*x
                b.seth(90 + (2 - num)*x)
                num += 1
                if num == 6:
                    return
                b.addToScreen()
    elif weapons[weapon] == "machine gun" and charge >= 4:
        charge -= 4
        for b in pbullets:
            if not b.onscreen:
                b.moveToPos(p.pos())
                b.damage = 1
                b.speed = 2
                b.direction = random.randint(70,110)
                b.seth(b.direction)
                num += 1
                b.addToScreen()
                if num == 7:
                    return
                

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

def stop():
    global stopped
    stopped = True

def chargeboost():
    global maxcharge, points
    if points >= 5:
        points -= 5
        maxcharge += 2
        updatescoreboard()

def healthboost():
    global health, points
    if points >= 10:
        points -= 10
        health += 1
        updatescoreboard()

def csboost():
    global chargespeed, points
    if points >= 10:
        points -= 10
        chargespeed += 0.2
        updatescoreboard()

def buypentashot(label):
    global points, weapons, pbullets
    if points >= 40 and 'pentashot' not in weapons and 'spreadshot' in weapons:
        points -= 40
        weapons.append('pentashot')
        for i in range(10):
            b = bullet(90,p.pos(), (0, 255, 0))
            pbullets.append(b)
        updatescoreboard()
        label.forget()
        
def buyminigun(label):
    global points, weapons, pbullets
    if points >= 40 and 'machine gun' not in weapons and 'spreadshot' in weapons:
        points -= 40
        weapons.append('machine gun')
        for i in range(10):
            b = bullet(90,p.pos(), (0, 255, 0))
            pbullets.append(b)
        updatescoreboard()
        label.forget()

def buymachenegun(label):
    global points, weapons, pbullets
    if points >= 20 and 'spreadshot' not in weapons:
        points -= 20
        weapons.append('spreadshot')
        for i in range(5):
            b = bullet(90, p.pos(), (0, 255, 0))
            pbullets.append(b)
        updatescoreboard()
        label.forget()

def buylazergun(label):
    global points, weapons, pbullets
    if points >= 30 and 'lazor' not in weapons:
        points -= 30
        weapons.append('lazor')
        for i in range(5):
            b = bullet(90, p.pos(), (0, 255, 0))
            pbullets.append(b)
        updatescoreboard()
        label.forget()

def buyblaster2gun(label):
    global points, weapons, pbullets
    if points >= 30 and 'blaster 2.0' not in weapons:
        points -= 30
        weapons.append('blaster 2.0')
        for i in range(5):
            b = bullet(90, p.pos(), (0, 255, 0))
            pbullets.append(b)
        updatescoreboard()
        label.forget()

def buyhomingmissile(label):
    global points, weapons, pbullets
    if points >= 60 and 'homingmissile' not in weapons:
        points -= 60
        weapons.append('homingmissile')
        for i in range(5):
            b = bullet(90, p.pos(), (0, 255, 0))
            pbullets.append(b)
        updatescoreboard()
        label.forget()

def buybombs(label):
    global points, weapons, pbullets
    if points >= 40 and 'bombs' not in weapons:
        points -= 40
        weapons.append('bombs')
        for i in range(5):
            b = bullet(90, p.pos(), (0, 255, 0))
            pbullets.append(b)
        updatescoreboard()
        label.forget()
        for i in range(15):
            b = bomb(90, p.pos(), (0, 255, 0))
            bbullets.append(b)

def changeweapon():
    global weapon, weapons
    weapon = (weapon + 1) % len(weapons)
    if len(weapons) != 1:
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

    chargeb = Button(root, text = 'max charge + 2 [self explanatory] (5 pts)', command = chargeboost)
    chargeb.pack()
    if 'spreadshot' not in weapons:
        macheneg = Button(root, text = 'spreadshot [sprays three bullets for 2 charge] (20 pts)', command = lambda: buymachenegun(macheneg))
        macheneg.pack()
    if 'lazor' not in weapons:
        lazerg = Button(root, text = 'lazor [instant, peircing ray for 3 charge] (30 pts)', command = lambda: buylazergun(lazerg))
        lazerg.pack()
    if 'blaster 2.0' not in weapons:
        bl2 = Button(root, text = 'blaster 2.0 [slow bullet that deals 2 damage for 3 charge] (30 pts)', command = lambda: buyblaster2gun(bl2))
        bl2.pack()
    if 'spreadshot' in weapons and 'pentashot' not in weapons:
        pentashotg = Button(root, text = 'pentashot [shoots 5 bullets for 3 charge], (40 pts)', command = lambda: buypentashot(pentashotg))
        pentashotg.pack()
    if 'spreadshot' in weapons and 'machine gun' not in weapons:
        gung = Button(root, text = 'machine gun [shoots 7 bullets for 4 charge], (40 pts)', command = lambda: buyminigun(gung))
        gung.pack()
    if 'homingmissile' not in weapons:
        homingmissileg = Button(root, text = 'homingmissile [its OBFISHMUS what this does] (60 pts)', command = lambda: buyhomingmissile(homingmissileg))
        homingmissileg.pack()
    if 'bombs' not in weapons:###D0ne
        bombsg = Button(root, text = 'bombs [its OBFISHMUS what this does] (40 pts)', command = lambda: buybombs(bombsg))
        bombsg.pack()
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
        score = Label(scoreboard, text = 'points: ' + str(points), font = ('Monaco', 16))
        score.pack()
        hitpoints = Label(scoreboard, text = 'health: ' + str(health), font = ('Monaco', 16))
        hitpoints.pack()
        weaponl = Label(scoreboard, text = 'weapon: ' + str(weapons[weapon]), font = ('Monaco', 16))
        weaponl.pack()
        battery = Label(scoreboard, text = 'charge: ' + str(int(round(charge))), font = ('Monaco', 16))
        battery.pack()
    except TclError:
        scoreboard = Tk()
        score = Label(scoreboard, text = 'points: ' + str(points), font = ('Monaco', 16))
        score.pack()
        hitpoints = Label(scoreboard, text = 'health: ' + str(health), font = ('Monaco', 16))
        hitpoints.pack()
        weaponl = Label(scoreboard, text = 'weapon: ' + str(weapons[weapon]), font = ('Monaco', 16))
        weaponl.pack()
        battery = Label(scoreboard, text = 'charge: ' + str(int(round(charge))), font = ('Monaco', 16))
        battery.pack()

def updatecharge():
    global scoreboard, battery
    try:
        battery.forget()
        battery = Label(scoreboard, text = 'charge: ' + str(str(int(round(charge)))), font = ('Monaco', 16))
        battery.pack()
    except TclError:
        scoreboard = Tk()
        score = Label(scoreboard, text = 'points: ' + str(points), font = ('Monaco', 16))
        score.pack()
        hitpoints = Label(scoreboard, text = 'health: ' + str(health), font = ('Monaco', 16))
        hitpoints.pack()
        weaponl = Label(scoreboard, text = 'weapon: ' + str(weapons[weapon]), font = ('Monaco', 16))
        weaponl.pack()
        battery = Label(scoreboard, text = 'charge: ' + str(int(round(charge))), font = ('Monaco', 16))
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
        loop()
    
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
                g = False
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

        for b in pbullets + hbullets + bbullets:
            if b.onscreen:
                b.move()
                for i in range(ennum):
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

color = (0, 255, 0)

p = Turtle()
screen = p.getscreen()
screen.colormode(255)
screen.tracer(0)
canvas = screen.getcanvas()
ABTShapes.registerABTShapes(screen)
screen.bgcolor(0, 0, 0)
p.turtlesize(3, 4, 2)
p.up()
p.left(90)
p.back(275)
p.pencolor(color)

mov = 0
enlist = []
pbullets = []
hbullets = []
bbullets = []
ennum = 0
n = 1
health = 20## 20
distance = 0## 0
kdistance = 20## 0
fite = False
points = 500## 0
stopped = False
started = False
firing = False
scoreboard = Tk()
root = 0
charge = 0## 0
chargespeed = 1
maxcharge = 50## 5
weapons = ['blaster']
weapon = 0
boss = boss()
boss.bossness = 2## 0
boss.hideturtle()
g = False
startofbullet = 0

screen.listen()
screen.onkeypress(movel, "Left")
screen.onkey(stopmovel, "Left")
screen.onkeypress(mover, "Right")
screen.onkey(stopmover, "Right")
screen.onkey(changeweapon, "w")
screen.onkey(changeweapon, "W")
screen.onkeypress(fireBullet, "space")
screen.title('Anything but That')
os.system('xset r off')

score = Label(scoreboard, text = 'points: ' + str(points), font = ('Monaco', 16))
score.pack()
hitpoints = Label(scoreboard, text = 'health: ' + str(health), font = ('Monaco', 16))
hitpoints.pack()
battery = Label(scoreboard, text = 'charge: ' + str(charge), font = ('Monaco', 16))
battery.pack()
weaponl = Label(scoreboard, text = 'weapon: ' + str(weapons[weapon]), font = ('Monaco', 16))
weaponl.pack()
   
for i in range(5):
    for l in range(1, 5):
        e = enemy(l)
        enlist.append(e)

for i in range(10):
    b = homingmissile(90, p.pos(), (0, 255, 0))
    hbullets.append(b)

for i in range(20):
    b = bullet(90, p.pos(), (0, 255, 0))
    pbullets.append(b)
    
start_tutorial()
