class Perform(object):
    
    def __init__(self, a):
        self.x = a[0]
        self.y = a[1]
        self.z = a[2]

    
    @staticmethod    
    def dot(a, b):
        return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]
    
    @staticmethod
    def cross(a, b):
        v1 = a[1] * b[2] - a[2] * b[1]
        v2 = a[2] * b[0] - a[0] * b[2]
        v3 = a[0] * b[1] - a[1] * b[0]
        return (v1, v2, v3)
    
    @staticmethod
    def normalize1(a, b):
        t1 = Perform.cross(a, b)
        toRet = Perform.normalize(t1)
        return toRet
        # toRet = [t1[0], t1[1], t1[2]]
        # currMag = sqrt(toRet[0] ** 2 + toRet[1] ** 2 + toRet[2] ** 2)
        # if currMag == 0:
        #     return (0, 0, 0)
        # toRet[0] = toRet[0] / float(currMag)
        # toRet[1] = toRet[1] / float(currMag)
        # toRet[2] = toRet[2] / float(currMag)
        # return (toRet[0], toRet[1], toRet[2])
    
    @staticmethod
    def normalize(a):
        toRet = [a[0], a[1], a[2]]
        currMag = sqrt(a[0] ** 2 + a[1] ** 2 + a[2] ** 2)
        if currMag == 0:
            return (0, 0, 0)
        toRet[0] /= float(currMag)
        toRet[1] /= float(currMag)
        toRet[2] /= float(currMag)
        return (toRet[0], toRet[1], toRet[2])
        
