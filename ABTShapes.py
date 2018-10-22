from turtle import *
from tkinter import *
import random

#x = Turtle()
#x.hideturtle()
#y = x.getscreen()
#y.colormode(255)

def registerABTShapes(screen):
    i = RawTurtle(screen)
    i.hideturtle()
    i.pencolor(255, 0, 0)
    i.fillcolor(0, 0, 0)
    i.begin_poly()
    i.seth(-60)
    i.begin_fill()
    i.forward(5)
    i.left(60)
    i.forward(2)
    i.right(120)
    i.forward(2)
    i.left(60)
    i.forward(3)
    i.right(120)
    i.forward(10)
    i.right(120)
    i.forward(3)
    i.left(60)
    i.forward(2)
    i.right(120)
    i.forward(2)
    i.left(60)
    i.forward(5)
    i.right(120)
    i.end_fill()
    i.end_poly()
    fe = i.get_poly()
    i.clear()
    screen.register_shape('5enemy', fe)
    ###----------New shape----------###
    i.up() #This section was created to make hollow circles for explosions
    i.fillcolor(0, 255, 0)
    i.pensize(5)
    i.begin_poly()
    i.goto(0, 0)
    i.clear()
    i.seth(0)
    radius = 5
    i.right(90)
    i.forward(radius)
    i.down()
    i.left(90)
    i.end_poly()
    c = i.get_poly()
    i.begin_poly()
    i.begin_fill()
    i.circle(radius)
    i.right(90)
    i.end_fill()
    i.end_poly()
    c = i.get_poly()
    screen.register_shape('Circle', c)
    i.reset()#Reset clears all the data; This should be used more often to avoid scenarios where
    i.hideturtle()#the order that these shapes are created in matters. Make sure to add hideturtle after reset
    ###----------New shape----------###
    i.pencolor(255, 0, 0)
    i.fillcolor(0, 0, 0)
    i.begin_poly()
    i.seth(0)
    i.begin_fill()
    for t in range(180):
        i.forward(2)
        i.right(2)
    i.end_fill()
    i.sety(i.ycor() - 10)
    i.circle(5)
    i.sety(i.ycor() - 50)
    i.circle(20)
    i.sety(i.ycor() - 20)
    i.circle(5)
    i.up()
    i.setx(i.xcor()-50)
    i.down()
    i.seth(-90)
    i.begin_fill()
    i.forward(10)
    i.right(90)
    i.forward(10)
    i.right(90)
    i.forward(100)
    i.right(90)
    i.forward(10)
    i.right(90)
    i.forward(90)
    i.end_fill()
    i.up()
    i.setx(i.xcor()+100)
    i.down()
    i.seth(-90)
    i.begin_fill()
    i.forward(10)
    i.left(90)
    i.forward(10)
    i.left(90)
    i.forward(100)
    i.left(90)
    i.forward(10)
    i.left(90)
    i.forward(90)
    i.end_fill()
    i.setx(i.xcor()-50)
    i.end_poly()
    bt = i.get_poly()
    screen.register_shape('boss2', bt)
    i.clear()
    ###----------New shape----------###
    i.up()
    i.seth(0)
    i.goto(0, 0)
    i.down()
    i.begin_poly()
    i.left(90)
    i.forward(10)
    i.right(90)
    for j in range(90):
        i.forward(0.2)
        i.right(1)
    i.left(90)
    i.forward(40)
    i.right(90+45)
    i.forward(20*(2**(1/2)))
    i.right(90)
    i.forward(20*(2**(1/2)))
    i.left(90+45)
    for j in range(180):
        i.forward(0.2)
        i.right(1)
    i.left(90+45)
    i.forward(20*(2**(1/2)))
    i.right(90)
    i.forward(20*(2**(1/2)))
    i.right(90+45)
    i.forward(40)
    i.left(90)
    for j in range(90):
        i.forward(0.2)
        i.right(1)
    i.right(90)
    i.forward(10)
    i.left(90)
    i.end_poly()
    bt = i.get_poly()
    screen.register_shape('bat', bt)
    i.clear()

#registerABTShapes(y)
    
