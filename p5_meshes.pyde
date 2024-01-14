# Provided code for Subdivison and Geodesic Spheres

from __future__ import division
import traceback

# My global variables
G = []
V = []
O = {}
currCorner = 0
cornerAppear = True
showRandomColors = False



# parameters used for object rotation by mouse
mouseX_old = 0
mouseY_old = 0
rot_mat = PMatrix3D()

# initalize things
def setup():
    size (800, 800, OPENGL)
    frameRate(30)
    noStroke()

# draw the current mesh (you will modify parts of this routine)
def draw():
    global G, V, O, currCorner, cornerAppear, showRandomColors
    
    background (100, 100, 180)    # clear the screen to black

    perspective (PI*0.2, 1.0, 0.01, 1000.0)
    camera (0, 0, 6, 0, 0, 0, 0, 1, 0)    # place the camera in the scene
    
    # create an ambient light source
    ambientLight (102, 102, 102)

    # create two directional light sources
    lightSpecular (202, 202, 202)
    directionalLight (100, 100, 100, -0.7, -0.7, -1)
    directionalLight (152, 152, 152, 0, 0, -1)
    
    pushMatrix();

    stroke (0)                    # draw polygons with black edges
    fill (200, 200, 200)          # set the polygon color to white
    ambient (200, 200, 200)
    specular (0, 0, 0)            # turn off specular highlights
    shininess (1.0)
    
    applyMatrix (rot_mat)   # rotate the object using the global rotation matrix

    # THIS IS WHERE YOU SHOULD DRAW YOUR MESH
    randomSeed(0)
    for c in range(0, len(V), 3):
        beginShape()
        if (showRandomColors):
            fill(random(255), random(255), random(255))
        else:
            fill(255, 255, 255)
        vertex(G[V[c]].x, G[V[c]].y, G[V[c]].z)
        vertex(G[V[c + 1]].x, G[V[c + 1]].y, G[V[c + 1]].z)
        vertex(G[V[c + 2]].x, G[V[c + 2]].y, G[V[c + 2]].z)
        endShape(CLOSE)
        if cornerAppear:
            pushMatrix()
            curr = G[V[currCorner]]
            cornerNext = G[V[next(currCorner)]]
            cornerPrev = G[V[prev(currCorner)]]
            mid = [(cornerNext.x + cornerPrev.x) / 2, (cornerNext.y + cornerPrev.y) / 2, (cornerNext.z + cornerPrev.z) / 2]
            offset = [(4 * curr.x + mid[0]) / 5, (4 * curr.y + mid[1]) / 5, (4 * curr.z + mid[2]) / 5]
            translate(offset[0], offset[1], offset[2])
            fill(200, 10, 100)
            sphere(0.08)
            popMatrix()
            #CHECK SHACHI GUIDE FOR THIS

    popMatrix()

# read in a mesh file (this needs to be modified)
def read_mesh(filename):
    global G, V, O, currCorner, cornerAppear, showRandomColors
    

    fname = "data/" + filename
    # read in the lines of a file
    with open(fname) as f:
        lines = f.readlines()

    # determine number of vertices (on first line)
    words = lines[0].split()
    num_vertices = int(words[1])
    print "number of vertices =", num_vertices

    # determine number of faces (on first second)
    words = lines[1].split()
    num_faces = int(words[1])
    print "number of faces =", num_faces

    # read in the vertices
    for i in range(num_vertices):
        words = lines[i+2].split()
        x = float(words[0])
        y = float(words[1])
        z = float(words[2])
        G.append(PVector(x, y, z))
        print "vertex: ", x, y, z

    # read in the faces2
    for i in range(num_faces):
        j = i + num_vertices + 2
        words = lines[j].split()
        nverts = int(words[0])
        if (nverts != 3):
            print "error: this face is not a triangle"
            exit()

        index1 = int(words[1])
        index2 = int(words[2])
        index3 = int(words[3])
        V += [index1, index2, index3]
        # V.append(index1, index2, index3)
        print "triangle: ", index1, index2, index3
    
    computeOTable(G, V)

# make sure proper error messages get reported when handling key presses
def keyPressed():
    try:
        handleKeyPressed()
    except Exception:
        traceback.print_exc()

# process key presses (call your own routines!)
def handleKeyPressed():
    global G, V, O, currCorner, cornerAppear, showRandomColors
    if key == '1':
        read_mesh ('tetra.ply')
    elif key == '2':
        G = []
        V = []
        read_mesh ('octa.ply')
    elif key == '3':
        G = []
        V = []
        read_mesh ('icos.ply')
    elif key == '4':
        G = []
        V = []
        read_mesh ('star.ply')
    elif key == 'n': # next
        currCorner = next(currCorner)
    elif key == 'p': # previous
        currCorner = prev(currCorner)
    elif key == 'o': # opposite
        currCorner = opp(currCorner)
    elif key == 's': # swing
        currCorner = swing(currCorner)
    elif key == 'd': # subdivide mesh
        subdivision()
    elif key == 'i': # inflate mesh
        inflate()
    elif key == 'r': # toggle random colors
        showRandomColors = not showRandomColors
    elif key == 'c': # toggle showing current corner
        cornerAppear = not cornerAppear
    elif key == 'q': # quit the program
        exit()

# remember where the user first clicked
def mousePressed():
    global mouseX_old, mouseY_old
    mouseX_old = mouseX
    mouseY_old = mouseY

# change the object rotation matrix while the mouse is being dragged
def mouseDragged():
    global rot_mat
    global mouseX_old, mouseY_old
    
    if (not mousePressed):
        return
    
    dx = mouseX - mouseX_old
    dy = mouseY - mouseY_old
    dy *= -1

    len = sqrt (dx*dx + dy*dy)
    if (len == 0):
        len = 1
    
    dx /= len
    dy /= len
    rmat = PMatrix3D()
    rmat.rotate (len * 0.005, dy, dx, 0)
    rot_mat.preApply (rmat)

    mouseX_old = mouseX
    mouseY_old = mouseY
    
# My helper functions

def next(cornerNum):
    triangleNum = cornerNum // 3
    return 3 * triangleNum + ((cornerNum + 1) % 3)

def prev(cornerNum):
    triangleNum = cornerNum // 3
    return 3 * triangleNum + ((cornerNum - 1) % 3)

def opp(cornerNum):
    return O[cornerNum]

def swing(cornerNum):
    return next(opp(next(cornerNum)))  

def computeOTable(G, V):
    global O, currCorner, cornerAppear, showRandomColors
    O = {}
    temp = []
    for v in range(len(V)):
        temp.append((min(V[next(v)], V[prev(v)]), max(V[next(v)], V[prev(v)]), v))
    temp = sorted(temp)
    for i in range(0, len(temp), 2):
        cornerA = temp[i][2]
        cornerB = temp[i + 1][2]
        O[cornerA] = cornerB
        O[cornerB] = cornerA
        
def inflate():
    global G
    for v in G:
        v.normalize()
            
def subdivision():
    global G, V, O, currCorner, cornerAppear, showRandomColors
    numEdges = len(V) // 2
    newG = G
    newV = []
    midPoint = {}
    
    for a, b in O.items():
        if a > b:
            continue
        end1 = G[V[prev(a)]]
        end2 = G[V[next(a)]]
        
        mid = (end1 + end2) * 0.5
        midIndex = len(newG)
        
        newG.append(mid)
        midPoint[a] = midIndex
        midPoint[b] = midIndex
            
    for x in range(0, len(V), 3):
        y = x + 1
        z = y + 1
        
        newV += [V[x], midPoint[z], midPoint[y]]
        newV += [midPoint[z], V[y], midPoint[x]]
        newV += [midPoint[y], midPoint[x], V[z]]
        newV += [midPoint[x], midPoint[y], midPoint[z]]
    
    G = newG
    V = newV
    computeOTable(G, V)

        
    




    
