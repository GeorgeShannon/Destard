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
      
      # Font information
      libtcod.console_set_custom_font('dejavu16x16_gs_tc.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
      
      # Initialize root console
      libtcod.console_init_root(self.width, self.height, 'Destard', False)
      
      # Renderer method
      #libtcod.sys_set_renderer(libtcod.RENDERER_SDL)

      # Map info.  MapFactory is the map construction object.  Maybe this should be generic so that new levels can be built.
      MapFactory = map.new_caf()
      self.map = map.new_map(self, MapFactory)
      self.rooms = map.get_rooms(MapFactory)
      self.level = 1

      # Objects
      self.objects = []
      lightsource_component = actors.LightSource(self, "torch", mobile=True)
      mover_component = actors.Mover()
      self.player = actors.Object(5, 5, '@', 'player', libtcod.white, blocks=True, lightsource=lightsource_component, mover=mover_component)
      self.objects.append(self.player)
      lightsource_component = actors.LightSource(self, "brazier")
      temptorch = actors.Object(14, 12, 'X', 'brazier', libtcod.black, blocks=True, lightsource=lightsource_component)
      self.objects.append(temptorch)

      map.place_player(self, MapFactory)
      #map.fill_rooms
      
      # This is the 'painting' console.  Map height and width are set up by the map gen.
      self.canvas_width = self.map_width
      self.canvas_height = self.map_height
      self.canvas = libtcod.console_new(self.canvas_width, self.canvas_height)
      libtcod.console_set_default_background(self.canvas, libtcod.black)
      libtcod.console_clear(self.canvas)
      
      # FOV map for rendering purposes.
      self.map_movement = True
      self.map_change = True
      self.fov_map = map.new_fov_map(self)
      
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
