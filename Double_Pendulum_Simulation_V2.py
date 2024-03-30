# Double Pendulum Simulation Version 2

import pygame
import math

pygame.init()

# Display
wn = pygame.display.set_mode((800, 700))
pygame.display.set_caption("Double Pendulum Simulation V2")

clock = pygame.time.Clock()

# Variables
m1 = 25
m2 = 10
r1 = 100
r2 = 150
a1 = math.pi / 2
a2 = math.pi / 2
a1_v = 0
a2_v = 0
a1_a = 0
a2_a = 0
g = 1
x1 = r1 * math.sin(a1)
y1 = -r1 * math.cos(a1) + 100
x2 = x1 + r2 * math.sin(a2)
y2 = y1 - r2 * math.cos(a2)
y1 *= -1
y2 *= -1

x1 += 500
x2 += 500
y1 += 300
y2 += 300

in_x1 = x1
in_y1 = y1
in_x2 = x2
in_y2 = y2

lines = []
last_pos2 = (0, 0)
new_pos2 = (0, 0)

# Button Variables
pace = 0
string_1 = 100
string_2 = 100
bob_1 = 100
bob_2 = 100
play = False
rest = False
wait = 0


# Background Lines
class Line(object):
    def __init__(self, start_x, start_y, end_x, end_y):
        self.x1 = start_x
        self.y1 = start_y
        self.x2 = end_x
        self.y2 = end_y

    def draw(self):
        pygame.draw.line(wn, (0, 0, 0), (self.x1, self.y1), (self.x2, self.y2))


def main_simulation():
    global x1, y1, x2, y2, r1, r2, a1, a2, a1_v, a2_v, a1_a, a2_a, m1, m2
    global pace, string_1, string_2, bob_1, bob_2, play, rest, wait
    run = True
    while run:
        if pace == 0:
            clock.tick(24)
        elif pace == 1:
            clock.tick(48)
        elif pace == 2:
            clock.tick(96)
        elif pace == -1:
            clock.tick(12)
        elif pace == -2:
            clock.tick(6)
        pygame.display.update()
        wn.fill((255, 255, 255))
        pygame.draw.rect(wn, (160, 160, 160), (0, 0, 200, 700))
        pygame.draw.rect(wn, (100, 100, 100), (200, 0, 600, 700), 8)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            pos = (0, 0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

            # Speed
            if 20 < pos[0] < 35 and 40 < pos[1] < 55:
                pace = -2
            elif 55 < pos[0] < 70 and 40 < pos[1] < 55:
                pace = -1
            elif 90 < pos[0] < 105 and 40 < pos[1] < 55:
                pace = 0
            elif 125 < pos[0] < 140 and 40 < pos[1] < 55:
                pace = 1
            elif 160 < pos[0] < 175 and 40 < pos[1] < 55:
                pace = 2

            # String 1
            elif 110 < pos[1] < 140 and 20 < pos[0] < 175:
                string_1 = pos[0]

            # String 2
            elif 175 < pos[1] < 205 and 20 < pos[0] < 175:
                string_2 = pos[0]

            # Mass 1
            elif 240 < pos[1] < 270 and 20 < pos[0] < 175:
                bob_1 = pos[0]

            # Mass 2
            elif 305 < pos[1] < 335 and 20 < pos[0] < 175:
                bob_2 = pos[0]

            elif 120 < pos[0] < 135 and 352 < pos[1] < 367:
                if play:
                    play = False
                else:
                    play = True

            elif 120 < pos[0] < 135 and 382 < pos[1] < 397:
                rest = True
                wait = 10
                reset()
                reset()

        if play:
            move_pendulum()
            calculate_next_move()
        background()

        pygame.draw.circle(wn, (0, 0, 0), (round(x1), round(y1)), round(m1))
        pygame.draw.circle(wn, (0, 0, 0), (round(x2), round(y2)), round(m2))
        pygame.draw.line(wn, (0, 0, 0), (round(x1), round(y1)), (round(x2), round(y2)), 3)
        pygame.draw.line(wn, (0, 0, 0), (round(x1), round(y1)), (500, 200), 3)

        speed()
        length_1()
        length_2()
        mass_1()
        mass_2()

        # Play
        font = pygame.font.SysFont("ariel", 30)
        restart = font.render("Play", 1, (0, 0, 0))
        wn.blit(restart, (60 - restart.get_width() // 2, 350))
        pygame.draw.rect(wn, (200, 200, 200), (120, 352, 15, 15))
        if play:
            pygame.draw.rect(wn, (100, 100, 100), (121, 353, 13, 13))

        # Reset
        label1 = font.render("Reset", 1, (0, 0, 0))
        wn.blit(label1, (60 - label1.get_width() // 2, 380))
        pygame.draw.rect(wn, (200, 200, 200), (120, 382, 15, 15))
        if rest:
            pygame.draw.rect(wn, (100, 100, 100), (121, 383, 13, 13))
            wait -= 1
            if wait == 0:
                rest = False


def move_pendulum():
    global x1, x2, y1, y2, r1, r2, a1, a2, a1_v, a2_v, a1_a, a2_a, new_pos2, last_pos2

    last_pos2 = (x2, y2)
    x1 = r1 * math.sin(a1)
    y1 = -r1 * math.cos(a1) + 100
    x2 = x1 + r2 * math.sin(a2)
    y2 = y1 - r2 * math.cos(a2)

    y1 *= -1
    y2 *= -1

    x1 += 500
    x2 += 500
    y1 += 300
    y2 += 300

    new_pos2 = (x2, y2)

    a1_v += a1_a
    a2_v += a2_a
    a1 += a1_v
    a2 += a2_v

    return x1, y1, x2, y2


def calculate_next_move():
    global r1, r2, a1, a2, a1_v, a2_v, a1_a, a2_a, g, m1, m2

    num1_1 = float(-g * (2 * m1 + m2) * math.sin(a1))
    num1_2 = float(-m2 * g * math.sin(a1 - 2 * a2))
    num1_3 = float(-2 * math.sin(a1 - a2) * m2)
    num1_4 = float(a2_v * a2_v * r2 + a1_v * a1_v * r1 * math.cos(a1 - a2))
    den1 = float(r1 * (2 * m1 + m2 - m2 * math.cos(2 * a1 - 2 * a2)))

    num2_1 = float(2 * math.sin(a1 - a2))
    num2_2 = float(a1_v * a1_v * r1 * (m1 + m2))
    num2_3 = float(g * (m1 + m2) * math.cos(a1))
    num2_4 = float(a2_v * a2_v * r2 * m2 * math.cos(a1 - a2))
    den2 = float(r2 * (2 * m1 + m2 - m2 * math.cos(2 * a1 - 2 * a2)))

    a1_a = (num1_1 + num1_2 + num1_3 * num1_4) / den1
    a2_a = (num2_1 * (num2_2 + num2_3 + num2_4)) / den2


def background():
    global new_pos2, last_pos2
    if last_pos2[0] != 1:
        lines.append(Line(round(new_pos2[0]), round(new_pos2[1]), round(last_pos2[0]), round(last_pos2[1])))
    for line in lines:
        line.draw()


def speed():
    global pace
    font = pygame.font.SysFont("ariel", 30)
    font1 = pygame.font.SysFont("ariel", 20)
    label = font.render("Speed", 1, (0, 0, 0))
    wn.blit(label, (100 - label.get_width() // 2, 20 - label.get_height() // 2))
    label1 = font1.render("x1/4", 1, (40, 40, 40))
    wn.blit(label1, (27 - label1.get_width() // 2, 57))
    label2 = font1.render("x1/2", 1, (40, 40, 40))
    wn.blit(label2, (62 - label2.get_width() // 2, 57))
    label3 = font1.render("x1", 1, (40, 40, 40))
    wn.blit(label3, (97 - label3.get_width() // 2, 57))
    label4 = font1.render("x2", 1, (40, 40, 40))
    wn.blit(label4, (132 - label4.get_width() // 2, 57))
    label5 = font1.render("x4", 1, (40, 40, 40))
    wn.blit(label5, (167 - label5.get_width() // 2, 57))
    pygame.draw.rect(wn, (200, 200, 200), (20, 40, 15, 15))
    pygame.draw.rect(wn, (200, 200, 200), (55, 40, 15, 15))
    pygame.draw.rect(wn, (200, 200, 200), (90, 40, 15, 15))
    pygame.draw.rect(wn, (200, 200, 200), (125, 40, 15, 15))
    pygame.draw.rect(wn, (200, 200, 200), (160, 40, 15, 15))

    if pace == -2:
        pygame.draw.rect(wn, (100, 100, 100), (21, 41, 13, 13))
    elif pace == -1:
        pygame.draw.rect(wn, (100, 100, 100), (56, 41, 13, 13))
    elif pace == 0:
        pygame.draw.rect(wn, (100, 100, 100), (91, 41, 13, 13))
    elif pace == 1:
        pygame.draw.rect(wn, (100, 100, 100), (126, 41, 13, 13))
    elif pace == 2:
        pygame.draw.rect(wn, (100, 100, 100), (161, 41, 13, 13))


def length_1():
    global string_1, r1
    pygame.draw.rect(wn, (100, 100, 100), (20, 120, 155, 10))
    pygame.draw.rect(wn, (200, 200, 200), (string_1 - 8, 110, 16, 30))
    font = pygame.font.SysFont("ariel", 30)
    label = font.render("String 1", 1, (0, 0, 0))
    wn.blit(label, (100 - label.get_width() // 2, 95 - label.get_height() // 2))
    r1 = string_1


def length_2():
    global string_2, r2
    pygame.draw.rect(wn, (100, 100, 100), (20, 185, 155, 10))
    pygame.draw.rect(wn, (200, 200, 200), (string_2 - 8, 175, 16, 30))
    font = pygame.font.SysFont("ariel", 30)
    label = font.render("String 2", 1, (0, 0, 0))
    wn.blit(label, (100 - label.get_width() // 2, 160 - label.get_height() // 2))
    r2 = 1.5 * string_2


def mass_1():
    global bob_1, m1
    pygame.draw.rect(wn, (100, 100, 100), (20, 250, 155, 10))
    pygame.draw.rect(wn, (200, 200, 200), (bob_1 - 8, 240, 16, 30))
    font = pygame.font.SysFont("ariel", 30)
    label = font.render("Mass 1", 1, (0, 0, 0))
    wn.blit(label, (100 - label.get_width() // 2, 225 - label.get_height() // 2))
    m1 = 0.15 * bob_1 + 7


def mass_2():
    global bob_2, m2
    pygame.draw.rect(wn, (100, 100, 100), (20, 315, 155, 10))
    pygame.draw.rect(wn, (200, 200, 200), (bob_2 - 8, 305, 16, 30))
    font = pygame.font.SysFont("ariel", 30)
    label = font.render("Mass 2", 1, (0, 0, 0))
    wn.blit(label, (100 - label.get_width() // 2, 290 - label.get_height() // 2))
    m2 = 0.15 * bob_2 + 7


def reset():
    global play, x1, x2, y1, y2, in_x1, in_x2, in_y1, in_y2
    global r1, r2, a1, a2, a1_v, a2_v, a1_a, a2_a, m1, m2, g
    x1 = in_x1
    x2 = in_x2
    y1 = in_y1
    y2 = in_y2
    m1 = 25
    m2 = 10
    r1 = 100
    r2 = 150
    a1 = math.pi / 2
    a2 = math.pi / 2
    a1_v = 0
    a2_v = 0
    a1_a = 0
    a2_a = 0
    g = 1
    play = False
    for line in lines:
        lines.pop(lines.index(line))
    for line in lines:
        lines.pop(lines.index(line))
    for line in lines:
        lines.pop(lines.index(line))
    for line in lines:
        lines.pop(lines.index(line))


main_simulation()
