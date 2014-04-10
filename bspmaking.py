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
            if random.randrange(0, 1) == 1:
                return "vertical"
            else:
                return "horizontal"

        if self.w > self.h:
            return "vertical"
        else:
            return "horizontal"

    def gatherleaves(self):
        collection = []
        if self.children:
            for kid in self.children:
                kid.gatherleaves()
        else:
            collection.append(self)
        return collection

    def branch(self):
        if not self.sizecheck:
            print "Minimum size."
            return

        if self.splitorientation() == "vertical":
            splitpos = random.randrange(3, self.h - 3)
            upperleaf = Leaf(self.x, self.y, self.w, splitpos)
            lowerleaf = Leaf(self.x, self.y+splitpos+1, self.w, self.h-splitpos-1)
            self.children.append(upperleaf)
            self.children.append(lowerleaf)
        else:
            splitpos = random.randrange(3, self.w - 3)
            leftleaf = Leaf(self.x, self.y, splitpos, self.h)
            rightleaf = Leaf(self.x+splitpos+1, self.y, self.w-splitpos-1, self.h)
            self.children.append(leftleaf)
            self.children.append(rightleaf)