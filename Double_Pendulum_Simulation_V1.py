#Double Pendulum Simulation V1
import turtle
import math
import time

#Screen
wn = turtle.Screen()
wn.title("Double Pendulum Simulation V1")
wn.setup(width=600, height=700)
wn.bgcolor("white")
wn.tracer(0)

#Constants
m1 = 20
m2 = 15
r1 = 50
r2 = 100
a1 = (math.pi)/1.3
a2 = (math.pi)/4
a1_v = 0
a2_v = 0
a1_a = 0
a2_a = 0
g = 1

#Pendulum Bobs
p1 = turtle.Turtle()
p1.speed(0)
p1.penup()
p1.color("black")
p1.shape("circle")
p1.shapesize(stretch_wid=(m1/10), stretch_len=(m1/10))

p2 = turtle.Turtle()
p2.speed(0)
p2.penup()
p2.color("black")
p2.shape("circle")
p2.shapesize(stretch_wid=(m2/10), stretch_len=(m2/10))

#Pendulum Strings
s1 = turtle.Turtle()
s1.speed(0)
s1.color("black")
s1.hideturtle()
s1.penup()
s1.pensize(2)

s2 = turtle.Turtle()
s2.speed(0)
s2.color("black")
s2.hideturtle()
s2.penup()
s2.pensize(2)

def s1_draw():
    s1.clear()
    s1.penup()
    s1.goto(0,100)
    s1.pendown()
    s1.goto(x1,y1)

def s2_draw():
    s2.clear()
    s2.penup()
    s2.goto(x1,y1)
    s2.pendown()
    s2.goto(x2,y2)


#Main Loop
while True:
    wn.update()
    time.sleep(0.015)
    
    x1 = r1*math.sin(a1)
    y1 = -r1*math.cos(a1) + 100
    x2 = x1 + r2*math.sin(a2)
    y2 = y1 - r2*math.cos(a2)

    p1.goto(x1,y1)
    p2.goto(x2,y2)

    p2.pensize(1)
    p2.pendown()

    s1_draw()
    s2_draw()
    
    a1_v += a1_a
    a2_v += a2_a
    a1 += a1_v
    a2 += a2_v

    num1_1 = float(-g*(2*m1 + m2)*math.sin(a1))
    num1_2 = float(-m2*g*math.sin(a1 - 2*a2))
    num1_3 = float(-2*math.sin(a1-a2)*m2)
    num1_4 = float(a2_v*a2_v*r2+a1_v*a1_v*r1*math.cos(a1-a2))
    den1 = float(r1*(2*m1+m2-m2*math.cos(2*a1-2*a2)))

    num2_1 = float(2*math.sin(a1-a2))
    num2_2 = float(a1_v*a1_v*r1*(m1+m2))
    num2_3 = float(g*(m1+m2)*math.cos(a1))
    num2_4 = float(a2_v*a2_v*r2*m2*math.cos(a1-a2))
    den2 = float(r2*(2*m1+m2-m2*math.cos(2*a1-2*a2)))

    a1_a = (num1_1+num1_2+num1_3*num1_4)/den1
    a2_a = (num2_1*(num2_2+num2_3+num2_4))/den2






    

