import random
# Note that the map generation can't deal with diagonally isolated tiles!  All tiles should have a free path in one of
#   cardinal directions.
#
#

# This function returns the dimensions of the room, assuming the layout is rectangular and has a leading and trailing return.
def measurements(layout):
    x = last_x = 0 # First char found is first incremented.
    y = -1 # Always have leading and trailing returns, otherwise we would start with line '1'.

    for char in layout:
        if char=="\n": # Increment y, and check to see if x is consistent before moving to the next line.
            y += 1
            if x==0 and last_x!=x: print "Non-rectangular room found!", x, last_x
            last_x = x
            x = 0
        else:
            x += 1
    x = last_x # Otherwise x is still 0 from the last reset.
    return x,y

def Make_chamberset(map, x,y,w,h):

    if w<6 or h<6:
        print "Chamberset too small.  Aborting creation."

    passes = random.randrange(1,min(w/3,h/3))

    # How should I do this?  Actually one way would be to just keep track of the division values - first pass gives the
    # first division, then the second pass gives two values...

    # First gives the line of division between A and B (x<MAX and >0.).  Second gives AA, AB, BA, and BB, and thus, two
    # more x or y

    for m in range(x, x+w):
        for n in range(y, y+h):
            if (m==x or m==x+w) or (n==y or n==y+h):
                map[m][n].permanent = True
                map[m][n].blocked = True
                map[m][n].block_sight = True
            else:
                map[m][n].permanent = True
                map[m][n].blocked = False
                map[m][n].block_sight = False

    passnum = 0
    alignment = "horizontal"
    while passnum <= passes:

        if random.randrange(0,1)==1:
            division = random.randrange(x+3,x+w-3)
            alignment = "horizontal"
        else:
            division = random.randrange(y+3,y+h-3)
            alignment = "vertical"

        for i in range()

        passnum += 1

    if passes >= 1: firstpass = random.randrange(x+3,x+w-3)
    if passes >= 2: secondpass = (random.randrange(y+3,y+h-3),random.randrange(y+3,y+h-3))
    if passes >= 3: thirdpass = (random.rangerange(x+3,firstpass-3),random.rangerange(firstpass+3,x+w-3),random.randrange(x+3,firstpass-3),random.rangerange(firstpass+3,x+w-3))


#
#
# LEGEND
# . = open ground
# X = wall
# , = open ground that can be built up (CA)
# x = wall that can be torn down (CA)
#
# b = brazier light source

### Special features

starting = {

'entrance': '''
XXXXXXX==|==XXXXXXX
XXX.............XXX
XXX..X.......X..XXX
XXX.............XXX
X.................X
X.................X
'''

}

### Random features

templefurniture = {

'layout1': '''
XXXXXXX
XX...XX
X.....X
X.....X
X.....X
X.X.X.X
X.....X
X.X.X.X
X.....X
X.X.X.X
X.....X
XX...XX
XX...XX
XX...XX
XX...XX
''',

'layout2': '''
XXXXXXX.X.....X.XXXXXXX
XXXXXXX.........XXXXXXX
XXXXXXX.X.....X.XXXXXXX
XXXXXXX.........XXXXXXX
..........==...........
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
XXX...XXX..XXX...XXX
XXXXXXXXX..XXXXXXXXX
XXXXXXXXX..XXXXXXXXX
XXXXXXXXX..XXXXXXXXX
XXXXXXXXX..XXXXXXXXX
XXXXXXXXX..XXXXXXXXX
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