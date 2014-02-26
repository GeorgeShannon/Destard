import random

class Leaf:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.children = []

    def sizecheck(self):
        if self.w > 6 or self.h > 6:
            return True
        else:
            return False


    def splitorientation(self):
        if self.w == self.h:
            if random.randrange(0,1) == 1:
                return "vertical"
            else:
                return "horizontallllll"

        if self.w > self.h:
            return "vertical"
        else:
            return "horizontal"


def branch(tree, trunk):
    if not trunk.sizecheck:
        return "minimum"

    if trunk.splitorientation == "vertical":
        splitpos = random.randrange(3, trunk.h - 3)
        upperleaf = Leaf(trunk.x, trunk.y, trunk.w, splitpos)
        lowerleaf = Leaf(trunk.x, trunk.y+splitpos+1, trunk.w, trunk.h-splitpos-1)
        tree.children.append(upperleaf)
        tree.children.append(lowerleaf)
    else:
        splitpos = random.randrange(3, trunk.w - 3)
        leftleaf = Leaf(trunk.x, trunk.y, splitpos, trunk.h)
        rightleaf = Leaf(trunk.x+splitpos+1, trunk.y, trunk.w-splitpos-1, trunk.h)
        tree.children.append(leftleaf)
        tree.children.append(rightleaf)