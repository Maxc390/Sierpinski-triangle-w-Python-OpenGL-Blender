import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
glutInit() 

def drawTriangle(points, color):
    glColor3fv(color)
    glBegin(GL_TRIANGLES)
    glVertex2fv(points[0])
    glVertex2fv(points[1])
    glVertex2fv(points[2])
    glEnd()

def getMid(p1, p2):
    return ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)

def sierpinski(points, degree):
    colormap = [(0, 0, 255), (255, 0, 0), (0, 255, 0)]  # Blue, Red, Green
    drawTriangle(points, colormap[degree])
    if degree > 0:
        sierpinski([points[0], getMid(points[0], points[1]), getMid(points[0], points[2])], degree-1)
        sierpinski([points[1], getMid(points[0], points[1]), getMid(points[1], points[2])], degree-1)
        sierpinski([points[2], getMid(points[2], points[1]), getMid(points[0], points[2])], degree-1)

def draw_cartesian_plane():
    glColor3f(0.5, 0.5, 0.5)  # Gray color for the axes
    glBegin(GL_LINES)
    glVertex2f(-300, 0)
    glVertex2f(300, 0)
    glVertex2f(0, -200)
    glVertex2f(0, 200)
    glEnd()

    # Labeling the X-axis
    for i in range(-300, 301, 50):
        render_text(str(i), i, -10)

    # Labeling the Y-axis
    for i in range(-200, 201, 50):
        render_text(str(i), -20, i)

def initialize():
    glClearColor(1, 1, 1, 1)
    glOrtho(-300, 300, -200, 200, -1, 1)

def render_text(text, x, y):
    glRasterPos2f(x, y)
    for char in text:
        glutBitmapCharacter(GLUT_BITMAP_9_BY_15, ord(char))

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    draw_cartesian_plane()
    
    myPoints = [[-100, -50], [0, 100], [100, -50]]
    sierpinski(myPoints, 2)  # Set the recursion depth/degree to 2

    pygame.display.flip()

def main():
    pygame.init()
    display_size = (600, 400)
    pygame.display.set_mode(display_size, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Sierpinski Triangle")

    initialize()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        display()
        pygame.time.wait(500)  # Add a small delay to observe each frame

if __name__ == "__main__":
    main()
