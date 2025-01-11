import pygame, random, math

# Dimension Definitions
SCREEN_WIDTH, SCREEN_HEIGHT = (800, 500)
PLATFORM_WIDTH, PLATFORM_HEIGHT = (2000, 2000)

# Other Definitions
NAME = "Agar.io Replicaish"

# Pygame initialization
pygame.init()
pygame.display.set_caption("{}".format(NAME))
clock = pygame.time.Clock()
try:
    font = pygame.font.Font("Ubuntu-B.ttf", 20)
    big_font = pygame.font.Font("Ubuntu-B.ttf", 24)
except:
    print("Font file not found: Ubuntu-B.ttf")
    font = pygame.font.SysFont('Ubuntu', 20, True)
    big_font = pygame.font.SysFont('Ubuntu', 24, True)

# Surface Definitions
MAIN_SURFACE = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
SCOREBOARD_SURFACE = pygame.Surface((95, 25), pygame.SRCALPHA)
LEADERBOARD_SURFACE = pygame.Surface((155, 278), pygame.SRCALPHA)
SCOREBOARD_SURFACE.fill((50, 50, 50, 80))
LEADERBOARD_SURFACE.fill((50, 50, 50, 80))

# Auxiliary Functions
def drawText(message, pos, color=(255, 255, 255)):
    """Blits text to main (global) screen."""
    MAIN_SURFACE.blit(font.render(message, 1, color), pos)

def getDistance(a, b):
    """Calculates Euclidean distance between given points."""
    diffX = math.fabs(a[0] - b[0])
    diffY = math.fabs(a[1] - b[1])
    return ((diffX ** 2) + (diffY ** 2)) ** (0.5)

# Auxiliary Classes
class Painter:
    """Used to organize the drawing/ updating procedure.
    Implementation based on Strategy Pattern.
    Note that Painter draws objects in a FIFO order.
    Objects added first, are always going to be drawn first.
    """

    def __init__(self):
        self.paintings = []

    def add(self, drawable):
        self.paintings.append(drawable)

    def paint(self):
        for drawing in self.paintings:
            drawing.draw()

class Camera:
    """Used to represent the concept of POV."""
    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        self.zoom = 0.5

    def centre(self, blobOrPos):
        """Makes sure that the given object will be at the center of player's view.
        Zoom is taken into account as well."""
        if isinstance(blobOrPos, Player):
            x, y = blobOrPos.x, blobOrPos.y
            self.x = (x - (x * self.zoom)) - x + (SCREEN_WIDTH / 2)
            self.y = (y - (y * self.zoom)) - y + (SCREEN_HEIGHT / 2)
        elif type(blobOrPos) == tuple:
            self.x, self.y = blobOrPos

    def update(self, target):
        self.zoom = 100 / (target.mass) + 0.3
        self.centre(target)

class Drawable:
    """Used as an abstract base-class for every drawable element."""

    def __init__(self, surface, camera):
        self.surface = surface
        self.camera = camera

    def draw(self):
        pass

class Grid(Drawable):
    """Used to represent the background grid."""

    def __init__(self, surface, camera):
        super().__init__(surface, camera)
        self.color = (230, 240, 240)

    def draw(self):
        # A grid is a set of horizontal and perpendicular lines
        zoom = self.camera.zoom
        x, y = self.camera.x, self.camera.y
        for i in range(0, 2001, 25):
            pygame.draw.line(self.surface, self.color, (x, i * zoom + y), (2001 * zoom + x, i * zoom + y), 3)
            pygame.draw.line(self.surface, self.color, (i * zoom + x, y), (i * zoom + x, 2001 * zoom + y), 3)

class HUD(Drawable):
    """Used to represent all necessary Head-Up Display information on screen."""

    def __init__(self, surface, camera):
        super().__init__(surface, camera)

    def draw(self):
        w, h = font.size("Score: " + str(int(blob.mass * 2)) + " ")
        MAIN_SURFACE.blit(pygame.transform.scale(SCOREBOARD_SURFACE, (w, h)),
                          (8, SCREEN_HEIGHT - 30))
        MAIN_SURFACE.blit(LEADERBOARD_SURFACE, (SCREEN_WIDTH - 160, 15))
        drawText("Score: " + str(int(blob.mass * 2)), (10, SCREEN_HEIGHT - 30))
        MAIN_SURFACE.blit(big_font.render("Leaderboard", 0, (255, 255, 255)),
                          (SCREEN_WIDTH - 157, 20))
        drawText("1. Skibidi", (SCREEN_WIDTH - 157, 20 + 25))
        drawText("2. Dodge", (SCREEN_WIDTH - 157, 20 + 25 * 2))
        drawText("3. Obamna", (SCREEN_WIDTH - 157, 20 + 25 * 3))
        drawText("4. ur mom", (SCREEN_WIDTH - 157, 20 + 25 * 4))
        drawText("5. pro team", (SCREEN_WIDTH - 157, 20 + 25 * 5))
        drawText("6. team plz", (SCREEN_WIDTH - 157, 20 + 25 * 6))
        drawText("7. HI", (SCREEN_WIDTH - 157, 20 + 25 * 7))
        drawText("8. ", (SCREEN_WIDTH - 157, 20 + 25 * 8))
        drawText("9. ..", (SCREEN_WIDTH - 157, 20 + 25 * 9))
        if (blob.mass <= 500):
            drawText("10. G #4", (SCREEN_WIDTH - 157, 20 + 25 * 10))
        else:
            drawText("10. player", (SCREEN_WIDTH - 157, 20 + 25 * 10), (210, 0, 0))

class Player(Drawable):
    """Used to represent the concept of a player."""
    COLOR_LIST = [
        (37, 7, 255),
        (35, 183, 253),
        (48, 254, 241),
        (19, 79, 251),
        (255, 7, 230),
        (255, 7, 23),
        (6, 254, 13)]

    FONT_COLOR = (50, 50, 50)

    def __init__(self, surface, camera, name=""):
        super().__init__(surface, camera)
        self.x = random.randint(100, 400)
        self.y = random.randint(100, 400)
        self.mass = 20
        self.speed = 4
        self.color = col = random.choice(Player.COLOR_LIST)
        self.outlineColor = (
            int(col[0] - col[0] / 3),
            int(col[1] - col[1] / 3),
            int(col[2] - col[2] / 3))
        if name: self.name = name
        else: self.name = "Anonymous"
        self.pieces = []

    def collisionDetection(self, edibles):
        """Detects cells being inside the radius of current player.
        Those cells are eaten."""
        for edible in edibles:
            if(getDistance((edible.x, edible.y), (self.x, self.y)) <= self.mass / 2):
                self.mass += 0.5
                edibles.remove(edible)

    def move(self):
        """Updates player's current position depending on player's mouse relative position."""
        dX, dY = pygame.mouse.get_pos()
        rotation = math.atan2(dY - float(SCREEN_HEIGHT) / 2, dX - float(SCREEN_WIDTH) / 2)
        rotation *= 180 / math.pi
        normalized = (90 - math.fabs(rotation)) / 90
        vx = self.speed * normalized
        vy = 0
        if rotation < 0:
            vy = -self.speed + math.fabs(vx)
        else:
            vy = self.speed - math.fabs(vx)
        tmpX = self.x + vx
        tmpY = self.y + vy
        # Add collision detection with the barriers
        if tmpX > 25 and tmpX < PLATFORM_WIDTH - 25:
            self.x = tmpX
        if tmpY > 25 and tmpY < PLATFORM_HEIGHT - 25:
            self.y = tmpY

    def draw(self):
        """Draws the player as an outlined circle."""
        zoom = self.camera.zoom
        x, y = self.camera.x, self.camera.y
        center = (int(self.x * zoom + x), int(self.y * zoom + y))

        pygame.draw.circle(self.surface, self.outlineColor, center, int((self.mass / 2 + 3) * zoom))
        pygame.draw.circle(self.surface, self.color, center, int(self.mass / 2 * zoom))
        fw, fh = font.size(self.name)
        drawText(self.name, (self.x * zoom + x - int(fw / 2), self.y * zoom + y - int(fh / 2)),
                 Player.FONT_COLOR)

class Barriers(Drawable):
    """Used to represent the barriers at the grid's edges."""

    def __init__(self, surface, camera):
        super().__init__(surface, camera)
        self.barrier_color = (0, 0, 0)  # Black color for the barrier
        self.barrier_thickness = 10  # Thickness of the barrier lines

    def draw(self):
        zoom = self.camera.zoom
        x, y = self.camera.x, self.camera.y
        # Define the four edges of the grid
        top_barrier = pygame.Rect(x, y, 2001 * zoom, self.barrier_thickness)
        bottom_barrier = pygame.Rect(x, 2001 * zoom + y - self.barrier_thickness, 2001 * zoom, self.barrier_thickness)
        left_barrier = pygame.Rect(x, y, self.barrier_thickness, 2001 * zoom)
        right_barrier = pygame.Rect(2001 * zoom + x - self.barrier_thickness, y, self.barrier_thickness, 2001 * zoom)

        # Draw the barriers
        pygame.draw.rect(self.surface, self.barrier_color, top_barrier)
        pygame.draw.rect(self.surface, self.barrier_color, bottom_barrier)
        pygame.draw.rect(self.surface, self.barrier_color, left_barrier)
        pygame.draw.rect(self.surface, self.barrier_color, right_barrier)

class Cell(Drawable):
    """Used to represent the fundamental entity of food (cells)."""
    CELL_COLORS = [
        (80, 252, 54),
        (36, 244, 255),
        (243, 31, 46),
        (4, 39, 243),
        (254, 6, 178),
        (255, 211, 7),
        (216, 6, 254),
        (145, 255, 7),
        (7, 255, 182),
        (255, 6, 86),
        (147, 7, 255)
    ]

    def __init__(self, surface, camera):
        super().__init__(surface, camera)
        self.x = random.randint(50, PLATFORM_WIDTH - 50)  # Random X position within grid limits
        self.y = random.randint(50, PLATFORM_HEIGHT - 50)  # Random Y position within grid limits
        self.mass = 7  # Set the mass of all food cells to 7 (same size)
        self.color = random.choice(Cell.CELL_COLORS)  # Random color for each food

    def draw(self):
        """Draws a food cell as a circle with the fixed size."""
        zoom = self.camera.zoom
        x, y = self.camera.x, self.camera.y
        center = (int(self.x * zoom + x), int(self.y * zoom + y))
        pygame.draw.circle(self.surface, self.color, center, int(self.mass * zoom))

class CellList:
    """Contains and manages the list of cells in the game."""
    
    def __init__(self, surface, camera, num_cells):
        self.surface = surface
        self.camera = camera
        # Scatter food randomly across the grid
        self.list = [Cell(self.surface, self.camera) for _ in range(num_cells)]

    def draw(self):
        """Draw all cells on the surface."""
        for cell in self.list:
            cell.draw()


# Initialize essential entities
cam = Camera()
grid = Grid(MAIN_SURFACE, cam)
cells = CellList(MAIN_SURFACE, cam, 2000)
blob = Player(MAIN_SURFACE, cam, "Player")
hud = HUD(MAIN_SURFACE, cam)
barriers = Barriers(MAIN_SURFACE, cam)  # Add the barrier object

painter = Painter()
painter.add(grid)
painter.add(cells)
painter.add(blob)
painter.add(hud)
painter.add(barriers)  # Add barriers to the painter

# Game main loop
while(True):
    clock.tick(70)
    for e in pygame.event.get():
        if(e.type == pygame.KEYDOWN):
            if(e.key == pygame.K_ESCAPE):
                pygame.quit()
                quit()
            if(e.key == pygame.K_w):
                blob.x -= 2
            if(e.key == pygame.K_s):
                blob.x += 2
            if(e.key == pygame.K_a):
                blob.y -= 2
            if(e.key == pygame.K_d):
                blob.y += 2
    blob.move()
    cam.update(blob)
    blob.collisionDetection(cells.list)
    MAIN_SURFACE.fill((255, 255, 255))
    painter.paint()
    pygame.display.update()
