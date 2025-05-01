import pygame
import sys
import random

# Inicializar pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 400, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man Básico")

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PINK = (255, 184, 255)
CYAN = (0, 255, 255)

# Configuración del juego
CELL_SIZE = 20
PACMAN_SPEED = 2
GHOST_SPEED = 1
SCORE = 0
GAME_OVER = False
WIN = False

# Laberinto (0: pared, 1: punto, 2: espacio vacío)
maze = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0],
    [0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 1, 0, 0, 2, 2, 0, 0, 1, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 1, 0, 2, 2, 2, 2, 0, 1, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0],
    [0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0],
    [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
    [0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

# Clase Pac-Man
class PacMan:
    def __init__(self):
        self.x = 10 * CELL_SIZE + CELL_SIZE // 2
        self.y = 16 * CELL_SIZE + CELL_SIZE // 2
        self.radius = CELL_SIZE // 2
        self.direction = 0  # 0: derecha, 1: arriba, 2: izquierda, 3: abajo
        self.mouth_angle = 0
        self.mouth_open = True
        self.speed = PACMAN_SPEED
        
    def move(self):
        # Movimiento según la dirección
        if self.direction == 0:  # Derecha
            new_x = self.x + self.speed
            new_y = self.y
        elif self.direction == 1:  # Arriba
            new_x = self.x
            new_y = self.y - self.speed
        elif self.direction == 2:  # Izquierda
            new_x = self.x - self.speed
            new_y = self.y
        elif self.direction == 3:  # Abajo
            new_x = self.x
            new_y = self.y + self.speed
            
        # Verificar colisión con paredes
        cell_x, cell_y = new_x // CELL_SIZE, new_y // CELL_SIZE
        if 0 <= cell_x < len(maze[0]) and 0 <= cell_y < len(maze):
            if maze[cell_y][cell_x] != 0:
                self.x, self.y = new_x, new_y
                
        # Animación de la boca
        if self.mouth_open:
            self.mouth_angle += 5
            if self.mouth_angle >= 45:
                self.mouth_open = False
        else:
            self.mouth_angle -= 5
            if self.mouth_angle <= 0:
                self.mouth_open = True
                
    def draw(self):
        # Dibujar Pac-Man
        start_angle = self.mouth_angle / 180 * 3.1416
        end_angle = (360 - self.mouth_angle) / 180 * 3.1416
        
        if self.direction == 0:  # Derecha
            pygame.draw.arc(screen, BLACK, 
                           (self.x - self.radius, self.y - self.radius, 
                            self.radius * 2, self.radius * 2),
                           start_angle, end_angle, 2)
        elif self.direction == 1:  # Arriba
            pygame.draw.arc(screen, BLACK, 
                           (self.x - self.radius, self.y - self.radius, 
                            self.radius * 2, self.radius * 2),
                           start_angle + 3.1416/2, end_angle + 3.1416/2, 2)
        elif self.direction == 2:  # Izquierda
            pygame.draw.arc(screen, BLACK, 
                           (self.x - self.radius, self.y - self.radius, 
                            self.radius * 2, self.radius * 2),
                           start_angle + 3.1416, end_angle + 3.1416, 2)
        elif self.direction == 3:  # Abajo
            pygame.draw.arc(screen, BLACK, 
                           (self.x - self.radius, self.y - self.radius, 
                            self.radius * 2, self.radius * 2),
                           start_angle + 3*3.1416/2, end_angle + 3*3.1416/2, 2)
            
        pygame.draw.circle(screen, YELLOW, (self.x, self.y), self.radius)

# Clase Fantasma
class Ghost:
    def __init__(self, x, y, color):
        self.x = x * CELL_SIZE + CELL_SIZE // 2
        self.y = y * CELL_SIZE + CELL_SIZE // 2
        self.radius = CELL_SIZE // 2
        self.color = color
        self.direction = random.randint(0, 3)
        self.speed = GHOST_SPEED
        self.change_direction_counter = 0
        
    def move(self):
        # Cambiar dirección aleatoriamente
        self.change_direction_counter += 1
        if self.change_direction_counter >= 30:
            self.direction = random.randint(0, 3)
            self.change_direction_counter = 0
            
        # Movimiento según la dirección
        if self.direction == 0:  # Derecha
            new_x = self.x + self.speed
            new_y = self.y
        elif self.direction == 1:  # Arriba
            new_x = self.x
            new_y = self.y - self.speed
        elif self.direction == 2:  # Izquierda
            new_x = self.x - self.speed
            new_y = self.y
        elif self.direction == 3:  # Abajo
            new_x = self.x
            new_y = self.y + self.speed
            
        # Verificar colisión con paredes
        cell_x, cell_y = new_x // CELL_SIZE, new_y // CELL_SIZE
        if 0 <= cell_x < len(maze[0]) and 0 <= cell_y < len(maze):
            if maze[cell_y][cell_x] != 0:
                self.x, self.y = new_x, new_y
            else:
                self.direction = random.randint(0, 3)
                
    def draw(self):
        # Dibujar fantasma
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
        pygame.draw.rect(screen, self.color, 
                        (self.x - self.radius, self.y, self.radius * 2, self.radius))
        
        # Ojos
        eye_radius = self.radius // 3
        pygame.draw.circle(screen, WHITE, 
                         (self.x - eye_radius, self.y - eye_radius // 2), eye_radius)
        pygame.draw.circle(screen, WHITE, 
                         (self.x + eye_radius, self.y - eye_radius // 2), eye_radius)
        
        # Pupilas
        pygame.draw.circle(screen, BLUE, 
                         (self.x - eye_radius, self.y - eye_radius // 2), eye_radius // 2)
        pygame.draw.circle(screen, BLUE, 
                         (self.x + eye_radius, self.y - eye_radius // 2), eye_radius // 2)

# Función para dibujar el laberinto
def draw_maze():
    for y in range(len(maze)):
        for x in range(len(maze[0])):
            if maze[y][x] == 0:  # Pared
                pygame.draw.rect(screen, BLUE, 
                                (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            elif maze[y][x] == 1:  # Punto
                pygame.draw.circle(screen, WHITE, 
                                 (x * CELL_SIZE + CELL_SIZE // 2, 
                                  y * CELL_SIZE + CELL_SIZE // 2), 
                                  CELL_SIZE // 6)

# Función para verificar colisión con puntos
def check_pellets():
    global SCORE, WIN
    
    cell_x, cell_y = pacman.x // CELL_SIZE, pacman.y // CELL_SIZE
    if 0 <= cell_x < len(maze[0]) and 0 <= cell_y < len(maze):
        if maze[cell_y][cell_x] == 1:
            maze[cell_y][cell_x] = 2  # Marcar como comido
            SCORE += 10
            
            # Verificar si se han comido todos los puntos
            all_eaten = True
            for row in maze:
                if 1 in row:
                    all_eaten = False
                    break
            if all_eaten:
                WIN = True

# Función para verificar colisión con fantasmas
def check_ghost_collision():
    global GAME_OVER
    
    for ghost in ghosts:
        distance = ((pacman.x - ghost.x) ** 2 + (pacman.y - ghost.y) ** 2) ** 0.5
        if distance < pacman.radius + ghost.radius:
            GAME_OVER = True

# Función para mostrar el puntaje
def show_score():
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Puntaje: {SCORE}", True, WHITE)
    screen.blit(score_text, (10, HEIGHT - 40))

# Función para mostrar pantalla de inicio
def show_start_screen():
    screen.fill(BLACK)
    font_large = pygame.font.SysFont(None, 48)
    font_small = pygame.font.SysFont(None, 36)
    
    title = font_large.render("PAC-MAN", True, YELLOW)
    instruction1 = font_small.render("Usa las flechas para mover a Pac-Man", True, WHITE)
    instruction2 = font_small.render("Presiona cualquier tecla para comenzar", True, WHITE)
    
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 3))
    screen.blit(instruction1, (WIDTH // 2 - instruction1.get_width() // 2, HEIGHT // 2))
    screen.blit(instruction2, (WIDTH // 2 - instruction2.get_width() // 2, HEIGHT // 2 + 50))
    
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                waiting = False

# Función para mostrar pantalla de fin de juego
def show_game_over_screen():
    screen.fill(BLACK)
    font_large = pygame.font.SysFont(None, 48)
    font_small = pygame.font.SysFont(None, 36)
    
    if WIN:
        message = font_large.render("¡GANASTE!", True, YELLOW)
    else:
        message = font_large.render("GAME OVER", True, RED)
    
    score = font_small.render(f"Puntaje final: {SCORE}", True, WHITE)
    restart = font_small.render("Presiona R para reiniciar", True, WHITE)
    quit_text = font_small.render("Presiona Q para salir", True, WHITE)
    
    screen.blit(message, (WIDTH // 2 - message.get_width() // 2, HEIGHT // 3))
    screen.blit(score, (WIDTH // 2 - score.get_width() // 2, HEIGHT // 2))
    screen.blit(restart, (WIDTH // 2 - restart.get_width() // 2, HEIGHT // 2 + 50))
    screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT // 2 + 100))
    
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()
                    waiting = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

# Función para reiniciar el juego
def reset_game():
    global SCORE, GAME_OVER, WIN, maze, pacman, ghosts
    
    # Restaurar el laberinto
    maze = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0],
        [0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0],
        [0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 1, 0, 0, 2, 2, 0, 0, 1, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 1, 0, 2, 2, 2, 2, 0, 1, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0],
        [0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0],
        [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
        [0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]
    
    # Reiniciar variables del juego
    SCORE = 0
    GAME_OVER = False
    WIN = False
    
    # Reiniciar personajes
    pacman = PacMan()
    ghosts = [
        Ghost(9, 8, RED),
        Ghost(10, 8, PINK),
        Ghost(9, 9, CYAN),
        Ghost(10, 9, (255, 184, 82))  # Fantasma naranja
    ]

# Crear personajes
pacman = PacMan()
ghosts = [
    Ghost(9, 8, RED),    # Fantasma rojo
    Ghost(10, 8, PINK),   # Fantasma rosa
    Ghost(9, 9, CYAN),    # Fantasma cian
    Ghost(10, 9, (255, 184, 82))  # Fantasma naranja
]

# Mostrar pantalla de inicio
show_start_screen()

# Bucle principal del juego
clock = pygame.time.Clock()
running = True

while running:
    # Manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                pacman.direction = 2
            elif event.key == pygame.K_RIGHT:
                pacman.direction = 0
            elif event.key == pygame.K_UP:
                pacman.direction = 1
            elif event.key == pygame.K_DOWN:
                pacman.direction = 3
    
    if not GAME_OVER and not WIN:
        # Actualizar personajes
        pacman.move()
        for ghost in ghosts:
            ghost.move()
        
        # Verificar colisiones
        check_pellets()
        check_ghost_collision()
        
        # Dibujar
        screen.fill(BLACK)
        draw_maze()
        pacman.draw()
        for ghost in ghosts:
            ghost.draw()
        show_score()
        
        pygame.display.flip()
    else:
        show_game_over_screen()
    
    # Controlar la velocidad del juego
    clock.tick(30)

pygame.quit()
sys.exit()