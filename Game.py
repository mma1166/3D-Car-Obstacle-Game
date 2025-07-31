from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
import numpy as np
import random
import time
import math

cheat_mode = False
target_bg_colour = [0.4, 0.7, 1.0]
score = 0
angle = 0.0
camera_radius = 4.0
camera_height = 2.0
width, height = 800, 600
car_x = 0.0
car_z = 0.0
car_speed = 0.0
drift_speed = 0.0
bg_colour = [0.4, 0.7, 1.0]
road_left = -4.0
road_right = 4.0
rain = False
trees = []
for _ in range(20):
    trees.append([random.uniform(-8, 8), random.uniform(5, 40)])

game_over = False
paused = False
obstacle_cars1 = []

last_generation_time_1 = time.time()
camera_mode = "third_person"


def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1, 1, 1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()

    gluOrtho2D(0, 1000, 0, 800)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glRasterPos2f(x, y)

    for ch in text:
        glutBitmapCharacter(font, ord(ch))

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)


def draw_cube():
    glBegin(GL_QUADS)

    # Front face
    glVertex3f(-0.5, -0.5,  0.5)
    glVertex3f( 0.5, -0.5,  0.5)
    glVertex3f( 0.5,  0.5,  0.5)
    glVertex3f(-0.5,  0.5,  0.5)

    # Back face
    glVertex3f(-0.5, -0.5, -0.5)
    glVertex3f(-0.5,  0.5, -0.5)
    glVertex3f( 0.5,  0.5, -0.5)
    glVertex3f( 0.5, -0.5, -0.5)

    # Top face
    glVertex3f(-0.5,  0.5, -0.5)
    glVertex3f(-0.5,  0.5,  0.5)
    glVertex3f( 0.5,  0.5,  0.5)
    glVertex3f( 0.5,  0.5, -0.5)

    # Bottom face
    glVertex3f(-0.5, -0.5, -0.5)
    glVertex3f( 0.5, -0.5, -0.5)
    glVertex3f( 0.5, -0.5,  0.5)
    glVertex3f(-0.5, -0.5,  0.5)

    # Right face
    glVertex3f( 0.5, -0.5, -0.5)
    glVertex3f( 0.5,  0.5, -0.5)
    glVertex3f( 0.5,  0.5,  0.5)
    glVertex3f( 0.5, -0.5,  0.5)

    # Left face
    glVertex3f(-0.5, -0.5, -0.5)
    glVertex3f(-0.5, -0.5,  0.5)
    glVertex3f(-0.5,  0.5,  0.5)
    glVertex3f(-0.5,  0.5, -0.5)

    glEnd()

def draw_sky():
    global bg_colour
    glPushMatrix()
    glColor3f(*bg_colour)

    radius = 15.0
    slices = 16
    stacks = 16
    for i in range(slices):
        lat0 = np.pi * (-0.5 + float(i) / slices)
        lat1 = np.pi * (-0.5 + float(i + 1) / slices)
        for j in range(stacks):
            lon0 = 2 * np.pi * float(j) / stacks
            lon1 = 2 * np.pi * float(j + 1) / stacks

            x0 = radius * np.cos(lat0) * np.cos(lon0)
            y0 = radius * np.sin(lat0)
            z0 = radius * np.cos(lat0) * np.sin(lon0)

            x1 = radius * np.cos(lat1) * np.cos(lon0)
            y1 = radius * np.sin(lat1)
            z1 = radius * np.cos(lat1) * np.sin(lon0)

            x2 = radius * np.cos(lat1) * np.cos(lon1)
            y2 = radius * np.sin(lat1)
            z2 = radius * np.cos(lat1) * np.sin(lon1)

            x3 = radius * np.cos(lat0) * np.cos(lon1)
            y3 = radius * np.sin(lat0)
            z3 = radius * np.cos(lat0) * np.sin(lon1)

            # Now drawing the triangles
            glBegin(GL_TRIANGLES)
            glVertex3f(x0, y0, z0)
            glVertex3f(x1, y1, z1)
            glVertex3f(x2, y2, z2)
            glEnd()

            glBegin(GL_TRIANGLES)
            glVertex3f(x0, y0, z0)
            glVertex3f(x2, y2, z2)
            glVertex3f(x3, y3, z3)
            glEnd()

    glPopMatrix()



def draw_road():
    glPushMatrix()
    scale_factor = max(0.1, (camera_radius / 2.0))
    road_width = scale_factor + 1.2
    glColor3f(0.5, 0.5, 0.5)
    glTranslatef(0.0, -0.5, 0.0)
    glScalef(road_width, 0.1, 12.5)
    draw_cube()
    glPopMatrix()


def draw_field():
    glPushMatrix()
    glColor3f(0.2, 0.8, 0.2)
    glTranslatef(0.0, -2.0, 0.0)
    glScalef(20.0, 0.0, 25.0)
    draw_cube()
    glPopMatrix()


def draw_hemisphere(radius=0.3, slices=32, stacks=16):
    for i in range(stacks):
        lat0 = math.pi * (i / stacks) / 2  # From 0 to π/2
        lat1 = math.pi * ((i + 1) / stacks) / 2

        z0 = radius * math.cos(lat0)
        zr0 = radius * math.sin(lat0)

        z1 = radius * math.cos(lat1)
        zr1 = radius * math.sin(lat1)

        glBegin(GL_TRIANGLE_STRIP)
        for j in range(slices + 1):
            lng = 2 * math.pi * (j / slices)
            x = math.cos(lng)
            y = math.sin(lng)

            glVertex3f(x * zr0, y * zr0, z0)
            glVertex3f(x * zr1, y * zr1, z1)
        glEnd()

def draw_car():
    # Body
    glPushMatrix()
    glColor3f(0.8, 0.2, 0.2)
    glScalef(1.0, 0.4, 0.6)
    draw_cube()
    glPopMatrix()

    # Roof
    glPushMatrix()
    glColor3f(0.9, 0.9, 0.9)
    glTranslatef(0, 0.4, 0)
    glScalef(0.6, 0.3, 0.4)
    draw_cube()
    glPopMatrix()

    # Wheels
    glColor3f(0.1, 0.1, 0.1)
    wheel_pos = [(-0.5, -0.2, 0.3), (0.5, -0.2, 0.3),
                 (-0.5, -0.2, -0.3), (0.5, -0.2, -0.3)]
    for pos in wheel_pos:
        glPushMatrix()
        glTranslatef(*pos)
        draw_hemisphere(0.15)
        glPopMatrix()

def init_trees():
    global trees
    trees = []

    road_width = camera_radius / 2.0

    min_tree_distance_from_road = 4.0

    road_left = -road_width + min_tree_distance_from_road
    road_right = road_width - min_tree_distance_from_road

    for _ in range(20):

        x = random.uniform(-15, 15)
        while road_left < x < road_right:
            x = random.uniform(-15, 15)

        z = random.uniform(-40, -15)
        trees.append([x, z])


def draw_tree(x, z):

    glPushMatrix()
    glColor3f(0.4, 0.2, 0.0)
    glTranslatef(x, -1, z)
    glScalef(0.2, 1.5, 0.2)
    draw_cube()
    glPopMatrix()


    glPushMatrix()
    glColor3f(0.0, 0.6, 0.0)
    glTranslatef(x, -0.5, z)


    radius = 0.5
    height = 1.5
    num_triangles = 16

    for i in range(num_triangles):
        angle0 = 2 * np.pi * i / num_triangles
        angle1 = 2 * np.pi * (i + 1) / num_triangles

        x0 = radius * np.cos(angle0)
        z0 = radius * np.sin(angle0)

        x1 = radius * np.cos(angle1)
        z1 = radius * np.sin(angle1)

        glBegin(GL_TRIANGLES)
        glVertex3f(0, height, 0)
        glVertex3f(x0, 0, z0)
        glVertex3f(x1, 0, z1)
        glEnd()

    glPopMatrix()



def update_scene():
    global car_x, car_speed, drift_speed, trees, game_over, obstacle_cars1, score, target_bg_colour

    if game_over or paused:
        return

    car_width = 1
    road_width = camera_radius / 2.0
    road_left = -road_width
    road_right = road_width

    car_x += drift_speed
    car_x = max(road_left + car_width, min(car_x, road_right - car_width))
    if key_states['w'] and not paused:
        car_speed = min(8, car_speed + 0.1)
    if key_states['s'] and not paused:
        if car_speed > 0:
            car_speed = max(1, car_speed - 0.1)

    if not key_states['w'] and not key_states['s']:
        car_speed *= 0.98
        road_width = camera_radius / 2.0

    for car in obstacle_cars1:
        car[1] += car_speed * 0.1

        if car[1] > 2:
            score += 1
            car[1] = random.uniform(-40, -20)
            car[0] = random.uniform(-road_width + 0.5, road_width - 0.5)

    player_radius = 0.8
    for car in obstacle_cars1:
        if isinstance(car, list):
            x, z = car
        else:
            x, z = car['x'], car['z']
        if abs(car_x - x) < player_radius and abs(0 - z) < player_radius:
            if not cheat_mode:
                game_over = True

    for i in range(len(trees)):
        while road_left < trees[i][0] < road_right:
            trees[i][0] = random.uniform(-8, 8)

        trees[i][1] += car_speed * 0.1

        if trees[i][1] > 20:
            if random.choice([True, False]):
                new_x = random.uniform(-8, road_left-1)
            else:
                new_x = random.uniform(road_right+1, 8)

            trees[i] = [new_x, random.uniform(-40, -5)]  # Reset to front




def display():
    global last_generation_time_1, score, angle, camera_mode

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    if camera_mode == "first_person":
        eye_height = 1.0
        look_ahead_distance = 10.0

        # Camera positioned at car's location but looking along the road (negative Z direction)
        gluLookAt(
            car_x,          # X position (same as car's lateral position)
            eye_height,     # Y position (eye level)
            0.5,            # Z position (slightly in front of car origin)
            car_x,          # Look at X (same lateral position)
            eye_height,     # Look at Y (same eye level)
            -look_ahead_distance,  # Look at Z (far ahead in driving direction)
            0.0, 1.0, 0.0   # Up vector
        )

    else:
        # In third-person mode, camera is behind the car.
        cam_x = car_x
        cam_y = camera_height
        cam_z = camera_radius + np.sin(angle)  # A bit behind the car, looking from a distance

        gluLookAt(cam_x, cam_y, cam_z,  # Eye position
                  car_x, 0.0, car_z,      # Look-at position (center of the car)
                  0.0, 1.0, 0.0)  # Up vector

    draw_sky()
    draw_field()
    draw_road()

    # Draw trees
    for tree in trees:
        draw_tree(tree[0], tree[1])

    # Draw car
    glPushMatrix()
    glTranslatef(car_x, 0, 0)
    draw_car()
    glPopMatrix()

    # Draw obstacle cars
    glColor3f(0.2, 0.2, 0.8)
    for car in obstacle_cars1:
        glPushMatrix()
        glTranslatef(car[0], -0.1, car[1])  # Position the car just above the road
        glScalef(0.8, 0.8, 0.8)
        draw_car()
        glPopMatrix()

    glColor3f(1.0, 1.0, 1.0)
    draw_text(900, 750, f"Score: {score}")  # Position at the top-right corner (adjust as needed)

    if game_over:
        glColor3f(1, 0, 0)
        draw_text(300, 400, f"GAME OVER! Final Score: {score} Press R to restart")

    if paused:
        glColor3f(1, 1, 0)
        draw_text(300, 400, "PAUSED")

    glutSwapBuffers()

def reshape(w, h):
    global width, height
    idth, height = w, h
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, w/h, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

def update_bg_colour():
    global bg_colour, target_bg_colour

    for i in range(3):
        if bg_colour[i] < target_bg_colour[i]:
            bg_colour[i] = min(bg_colour[i] + 0.01, target_bg_colour[i])
        elif bg_colour[i] > target_bg_colour[i]:
            bg_colour[i] = max(bg_colour[i] - 0.01, target_bg_colour[i])

def keyboard(key, x, y):
    global car_speed, drift_speed, game_over, paused, score, bg_colour, target_bg_colour, rain, camera_mode, cheat_mode

    key = key.decode('utf-8').lower()
    if key in key_states:
        key_states[key] = True

    if key == 'r' and not paused:
        global car_x, trees, obstacle_cars1

        car_x = 0.0
        car_speed = 0.0
        drift_speed = 0.0
        score = 0
        game_over = False
        paused = False

        init_trees()
        init_obstacle_cars()

    elif key == 'p':
        paused = not paused
    elif key == 'q':
        glutLeaveMainLoop()

    elif key == 'v':
        camera_mode = "first_person" if camera_mode == "third_person" else "third_person"
    elif key == 'a':
        drift_speed = -0.05
    elif key == 'd':
        drift_speed = 0.05
    if key == 'k' and not rain:
        target_bg_colour = [0.4, 0.7, 1.0]
        update_bg_colour()
        draw_sky()
    elif key == 'l':
        target_bg_colour = [0.1, 0.1, 0.2]
        update_bg_colour()
        draw_sky()

    if key == 'c':
        cheat_mode = not cheat_mode
        print(f"Cheat mode {'enabled' if cheat_mode else 'disabled'}")



def keyboard_up(key, x, y):
    key = key.decode('utf-8').lower()
    if key in key_states:
        key_states[key] = False
    if key == 'a' or key == 'd':
        drift_speed = 0.0

def special_keys(key, x, y):
    global raindrop_speed, rain_tilt,angle

    if key == GLUT_KEY_DOWN:
        angle += 0.1
    elif key == GLUT_KEY_UP:
        angle -= 0.1

def timer(_):
    update_scene()
    glutPostRedisplay()
    glutTimerFunc(16, timer, 0)

def init_obstacle_cars():
    global obstacle_cars1
    road_width = camera_radius / 2.0
    road_left = -road_width
    road_right = road_width
    obstacle_cars1 = []
    x = random.uniform(road_left + 0.5, road_right - 0.5)
    obstacle_cars1.append([x, random.uniform(-40, -20)])

key_states = {'w': False, 's': False, 'a': False, 'd': False}
init_trees()

glutInit(sys.argv)
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowSize(800, 600)
glutCreateWindow(b"3D Car Obstacle Game")
glEnable(GL_DEPTH_TEST)
glutDisplayFunc(display)
glutReshapeFunc(reshape)
glutSpecialFunc(special_keys)
glutKeyboardFunc(keyboard)
glutKeyboardUpFunc(keyboard_up)
glutTimerFunc(0, timer, 0)
init_obstacle_cars()
glutMainLoop()