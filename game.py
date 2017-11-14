import libtcodpy as libtcod
import actors
import map
import menu

# Window size
CONSOLE_WIDTH = 80
CONSOLE_HEIGHT = 50

DEBUG = True


class Game:
    def __init__(self):
        # Console information
        self.width = CONSOLE_WIDTH
        self.height = CONSOLE_HEIGHT
        self.objects = []

        # Font information
        libtcod.console_set_custom_font('fonts/prestige12x12_gs_tc.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
        #libtcod.console_set_custom_font('fonts/dejavu_wide12x12_gs_tc.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
        #libtcod.console_set_custom_font('fonts/terminal16x16_gs_ro.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_ASCII_INROW)

        # Initialize root console
        libtcod.console_init_root(self.width, self.height, 'Destard', False)

        # Renderer method
        #libtcod.sys_set_renderer(libtcod.RENDERER_SDL)

        # Map info.  Level is the map construction object - Maybe this should be generic so that new levels can be built.
        self.level = map.new_level(1)
        self.map = map.get_map_from_level(self)
        self.objects = map.get_objects_from_level(self)
        #self.rooms = self.factory.get_rooms(self.map)

        # Objects
        lightsource_component = actors.LightSource(self.map, "torch", mobile=True)
        mover_component = actors.Mover()
        self.player = actors.Object(5, 5, '@', 'player', libtcod.white, blocks=True, lightsource=lightsource_component, mover=mover_component)
        self.objects.append(self.player)
        map.initial_place_player(self)

        # This is the 'painting' console.  Map height and width are set up by the map gen.
        self.canvas_width = self.map_width
        self.canvas_height = self.map_height
        self.canvas = libtcod.console_new(self.canvas_width, self.canvas_height)
        libtcod.console_set_default_background(self.canvas, libtcod.black)
        libtcod.console_clear(self.canvas)

        # FOV map for rendering purposes.
        self.map_movement = True
        self.map_change = True
        self.fov_map = map.new_fov_map(self.map)
      
        # Torch info.  Should be replaced with torch object held by player or defaulting to some small value.
        #self.torch_radius = 20
        #self.torch_flicker_exponent = 1
        #self.torch_flicker_style = 'Random'

        # Game state information
        self.state = 'playing'

        # Debug setting.  Other functions will use this for debug info.  HOPEFULLY
        self.debug_showexplored = False
        self.debug_troubletiles = False


    def is_blocked(self, x, y):
        # Check map tile
        if self.map[x][y].blocked == True:
            return True
         
        # Then check the object list
        for thing in self.objects:
            if thing.blocks and thing.x == x and thing.y == y:
                return True
      
        # Not an object or a wall tile!
        return False
      
    def upper_left_of_map(self):
        a = min(max(self.player.x - (self.width-menu.reserved_width())/2,0),self.map_width-(self.width-menu.reserved_width()))
      
        b = min(max(self.player.y - (self.height-menu.reserved_height())/2,0),self.map_height-(self.height-menu.reserved_height()))
      
        return [a,b]
