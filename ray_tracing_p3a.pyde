# Sahej Panag

from __future__ import division
import traceback
from functions import *

debug_flag = True
  

def setup():
    size(320, 320) 
    noStroke()
    colorMode(RGB, 1.0)
    background(0, 0, 0)
    frameRate(30)

# make sure proper error messages get reported when handling key presses
def keyPressed():
    try:
        handleKeyPressed()
    except Exception:
        traceback.print_exc()

# read and interpret a scene description .cli file based on which key has been pressed
def handleKeyPressed():
    if key == '1':
        interpreter("01_one_sphere.cli")
    elif key == '2':
        interpreter("02_three_spheres.cli")
    elif key == '3':
        interpreter("03_shiny_sphere.cli")
    elif key == '4':
        interpreter("04_many_spheres.cli")
    elif key == '5':
        interpreter("05_one_triangle.cli")
    elif key == '6':
        interpreter("06_icosahedron_and_sphere.cli")
    elif key == '7':
        interpreter("07_colorful_lights.cli")
    elif key == '8':
        interpreter("08_reflective_sphere.cli")
    elif key == '9':
        interpreter("09_mirror_spheres.cli")
    elif key == '0':
        interpreter("10_reflections_in_reflections.cli")
    elif key == '-':
        interpreter("11_star.cli")

# You should add code for each command that calls routines that you write.
# Some of the commands will not be used until Part B of this project.
def interpreter(fname):
    global fov, sphereList, uvw, backgroundRGB, eye, currSurface, lightList, triangleList, trianglePoints
    
    reset_scene()  # you should initialize any data structures that you will use here
    
    fname = "data/" + fname
    with open(fname) as f:
        lines = f.readlines()

    # parse the lines in the file in turn
    for line in lines:
        words = line.split()  # split up the line into individual tokens
        if len(words) == 0:   # skip empty lines
            continue
        if words[0] == 'sphere':
            x = float(words[2])
            y = float(words[3])
            z = float(words[4])
            radius = float(words[1])
            # newMat = [currSurface.dr, currSurface.dg, currSurface.db]
            sphereList.append(SphereMake(x, y, z, radius, Surface(currSurface.dr, currSurface.dg, currSurface.db, currSurface.ar, currSurface.ag, currSurface.ab, currSurface.sr, currSurface.sg, currSurface.sb, currSurface.spec_power, currSurface.k_refl)))
        elif words[0] == 'fov':
            fov = float(words[1])
        elif words[0] == 'eye':
            x = float(words[1])
            y = float(words[2])
            z = float(words[3])
            eye = (x, y, z)
        elif words[0] == 'uvw':
            uvw[0] = (float(words[1]), float(words[2]), float(words[3]))
            uvw[1] = (float(words[4]), float(words[5]), float(words[6]))
            uvw[2] = (float(words[7]), float(words[8]), float(words[9])) 
        elif words[0] == 'background':
            r = float(words[1])
            g = float(words[2])
            b = float(words[3])
            backgroundRGB = (r,g,b)
        elif words[0] == 'light':
            x = float(words[1])
            y = float(words[2])
            z = float(words[3])
            r = float(words[4])
            g = float(words[5])
            b = float(words[6])
            lightList.append(Light(x,y,z,r,g,b))
        elif words[0] == 'surface':
            currSurface.dr = float(words[1])
            currSurface.dg = float(words[2])
            currSurface.db = float(words[3])
            # double check this
            
            currSurface.ar = float(words[4])
            currSurface.ag = float(words[5])
            currSurface.ab = float(words[6])
            
            currSurface.sr = float(words[7])
            currSurface.sg = float(words[8])
            currSurface.sb = float(words[9])
            
            currSurface.spec_power = float(words[10])
            currSurface.k_refl = float(words[11])
        elif words[0] == 'begin':
            trianglePoints = []
            # start storing triangle
        elif words[0] == 'vertex':
            x = float(words[1])
            y = float(words[2])
            z = float(words[3])
            trianglePoints.append((x,y,z))
        elif words[0] == 'end':
            sphereList.append(triangleMake(trianglePoints[0], trianglePoints[1], trianglePoints[2], Surface(currSurface.dr, currSurface.dg, currSurface.db, currSurface.ar, currSurface.ag, currSurface.ab, currSurface.sr, currSurface.sg, currSurface.sb, currSurface.spec_power, currSurface.k_refl)))
            # stop storing triangle
        elif words[0] == 'render':
            render_scene()    # render the scene (this is where most of the work happens)
        elif words[0] == '#':
            pass  # ignore lines that start with the comment symbol (pound-sign)
        else:
            print ("unknown command: " + word[0])

# render the ray tracing scene
def render_scene():
    global sphereList, lightList, fov, uvw, eye, currSurface, backgroundRGB, debug_flag
    
    
    for j in range(height):
        if j%(height//80) == 0:
            print j * 100 // height, "%"
        for i in range(width):
            debug_flag = False
            if (i == 208 and j == 254):
                debug_flag = True
            ww = 1/tan(radians(fov/2))
            v = ((2 * j)/ height) - 1
            u = ((2 * i)/ width) - 1
            xDir = (u * uvw[0][0] + v * uvw[1][0] - ww * uvw[2][0])
            yDir = (u * uvw[0][1] + v * uvw[1][1] - ww * uvw[2][1])
            zDir = (u * uvw[0][2] + v * uvw[1][2] - ww * uvw[2][2])
            temp = Perform.normalize((xDir, yDir, zDir))
            v2 = (temp[0], -temp[1], temp[2])
            
            myRay = Ray(eye, v2)
            hit = intersectShade(myRay)
            theColor = colorG(myRay, hit.sphereM, hit.intersect, hit.normV, hit.poinT)
            set (i, j, color(*theColor))

# here you should reset any data structures that you will use for your scene (e.g. list of spheres)
def reset_scene():
    global sphereList, lightList, fov, uvw, eye, currSurface, backgroundRGB, trianglePoints, shadowOrigin
    sphereList = []
    lightList = []
    trianglePoints = []
    uvw = [(0, 0, 0), (0, 0, 0), (0, 0, 0)]
    backgroundRGB = (0, 0, 0)
    currSurface = Surface(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    eye = (0, 0, 0)
    fov = 0 
    shadowOrigin = eye

    

# prints mouse location clicks, for help debugging
def mousePressed():
    print ("You pressed the mouse at " + str(mouseX) + " " + str(mouseY))

# this function should remain empty for this assignment
def draw():
    pass

def colorG(ray, sphereM, intersect, normV, t, max_depth = 10):
    global lightList
    
    if t == 100000:
        return (backgroundRGB[0], backgroundRGB[1], backgroundRGB[2])
    
    
    r = 0
    g = 0
    b = 0
    
    #  for some reason refl keeps returning as 0 so does hit
    refl = sphereM.surface.k_refl

    # does not ever go into this case
    if (refl > 0 and max_depth > 0):
        # calculate reflection origin
        offsetNorm = (normV[0] * 0.0001, normV[1] * 0.0001, normV[2] * 0.0001)
        reflectionOrigin = (intersect[0] + offsetNorm[0], intersect[1] + offsetNorm[1], intersect[2] + offsetNorm[2])
        # calculate R
        D = (-1 * ray.stop[0], -1 * ray.stop[1], -1 * ray.stop[2])
        scalar = Perform.dot(normV, D) * 2
        offsetRef = (normV[0] * scalar, normV[1] * scalar, normV[2] * scalar)
        R = (ray.stop[0] + offsetRef[0], ray.stop[1] + offsetRef[1], ray.stop[2] + offsetRef[2])
        # get ray and hit
        reflectionRay = Ray(reflectionOrigin, R)
        reflectionHit = intersectShade(reflectionRay)
        # check background color
        if (reflectionHit.poinT >= 100000):
            # multiply by reflection pls
            r += backgroundRGB[0] * refl
            g += backgroundRGB[1] * refl
            b += backgroundRGB[2] * refl
        # recurse
        tempR = colorG(reflectionRay, reflectionHit.sphereM, reflectionHit.intersect, reflectionHit.normV, reflectionHit.poinT, max_depth - 1)
        reflectColor = (tempR[0] * refl, tempR[1] * refl, tempR[2] * refl)
        # set color
        r += reflectColor[0]
        g += reflectColor[1]
        b += reflectColor[2]
        
    
    for i in lightList:
        # get my light positions
        lightX = i.x - intersect[0]
        lightY = i.y - intersect[1]
        lightZ = i.z - intersect[2]
        light = (lightX, lightY, lightZ)
        # get norm of light
        lightVec = Perform.normalize(light)
        # pass to check shadow ray
        lightPass = (i.x, i.y, i.z)

        
        # get ray direction
        rayX = -1 * ray.stop[0]
        rayY = -1 * ray.stop[1]
        rayZ = -1 * ray.stop[2]
        rayVec = (rayX, rayY, rayZ)
        
        
        # calculate shadow ray
        shadowOrigin = (intersect[0] + normV[0] * 0.0001, intersect[1] + normV[1] * 0.0001, intersect[2] + normV[2] * 0.0001)
        shadowDir = Perform.normalize(lightVec)
        shadowRay = Ray(shadowOrigin, shadowDir)
        shadowHit = intersectShade(shadowRay)
        shadowTerm = 1
        
        # check case
        if (shadowHit.poinT <= abs(distHelper(lightPass, intersect))):
            shadowTerm = 0
            
        else:
            if debug_flag:
                print "checking shadow for light with position: ", lightPass
                print "hit position: ", intersect
                print "shadow ray origin (should be the hit position slightly offset away from the surface): ", shadowRay.start 
                print "shadow ray direction: ", shadowRay.stop
                print "shadow hit: ", shadowHit.intersect
                print "distance from light to original hit:", distHelper(lightPass, intersect)
                print ""
            # calculate H
            tempH = (lightVec[0] + rayVec[0], lightVec[1] + rayVec[1], lightVec[2] + rayVec[2])
            H = Perform.normalize(tempH)
            # calculate specular coefficient (use to make spec color later)
            tempS = Perform.dot(H, normV)
            specCo = (max(0, tempS)) ** sphereM.surface.spec_power
            # diffuse coefficient (use to make diffuse color later)
            tempD = Perform.dot(normV, lightVec)
            diffCo = max(0, tempD)
            
            # add spec color
            r += i.r * sphereM.surface.sr * specCo 
            g += i.g * sphereM.surface.sg * specCo 
            b += i.b * sphereM.surface.sb * specCo 
            #specColor = (specR, specG, specB)
            
            # add diffuse color
            r += sphereM.surface.dr * i.r * diffCo
            g += sphereM.surface.dg * i.g * diffCo
            b += sphereM.surface.db * i.b * diffCo
            #diffColor = (diffR, diffG, diffB)

    
    # shadow term
        # r *= shadowTerm
        # g *= shadowTerm
        # b *= shadowTerm
    
    
    # ambient color
    r += sphereM.surface.ar
    g += sphereM.surface.ag 
    b += sphereM.surface.ab 
    
    
    theColor = (r, g, b)
    return theColor


def distHelper(a, b):
    return sqrt(((b[0] - a[0]) ** 2) + ((b[1] - a[1]) ** 2) + ((b[2] - a[2]) ** 2))
    
def intersectShade(ray):
    minT = 100000
    global sphereList
    hit = Met(SphereMake(0, 0, 0, 0, Surface(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)), Ray((0, 0, 0), (0, 0, 0)), minT, 0)
    for x in sphereList:
        t = x.intersect(ray)
        if t is not None:
            if type(x) == SphereMake:
                posMet = Met(x, ray, t, 0)
            else:
                posMet = Met(x, ray, t, x.surrNormal)
            if posMet.poinT < hit.poinT:
                minT = posMet.poinT
                hit = posMet
    
    return hit


class Ray(object):
        def __init__(self, start, stop):
            self.start = start
            self.stop = stop
            
class triangleMake(object):
    global debug_flag
    def __init__(self, a, b, c, surface):
        self.a = a
        self.b = b
        self.c = c
        
        # obtain sides
        self.ab = (b[0] - a[0], b[1] - a[1], b[2] - a[2])
        self.bc = (c[0] - b[0], c[1] - b[1], c[2] - b[2])
        self.ca = (a[0] - c[0], a[1] - c[1], a[2] - c[2])
        
        self.surrNormal = Perform.normalize1(self.ab, self.bc)
        self.nx = self.surrNormal[0]
        self.ny = self.surrNormal[1]
        self.nz = self.surrNormal[2]
        self.surface = surface

    def intersect(self, ray):
        # if debug_flag:
        #     print "testing intersection with triangle whose color is ", (self.surface.dr, self.surface.dg, self.surface.db)
        # calculate denom
        dx = ray.stop[0]
        dy = ray.stop[1]
        dz = ray.stop[2]
        d = (dx, dy, dz)
        denom = Perform.dot(self.surrNormal, d) 
        if denom == 0:
            return None
        # calculate num
        temp = [0, 0, 0]
        temp[0] = self.a[0] - ray.start[0]
        temp[1] = self.a[1] - ray.start[1]
        temp[2] = self.a[2] - ray.start[2]
        diff = (temp[0], temp[1], temp[2])
        num = Perform.dot(self.surrNormal, diff)
        poinT = num / denom
        if poinT < 0:
            return None
        # if debug_flag:
        #     print "ray direction: ", ray.stop
        #     print "normal vector: ", self.surrNormal
        #     print "plane intersects at at t=%f" % poinT
        return poinT
    
class SphereMake(object):
    def __init__(self, x, y, z, radius, surface):
        self.x = x
        self.y = y
        self.z = z
        self.radius = radius
        self.surface = surface
        
    def intersect(self, ray):
        dx = ray.stop[0]
        dy = ray.stop[1]
        dz = ray.stop[2]
        ux = ray.start[0] - self.x
        uy = ray.start[1] - self.y
        uz = ray.start[2] - self.z
        radius = self.radius
        a = (dx ** 2) + (dy ** 2) + (dz ** 2)
        # recheck this
        if a == 0:
            return None
        b = (2 * dx * ux) + (2 * dy * uy) + (2 * dz * uz)
        c = ((ux ** 2) + (uy ** 2) + (uz ** 2) - (radius ** 2))
        checker = (b ** 2) - (4 * a * c)
        if (checker >= 0):
            op1 = (-b - ((b ** 2) - (4 * a * c)) ** 0.5)/(2 * a)
            op2 = (-b + ((b ** 2) - (4 * a * c)) ** 0.5)/(2 * a)
            hitMin = min(op1, op2)
            hitMax = max(op1, op2)
            if hitMin >= 0:
                return hitMin
            elif hitMax >= 0:
                return hitMax
        return None
    
            
class Met(object):
    def __init__(self, sphereM, ray, poinT, normV):
        self.poinT = poinT
        self.sphereM = sphereM
        xT = ray.start[0] + poinT * ray.stop[0]
        yT = ray.start[1] + poinT * ray.stop[1]
        zT = ray.start[2] + poinT * ray.stop[2]
        self.intersect = (xT, yT, zT)
        if type(sphereM) == SphereMake:
            xM = xT - sphereM.x
            yM = yT - sphereM.y
            zM = zT - sphereM.z
            self.normV = Perform.normalize((xM, yM, zM))
        else:
            self.normV = sphereM.surrNormal
            normDir = Perform.dot(self.normV, ray.stop)
            if normDir >= 0:
                self.normV = (-1 * self.normV[0], -1 * self.normV[1], -1 * self.normV[2])
            # calculate triple 1
            t1 = (self.intersect[0] - sphereM.a[0], self.intersect[1] - sphereM.a[1], self.intersect[2] - sphereM.a[2])
            temp1 = Perform.cross(t1, sphereM.ab)
            triple1 = Perform.dot(temp1, self.normV)
            # calculate triple 2
            t2 = (self.intersect[0] - sphereM.b[0], self.intersect[1] - sphereM.b[1], self.intersect[2] - sphereM.b[2])
            temp = Perform.cross(t2, sphereM.bc)
            triple2 = Perform.dot(temp, self.normV)
            # calculate triple 3
            t3 = (self.intersect[0] - sphereM.c[0], self.intersect[1] - sphereM.c[1], self.intersect[2] - sphereM.c[2])
            temp = Perform.cross(t3, sphereM.ca)
            triple3 = Perform.dot(temp, self.normV)

            if ((triple1 > 0) == (triple2 > 0) == (triple3 > 0)) is False:
                self.poinT = 100000
                # if debug_flag:
                #     print "no match"
            else:
                self.poinT = poinT
                # if debug_flag:
                #     print "triple 1: ", triple1
                #     print "triple 2: ", triple2
                #     print "triple 3: ", triple3
            # store hit information
        
class Light(object):
    def __init__(self, x, y, z, r, g, b):
        self.x = x
        self.y = y
        self.z = z
        self.r = r
        self.g = g
        self.b = b

class Surface(object):
    def __init__(self, dr, dg, db,  ar, ag, ab,  sr, sg, sb,  spec_power, k_refl):
        self.dr = dr
        self.dg = dg
        self.db = db
        self.d = (self.dr, self.dg, self.db)
        self.ar = ar
        self.ag = ag
        self.ab = ab
        self.a = (self.ar, self.ag, self.ab)
        self.sr = sr
        self.sg = sg
        self.sb = sb
        self.s = (self.sr, self.sg, self.sb)
        self.spec_power = spec_power
        self.k_refl = k_refl
        
    
        
    
