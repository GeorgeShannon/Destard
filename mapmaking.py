from DisjointSet import DisjointSet
import levelmaking
#import bspmaking
import random
import libtcodpy as libtcod

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


# Create a map, fully blocked.
def map_init(height, width):
    print height, width
    map = [[Tile(True)
        for y in range(height) ]
            for x in range(width) ]
    return map


# This tile describes features of the dungeon, e.g., floors, walls
class Tile:
    # A tile of the map, and its properties
    def __init__(self, blocked, block_sight=None, permanent=False, debug=False):
        self.blocked = blocked
        
        # All tiles are initially unexplored
        self.explored = False

        # By default, if a tile is blocked, it also blocks sight
        if block_sight is None:
            block_sight = blocked
        self.block_sight = block_sight
        self.permanent = permanent
        self.debug = debug


# Used to make rooms at locations.
class Chamber:
    # A rectangle on the map, used to characterize a room, along with the type and any features it has.
    def __init__(self, x, y, w, h, style, features={}):
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
        #print self.x1, self.y1, "to", self.x2, self.y2, "vs", other.x1, other.y1, "to", other.x2, other.y2
        return self.x1 <= other.x2 and self.x2 >= other.x1 and self.y1 <= other.y2 and self.y2 >= other.y1


# A map using CA to build caves but also add pre-set rooms and features.
class FullMap:
    # A map using CA to build caves but also pre-set rooms.
    def __init__(self, width, height, levelnum, initial_open=0.60):
        self.__height = height
        self.__width = width
        self.__area = height * width
        self.__map = []
        self.__levelnum = levelnum
        self.__rooms = []
        self.__ds = DisjointSet()
        self.__up_loc = 0
        self.center_pt = (int(self.__height/2), int(self.__width/2))
        self.objects = []
        self.eventdict = {}
        self.gen_map(initial_open)

    def gen_map(self, initial_open):
        # Create an initial map
        self.__map = map_init(self.__height, self.__width)

        # make all border squares walls
        for j in range(0, self.__width-1):
            self.__map[j][0].permanent = True
            self.__map[j][self.__height-1].permanent = True

        for j in range(0, self.__height-1):
            self.__map[0][j].permanent = True
            self.__map[self.__width-1][j].permanent = True

        # Chew out randomized spots on the map
        self.randomize(initial_open)

        # Make a list of level features to make
        levellist = levelmaking.choose_levelset(self.__levelnum)

        # Init a counter for events
        currentevent = 1

        # For each item, get the features to make a Chamber out of.  Make a chamber and dig a proper room out of it.
        for item in levellist:
            # Select an item from the possible ones, given the type.
            itemselection = levelmaking.select_elements(item)

            # Want to look until a placement is found.
            placed = False
            while not placed:

                # Given this item, what arguments do we need to actually make the room?
                args = levelmaking.set_element_values(item, itemselection, self.__width, self.__height)
                new_room = Chamber(*args)

                # Check against other rooms to ensure this new room overlaps none of the others
                # This needs to go somewhere else!
                intersected = False
                for other_room in self.__rooms:
                    if new_room.intersect(other_room):
                        intersected = True
                        print "Failed intersection test!"
                        break

                # In cases of intersection, note the failure, and try again (another loop).  Otherwise, perform the
                # dig-a-room operations and make a note to finish the loop.
                if intersected:
                    print "Failed making", new_room.style
                else:
                    # i.e., no intersections, so paint a room
                    levelmaking.dig_room(self.__map, new_room, itemselection)
                    roomobjects = levelmaking.collect_features(self.__map, new_room, itemselection)
                    self.objects += roomobjects
                    print "Successfully dug", new_room.style
                    self.__rooms.append(new_room)
                    placed = True

                    (new_x, new_y) = new_room.center()  # Previously used for player placement (center of first room)

        # Perform CA operation - how many loops to perform?
        loops = random.randrange(2, 3)
        self.ca_operation(loops)

        # Check for other room-making operations


        # Join the areas of the level
        self.__join_rooms()
        self.check_open()

    def finalize_map(self):
        return self.__map

    def finalize_obects(self):
        return self.objects

    def get_rooms(self):
        return self.__rooms

    def is_map_blocked(self, x, y):
        if self.__map[x][y].is_blocked:
            return True
        else:
            return False

    def randomize(self, initial_open):
        open_count = int(self.__width * self.__height * initial_open)
        while open_count > 0:
            rand_r = random.randrange(1, self.__height-1)
            rand_c = random.randrange(1, self.__width-1)

            if self.__map[rand_c][rand_r].blocked and not self.__map[rand_c][rand_r].permanent:
                self.__map[rand_c][rand_r].blocked = False
                self.__map[rand_c][rand_r].block_sight = False
                open_count -= 1

    def check_open(self):
        count = 0
        for x in range(1, self.__width):
            for y in range(1, self.__height):
                if self.__map[x][y].blocked:
                    count += 1
        print 'open tiles: ', count


    def ca_operation(self, loops):
    # For non-permanent tiles, grow or kill depending on their surroundings.
        while loops > 0:
            for r in range(1, self.__height-1):
                for c in range(1, self.__width-1):
                    if not self.__map[c][r].permanent:
                        wall_count = self.__adj_wall_count(r, c)
                        if not self.__map[c][r].blocked:
                            if wall_count > 5:
                                self.__map[c][r].blocked = True
                                self.__map[c][r].block_sight = True
                        elif wall_count < 4:
                            self.__map[c][r].blocked = False
                            self.__map[c][r].block_sight = False
            loops -= 1

    def __adj_wall_count(self, sr, sc):
    # How many walls are surrounding a tile?
        count = 0

        for r in (-1, 0, 1):
            for c in (-1, 0, 1):
                if self.__map[(sc + c)][sr + r].blocked and not(c == 0 and r == 0):
                    count += 1

        return count

    def __join_rooms(self):

        all_caves = self.__determine_areas()

        # Build a tunneling map for pathing - use the permanent state check to determine passability.
        tunnelingmap = libtcod.map_new(self.__width, self.__height)
        for x in range(1, self.__width-1):
            for y in range(1, self.__height-1):
                perm_wall = (self.__map[x][y].permanent and self.__map[x][y].blocked)
                libtcod.map_set_properties(tunnelingmap, x, y, True, not perm_wall)

        # The tunneling path will let us move from the origin to the center.
        tunnelingpath = libtcod.dijkstra_new(tunnelingmap, 0.0)

        # The center needs to be non-permanent, otherwise we can't path to it.
        center_x, center_y = self.__find_good_center(self.center_pt)

        for cave in all_caves.keys():
            # This comment used to run the joining.  The function is still usable!
            #self.__join_points(all_caves[cave][0])
            origin_x = all_caves[cave][0][0]
            origin_y = all_caves[cave][0][1]

            libtcod.dijkstra_compute(tunnelingpath, origin_x, origin_y)
            if not libtcod.dijkstra_path_set(tunnelingpath, center_x, center_y):
                print "Could not path! Center point permanent:", self.__map[center_x][center_y].permanent
            prev_pt = (origin_x, origin_y)
            while not libtcod.dijkstra_is_empty(tunnelingpath):
                x, y = libtcod.dijkstra_path_walk(tunnelingpath)
                next_pt = (x, y)
                if x is not None:

                    root1 = self.__ds.find(next_pt)
                    root2 = self.__ds.find(prev_pt)

                    if root1 != root2:
                        self.__ds.union(root1, root2)

                    self.__map[next_pt[0]][next_pt[1]].blocked = False
                    self.__map[next_pt[0]][next_pt[1]].block_sight = False
                    self.__map[next_pt[0]][next_pt[1]].debug = True          # DEBUG

                    if self.__stop_drawing(prev_pt, next_pt, self.center_pt):
                        print "Done cave", cave
                        break

                    prev_pt = next_pt

        all_caves = self.__determine_areas()


    def __determine_areas(self):
        # divide the square into equivalence classes
        for r in range(1, self.__height-1):
            for c in range(1, self.__width-1):
                if not self.__map[c][r].blocked:
                    self.__union_adj_sqr(c, r)

        # Get a list of unaccessible areas to work over.
        areas = self.__ds.split_sets()
        print "Number of areas is", len(areas)
        return areas

    def __find_good_center(self, pt):
        # This function randomly moves the center to find a good 'end' point for cave joining function.
        # That is, the center can't be permanent.
        x = pt[0]
        y = pt[1]
        while self.__map[x][y].permanent:
            x += random.randrange(-1, 1)
            y += random.randrange(-1, 1)
        pt = (x, y)
        return pt

    def __stop_drawing(self, pt, npt, cpt):
        if self.__ds.find(npt) == self.__ds.find(cpt):
            return 1
        if self.__ds.find(pt) != self.__ds.find(npt) and not self.__map[npt[0]][npt[1]].blocked:
            return 1
        else:
            return 0

    def __get_tunnel_dir(self, pt1, pt2):
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

        return h_dir, v_dir

    def __union_adj_sqr(self, sr, sc):
        loc = (sr, sc)

        for r in (-1, 0):
            for c in (-1, 0):
                nloc = (sr+r, sc+c)

                if not self.__map[nloc[0]][nloc[1]].blocked and (r+c != -2):
                    root1 = self.__ds.find(loc)
                    root2 = self.__ds.find(nloc)

                    if root1 != root2:
                        self.__ds.union(root1,root2)