import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math

def init():
    pygame.init()
    display = (1500, 800) # Proporção da criação de janela
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(300, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -20.0)  # Ajuste o valor negativo para afastar a cena

def draw_sphere(radius, slices, stacks):
    quadric = gluNewQuadric()
    gluSphere(quadric, radius, slices, stacks)
    gluDeleteQuadric(quadric)

def draw_orbit(radius): #Desenhar uma trajetória de órbita
    glBegin(GL_LINE_LOOP)
    for angle in range(0, 360, 10):
        x = radius * math.cos(math.radians(angle))
        y = radius * math.sin(math.radians(angle))
        glVertex2f(x, y)
    glEnd()

def draw_solar_system():
    # Sol
    glColor3f(1.0, 1.0, 0.0)
    draw_sphere(1.0, 50, 50)

    # Órbitas
    glColor3f(1.0, 1.0, 1.0)
    for orbit_radius in range(2, 18, 2): # quantida de órbitas
        draw_orbit(orbit_radius)

    # Planetas
    planets = [
        {"distance": 2.0, "radius": 0.1, "color": (0.66, 0.18, 0.13), "speed": 0.4},
        {"distance": 4.0, "radius": 0.2, "color": (0.81, 0.71, 0.4), "speed": 0.1},
        {"distance": 6.0, "radius": 0.2, "color": (0.1, 0.1, 0.85), "speed": 0.07},
        {"distance": 8.0, "radius": 0.15, "color": (0.8, 0.1, 0.1), "speed": 0.05},
        {"distance": 10.0, "radius": 0.4, "color": (1.0, 0.64, 0.0), "speed": 0.03},
        {"distance": 12.0, "radius": 0.3, "color": (0.5, 0.5, 0.5), "speed": 0.02},
        {"distance": 14.0, "radius": 0.3, "color": (1.0, 1.0, 1.0), "speed": 0.01},
        {"distance": 16.0, "radius": 0.28, "color": (0.0, 0.0, 1.0), "speed": 0.005},
    ]

    for planet in planets:
        distance = planet["distance"]
        radius = planet["radius"]
        color = planet["color"]
        speed = planet["speed"]

        glPushMatrix()
        glColor3f(*color)
        glRotatef(pygame.time.get_ticks() * speed % 360, 0, 0, 1)
        glTranslate(distance, 0, 0)
        draw_sphere(radius, 30, 30)
        glPopMatrix()

def handle_key_press():
    rotation_speed = 1.0

    keys = pygame.key.get_pressed()

    if keys[K_LEFT]:
        glRotatef(rotation_speed, 0, 1, 0)
    elif keys[K_RIGHT]:
        glRotatef(-rotation_speed, 0, 1, 0)
    if keys[K_UP]:
        glRotatef(rotation_speed, 1, 0, 0)
    elif keys[K_DOWN]:
        glRotatef(-rotation_speed, 1, 0, 0)

def main():
    init()
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        handle_key_press()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_solar_system()
        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    main()
