import math
import pygame as py
from sys import exit
import pickle
from pygame import mixer

py.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
py.init()
py.mixer.music.load("sounds/music.wav")
py.mixer.music.play(-1, 0.0, 5000)

class Game:
    """ The Game class initializes and manages the game states, event handling, and main game loop for a menu-based game
    with multiple game modes, such as normal play, speedrun, controls, and settings.

    Attributes:
    screen (pygame.Surface): The game window with a resolution of 1400x800
    font (pygame.Font): Holds the font used for rendering text
    clock (pygame.time.Clock): The clock regulates the frame rate
    menu_active (bool): Tracks if the menu is currently active
    normal_active (bool): Tracks if the normal game mode is active
    speedrun_active (bool): Tracks if the speedrun mode is active
    controls_active (bool): Tracks if the controls menu is active
    settings_active (bool): Tracks if the settings menu is active
    playing_active (bool): Tracks if the game is currently in a playing state
    menu_buttons (list[Button]): A list of buttons displayed on the menu
    level_buttons (list[Button]): A list of buttons displayed on the level selection
    mouse_pos (tuple): Tracks the mouse position when the mouse is clicked
    menu_page (Menu_page): Instance of the Menu_page class to draw the menu
    level_select (Level_select): Instance of the Level_select class for level selection
    levels (Levels): Instance of the Levels class, representing the current level
    speedrun_page (Speedrun): Instance of the Speedrun class
    settings_page (Settings): Instance of the Settings class
    shooting (bool): Tracks if the player is shooting.
    paused (bool): Tracks if the game is paused.
    pause_button (bool): Tracks if the pause button is pressed down
    pause_text (pygame.Surface): Text surface for displaying the "Pause" message
    pause_rect (pygame.Rect): Rectangle defining the position of the pause text
    controls_image (pygame.Surface): Image for displaying the controls
    controls_rect (pygame.Rect): Rectangle defining the position of the control image
    throw_fx (pygame.mixer.Sound): Sound effect for throwing action
    jump_fx (pygame.mixer.Sound): Sound effect for jumping
    game_over_fx (pygame.mixer.Sound): Sound effect for game over
    level_complete_fx (pygame.mixer.Sound): Sound effect for completing a level

     Methods:
     mainloop: The main loop of the game that continuously processes events, updates game states, and renders graphics
     on the screen. Handles user input like mouse clicks and key presses and controls transitions between different game
     states

     escape: Handles escape functionality, allowing the player to return to the main menu from various
        game states. Resets the game state and relevant attributes
        Args:
            type (int): A type indicator for triggering the escape functionality
         """

    def __init__(self):
        self.screen = py.display.set_mode((1400, 800))
        self.font = py.font.Font("font/Pixeltype.ttf", 50)  # loads the font
        self.clock = py.time.Clock()
        self.menu_active = True  # makes the game change to the menu state when True
        self.normal_active = False  # makes the game change to the normal state when True
        self.speedrun_active = False  # makes the game change to the speedrun state when True
        self.controls_active = False  # makes the game change to the controls state when True
        self.settings_active = False  # makes the game change to the settings state when True
        self.playing_active = False  # makes the game change to the playing state when True
        self.menu_buttons = [Button(200, 700, "buttons/normal.png", self), Button(1200, 700, "buttons/speedrun.png", self),
                             Button(600, 700, "buttons/controls.png", self), Button(800, 700, "buttons/settings.png", self)]
        self.level_buttons = [Button(250, 500, "buttons/basketball_button.png", self), Button(550, 500,"buttons/basketball_button.png", self),
                              Button(850, 500, "buttons/basketball_button.png", self), Button(1150, 500, "buttons/basketball_button.png", self)]
        self.mouse_pos = (0, 0)
        self.menu_page = Menu_page(self)  # instantiates the menu page class
        self.level_select = Level_select(self)  # instantiates the level select page class
        self.levels = Levels(self,1)
        self.speedrun_page = Speedrun(self)
        self.settings_page = Settings(self)
        self.shooting = False
        self.paused = False
        self.pause_button = True
        self.pause_text = self.font.render("Pause", False,
                                                       (64, 64, 64))  # creates the message text
        self.pause_text = py.transform.rotozoom(self.pause_text, 0, 3)  # makes message text bigger
        self.pause_rect = self.pause_text.get_rect(center=(700, 400))  # creates where text will be placed
        self.controls_image = py.image.load("images/Controls.png").convert_alpha()
        self.controls_rect = self.controls_image.get_rect(center=(700, 350))
        # load sounds
        self.throw_fx = py.mixer.Sound("sounds/throw.wav")
        self.jump_fx = py.mixer.Sound("sounds/jump.wav")
        self.game_over_fx = py.mixer.Sound("sounds/game_over.wav")
        self.level_complete_fx = py.mixer.Sound("sounds/clap.mp3")


    def mainloop(self):
        while True:
            for event in py.event.get():  # event loop
                if event.type == py.QUIT:
                    py.quit()
                    exit()
                if event.type == py.MOUSEBUTTONDOWN:
                    if self.menu_page.start_count > 120:  # gets mouse position when mouse menu_buttons pressed
                        self.mouse_pos = py.mouse.get_pos()
                    if self.playing_active or self.speedrun_page.speed_start:  # changes the shooting to True when mouse button is pressed
                        self.shooting = True



            if self.menu_active:
                if self.menu_buttons[0].get_pressed:
                    self.mouse_pos = (0, 0)
                    self.menu_active = False
                    self.normal_active = True
                elif self.menu_buttons[1].get_pressed:
                    self.mouse_pos = (0, 0)
                    self.menu_active = False
                    self.speedrun_active = True
                elif self.menu_buttons[2].get_pressed:
                    self.mouse_pos = (0, 0)
                    self.menu_active = False
                    self.controls_active = True
                elif self.menu_buttons[3].get_pressed:
                    self.mouse_pos = (0, 0)
                    self.menu_active = False
                    self.settings_active = True

            self.escape(1)
            for menu_buttons in self.menu_buttons:
                menu_buttons.reset()

            if self.normal_active:
                if self.level_buttons[0].get_pressed:
                    self.levels = Levels(self, 1)
                if self.level_buttons[1].get_pressed:
                    self.levels = Levels(self, 2)
                if self.level_buttons[2].get_pressed:
                    self.levels = Levels(self, 3)
                if self.level_buttons[3].get_pressed:
                    self.levels = Levels(self, 4)

            for level_buttons in self.level_buttons:
                if level_buttons.get_pressed:
                    self.playing_active = True
                    self.normal_active = False

            for level_buttons in self.level_buttons:
                level_buttons.reset()

            # loads the game state
            if self.menu_active:
                self.menu_page.draw()
            elif self.normal_active:
                self.level_select.draw()
            elif self.playing_active:
                if not self.paused:
                    self.levels.draw()
                keys = py.key.get_pressed()
                if self.paused:
                    self.screen.blit(self.pause_text, self.pause_rect)
                    if keys[py.K_p] and self.pause_button:
                        self.paused = False
                        self.pause_button = False
                else:
                    if keys[py.K_p] and self.pause_button:
                        self.paused = True
                        self.pause_button = False
                if not keys[py.K_p]:  # checks if the pause button has been lifted
                    self.pause_button = True
            elif self.speedrun_active:
                if not self.paused: # draws the speedrun state if the game is not paused
                    self.speedrun_page.draw()
                keys = py.key.get_pressed()
                if self.paused:
                    self.screen.blit(self.pause_text, self.pause_rect)
                    if keys[py.K_p] and self.pause_button:
                        self.paused = False
                        self.pause_button = False
                else:
                    if keys[py.K_p] and self.pause_button:
                        self.paused = True
                        self.pause_button = False
                if not keys[py.K_p]:  # checks if the pause button has been lifted
                    self.pause_button = True
            elif self.controls_active:
                self.screen.blit(self.controls_image,self.controls_rect)
            elif self.settings_active:
                self.settings_page.draw()


            py.display.update()
            self.clock.tick(60)  # sets frame rate to 60 fps

    def escape(self, type):
        keys = py.key.get_pressed()
        if keys[py.K_ESCAPE] or not type:
            self.levels.counter_centers = [(175, 25), (125, 25), (75, 25), (25, 25)]
            self.levels.ball_message_active = False
            self.levels.time_message_active = False
            self.menu_active = True  # makes the game change to the menu state when True
            self.normal_active = False  # makes the game change to the normal state when True
            self.speedrun_active = False  # makes the game change to the speedrun state when True
            self.controls_active = False  # makes the game change to the controls state when True
            self.settings_active = False  # makes the game change to the settings state when True
            self.playing_active = False  # makes the game change to the playing state when True
            self.shooting = False
            self.paused = False
            self.levels.medal = 1
            self.levels.time = 0
            self.speedrun_page.speed_start = False

class Menu_page:
    """
    The Menu Page class displays the menu page on the screen and registers when the player clicks any of the menu
    buttons and changes the state of the game depending on the button pressed.

    Attributes:
    Parent (class): Holds reference to the game class
    start_count (int): Holds the time since the menu state has been active for the first time
    mj (pygame.Surface): Holds an image of Michael Jordon
    message_surface (pygame.Surface): text surface for displaying g the message "protect the legacy"
    message_rect (pygame.Rect): Rectangle defining the position of the message surface
    credit_surface (pygame.Surface): text surface for displaying the message " By Thomas Way"
    credit_rect (pygame.Rect): Rectangle defining the position of the credit surface
    title_surface (Pygame.Surface): Holds the image of the title
    title_rect (pygame.Surface): Rectangle defining the position of the image for title surface

    Methods:
    draw: This displays all the surfaces on the screen and checks if any of the buttons have been pressed and changes
    the games state.
    """

    def __init__(self, parent):
        self.parent = parent
        self.start_count = 0 # controls how long the start-up screen stays on
        self.mj = py.image.load("images/mj.png").convert_alpha()
        self.mj = py.transform.rotozoom(self.mj, 0, 0.75)
        self.mj_rect = self.mj.get_rect(center = (700,500))
        self.message_surface = self.parent.font.render("Protect The Legacy", False, (64, 64, 64))  # creates the message text
        self.message_surface = py.transform.rotozoom(self.message_surface, 0, 2)  # makes message text bigger
        self.message_rect = self.message_surface.get_rect(center=(700, 100))  # creates where text will be placed
        self.credit_surface = self.parent.font.render("By Thomas Way", False, (64, 64, 64))  # creates the credit text
        self.credit_rect = self.credit_surface.get_rect(center=(1000, 700))  # creates where text will be placed
        self.title_surface = py.image.load("images/slamdunk.png").convert_alpha()  # loads title text
        self.title_rect = self.title_surface.get_rect(center=(700, 300))  # creates where the title will be placed
        if not isinstance(parent, Game):
            print("Menu's Game class not passed:",)

    def draw(self):
        if self.start_count <= 120:  # start up section
            self.parent.screen.fill(py.Color((211, 101, 4)))
            self.parent.screen.blit(self.mj, self.mj_rect)
            self.parent.screen.blit(self.credit_surface, self.credit_rect) # this puts the text onto the screen
            self.parent.screen.blit(self.message_surface, self.message_rect)  # this puts the text onto the screen
            self.start_count += 1  # adds for 3 seconds
        else:
            # main menu section
            self.parent.screen.fill(py.Color((58, 140, 250)))  # makes the screen blue
            self.parent.screen.blit(self.title_surface, self.title_rect)
            for button in self.parent.menu_buttons:
                self.parent.screen.blit(button.text, button.rect)
            for button in self.parent.menu_buttons:  # checks if a button has been pressed
                button.getpressed(self.parent.mouse_pos)

class Level_select:
    """
    The Level Select class displays the level buttons on the screen, checks for if the buttons have been pressed and
    changes the level variable and game state corresponding to the button pressed

    Attributes:
    parent (class): holds reference to the game class
    title_surface (pygame.Surface): text surface for displaying the message "Level Select"
    title_rect (pygame.Rect): Rectangle defining the position of the title surface
    one_surface (pygame.Surface): text surface for displaying the message "1"
    two_surface (pygame.Surface): text surface for displaying the message "2"
    three_surface (pygame.Surface): text surface for displaying the message "3"
    four_surface (pygame.Surface): text surface for displaying the message "4"
    one_rect (pygame.Rect): Rectangle that defines the position of the one_surface
    two_rect (pygame.Rect): Rectangle that defines the position of the two_surface
    three_rect (pygame.Rect): Rectangle that defines the position of the three_surface
    four_rect (pygame.Rect): Rectangle that defines the position of the four_surface

    Methods:
    draw: this displays the level buttons on the screen, checks for if the buttons have been pressed and
    changes the level variable and game state corresponding to the button pressed
    """
    def __init__(self, parent):
        self.parent = parent
        self.title_surface = self.parent.font.render("Level select", False,
                                                       (64, 64, 64))  # creates the message text
        self.title_surface = py.transform.rotozoom(self.title_surface, 0, 3)  # makes message text bigger
        self.title_rect = self.title_surface.get_rect(center=(700, 100))  # creates where text will be placed
        self.one_surface = py.transform.rotozoom(self.parent.font.render("1", False, (160, 32, 240)),0, 3)  # creates 1
        self.two_surface = py.transform.rotozoom(self.parent.font.render("2", False, (160, 32, 240)),0,3)  # creates 2
        self.three_surface = py.transform.rotozoom(self.parent.font.render("3", False, (160, 32, 240)) ,0,3) # creates 3
        self.four_surface = py.transform.rotozoom(self.parent.font.render("4", False, (160, 32, 240)),0,3)  # creates 4
        self.one_rect = self.one_surface.get_rect(center=(250, 500))  # creates number will be placed
        self.two_rect = self.two_surface.get_rect(center=(550, 500))  # creates number will be placed
        self.three_rect = self.three_surface.get_rect(center=(850, 500))  # creates number will be placed
        self.four_rect = self.four_surface.get_rect(center=(1150, 500))  # creates number will be placed
        if not isinstance(parent, Game):
            print("Level select's Game class not passed:",)

    def draw(self):  # draws the level select page
        self.parent.screen.fill(py.Color((58, 140, 250)))
        self.parent.screen.blit(self.title_surface, self.title_rect)
        for buttons in self.parent.level_buttons:  # displays buttons
            self.parent.screen.blit(buttons.text, buttons.rect)
        self.parent.screen.blit(self.one_surface, self.one_rect)  # displays buttons numbers
        self.parent.screen.blit(self.two_surface, self.two_rect)
        self.parent.screen.blit(self.three_surface, self.three_rect)
        self.parent.screen.blit(self.four_surface, self.four_rect)
        for button in self.parent.level_buttons:  # checks if a button has been pressed
            button.getpressed(self.parent.mouse_pos)

class Button:
    """
    The Button class is used to create all the buttons in the game. It checks if the area the button is in has been
    pressed. when this occurs the button will be registered as pressed until it has been reset

    Attributes:
    parent (class): Holds the class of the page that displays the buttons
    x (int): holds the x position of the button
    y (int): holds the y position of the button
    text (pygame.Surface): Holds the image of the button
    rect (pygame.Rect): Rectangle that defines the position of the button
    get_pressed (bool): Holds if the button haas been pressed

    Methods:
    getpressed: checks if the button has been pressed and then makes the get_pressed attribute True
              Args:
              mouse_pos (tuple): this hold where the mouse was on the screen when it was pressed

    reset: resets the get_pressed attribute to False
    """
    def __init__(self, x, y, text, parent):
        self.parent = parent
        self.x = x  # x coordinate
        self.y = y  # y coordinate
        self.text = py.image.load(text).convert_alpha()  # button image
        if x == 500 or x == 899:
            self.text = py.transform.rotozoom(self.text, 0, 1)
        elif x == 877 or x == 518:
            self.text = py.transform.rotozoom(self.text, 0, 0.2)
        else:
            self.text = py.transform.rotozoom(self.text, 0, 0.5)
        self.rect = self.text.get_rect(center=(self.x, self.y))
        self.get_pressed = False  # turns true when button is pressed
        if not isinstance(parent, object):
            print("Buttons parent class not passed")
        if not isinstance(text, str):
            print("Buttons text is not string")
        if not isinstance(x, int):
            print("buttons x coordinate is not integer")
        if not isinstance(y, int):
            print("buttons y coordinate is not integer")


    def getpressed(self, mouse_pos):  # function that makes the self.get_pressed true when pressed
        if self.rect.collidepoint(mouse_pos):
            self.get_pressed = True


    def reset(self):
        self.get_pressed = False

class Levels:
    """
    The Levels class manages the creation, rendering, and logic of each level in the game.

    Attributes:
    parent (class): Holds reference to the game class
    player (Player): The player character object
    dirt, grass (pygame.Surface): Surfaces representing dirt and grass tiles in the game
    goal_image, lava_image, platform_image (pygame.Surface): Surfaces for game objects
    gold_image, silver_image, bronze_image (pygame.Surface): Surfaces for medal images
    medal_rect (pygame.Rect): Rectangle that defines the position of the medal surfaces
    complete_surface (pygame.Surface): Text surface for displaying "Level Complete" message
    complete_rect (pygame.Rect): Rectangle that defines the position of the complete_surface
    complete_buttons (list): List of Button objects for retrying or proceeding to the next level
    medal (int): Represents the current medal to be given to the player
    time (float): Holds the time taken for the player to complete the level
    objective_time (float): Holds the time needed for the player to get a better medal
    time_rect (tuple): The rectangle defining the position of the time surface
    ball_message (Surface): Text message telling player that there is better medal rewarded with fewer balls used
    ball_message_active (bool): Tracks whether the ball message is active
    time_message_active (bool): Tracks whether the time-related message is active
    counter_centers (list): List of counter center coordinates
    r_up (bool): Tracks whether the 'R' key is being pressed for resetting the level
    level_number (int): Current level number
    tile_list, slime_list, lava_list (list): Lists holding game objects such as tiles, slimes, and lava
    goal (pygame.Surface): Surface for the goal object
    level_complete (bool): Tracks whether the level has been completed
    game_over (bool): Tracks whether the game is over
    world_data (list): Data loaded from the level file, defining the level layout
    time_message (pygame.Surface): Rendered text surface for displaying time-related goals
    speed_complete_message (pygame.Surface): Rendered text for displaying completion time
    speed_complete_message_rect (pygame.Rect): Rect for defining the position of the speed_complete_message

    Methods:
     __init__(self, parent, number): Initializes the level based on the level number and loads data.

    draw(self): Draws the level, including tiles, objects, and player actions.

    ball_removal(self): Checks and removes balls that collide with lava.

    r_reset(self): Resets the level when the 'R' key is pressed.

    reset(self): Resets level state and reloads tiles and objects.
    """

    def __init__(self, parent,number):
        self.parent = parent
        self.player = Player(self)
        self.dirt = py.image.load("images/dirt.png").convert()
        self.grass = py.image.load("images/grass.png").convert()
        self.goal_image = py.image.load("images/basket.png").convert_alpha()
        self.lava_image = py.image.load("images/lava.png").convert_alpha()
        self.platform_image = py.image.load("images/platform.png").convert_alpha()
        self.gold_image = py.image.load("images/gold_medal.png").convert_alpha()
        self.silver_image = py.image.load("images/silver_medal.png").convert_alpha()
        self.bronze_image = py.image.load("images/bronze_medal.png").convert_alpha()
        self.medal_rect = self.gold_image.get_rect(center=(700, 350))
        self.complete_surface = self.parent.font.render("Level Complete", False,
                                                       (64, 64, 64))  # creates the message text
        self.complete_surface = py.transform.rotozoom(self.complete_surface, 0, 1.2)  # makes message text bigger
        self.complete_rect = self.complete_surface.get_rect(center=(700, 250))  # creates where text will be placed
        self.complete_buttons = [Button(500,460,"images/retry.png", self), Button(899,460,"images/next.png", self)]
        self.medal = 1
        self.time = 0
        self.objective_time = 0
        self.time_rect = (675, 10, 50, 50)
        self.ball_message = py.transform.rotozoom(self.parent.font.render("Use one ball for a better medal", False,
                                                       (64, 64, 64)),0, 0.4)  # creates the message text
        self.ball_message_active = False
        self.time_message_active = False
        self.counter_centers = [(175, 25),(125, 25),(75, 25), (25, 25)]
        self.r_up = True
        self.level_number = number
        self.tile_list = []
        self.slime_list = []
        self.lava_list = []
        self.goal = ""
        self.level_complete = False
        self.game_over = False
        pickle_in = open(f"levels/level{self.level_number}_data", "rb")
        self.world_data = pickle.load(pickle_in)
        pickle_in = open(f"times/level{self.level_number}_time", "rb")
        self.objective_time = pickle.load(pickle_in)
        time = str(self.objective_time/60)
        self.time_message = py.transform.rotozoom(self.parent.font.render(("Beat the level in under"+time+" seconds"), False,
                                                       (64, 64, 64)),0,0.4)  # creates the message text
        self.speed_complete_message = py.transform.rotozoom(self.parent.font.render(("Your time is:"), False,
                                                       (64, 64, 64)),0,3)  # creates the message text
        self.speed_complete_message_rect = self.speed_complete_message.get_rect(center=(700, 100))

        row_count = 0  # creates the tiles needed in the levels
        for rows in self.world_data:
            column_count = 0
            for tiles in rows:
                tile = 0
                if tiles == 1:  # creates dirt tiles
                    tile = Surface(self, self.dirt, (50, 50))
                    tile.rect.x = column_count * 50
                    tile.rect.y = row_count * 50
                elif tiles == 2:  # creates grass tiles
                    tile = Surface(self, self.grass, (50, 50))
                    tile.rect.x = column_count * 50
                    tile.rect.y = row_count * 50
                elif tiles == 3:  # creates the goal
                    self.goal = Surface(self, self.goal_image, (50, 50))
                    self.goal.rect.x = column_count * 50
                    self.goal.rect.y = row_count * 50
                elif tiles == 4:  # creates a slime
                    slime = Slime(self, "l")
                    slime.rect.x = column_count * 50
                    slime.rect.y = row_count * 50
                    slime.rect.y += 20
                    self.slime_list.append(slime)
                elif tiles == 5:  # creates a slime
                    slime = Slime(self, "r")
                    slime.rect.x = column_count * 50
                    slime.rect.y = row_count * 50
                    slime.rect.y += 20
                    slime.rect.x += 20
                    self.slime_list.append(slime)
                elif tiles == 6:  # creates lava
                    lava = Surface(self, self.lava_image,(50, 20))
                    lava.rect.x = column_count * 50
                    lava.rect.y = row_count * 50
                    lava.rect.y += 30
                    self.lava_list.append(lava)
                elif tiles == 7: # creates a horizontal platform
                    tile = Platform(self, self.platform_image, (50, 25), 1, 1)
                    tile.rect.x = column_count * 50
                    tile.rect.y = row_count * 50
                    tile.orig_pos = tile.rect.center
                elif tiles == 8: # creates a horizontal platform
                    tile = Platform(self, self.platform_image, (50, 25), 1, -1)
                    tile.rect.x = column_count * 50
                    tile.rect.y = row_count * 50
                    tile.orig_pos = tile.rect.center
                elif tiles == 9:  # creates a vertical platform
                    tile = Platform(self, self.platform_image, (50, 25), 0, 1)
                    tile.rect.x = column_count * 50
                    tile.rect.y = row_count * 50
                    tile.orig_pos = tile.rect.center
                elif tiles == 10:  # creates a vertical platform
                    tile = Platform(self, self.platform_image, (50, 25), 0, -1)
                    tile.rect.x = column_count * 50
                    tile.rect.y = row_count * 50
                    tile.orig_pos = tile.rect.center
                if tile != 0:
                    self.tile_list.append(tile)
                column_count += 1
            row_count += 1
        if not isinstance(parent, object):
            print("Levels Game class not passed")
        if not isinstance(number, int):
            print("Number is not an integer")

    def draw(self):  # draws the levels
        if not self.level_complete:
            self.parent.screen.fill(py.Color((50, 150, 200)))
            for tile in self.tile_list:
                tile.draw()
            for lava in self.lava_list:
                lava.draw()
            self.goal.draw()
            for slime in self.slime_list:
                slime.draw()
            self.player.draw()
            self.ball_removal()
            self.r_reset()
            self.time += 1
            if self.parent.speedrun_page.speed_start:  # displays time in minutes
                time = str(self.parent.speedrun_page.minute_conversion(round(self.time/60, 1)))
            else:  # displays time in seconds
                time = str(round(self.time / 60, 1))
            time_surface = self.parent.font.render(time, False,
                                                       (64, 64, 64))
            self.parent.screen.blit(time_surface, self.time_rect)
            for counters in self.counter_centers:  # draws the counters
                py.draw.circle(self.parent.screen,
                               "orange", counters, 20)
            if self.game_over:  # checks for a game over
                self.reset()
        else:  # draws level complete screen
            if not self.parent.speedrun_page.speed_start:
                py.draw.rect(self.parent.screen, (255, 239, 222),(400, 200, 600, 300))
                self.parent.screen.blit(self.complete_surface, self.complete_rect)
                self.parent.screen.blit(self.medal, self.medal_rect)
                if self.ball_message_active:
                    self.parent.screen.blit(self.ball_message, (402, 340, 1,1))
                if self.time_message_active:
                    self.parent.screen.blit(self.time_message, (402, 320, 1,1))
                for buttons in self.complete_buttons:
                    self.parent.screen.blit(buttons.text, buttons.rect)
                    buttons.getpressed(self.parent.mouse_pos)
                if self.complete_buttons[0].get_pressed:
                    self.reset()
                if self.complete_buttons[1].get_pressed:
                    if self.level_number < 4:
                        self.level_number += 1
                        pickle_in = open(f"levels/level{self.level_number}_data", "rb")
                        self.world_data = pickle.load(pickle_in)
                        pickle_in = open(f"times/level{self.level_number}_time", "rb")
                        self.objective_time = pickle.load(pickle_in)
                        time = str(self.objective_time / 60)
                        self.time_message = py.transform.rotozoom(self.parent.font.render(("Beat the level in under "+time+
                                                                    " seconds"), False,
                                                                    (64, 64, 64)),0,0.4)  # creates the message text
                        self.reset()
                    else:
                        self.parent.escape(0)
                for buttons in self.complete_buttons:
                    buttons.reset()
            else:
                if self.level_number < 4:
                    self.level_number += 1
                    pickle_in = open(f"levels/level{self.level_number}_data", "rb")
                    self.world_data = pickle.load(pickle_in)
                    pickle_in = open(f"times/level{self.level_number}_time", "rb")
                    self.objective_time = pickle.load(pickle_in)
                    self.reset()
                else:  # speedrun complete page displays
                    self.parent.screen.fill(py.Color((50, 150, 200)))
                    self.parent.screen.blit(self.speed_complete_message,self.speed_complete_message_rect)
                    time = str(self.parent.speedrun_page.minute_conversion(round(self.time / 60, 1)))
                    time_surface = py.transform.rotozoom(self.parent.font.render(time, False,
                                                           (64, 64, 64)), 0,2)
                    time_rect = time_surface.get_rect(center=(700, 225))
                    self.parent.screen.blit(time_surface,time_rect)
                    speed_leave_message = py.transform.rotozoom(
                        self.parent.font.render(("Press Enter For Scoreboard"), False,
                                                (64, 64, 64)), 0, 1)  # creates the message text
                    speed_leave_message_rect = self.speed_complete_message.get_rect(center=(750, 500))
                    self.parent.screen.blit(speed_leave_message, speed_leave_message_rect)
                    keys = py.key.get_pressed()
                    if keys[py.K_RETURN]:
                        self.parent.speedrun_page.speed_start = False
                        self.parent.mouse_pos = (0,0)
                        self.parent.speedrun_page.scoreboard_update(round(self.time/60, 1))

    def ball_removal(self):  # destroys balls if they hit lava
        count = 0
        for balls in self.player.ball_list:
            for lava in self.lava_list:
                if balls.rect.colliderect(lava):
                    self.player.ball_list.pop(count)
                    break
            count += 1

    def r_reset(self):  # resets the level when r is pressed
        keys = py.key.get_pressed()
        if keys[py.K_r] and self.r_up:
            self.reset()
            self.r_up = False
        if not keys[py.K_r]:
            self.r_up = True
    def reset(self):  # resets the level variables
        self.counter_centers = [(175, 25), (125, 25), (75, 25), (25, 25)]
        self.ball_message_active = False
        self.time_message_active = False
        if not self.parent.speedrun_page.speed_start:
            self.time = 0
        self.medal = 1
        self.parent.mouse_pos = (0, 0)
        self.level_complete = False
        self.game_over = False
        self.parent.shooting = False
        self.player.rect.x = 50
        self.player.rect.y = 600
        self.player.ball_number = 0
        self.player.ball_list = []
        self.slime_list = []
        self.lava_list = []
        self.tile_list = []
        row_count = 0  # creates the tiles needed in the levels
        for rows in self.world_data:
            column_count = 0
            for tiles in rows:
                tile = 0
                if tiles == 1:  # creates dirt tiles
                    tile = Surface(self, self.dirt, (50, 50))
                    tile.rect.x = column_count * 50
                    tile.rect.y = row_count * 50
                elif tiles == 2:  # creates grass tiles
                    tile = Surface(self, self.grass, (50, 50))
                    tile.rect.x = column_count * 50
                    tile.rect.y = row_count * 50
                elif tiles == 3:  # creates the goal
                    self.goal = Surface(self, self.goal_image, (50, 50))
                    self.goal.rect.x = column_count * 50
                    self.goal.rect.y = row_count * 50
                elif tiles == 4:  # creates a slime
                    slime = Slime(self, "l")
                    slime.rect.x = column_count * 50
                    slime.rect.y = row_count * 50
                    slime.rect.y += 20
                    slime.orig_pos = slime.rect.topleft
                    self.slime_list.append(slime)
                elif tiles == 5:  # creates a slime
                    slime = Slime(self, "r")
                    slime.rect.x = column_count * 50
                    slime.rect.y = row_count * 50
                    slime.rect.y += 20
                    slime.rect.x += 20
                    slime.orig_pos = slime.rect.topleft
                    self.slime_list.append(slime)
                elif tiles == 6:  # creates lava
                    lava = Surface(self, self.lava_image, (50, 20))
                    lava.rect.x = column_count * 50
                    lava.rect.y = row_count * 50
                    lava.rect.y += 30
                    self.lava_list.append(lava)
                elif tiles == 7:  # creates a horizontal platform
                    tile = Platform(self, self.platform_image, (50, 25), 1, 1)
                    tile.rect.x = column_count * 50
                    tile.rect.y = row_count * 50
                    tile.orig_pos = tile.rect.center
                elif tiles == 8:  # creates a horizontal platform
                    tile = Platform(self, self.platform_image, (50, 25), 1, -1)
                    tile.rect.x = column_count * 50
                    tile.rect.y = row_count * 50
                    tile.orig_pos = tile.rect.center
                elif tiles == 9:  # creates a vertical platform
                    tile = Platform(self, self.platform_image, (50, 25), 0, 1)
                    tile.rect.x = column_count * 50
                    tile.rect.y = row_count * 50
                    tile.orig_pos = tile.rect.center
                elif tiles == 10:  # creates a vertical platform
                    tile = Platform(self, self.platform_image, (50, 25), 0, -1)
                    tile.rect.x = column_count * 50
                    tile.rect.y = row_count * 50
                    tile.orig_pos = tile.rect.center
                if tile != 0:
                    self.tile_list.append(tile)
                column_count += 1
            row_count += 1

class Player:  # contains the player characters movement and display
    """
    The Player class manages the creation, rendering, and logic of the player character in the game

    Attributes:
    parent (class): Holds reference to the Levels class
    player_image1_right (pygame.Surface): The first image of the player walking right
    player_image2_right (pygame.Surface): The second image of the player walking right
    player_image1_left (pygame.Surface): The first image of the player walking left
    player_image2_left (pygame.Surface): The second image of the player walking left
    player_jump_right (pygame.Surface): The image of the player jumping to the right
    player_jump_left (pygame.Surface): The image of the player jumping to the left
    player_image_list (list): A list holding all the player images for animations.
    image_index (int): Index to control the currently displayed image from player_image_list
    gravity (int): The gravity value that controls player vertical movement and jump physics
    rect (Rect): Rectangle used to define the position of the player and used in collisions
    jumping (bool): checks if the player is currently jumping
    face (str): Direction the player is facing
    rect_width (int): The width of the player's rectangle
    rect_height (int): The height of the player's rectangle
    bottom_collision (bool): Checks if the player is standing on a solid surface
    ball_list (list): A list that holds instances of Ball objects that the player throws
    ball_number (int): The number of balls currently in play

    Methods:
    player_input: This registers the input for the players movement and changes the player characters rectangle this is
    also where the x_collisions and y_collisions functions are called.

    draw: Draws the player depending on what action they are carrying out and calls the player input, balls and enemy
    collision function are called.

    Y_collisions: checks for vertical collisions and adjusts the players rectangle and velocity accordingly
                Args:
                my (int): Holds how far the player was going to move in the y direction
                gravity (int) Holds how much gravity will be added to the player rectangle this frame

    x_collisions: checks for horizontal collisions and adjusts the players rectangle and velocity accordingly
                Args:
                mx (int): Holds how far teh player was going to move in the x direction

    balls: checks if the mouse button has been pressed and creates a ball, it also draws the balls and calls the ball
    calculation fucntions before the balls are created

    ball_calculation: checks where the mouse was when the mouse button was pressed and then calculates the x and y
    velocity needed to move in  the direction of the mouse

    enemy_collision: checks if the player has collided with a slime or lava and resets the level if they have
    """

    def __init__(self,parent):
        self.parent = parent
        self.player_image1_right = py.transform.rotozoom(py.image.load("player/player_walk_1.png").convert_alpha(),0,0.6)
        self.player_image2_right = py.transform.rotozoom(py.image.load("player/player_walk_2.png").convert_alpha(),0,0.6)
        self.player_image1_left = py.transform.flip(self.player_image1_right, True, False)
        self.player_image2_left = py.transform.flip(self.player_image2_right, True, False)
        self.player_jump_right = py.transform.rotozoom(py.image.load("player/jump.png").convert_alpha(),0,0.6)
        self.player_jump_left = py.transform.flip(self.player_jump_right, True,False)
        self.player_image_list = [self.player_image2_right,self.player_image1_right,self.player_image2_left,
                                  self.player_image1_left, self.player_jump_right, self.player_jump_left]
        self.image_index = 1  # controls what image is displayed
        self.gravity = 0
        self.rect = self.player_image1_left.get_rect(topleft=(50, 600))
        self.jumping = False
        self.face = "r"
        self.rect_width = self.player_image1_left.get_width()
        self.rect_height = self.player_image1_left.get_height()
        self.bottom_collision = True
        self.ball_list = []
        self.ball_number = 0
        if not isinstance(parent, Levels):
            print("players levels class not passed")

    def player_input(self):  # controls the inputs
        mx = 0
        my = 0
        keys = py.key.get_pressed()
        if keys[py.K_SPACE] and not self.jumping and self.bottom_collision:
            if self.parent.parent.settings_page.jump_fx:
                self.parent.parent.jump_fx.play()
            self.gravity = -12
            self.jumping = True
            self.bottom_collision = False
        if not keys[py.K_SPACE]:
            self.jumping = False
        if keys[py.K_d]:
            mx += 5
        if keys[py.K_a]:
            mx -= 5
        self.gravity += 1
        if self.gravity > 20:
            self.gravity = 20
        my += self.gravity
        self.bottom_collision = False 
        collect = self.y_collisions(my, self.gravity)
        my = collect[0]
        self.gravity = collect[1]
        mx = self.x_collisions(mx)
        if my == -20:
            self.gravity = my
        self.rect.x += mx
        self.rect.y += my

    def draw(self):  # draws player character depending on what their movement is
        self.player_input()  # controls players movement
        keys = py.key.get_pressed()
        if self.gravity < 0:  # displays jumping sprite
            if self.face == "r":
                self.image_index = 4
            elif self.face == "l":
                self.image_index = 5
        elif keys[py.K_d] and self.bottom_collision:  # displays right walk
            if self.image_index > 1.8:
                self.image_index = 0
            self.image_index += 0.2
            self.face = "r"
        elif keys[py.K_a] and self.bottom_collision:  # displays left walk
            if self.image_index > 3.8:
                self.image_index = 2
            self.image_index += 0.2
            self.face = "l"
        if self.bottom_collision and self.face == "r" and not keys[py.K_a] and not keys[py.K_d]:
            self.image_index = 1
        elif self.bottom_collision and self.face == "l" and not keys[py.K_a] and not keys[py.K_d]:
            self.image_index = 3
        index = int(self.image_index)  # makes sure the index is not a float
        self.parent.parent.screen.blit(self.player_image_list[index], self.rect)
        self.balls()  # controls balls
        self.enemy_collisions()

    def y_collisions(self,my,gravity):  # holds all the outcomes of the player y collision events
        for tile in self.parent.tile_list:  # checks for collision in the y direction
            if tile.type == 3 or tile.type == 1:
                if tile.rect.colliderect((self.rect.x, self.rect.y + my,self.rect_width,self.rect_height)):
                    if gravity < 0:  # checks for jumping collisions
                        my = tile.rect.bottom - self.rect.top
                        gravity = 0
                    if gravity > 0:  # checks for falling collisions
                        my = tile.rect.top - self.rect.bottom
                        self.bottom_collision = True
                        if tile.type == 1:  # checks if falling on a horizontal moving platform
                            self.rect.x += tile.speed
                        gravity = 0
            elif tile.type == 0:  # checks if the player is colliding with a vertical moving block
                if tile.rect.colliderect((self.rect.x, self.rect.y + my,self.rect_width,self.rect_height)):
                    if gravity < 0:  # checks for jumping collisions
                        my = tile.rect.bottom - self.rect.top
                        gravity = 0
                    if gravity > 0:  # checks for falling collisions
                        my = tile.rect.top - self.rect.bottom - 1
                        self.bottom_collision = True
                        if tile.type == 0 and tile.speed > 0:
                            self.rect.y += tile.speed
                        gravity = 0
        package = (my,gravity)
        return package

    def x_collisions(self,mx): # holds all the outcomes of the player x collision events
        for tile in self.parent.tile_list:  # checks for collision in the x direction
            if tile.rect.colliderect((self.rect.x + mx, self.rect.y, self.rect_width, self.rect_height)):
                mx = 0
        return mx

    def balls(self):  # draws and creates the balls
        if self.parent.parent.shooting and self.ball_number < 4:
            if self.parent.parent.settings_page.throw_fx:
                self.parent.parent.throw_fx.play()
            new_id = 0
            for x in self.ball_list:
                new_id += 1
            direction = self.ball_calculation()
            ball = Ball(self, self.rect.center[0],self.rect.center[1],10,"orange",
                        0.7, direction[0], direction[1], new_id)
            self.ball_list.append(ball)
            self.ball_number += 1
            self.parent.counter_centers.pop(0)
            self.parent.parent.shooting = False
        for balls in self.ball_list:
            balls.draw()

    def ball_calculation(self):  # calculates direction the ball will be shot
        x_direct = self.parent.parent.mouse_pos[0] - self.rect.center[0]
        y_direct = self.parent.parent.mouse_pos[1] - self.rect.center[1]
        x_neg = 1
        y_neg = 1
        if x_direct < 0:
            x_neg = -1
        if y_direct < 0:
            y_neg = -1
        square_x = x_direct**2
        square_y = y_direct**2
        orig_total = square_x + square_y
        x_percent = square_x / orig_total
        y_percent = square_y / orig_total
        new_x = math.sqrt(250 * x_percent)
        new_y = math.sqrt(250 * y_percent)
        new_x = new_x * x_neg
        new_y = new_y * y_neg
        package = (new_x, new_y)
        return package

    def enemy_collisions(self):  # detects if the player has collided with an obstacle and creates a game over if true
        for slime in self.parent.slime_list:  # checks for slime collisions
            if self.rect.colliderect(slime.rect):
                if self.parent.parent.settings_page.death_fx:
                    self.parent.parent.game_over_fx.play()
                self.parent.game_over = True
        for lava in self.parent.lava_list:
            if self.rect.colliderect(lava.rect):  # checks for lava collisions:
                self.parent.game_over = True
                if self.parent.parent.settings_page.death_fx:
                    self.parent.parent.game_over_fx.play()

class Surface:  # Creates the flat platforms
    """
    The Surface Class creates the surfaces the player can interact with

    Attributes:
    parent (class): Holds reference to the levels class
    image (pygame.Surface): Holds the image of the tile
    rect (pygame.rect): Rectangle that defines the position of the tile and collision detection of the box of the tile
    type (int): Used to define whether this is a stationary, horizontal or vertical moving block

    Methods:
    draw: Displays the tile on the screen
    """
    def __init__(self,parent, image, size):
        self.parent = parent
        self.image = py.transform.scale(image, size)
        self.rect = self.image.get_rect()
        self.type = 3
        if not isinstance(parent, object):
            print("Surface parent class not passed")
        if not isinstance(size, tuple):
            print("Surface size is not a tuple")
    def draw(self):
        self.parent.parent.screen.blit(self.image, self.rect)

    def move(self):
        pass

class Ball:
    """
    The ball class manages the creation, rendering, and logic of the ball in the game

    Attributes:
    parent (class): Holds reference to the player class
    x_pos (int): Holds the x position of the ball
    y_pos (int): Holds the y position of the ball
    radius (int): Holds the radius of the ball
    colour (RGB): Holds the RGB value for the ball
    retention (float): Holds how much of the ball's velocity will be retained after a bounce
    x_speeed (int): Holds how far the ball will move horizontally this frame
    y_speed (int): Holds how far the ball will move vertically this frame
    id (int): holds the position of the ball in the Player Class's ball list
    on_floor (bool): holds if the ball is in contact with a floor
    gravity (int): The gravity value that controls ball vertical movement and bounce physics
    stop_bounce (int): This is the value that the y velocity has to get to for the ball to stop moving
    momentum (int): Takes in the y speed before processing the y speed in collisions, so they can be compared
    goal_top_pass (bool): Tells the game if the ball has gone through the top of the goal
    rect (pygame.Rect) Rectangle used in collision detection

    Methods:
    draw: Draws the ball. Calls the friction, x_collisions, y collisions, goal_collisons and move functions

    move: Adds the final x and y speed onto the balls x and y pos

    friction: Decreases the absolute value of the x velocity over time

    x_collisions: Checks for horizontal collisions and adjusts the balls velocity accordingly

    y_collisions: Checks for vertical collisions and adjusts the balls velocity accordingly

    goal_collisions: Checks if the ball has gone through the top and bottom of the hoop and then turns the level
    complete variable to true if this occurs
    """
    def __init__(self, parent, x_pos, y_pos, radius, colour, retention, x_speed, y_speed, id):
        self.parent = parent
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.radius = radius
        self.colour = colour
        self.retention = retention
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.id = id
        self.circle = ""
        self.on_floor = False
        self.gravity = 0.5
        self.stop_bounce = 1
        self.momentum = y_speed
        self.goal_top_pass = False
        self.rect = py.Rect(self.x_pos - self.radius, self.y_pos - self.radius, self.radius * 2, self.radius * 2)
        self.count = 0
        if not isinstance(parent, object):
            print("ball parent class not passed")
        if not isinstance(x_pos, int):
            print("ball x_pos is not an integer")
        if not isinstance(y_pos, int):
            print("ball y_pos is not an integer")
        if not isinstance(radius, int):
            print("ball radius is not an integer")
        if not isinstance(retention, float):
            print("ball retention is not a float")

    def draw(self):
        self.rect = py.Rect(self.x_pos - self.radius, self.y_pos - self.radius, self.radius * 2, self.radius * 2)
        self.friction()
        self.x_collisions()
        self.y_collisions()
        self.goal_collisions()
        self.move()
        # draws the ball
        self.circle = py.draw.circle(self.parent.parent.parent.screen,
                                     self.colour, (self.x_pos, self.y_pos), self.radius)

    def move(self):
        self.x_pos += self.x_speed
        self.y_pos += self.momentum
        self.y_speed = self.momentum

    def friction(self):  # slows ball down in the x direction
        if self.x_speed < 0:
            self.x_speed += 0.02
        elif self.x_speed > 0:
            self.x_speed -= 0.02
        else:
            self.x_speed = self.x_speed

    def x_collisions(self):  # holds all the outcomes of the ball x collision events
        for tile in self.parent.parent.tile_list:  # checks for collision in the x direction
            if self.y_speed > 0:  # checks for upwards collisions
                if tile.rect.colliderect((self.x_pos - self.radius + self.x_speed, self.y_pos - self.radius - 2, self.radius * 2, self.radius * 2)):
                    self.x_speed = self.x_speed * -1 * self.retention
            else:
                if tile.rect.colliderect((self.x_pos - self.radius + self.x_speed, self.y_pos - self.radius + 2, self.radius * 2, self.radius * 2)):
                    self.x_speed = self.x_speed * -1 * self.retention
        if self.parent.parent.goal.rect.colliderect((self.x_pos - self.radius + self.x_speed, self.y_pos - self.radius,
                                              self.radius * 2, self.radius * 2)):
            self.x_speed = self.x_speed * -1 * self.retention

    def y_collisions(self):  # holds all the outcomes of the ball y collision events
        self.momentum += self.gravity
        for tile in self.parent.parent.tile_list:  # checks for collision in the y direction
            if tile.rect.colliderect((self.x_pos - self.radius,
                                      self.y_pos - self.radius + self.y_speed, self.radius * 2, self.radius * 2)):
                if self.gravity == 0:
                    if tile.type == 1:  # checks if falling on a horizontal moving platform
                        self.x_pos += tile.speed
                    if tile.type == 0:
                        self.y_pos += tile.speed
                if self.y_speed < 0:  # checks for upwards collisions
                    self.momentum = self.momentum * -1 * self.retention
                    self.on_floor = True
                if self.y_speed > 0:  # checks for falling collisions
                    self.momentum = self.momentum * -1 * self.retention
                    if abs(self.momentum) < self.stop_bounce:  # makes it so the ball doesn't bounce forever
                        self.momentum = 0
                        self.gravity = 0
                        self.x_speed = 0
                    self.on_floor = True
            else:
                self.on_floor = False
            if self.on_floor:
                break

    def goal_collisions(self):
        if self.rect.colliderect((self.parent.parent.goal.rect.left, self.parent.parent.goal.rect.top, 50, 20)):
            self.goal_top_pass = True
        if self.goal_top_pass:
            if self.rect.colliderect((self.parent.parent.goal.rect.left, self.parent.parent.goal.rect.bottom, 50, 20)):
                self.parent.parent.level_complete = True
                if self.parent.parent.parent.settings_page.level_complete_fx:
                    self.parent.parent.parent.level_complete_fx.play()
                if self.parent.ball_number == 1:
                    self.parent.parent.medal += 1
                else:
                    self.parent.parent.ball_message_active = True
                if self.parent.parent.time < self.parent.parent.objective_time:
                    self.parent.parent.medal += 1
                else:
                    self.parent.parent.time_message_active = True
                if self.parent.parent.medal == 1:
                    self.parent.parent.medal = self.parent.parent.bronze_image
                elif self.parent.parent.medal == 2:
                    self.parent.parent.medal = self.parent.parent.silver_image
                elif self.parent.parent.medal == 3:
                    self.parent.parent.medal = self.parent.parent.gold_image

class Slime:
    """
    The Slime class manages the creation, rendering, and logic of the slimes in the game

    Attributes:
    parent (class): Holds reference to the levels class
    image (pygame.Surface): Holds the image of the slime
    rect (pygame.Rect): Rectangle that defines the position of the slime and used for collision detection
    rect_width (int): The width of the slimes rectangle
    rect_height (int): The height of the slimes rectangle
    bottom collision (bool): Holds if the slime is on the floor
    x_speed (int): Holds how far the slime is about to move horizontally
    y_speed (int): Holds how far the slime is about to move vertically
    gravity (int): Holds the gravity that will be added to the slimes y position each frame
    friction (int): added onto the x speed to slow the slimes x velocity when it jumps
    count (int): stops the slime from acting for a second
    direction (sting): Holds what direction the slime is going to jump
    start_up (bool): Holds if it has been a second since the slimes creation

    Methods:
    draw: Draws the slime and calls the move function

    y_collisions: checks for vertical collisions and adjusts the slimes rectangle and velocity accordingly
                Args:
                my (int): Holds how far the slime was going to move in the y direction

    x_collisions: checks for horizontal collisions and adjusts the players rectangle and velocity accordingly
                Args:
                mx (int): Holds how far teh player was going to move in the x direction

    move: Calls the x and y collision functions and then makes the slime jump left and then right eaual distance
    """
    def __init__(self,parent, direction):  # creates enemy attributes
        self.parent = parent
        self.image = py.transform.scale(py.image.load("images/blob.png").convert_alpha(), (30, 30))
        self.rect = self.image.get_rect()
        self.rect_width = self.image.get_width()
        self.rect_height = self.image.get_height()
        self.bottom_collision = False
        self.x_speed = 10
        self.y_speed = 0
        self.gravity = 2
        self.friction = -1
        self.count = 0
        self.direction = direction
        self.start_up = False
        if not isinstance(parent, object):
            print("slime class not passed")
    def draw(self):  # displays slime
        self.move()
        self.parent.parent.screen.blit(self.image, self.rect)

    def y_collisions(self, my):  # holds all the outcomes of the slime y collision events
        for tile in self.parent.tile_list:  # checks for collision in the y direction
            if tile.rect.colliderect((self.rect.x, self.rect.y + my, self.rect_width, self.rect_height)):
                if self.y_speed < 0:  # checks for jumping collisions
                    my = tile.rect.bottom - self.rect.top
                if self.y_speed > 0:  # checks for falling collisions
                    my = tile.rect.top - self.rect.bottom
                    self.bottom_collision = True
        return my

    def x_collisions(self, mx):  # holds all the outcomes of the slime x collision events
        for tile in self.parent.tile_list:  # checks for collision in the x direction
            if tile.rect.colliderect((self.rect.x + mx, self.rect.y, self.rect_width, self.rect_height)):
                mx = 0
        return mx
    def move(self):
        self.count += 1 # makes teh slime wait a second to jump
        if self.count == 60 and self.bottom_collision: # makes the slime jump
            self.y_speed = -10
            self.count = 0
            self.start_up = True
            self.bottom_collision = False
            if self.direction == "l":  # makes the slime go left then sets it to go right the next jump
                self.x_speed = -10
                self.friction = 0.1
                self.direction = "r"
            elif self.direction == "r":  # makes the slime go right then sets it to go left next jump
                self.x_speed = 10
                self.friction = -0.105
                self.direction = "l"

        self.y_speed = self.y_collisions(self.y_speed)  # calculates y collisions
        if self.bottom_collision:
            self.gravity = 0
        else:
            self.gravity = 2
        self.y_speed += self.gravity
        self.x_speed = self.x_collisions(self.x_speed)  # calculates x collisions
        if self.start_up:  # waits for first jump to start movement
            if not self.bottom_collision:
                self.x_speed += self.friction
                self.rect.x += self.x_speed
            self.rect.y += self.y_speed

class Platform(Surface):
    """
    Subclass inheriting from the Surface Class that creates moving platforms

    Attributes:
    type (int): Used to define whether this is a stationary, horizontal or vertical moving block
    speed (int): This is how many pixels the platform will move per frame
    orig_pos (tuple): The platform will only move 50 pixels left or right of this position

    Methods:
    draw: Draws the platform on the screen and calls the move function

    move: adds the speed onto the x or y of the platform depending on the type and then when the platform gets 50 pixels
    away from the original position it reverses then speed
    """
    def __init__(self, parent, image, size, type, speed):
        super().__init__(parent, image, size)
        self.type = type
        self.speed = speed
        self.orig_pos = (0, 0)

    def draw(self):
        self.move()
        self.parent.parent.screen.blit(self.image, self.rect)

    def move(self):
        if self.type:
            self.rect.x += self.speed
            if self.rect.center[0] > self.orig_pos[0] + 50:
                self.speed = self.speed * -1
            if self.rect.center[0] < self.orig_pos[0] - 50:
                self.speed = self.speed * -1
        else:
            self.rect.y += self.speed
            if self.rect.center[1] > self.orig_pos[1] + 50:
                self.speed = self.speed * -1
            if self.rect.center[1] < self.orig_pos[1] - 50:
                self.speed = self.speed * -1

class Speedrun:
    """
    The Speedrun class displays the scoreboard and updates it when the speedrun is completed

    Attributes:
    parent (class): This holds reference to the game class
    title_surface (pygame.Surface): Message surface telling the player this is the scoreboard page
    time_list (list): list that holds the speedrun times
    score_5 (pygame.Surface): Surface that displays time 5
    score_4 (pygame.Surface): Surface that displays time 4
    score_3 (pygame.Surface): Surface that displays time 3
    score_2 (pygame.Surface): Surface that displays time 2
    score_1 (pygame.Surface): Surface that displays time 1
    play_button (Button): Button object that will start the speedrun when pressed
    score_1_rect (pygame.Rect): Rectangle that defines the position of the score_1 surface
    score_2_rect (pygame.Rect): Rectangle that defines the position of the score_2 surface
    score_3_rect (pygame.Rect): Rectangle that defines the position of the score_3 surface
    score_4_rect (pygame.Rect): Rectangle that defines the position of the score_4 surface
    score_5_rect (pygame.Rect): Rectangle that defines the position of the score_5 surface
    title_rect (pygame.Rect): Rectangle that defines the position of the title_surface
    speed_start (bool): Tracks if the speedrun is active

    Methods:
    minute_conversion: changes the time from seconds to minutes
                     Args:
                     time (int): the time in seconds

    draw: Draws the scoreboard and calls and play_check function if the speed_active is False and draws the levels if
    it's true

    play_check: checks if the play_button has been pressed

    scoreboard_update: updates the score files and surfaces if the player gets within their top 5 times
    """
    def minute_conversion(self, time):  # converts seconds to minutes
        minute = str(int(time//60))
        second = str(round(time % 60, 1))
        if time != 0:
            if float(second) < 10:
                new_time = minute + ": 0" + second
            else:
                new_time = minute + ": " + second
        else:
            new_time = "--: --"
        return new_time

    def __init__(self, parent):
        self.parent = parent
        self.title_surface = py.transform.rotozoom(self.parent.font.render("Scoreboard", False,
                                                     (64, 64, 64)),0,2 ) # creates the message text
        self.time_list = []
        pickle_in = open("speedrun times/speedrun_time5", "rb")
        self.time_list.append(pickle.load(pickle_in))
        time = self.minute_conversion(float(self.time_list[0]))
        self.score_5 = py.transform.rotozoom(self.parent.font.render(time, False, (64, 64, 64)),0,2)
        pickle_in = open("speedrun times/speedrun_time4", "rb")
        self.time_list.append(pickle.load(pickle_in))
        time = self.minute_conversion(float(self.time_list[1]))
        self.score_4 = py.transform.rotozoom(self.parent.font.render(time, False, (64, 64, 64)),0,2)
        pickle_in = open("speedrun times/speedrun_time3", "rb")
        self.time_list.append(pickle.load(pickle_in))
        time = self.minute_conversion(float(self.time_list[2]))
        self.score_3 = py.transform.rotozoom(self.parent.font.render(time, False, (64, 64, 64)),0,2)
        pickle_in = open("speedrun times/speedrun_time2", "rb")
        self.time_list.append(pickle.load(pickle_in))
        time = self.minute_conversion(float(self.time_list[3]))
        self.score_2 = py.transform.rotozoom(self.parent.font.render(time, False, (64, 64, 64)),0,2)
        pickle_in = open("speedrun times/speedrun_time1", "rb")
        self.time_list.append(pickle.load(pickle_in))
        time = self.minute_conversion(float(self.time_list[4]))
        self.score_1 = py.transform.rotozoom(self.parent.font.render(time, False, (64, 64, 64)),0,2)
        self.play_button = Button(1000, 500, "images/play.png", self)
        self.score_1_rect = self.score_1.get_rect(center=(700, 200))
        self.score_2_rect = self.score_2.get_rect(center=(700, 300))
        self.score_3_rect = self.score_3.get_rect(center=(700, 400))
        self.score_4_rect = self.score_4.get_rect(center=(700, 500))
        self.score_5_rect = self.score_5.get_rect(center=(700, 600))
        self.title_rect = self.title_surface.get_rect(center=(700, 100))  # creates where text will be placed
        self.speed_start = False
        if not isinstance(parent, object):
            print("speedrun class not passed")

    def draw(self):  # displays speedrun page
        if not self.speed_start:
            self.play_check()
            self.parent.screen.fill(py.Color((58, 140, 250)))
            self.parent.screen.blit(self.title_surface, self.title_rect)
            py.draw.rect(self.parent.screen, (0, 0, 0), (500, 115, 400, 10))
            self.parent.screen.blit(self.play_button.text, self.play_button.rect)
            self.parent.screen.blit(self.score_1, self.score_1_rect)
            self.parent.screen.blit(self.score_2, self.score_2_rect)
            self.parent.screen.blit(self.score_3, self.score_3_rect)
            self.parent.screen.blit(self.score_4, self.score_4_rect)
            self.parent.screen.blit(self.score_5, self.score_5_rect)
        else:
            self.parent.levels.draw()

    def play_check(self):  # checks if the play button has been pressed
        self.play_button.getpressed(self.parent.mouse_pos)
        if self.play_button.get_pressed:
            self.speed_start = True
            self.parent.levels = Levels(self.parent, 1)
        self.play_button.reset()

    def scoreboard_update(self, new_time):  # updates the scoreboard
        count = 1
        time_place = 6
        for times in self.time_list:  # checks where to place the new time
            if new_time < times or times == 0:
                time_place = count
            count += 1
        if time_place != 6:  # reloads all the scores
            self.time_list.insert(time_place, new_time)
            self.time_list.pop(0)
            time = self.minute_conversion(float(self.time_list[0]))
            self.score_5 = py.transform.rotozoom(self.parent.font.render(time, False, (64, 64, 64)), 0, 2)
            time = self.minute_conversion(float(self.time_list[1]))
            self.score_4 = py.transform.rotozoom(self.parent.font.render(time, False, (64, 64, 64)), 0, 2)
            time = self.minute_conversion(float(self.time_list[2]))
            self.score_3 = py.transform.rotozoom(self.parent.font.render(time, False, (64, 64, 64)), 0, 2)
            time = self.minute_conversion(float(self.time_list[3]))
            self.score_2 = py.transform.rotozoom(self.parent.font.render(time, False, (64, 64, 64)), 0, 2)
            time = self.minute_conversion(float(self.time_list[4]))
            self.score_1 = py.transform.rotozoom(self.parent.font.render(time, False, (64, 64, 64)), 0, 2)
            # loads the times back into the files
            with open("speedrun times/speedrun_time5", "wb") as file:
                pickle.dump(self.time_list[0], file)
            with open("speedrun times/speedrun_time4", "wb") as file:
                pickle.dump(self.time_list[1], file)
            with open("speedrun times/speedrun_time3", "wb") as file:
                pickle.dump(self.time_list[2], file)
            with open("speedrun times/speedrun_time2", "wb") as file:
                pickle.dump(self.time_list[3], file)
            with open("speedrun times/speedrun_time1", "wb") as file:
                pickle.dump(self.time_list[4], file)

class Settings:
    """
    The Settings class draws the settings page which allows the player to turn off sound effects and reset scoreboard

    Attributes:
    parent (class): holds reference to the game class
    buttons (list): list of all the button objects that will be on the settings page
    title_surface (pygame.Surface): Surface that holds a message telling the player this is the settings page
    title_rect (pygame.Rect): Rectangle that defines the position of the title_surface
    sound_surface (pygame.Surface): Surface that holds a message telling the player buttons on the left are for sound
    sound_rect (pygame.Surface): Rectangle that defines the position of the sound_surface
    jump_fx (bool): Tracks if the jump fx are active
    throw_fx (bool): Tracks if the throw fx are active
    death_fx (bool): Tracks if the death fx are active
    bg_music (bool): Tracks if the bg music is active
    level_complete_fx (bool): Tracks if the level complete fx are active
    score_set_surface (pygame.Surface): Surface of a message suggesting buttons on the right reset the scoreboard
    score_set_rect (pygame.Rect): Rectangle that defines the position of the score_set_surface
    on_surface (pygame.Surface): Surface that holds message on
    on_off_rect (pygame.Rect): Rectangle that defines the position of the on_surface and off_surface
    off_surface (pygame.Surface): Surface that holds the message off
    display_count (int): Counts for a second then turn off the on or off surface
    current_sound_state (pygame.Surface): Holds either the on or off surface depending on the state of the sound
    sure (bool): Tracks if the "are you sure" page is active
    sure_buttons (list): List of button objects that are on the "are you sure" page
    sure_text (pygame.Surface): Surface that asks the player if they are sure
    sure_text_rect (pygame.Rect): Rectangle that defines the position of the sure_text

    Methods:
    draw: Draws the settings page and calls the sound_control, are_you_sure, and display_on functions

    sound_control: Checks if any of the sound buttons have been pressed and changes the sound state accordingly

    score_reset: Removes all the times from the time_list, files and updates the score surfaces

    display_on: If the display_count is below 60 it displays the current_sound_state

    are_you_sure: This displays a page that asks the player if they are sure and the player can click yes or no
    """
    def __init__(self, parent):
        self.parent = parent
        self.buttons = [Button(250,400,"buttons/BG_music.jpg", self), Button(450,400,"buttons/jump.jpg", self),
                        Button(250,500,"buttons/throw.jpg", self), Button(450,500,"buttons/death.jpg", self),
                        Button(350,600, "buttons/complete_fx.png", self), Button(1050,400,"buttons/Reset.png", self)]
        self.title_surface = self.parent.font.render("Settings", False,
                                                       (64, 64, 64))  # creates the message text
        self.title_surface = py.transform.rotozoom(self.title_surface, 0, 3)  # makes message text bigger
        self.title_rect = self.title_surface.get_rect(center=(700, 100))  # creates where text will be placed
        self.sound_surface = self.parent.font.render("Sound", False,
                                                     (64, 64, 64))  # creates the message text
        self.sound_surface = py.transform.rotozoom(self.sound_surface, 0, 2)  # makes message text bigger
        self.sound_rect = self.title_surface.get_rect(center=(450, 350))  # creates where text will be placed
        self.jump_fx = True
        self.throw_fx = True
        self.death_fx = True
        self.bg_music = True
        self.level_complete_fx = True
        self.score_set_surface = self.parent.font.render("Scoreboard", False,
                                                     (64, 64, 64))  # creates the message text
        self.score_set_surface = py.transform.rotozoom(self.score_set_surface, 0, 2)  # makes message text bigger
        self.score_set_rect = self.title_surface.get_rect(center=(1050, 350))  # creates where text will be placed
        self.on_surface = self.parent.font.render("ON", False,
                                                     (64, 64, 64))  # creates the message text
        self.on_off_rect = self.on_surface.get_rect(center=(700, 350))  # creates where text will be placed
        self.off_surface = self.parent.font.render("OFF", False,
                                                  (64, 64, 64))  # creates the message text
        self.display_count = 60
        self.current_sound_state = self.on_surface
        self.sure = False  # holds if the player is in the "are you sure" page
        self.sure_buttons = [Button(877,440,"buttons/yes.png", self), Button(518,440,"buttons/no.png", self)]
        self.sure_text = py.transform.rotozoom(self.parent.font.render("Are You Sure?", False,
                                                  (64, 64, 64)),0,1.5)  # creates the message text
        self.sure_text_rect = self.sure_text.get_rect(center=(700, 250))  # creates where text will be placed

    def draw(self):
        self.parent.screen.fill(py.Color((58, 140, 250)))
        self.parent.screen.blit(self.title_surface, self.title_rect)
        self.parent.screen.blit(self.sound_surface, self.sound_rect)
        self.parent.screen.blit(self.score_set_surface,self.score_set_rect)
        for buttons in self.buttons:  # displays buttons
            self.parent.screen.blit(buttons.text, buttons.rect)
            buttons.getpressed(self.parent.mouse_pos)
        if not self.sure:
            self.sound_control()
        if self.buttons[5].get_pressed:
            self.sure = True
        self.are_you_sure()
        for buttons in self.buttons:
            buttons.reset()
        self.display_on()
        self.parent.mouse_pos = (0,0)

    def sound_control(self):
        if self.buttons[0].get_pressed:
            if self.bg_music:
                py.mixer.music.stop()
                self.bg_music = False
                self.current_sound_state = self.off_surface
                self.display_count = 0
            else:
                py.mixer.music.play(-1, 0.0, 5000)
                self.bg_music = True
                self.current_sound_state = self.on_surface
                self.display_count = 0
        if self.buttons[1].get_pressed:
            if self.jump_fx:
                self.jump_fx = False
                self.current_sound_state = self.off_surface
                self.display_count = 0
            else:
                self.jump_fx = True
                self.current_sound_state = self.on_surface
                self.display_count = 0
        if self.buttons[2].get_pressed:
            if self.throw_fx:
                self.throw_fx = False
                self.current_sound_state = self.off_surface
                self.display_count = 0
            else:
                self.throw_fx = True
                self.current_sound_state = self.on_surface
                self.display_count = 0
        if self.buttons[3].get_pressed:
            if self.death_fx:
                self.death_fx = False
                self.current_sound_state = self.off_surface
                self.display_count = 0
            else:
                self.death_fx = True
                self.current_sound_state = self.on_surface
                self.display_count = 0
        if self.buttons[4].get_pressed:
            if self.level_complete_fx:
                self.level_complete_fx = False
                self.current_sound_state = self.off_surface
                self.display_count = 0
            else:
                self.level_complete_fx = True
                self.current_sound_state = self.on_surface
                self.display_count = 0

    def score_reset(self):
        self.parent.speedrun_page.time_list = [0, 0, 0, 0, 0]
        with open("speedrun times/speedrun_time5", "wb") as file:
            pickle.dump(self.parent.speedrun_page.time_list[0], file)
        with open("speedrun times/speedrun_time4", "wb") as file:
            pickle.dump(self.parent.speedrun_page.time_list[1], file)
        with open("speedrun times/speedrun_time3", "wb") as file:
            pickle.dump(self.parent.speedrun_page.time_list[2], file)
        with open("speedrun times/speedrun_time2", "wb") as file:
            pickle.dump(self.parent.speedrun_page.time_list[3], file)
        with open("speedrun times/speedrun_time1", "wb") as file:
            pickle.dump(self.parent.speedrun_page.time_list[4], file)
        time = self.parent.speedrun_page.minute_conversion(float(self.parent.speedrun_page.time_list[0]))
        self.parent.speedrun_page.score_5 = py.transform.rotozoom(self.parent.font.render(time, False, (64, 64, 64)), 0, 2)
        time = self.parent.speedrun_page.minute_conversion(float(self.parent.speedrun_page.time_list[1]))
        self.parent.speedrun_page.score_4 = py.transform.rotozoom(self.parent.font.render(time, False, (64, 64, 64)), 0, 2)
        time = self.parent.speedrun_page.minute_conversion(float(self.parent.speedrun_page.time_list[2]))
        self.parent.speedrun_page.score_3 = py.transform.rotozoom(self.parent.font.render(time, False, (64, 64, 64)), 0, 2)
        time = self.parent.speedrun_page.minute_conversion(float(self.parent.speedrun_page.time_list[3]))
        self.parent.speedrun_page.score_2 = py.transform.rotozoom(self.parent.font.render(time, False, (64, 64, 64)), 0, 2)
        time = self.parent.speedrun_page.minute_conversion(float(self.parent.speedrun_page.time_list[4]))
        self.parent.speedrun_page.score_1 = py.transform.rotozoom(self.parent.font.render(time, False, (64, 64, 64)), 0, 2)

    def display_on(self):
        if self.display_count < 60:
            self.parent.screen.blit(self.current_sound_state, self.on_off_rect)
            self.display_count += 1
    def are_you_sure(self):
        # This is turns the "are you sure" screen on when the reset button has been pressed
        if self.sure:
            py.draw.rect(self.parent.screen, (255, 239, 222), (400, 200, 600, 300))
            self.parent.screen.blit(self.sure_text, self.sure_text_rect)
            for buttons in self.sure_buttons:
                self.parent.screen.blit(buttons.text, buttons.rect)
                buttons.getpressed(self.parent.mouse_pos)
            if self.sure_buttons[0].get_pressed:  # activates if yes is pressed
                self.score_reset()
                self.sure = False
            if self.sure_buttons[1].get_pressed:  # activates if no is pressed
                self.sure = False
            for buttons in self.sure_buttons:
                buttons.reset()


game = Game()
game.mainloop()