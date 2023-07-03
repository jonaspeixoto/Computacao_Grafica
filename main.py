import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import random

def init():
    pygame.init()
    display = (1500, 800)  # Proporção da criação de janela
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(300, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -20.0)  # Ajuste o valor negativo para afastar a cena
    

def draw_sphere(radius, slices, stacks, texture_id=None):
    """
    The draw_sphere function draws a sphere in OpenGL.

    :param radius: Define the radius of the sphere
    :param slices: Define the number of subdivisions (similar to lines of longitude)
    :param stacks: Define how many slices the sphere will have
    :param texture_id : :param texture_id: Add a texture to the sphere
    :return: Nothing

    """
    quadric = gluNewQuadric()
    gluQuadricTexture(quadric, GL_TRUE)
    if texture_id is not None:
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, texture_id)
    gluSphere(quadric, radius, slices, stacks)
    gluDeleteQuadric(quadric)
    if texture_id is not None:
        glDisable(GL_TEXTURE_2D)


def draw_orbit(radius):  # Desenhar uma trajetória de órbita
    """
    The draw_orbit function draws a circle with the given radius.
    The function uses the GL_LINE_LOOP primitive to draw a series of connected line segments,
    where each segment is defined by two vertices. The first vertex is at (0, 0), and subsequent vertices are 
    calculated using trigonometry based on an angle that increases in increments of 10 degrees.
    
    :param radius: Determine the radius of the orbit
    :return: Nothing

    """
    glBegin(GL_LINE_LOOP)
    for angle in range(0, 360, 10):
        x = radius * math.cos(math.radians(angle))
        y = radius * math.sin(math.radians(angle))
        glVertex2f(x, y)
    glEnd()

def draw_solar_system():
    # Draw sun in position (0,0,0)
    glColor3f(1.0, 1.0, 0.0)
    sun_texture_id = load_texture("src\img\sun_texture_2.jpg")
    draw_sphere(1.0, 50, 50, sun_texture_id)
    

    # Draw orbit around position (0,0,0)
    glColor3f(1.0, 1.0, 1.0)
    for orbit_radius in range(2, 18, 2):  # quantida de órbitas
        draw_orbit(orbit_radius)

    # planets
    planets = [
        {"name": "Mercury", "distance": 2.0, "radius": 0.2, "color": (0.66, 0.18, 0.13), "speed": 0.2},
        {"name": "Venus", "distance": 4.0, "radius": 0.4, "color": (0.81, 0.71, 0.4), "speed": 0.05},
        {"name": "Earth", "distance": 6.0, "radius": 0.4, "color": (0.1, 0.1, 0.85), "speed": 0.03, "texture": "src\img\earth_texture.jpg"},
        {"name": "Mars", "distance": 8.0, "radius": 0.3, "color": (0.8, 0.1, 0.1), "speed": 0.025, "texture":"src\img\mars_texture_.jpg"},
        {"name": "Jupiter", "distance": 10.0, "radius": 0.8, "color": (1.0, 0.64, 0.0), "speed": 0.015},
        {"name": "Saturn", "distance": 12.0, "radius": 0.6, "color": (0.5, 0.5, 0.5), "speed": 0.01},
        {"name": "Uranus", "distance": 14.0, "radius": 0.6, "color": (1.0, 1.0, 1.0), "speed": 0.005},
        {"name": "Neptune", "distance": 16.0, "radius": 0.6, "color": (0.0, 0.0, 1.0), "speed": 0.0009},
    ]

    for planet in planets:
        distance = planet["distance"]
        radius = planet["radius"]
        color = planet["color"]
        speed = planet["speed"]
        # speed = 0


        texture_id = None
        try:
            texture_path = planet["texture"]
            texture_id = load_texture(texture_path)
        except KeyError:
            pass

        glPushMatrix()
        glColor3f(*color)
        glRotatef(pygame.time.get_ticks() * speed % 360, 0, 0, 1)
        glTranslate(distance, 0, 0)
        draw_sphere(radius, 30, 30,texture_id)
        glPopMatrix()

def draw_stars(stars):
    """
    The draw_stars function draws the stars in the space.
    
    :param stars: Pass in the list of stars to be drawn
    :return: Nothing
    """
    glColor3f(1.0, 1.0, 1.0)
    glPointSize(1.0)
    glBegin(GL_POINTS)
    for star in stars:
        glVertex3f(star[0], star[1], star[2])
    glEnd()

def generate_stars(num_stars):
    """
    The generate_stars function generates a list of random (x, y, z) coordinates for the stars.
    :param num_stars: Determine how many stars are generated
    :return: A list of tuples
    """
    stars = []
    for _ in range(num_stars):
        x = random.uniform(-20, 20)
        y = random.uniform(-20, 20)
        z = random.uniform(-20, 20)
        stars.append((x, y, z))
    return stars

def handle_key_press():
    """
    The handle_key_press function handles the key presses.
    :return: Nothing
    """
    rotation_speed = 1.0
    translation_speed = 0.1

    keys = pygame.key.get_pressed()

    if keys[K_LEFT]:
        glRotatef(rotation_speed, 0, 1, 0)
    elif keys[K_RIGHT]:
        glRotatef(-rotation_speed, 0, 1, 0)
    if keys[K_UP]:
        glRotatef(rotation_speed, 1, 0, 0)
    elif keys[K_DOWN]:
        glRotatef(-rotation_speed, 1, 0, 0)
    if keys[K_w]:
        glTranslatef(0, 0, translation_speed)
    elif keys[K_s]:
        glTranslatef(0, 0, -translation_speed)
    if keys[K_a]:
        glTranslatef(-translation_speed, 0, 0 )
    elif keys[K_d]:
         glTranslatef(translation_speed, 0, 0 )
    if keys[K_q]:
        glTranslatef(0,-translation_speed, 0)
    elif keys[K_e]:
         glTranslatef(0,translation_speed, 0)

def load_texture(texture_path):
    """
    The load_texture function takes a path to an image file and loads it into OpenGL.
    It returns the id of the texture object that was created.
    :param texture_path: Load the image from a file
    :return: A texture id
    """
    texture_surface = pygame.image.load(texture_path)
    texture_data = pygame.image.tostring(texture_surface, "RGB", 1)
    width = texture_surface.get_width()
    height = texture_surface.get_height()

    glEnable(GL_TEXTURE_2D)
    texid = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texid)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, texture_data)  # load data in opengl 
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR) # Filter image
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    return texid


def main():
    init()
    clock = pygame.time.Clock()

    num_stars = 1000
    stars = generate_stars(num_stars)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        handle_key_press()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_solar_system()
        draw_stars(stars)
        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    main()
