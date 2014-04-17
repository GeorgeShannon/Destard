# Intended for listing what elements are needed for a level.  'levelset' below details the features that are required
# and decided upon.

import random

leveltype = {
"starting" : 0,
"temple" : 0,
"complex" : 0,
"engravings" : 0
}

level1 = {
"starting" : 1,
"temple" : 3,
"complex" : 1,
"engravings" : 0
}

def build_elements(level, map):

    while True:

        temples = 0
        complexes = 0


        # Requirements
        if level[starting]:
            buildroom(entrance)

        if level[complex]>complexes:
            while True:
                buildroom(complex)

        # Temple and 'complex' features
        if random.randint(0, 100) < 40:
            level['temple'] = random.randint(2, 3)
            level['complex'] = 1
        else:
            level['temple'] = random.randint(3, 4)
            level['complex'] = 0

        # Engravings
        level['engravings'] = random.randint(3, 5)

def buildroom(type):
    if type == "entrance":
        pass

    if type == "temple":
        pass

    if type == complex:
        h = random.randrange(10,30)
        w = random.randrange(10,30)
        x =
        newcomplex = Chamber()
