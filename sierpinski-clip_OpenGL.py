import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from shapely.geometry import Polygon

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

def clip_polygon(subject_polygon, clip_polygon):
    subject_poly = Polygon(subject_polygon)
    clip_poly = Polygon(clip_polygon)

    # Clip the subject polygon with the clip polygon
    clipped_result = subject_poly.intersection(clip_poly).exterior.coords[:-1]

    return clipped_result

def draw_cartesian_plane():
    glColor3f(0.5, 0.5, 0.5)  # Gray color for the axes
    glBegin(GL_LINES)
    glVertex2f(-300, 0)
    glVertex2f(300, 0)
    glVertex2f(0, -200)
    glVertex2f(0, 200)
    glEnd()

def initialize():
    glClearColor(1, 1, 1, 1)
    glOrtho(-300, 300, -200, 200, -1, 1)

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    draw_cartesian_plane()
    
    myPoints = [[-100, -50], [0, 100], [100, -50]]
    
    
    sierpinski(myPoints, 2)  # Set the recursion depth to 2

    # Clip the generated Sierpinski triangle to retain only the first original triangle
    clipped_result = clip_polygon(myPoints, [[-300, -200], [300, -200], [300, 200], [-300, 200]])
    
    # Draw the clipped result in blue
    drawTriangle(clipped_result, (0, 0, 255))
    

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
