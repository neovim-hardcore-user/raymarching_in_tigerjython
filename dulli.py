from gturtle import *
import time
from math import *


res = [600, 600]
scale = 1

lightPos = [0, 5, 0]
cameraPos = [0, 4, 6]


def length(pos1, pos2):
    distance = sqrt((pos2[0] - pos1[0]) ** 2 + \
                    (pos2[1] - pos1[1]) ** 2 + \
                    (pos2[2] - pos1[2]) ** 2)
    return distance

def normalize(vector):
    magnitude = sqrt(vector[0] ** 2 + vector[1] ** 2 + vector[2] ** 2)
    if magnitude == 0:
        return vector

    normalized_vector = (vector[0] / magnitude, vector[1] / magnitude, vector[2] / magnitude)
    return normalized_vector


def dot_product(vector1, vector2):
    dp = vector1[0] * vector2[0] + \
         vector1[1] * vector2[1] + \
         vector1[2] * vector2[2]
    return dp

def sphereDist(p, center, radius):
    return length(p, center) - radius

def sceneDist(p):
    sphere = sphereDist(p, [-1.5, 1, 0], 1.3)
    plane = p[1]
    
    return min(sphere, plane)


def raymarch(rayOrigin, rayDirection):
    DO = 0
    
    for i in range(100):
        p = [DO * rayDirection[0] + rayOrigin[0], 
             DO * rayDirection[1] + rayOrigin[1], 
             DO * rayDirection[2] + rayOrigin[2]]
        dist = sceneDist(p)
        DO += dist
        if dist < 0.001 or DO > 50:
            break
    
    return [DO, i, p]

def getNormal(p):
    d = sceneDist(p)
    n = [d-sceneDist([p[0]-0.001, p[1], p[2]]), 
         d-sceneDist([p[0], p[1]-0.001, p[2]]), 
         d-sceneDist([p[0], p[1], p[2]-0.001])]
    
    return normalize(n)

def getLight(p):
    l = normalize([lightPos[0] - p[0], 
                   lightPos[1] - p[1], 
                   lightPos[2] - p[2]])
    
    normal = getNormal(p)
    
    dif = max(min(dot_product(normal, l), 1), 0)
    
    d = raymarch([p[0]+normal[0]*0.002, 
                  p[1]+normal[1]*0.002,
                  p[2]+normal[2]*0.002], l)
                  
    if d[0]<length(lightPos, p):
        dif *= 0.2

    return dif/1.3
    

def shader(p, t):
    pos = [(p[0]-0.5)*2, (-p[1]+0.5)*2]

    
    rayDirection = normalize([pos[0], pos[1], -1])
    d = raymarch(cameraPos, rayDirection)
    
    x = getLight(d[2])

    return (x, x, x)


makeTurtle()
speed(-1)
hideTurtle()



st = time.time()


for x in range(res[0]):
    for y in range(res[1]):
        color = shader([x/res[0], y/res[1]], 0)

        setPenColor(color)

        
        setPos(x*scale-res[0]*scale/2, -y*scale+res[1]*scale/2)
        forward(scale)


print(time.time()-st)


