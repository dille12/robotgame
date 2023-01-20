import pygame
import random
from values import *
import math
from numpy import array as v2



def print_s(game, text_str, slot, color=[255, 255, 255], highlight=False):
    text = game.terminal[30].render(str(text_str), False, color)

    game.screen.blit(
        text, (game.resolution[0] - 10 - text.get_rect().size[0], slot * 30)
    )  #


def towards_target_int(pos, target, panning=0.15):
    return pos + (target - pos) * panning

def append_to_list(list, obj):
    if obj not in list:
        if not obj.get_circuit_breaker():
            list.append(obj)

def rotate_point(v, angle):
    rads = math.radians(-angle)
    x = v[0] * math.cos(rads) - v[1] * math.sin(rads)
    y = v[1] * math.cos(rads) + v[0] * math.sin(rads)

    return v2([x,y])


def towards_target(pos, target, panning=0.15):
    return minus(
        pos[i], minus(minus(target[i], pos[i], op="-"), [panning, panning], op="*")
    )


def render_text(
    game, string, pos, font_size, centerx=False, centery=False, color=[255, 255, 255]
):
    text = game.terminal[font_size].render(str(string), False, color)

    if centerx:
        pos[0] -= text.get_size()[0] / 2
    if centery:
        pos[1] -= text.get_size()[1] / 2

    game.screen.blit(text, pos)  #

def blit_glitch(game, image, pos, glitch = 2, diagonal = False):
    upper_pos = 0
    lower_pos = random.randint(2, 5)
    image_size = image.get_size()
    while 1:
        if random.randint(1, 5) == 1:
            game.screen.blit(
                image,
                [pos[0] + random.randint(-glitch, glitch), pos[1] + upper_pos + (0 if not diagonal else random.randint(-glitch, glitch))],
                area=[0, upper_pos, image_size[0], lower_pos],
            )
        if lower_pos == image_size[1]:
            break
        upper_pos = lower_pos
        lower_pos += random.randint(2, 5)
        if lower_pos >= image_size[1]:
            lower_pos = image_size[1]



def render_text_glitch(
    game, string, pos, font_size, color=[255, 255, 255], centerx=False, glitch=10
):
    # color = pick_random_from_list([[255,0,0], [0,255,0], [0,0,255]])
    text = game.terminal[font_size].render(str(string), False, color)
    text2 = game.terminal[font_size].render(
        str(string), False, minus([255, 255, 255], color, op="-")
    )
    upper_pos = 0
    lower_pos = random.randint(2, 5)
    text_size = text.get_size()
    if centerx:
        pos[0] -= text_size[0] / 2
    while 1:
        if random.randint(1, 5) == 1:
            game.screen.blit(
                text if random.uniform(0, 1) > 0.1 else text2,
                [pos[0] + random.randint(-glitch, glitch), pos[1] + upper_pos],
                area=[0, upper_pos, text_size[0], lower_pos],
            )
        if lower_pos == text_size[1]:
            break
        upper_pos = lower_pos
        lower_pos += random.randint(2, 5)
        if lower_pos >= text_size[1]:
            lower_pos = text_size[1]

def get_angle_diff(angle1, angle2):
    return (angle1 - angle2 + 180 + 360) % 360 - 180


def list_play(list):
    for y in list:
        y.stop()
    pick_random_from_list(list).play()


def pick_random_from_list(list):
    return list[random.randint(0, len(list) - 1)]

def pivot_child_around_parent(part):

    parent = part.parent
    angle_to_parent = part.parent_angle_difference

    current_angle = get_angle_diff(part.angle, parent.angle)

    if angle_to_parent != current_angle:
        print(">>>>>>>>>>>>>>>>>")
        print("Child:", part.name, "Parent:", parent.name)

        print("Original delta", part.delta_to_parent)
        diff = get_angle_diff(angle_to_parent, current_angle)
        print("SHOULD BE ROTATED BY", diff)

        pos = rotate_point(part.delta_to_parent, diff)
        print("New pos:", pos)
        part.pos = pos + parent.pos
        part.parent_angle_difference = current_angle
        part.delta_to_parent = pos

        print("New delta:", part.delta_to_parent)
        print("<<<<<<<<<<<<<<<")




def rot_center(image, angle, x, y):

    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(center=(x, y)).center)

    return rotated_image, new_rect


def rotate(surface, angle, pivot, offset):
    """Rotate the surface around the pivot point.

    Args:
        surface (pygame.Surface): The surface that is to be rotated.
        angle (float): Rotate by this angle.
        pivot (tuple, list, pygame.math.Vector2): The pivot point.
        offset (pygame.math.Vector2): This vector is added to the pivot.
    """
    rotated_image = pygame.transform.rotozoom(surface, angle, 1)  # Rotate the image.
    rotated_offset = offset.rotate(-angle)  # Rotate the offset vector.
    # Add the offset vector to the center/pivot point to shift the rect.
    rect = rotated_image.get_rect(center=pivot+rotated_offset)
    return rotated_image, rect  # Return the rotated image and shifted rect.


def minus(list1, list2, op="+"):
    try:
        list_1 = list1.copy()
        list_2 = list2.copy()
    except:
        list_1 = list1
        list_2 = list2
    for x in range(len(list1)):
        if op == "+":
            list_1[x] += list_2[x]
        elif op == "/":
            list_1[x] /= list_2[x]
        elif op == "*":
            list_1[x] *= list_2[x]
        else:
            list_1[x] -= list_2[x]
    return list_1


def mult(list1, am):
    try:
        list_1 = list1.copy()
    except:
        list_1 = list1

    for x in range(len(list1)):
        list_1[x] *= am
    return list_1


def closest_point(rect, p):
    dir = None
    if p[0] < rect.x:
        dx = rect.x
        dir = "left"
    elif p[0] > rect.x + rect.w:
        dx = rect.x + rect.w
        dir = "right"
    else:
        dx = p[0]


    if p[1] < rect.y:
        dy = rect.y
        dir = "up"
    elif p[1] > rect.y + rect.h:
        dy = rect.y + rect.h
        dir = "down"
    else:
        dy = p[1]

    return (dx, dy, dir)



def point_inside(point, point2, tolerance):
    boolean = (
        point2[0] < point[0] < point2[0] + tolerance[0]
        and point2[1] < point[1] < point2[1] + tolerance[1]
    )
    return boolean

def get_angle(pos1,pos2, radians = False):
    if radians:
        return math.atan2(pos2[1]-pos1[1], pos2[0]-pos1[0])
    else:
        return math.degrees(math.atan2(pos2[1]-pos1[1], pos2[0]-pos1[0]))



def get_dist_points(point_1, point_2):
    return math.sqrt((point_2[0] - point_1[0]) ** 2 + (point_2[1] - point_1[1]) ** 2)


def get_shortest_route(point, routes):
    complete_route = [0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0]
    for route in routes:
        if point in route:

            temp = []

            for x in route:
                temp.append(x)
                if x == point:
                    if len(complete_route) > len(temp):
                        complete_route = temp
                    break

    return complete_route
