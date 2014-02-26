# Intended for listing what elements are needed for a level.  'levelset' below details the features that are required
# and decided upon.

import random

levelset = {
"starting" : 0,
"temple" : 0,
"complex" : 0,
"engravings" : 0
}

def build_elements(level):

    # Requirements
    if level == 1:
        levelset['starting'] = 1

    # Temple and 'complex' features
    if random.randint(0, 100) < 40:
        levelset['temple'] = random.randint(2, 3)
        levelset['complex'] = 1
    else:
        levelset['temple'] = random.randint(3, 4)
        levelset['complex'] = 0

    # Engravings
    levelset['engravings'] = random.randint(3, 5)