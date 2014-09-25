import random
import bspmaking
# Note that the map generation can't deal with diagonally isolated tiles!  All tiles should have a free path in one of
#   cardinal directions.
#
#

# This function returns the dimensions of the room, assuming the layout is rectangular and has a leading and trailing return.
def measurements(layout):
    x = last_x = 0 # First char found is first incremented.
    y = -1 # Always have leading and trailing returns, otherwise we would start with line '1'.

    for char in layout:
        if char == "\n": # Increment y, and check to see if x is consistent before moving to the next line.
            y += 1
            if x == 0 and last_x != x:
                print "Non-rectangular room found!", x, last_x
            last_x = x
            x = 0
        else:
            x += 1
    x = last_x # Otherwise x is still 0 from the last reset.
    print x, y
    return x, y

def Make_chamberset(map, x,y,w,h):
    core = bspmaking.Leaf(x,y,w,h)

    while True:
        bspmaking.Leaf(x,y,w,h)


#
#
# LEGEND
# . = open ground (permanent)
# X = wall (permanent)
# , = open ground that can be built up (CA)
# x = wall that can be torn down (CA)
#
# b = brazier light source


### Special features

starting = {

'entrance1': '''
XXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXX
XXXXXXXX==|==XXXXXXXX
XXXXXX.........XXXXXX
XXXXXX.........XXXXXX
XXXX.............XXXX
XXXX...X.....X...XXXX
XXX...............XXX
XXX...X.......X...XXX
XX.................XX
'''
}

### Random features

templefurniture = {

'layout1': '''
XXXXXXXXXXXXX
XXXXX&&&XXXXX
XXXX.....XXXX
XXX.......XXX
XX....A....XX
XX.........XX
XX..X...X..XX
X&.........&X
X&..X...X..&X
X&.........&X
XX..X...X..XX
XX.........XX
XXX.......XXX
XXXX.....XXXX
XXXX.....XXXX
''',

'layout2': '''
XXXXXXX.X.....X.XXXXXXX
XXXXXXX.........XXXXXXX
XXXXXXX.X.....X.XXXXXXX
XXXXXXX.........XXXXXXX
.......................
.X.X.X...........X.X.X.
.......................
...........b...........
.......................
.X.X.X...........X.X.X.
.......................
XXXXXXX.X.....X.XXXXXXX
XXXXXXX.........XXXXXXX
XXXXXXX.X.....X.XXXXXXX
XXXXXXX.........XXXXXXX
''',

'layout3': '''
XXXXXXXXXXXXXXXXXXXX
XXXXXXXX....XXXXXXXX
XXXXXX........XXXXXX
XXXXX..........XXXXX
XXXXX..........XXXXX
XXXXXX........XXXXXX
XXXXXXXX....XXXXXXXX
XXXXXXXX....XXXXXXXX
XXX...XX....XX...XXX
XX................XX
XX................XX
XX................XX
XXX...XX....XX...XXX
XXXXXXXX....XXXXXXXX
XXXXXXXX....XXXXXXXX
XXXXXXXX....XXXXXXXX
XXXXXXX......XXXXXXX
''',

'layout4': '''
XXXXXXXXXXXXXXX
X.............X
X.XX.......XX.X
X.XX.......XX.X
X.............X
X..............
X..............
X......b......X
..............X
..............X
X.............X
X.XX.......XX.X
X.XX.......XX.X
X.............X
XXXXXXXXXXXXXXX
'''

}