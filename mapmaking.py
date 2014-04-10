from DisjointSet import DisjointSet
import roommaking
import bspmaking
import random

# Holdover from the cellular automata code... not used anymore.
PERM_WALL = 0
WALL = 1
PERM_FLOOR = 2
FLOOR = 3

# Information about rooms for original map making
ROOM_MAX_SIZE = 8
ROOM_MIN_SIZE = 4
MAX_ROOMS = 4
MAX_ROOM_MONSTERS = 1
MAX_ROOM_ITEMS = 6

#Init room set
#num_rooms = 0


# This tile describes features of the dungeon, e.g., floors, walls
class Tile:
    # A tile of the map, and its properties
    def __init__(self, blocked, block_sight=None, permanent=False, debug=False):
        self.blocked = blocked
        
        # All tiles are initially unexplored
        self.explored = False

        # By default, if a tile is blocked, it also blocks sight
        if block_sight is None: block_sight = blocked
        self.block_sight = block_sight
        self.permanent = permanent
        self.debug = debug


# Used to make rooms at locations.
class Chamber:
    # A rectangle on the map, used to characterize a room, along with the type and any features it has.
    def __init__(self, x, y, w, h, style, features = {}):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h
        self.style = style
        self.features = features
    
    def center(self):
        center_x = (self.x1 + self.x2) / 2
        center_y = (self.y1 + self.y2) / 2
        return center_x, center_y
        
    def intersect(self, other):
        # returns true if this Rect intersects with another
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and self.y1 <= other.y2 and self.y2 >= other.y1)

# An internal check for whether a map tile is blocked (by a wall)
def is_blocked(map, x, y):
    # first test the map tile
    if map[x][y].blocked:
        return True    
    return False
        
# Create a map, fully blocked.
def map_init(height, width):
    print height, width
    map = [[Tile(True)
        for y in range(height) ]
            for x in range(width) ]
    return map


# A map of this class consists of 
class CA_CaveFactory:
    def __init__(self, width, height, initial_open=0.60):
        self.__height = height
        self.__width = width
        self.__area = height * width
        self.__CAmap = []
        self.__rooms = []
        self.__leveldata = {}
        self.__ds = DisjointSet()
        self.__up_loc = 0
        self.center_pt = (int(self.__height/2), int(self.__width/2))
        self.__gen_initial_map(width, height, initial_open)

    # Performs the CA operation, then joins separate rooms.  Returns the map, consisting of a grid of ints.    
    def gen_map(self):
        loops = random.randrange(2, 4)
        while loops > 0:
            for r in range(1, self.__height-1):
                for c in range(1, self.__width-1):
                    if not self.__CAmap[c][r].permanent:
                        wall_count = self.__adj_wall_count(r, c)
                        if not self.__CAmap[c][r].blocked:
                            if wall_count > 5:
                                self.__CAmap[c][r].blocked = True
                                self.__CAmap[c][r].block_sight = True
                        elif wall_count < 4:
                            self.__CAmap[c][r].blocked = False
                            self.__CAmap[c][r].block_sight = False

            loops -= 1

        self.__join_rooms()

        return self.__CAmap
        
    def get_rooms(self):
        return self.__rooms
        
    def create_room(self, room, layout):
        # go through the tiles in the defined rectangle and construct them according to the layout
        x = room.x1 + 1
        y = room.y1
        for char in layout:
            if char == ".":
                self.__CAmap[x][y].permanent = True
                self.__CAmap[x][y].blocked = False
                self.__CAmap[x][y].block_sight = False
            if char == ",":
                self.__CAmap[x][y].permanent = False
                self.__CAmap[x][y].blocked = False
                self.__CAmap[x][y].block_sight = False
            if char == "X":
                self.__CAmap[x][y].permanent = True
                self.__CAmap[x][y].blocked = True
                self.__CAmap[x][y].block_sight = True
            if char == "x":
                self.__CAmap[x][y].permanent = False
                self.__CAmap[x][y].blocked = True
                self.__CAmap[x][y].block_sight = True
            x += 1
            if char == "\n":
                x = room.x1 + 1
                y += 1

    def create_room_features(self, room, layout):
        # Start with an empty set to put level data in
        leveldata = {}

        # go through the tiles in the defined rectangle and construct them according to the layout
        x = room.x1 + 1
        y = room.y1
        for char in layout:
            element = None
            if char == "=": element = "monastery doorway"
            if char == "b": element = "brazier"
            if element: leveldata.update({(x,y):element})
            x += 1
            if char == "\n":
                x = room.x1 + 1
                y += 1

        return leveldata


    def __set_border(self):
        # make all border squares walls
        # This could be moved to a superclass
        for j in range(0,self.__width-1):
            self.__CAmap[j][0].permanent = True
            self.__CAmap[j][self.__height-1].permanent = True

        for j in range(0,self.__height-1):
            self.__CAmap[0][j].permanent = True
            self.__CAmap[self.__width-1][j].permanent = True


    def __gen_initial_map(self,width,height,initial_open):
        # Create an initial map with random tiles removed, plus rooms and fixtures.
        self.__CAmap = map_init(height,width)

        open_count = int(self.__area * initial_open)
        self.__set_border()

        for r in range(MAX_ROOMS):

            # Pick a random selection from our options.
            roomselection = random.choice(roommaking.templefurniture.keys())
            layoutselection = roommaking.templefurniture[roomselection]

            # Get the width and height
            w, h = roommaking.measurements(layoutselection)

            # Find a spot without going off the edge of the map
            x = random.randrange(0, self.__width - w - 1)
            y = random.randrange(0, self.__height - h - 1)
            
            # Build rooms as Chambers
            new_room = Chamber(x, y, w, h, 'temple')
            
            # Check against other rooms to ensure this new room overlaps none of the others
            failed = False
            for other_room in self.__rooms:
                if new_room.intersect(other_room):
                    failed = True
                    break
            
            if not failed:
                # i.e., no intersections, so paint a room
                self.create_room(new_room, layoutselection)

                # Give it some features
                new_room_features = self.create_room_features(new_room, layoutselection)
                self.__leveldata.update(new_room_features)

                print self.__leveldata
                self.__rooms.append(new_room)
                
                (new_x, new_y) = new_room.center()  # Previously used for player placement (center of first room)

        tree = bspmaking.Leaf(20,20,20,10)
        tree.branch()
        leaves = tree.gatherleaves()
        print leaves
        for leaf in leaves:
            print "Leaf:", leaf.w, leaf.y

        # Chew out a certain amount of 'noise' for the CA function to work over.
        while open_count > 0:
            rand_r = random.randrange(1,self.__height-1)
            rand_c = random.randrange(1,self.__width-1)

            if self.__CAmap[rand_c][rand_r].blocked and not self.__CAmap[rand_c][rand_r].permanent:
                self.__CAmap[rand_c][rand_r].blocked = False
                self.__CAmap[rand_c][rand_r].block_sight = False
                open_count -= 1

    def __adj_wall_count(self,sr,sc):
    # How many walls are surrounding a tile?
        count = 0

        for r in (-1,0,1):
            for c in (-1,0,1):
                if self.__CAmap[(sc + c)][sr + r].blocked and not(c == 0 and r == 0):
                    count += 1

        return count

    def __join_rooms(self):
        # divide the square into equivalence classes
        for r in range(1,self.__height-1):
            for c in range(1,self.__width-1):
                if not self.__CAmap[c][r].blocked:
                    self.__union_adj_sqr(c,r)

        all_caves = self.__ds.split_sets()

        for cave in all_caves.keys():
            self.__join_points(all_caves[cave][0])

    def __join_points(self,pt1):
        next_pt = pt1

        while 1:
            dir = self.__get_tunnel_dir(pt1,self.center_pt) ### This determines the next point to 'drill' to.  Unfortunately it will still drill through 'permanent' tiles.  How to fix?  We could, possibly, use a pathfinding algorithm to get to work our way to the center point.  That should work but might be overkill.  Let's see how often it happens first while I work on cave building.

            if (dir[0] == 0) or (dir[1] == 0):
                next_pt = (pt1[0] + dir[0],pt1[1] + dir[1])
            else:
                if random.randrange(0,1):
                    next_pt = (pt1[0] + dir[0],pt1[1])
                else:
                    next_pt = (pt1[0],pt1[1] + dir[1])

            if self.__CAmap[next_pt[0]][next_pt[1]].permanent: print "Uh oh, permanent tile at", next_pt[0], next_pt[1]

            if self.__stop_drawing(pt1,next_pt,self.center_pt):
                return
            
            root1 = self.__ds.find(next_pt)
            root2 = self.__ds.find(pt1)

            if root1 != root2:
                self.__ds.union(root1,root2)

            self.__CAmap[next_pt[0]][next_pt[1]].blocked = False
            self.__CAmap[next_pt[0]][next_pt[1]].block_sight = False
            self.__CAmap[next_pt[0]][next_pt[1]].debug = True          ### DEBUG

            pt1 = next_pt

    def __stop_drawing(self,pt,npt,cpt):
        if self.__ds.find(npt) == self.__ds.find(cpt):
            return 1
        if self.__ds.find(pt) != self.__ds.find(npt) and not self.__CAmap[npt[0]][npt[1]].blocked:
            return 1
        else:
            return 0

    def __get_tunnel_dir(self,pt1,pt2):
        if pt1[0] < pt2[0]:
            h_dir = +1
        elif pt1[0] > pt2[0]:
            h_dir = -1
        else:
            h_dir = 0

        if pt1[1] < pt2[1]:
            v_dir = +1
        elif pt1[1] > pt2[1]:
            v_dir = -1
        else:
            v_dir = 0

        return (h_dir,v_dir)

    def __union_adj_sqr(self,sr,sc):
        loc = (sr,sc)

        for r in (-1,0):
            for c in (-1,0):
                nloc = (sr+r,sc+c)

                if not self.__CAmap[nloc[0]][nloc[1]].blocked and (r+c != -2):
                    root1 = self.__ds.find(loc)
                    root2 = self.__ds.find(nloc)

                    if root1 != root2:
                        self.__ds.union(root1,root2)
            