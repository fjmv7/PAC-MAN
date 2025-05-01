import pygame
import sys
from constants import *
from characters import PacMan, Ghost

# Inicializar pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man Básico")

# Variables del juego
SCORE = 0
GAME_OVER = False
WIN = False

# Función para dibujar el laberinto
def draw_maze(screen, maze):
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
def check_pellets(pacman, maze):
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
def check_ghost_collision(pacman, ghosts):
    global GAME_OVER
    
    for ghost in ghosts:
        distance = ((pacman.x - ghost.x) ** 2 + (pacman.y - ghost.y) ** 2) ** 0.5
        if distance < pacman.radius + ghost.radius:
            GAME_OVER = True

# Función para mostrar el puntaje
def show_score(screen, score):
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Puntaje: {score}", True, WHITE)
    screen.blit(score_text, (10, HEIGHT - 40))

# Función para mostrar pantalla de inicio
def show_start_screen(screen):
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
def show_game_over_screen(screen, win, score):
    screen.fill(BLACK)
    font_large = pygame.font.SysFont(None, 48)
    font_small = pygame.font.SysFont(None, 36)
    
    if win:
        message = font_large.render("¡GANASTE!", True, YELLOW)
    else:
        message = font_large.render("GAME OVER", True, RED)
    
    score_text = font_small.render(f"Puntaje final: {score}", True, WHITE)
    restart = font_small.render("Presiona R para reiniciar", True, WHITE)
    quit_text = font_small.render("Presiona Q para salir", True, WHITE)
    
    screen.blit(message, (WIDTH // 2 - message.get_width() // 2, HEIGHT // 3))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
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
                    return True  # Reiniciar
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
    return False

# Función para reiniciar el juego
def reset_game():
    global SCORE, GAME_OVER, WIN
    
    # Restaurar el laberinto
    maze = [row[:] for row in MAZE]
    
    # Reiniciar variables del juego
    SCORE = 0
    GAME_OVER = False
    WIN = False
    
    # Crear personajes
    pacman = PacMan()
    ghosts = [
        Ghost(9, 8, RED),
        Ghost(10, 8, PINK),
        Ghost(9, 9, CYAN),
        Ghost(10, 9, ORANGE)
    ]
    
    return pacman, ghosts, maze

# Función principal del juego
def main():
    global SCORE, GAME_OVER, WIN
    
    # Mostrar pantalla de inicio
    show_start_screen(screen)
    
    # Inicializar juego
    pacman, ghosts, maze = reset_game()
    
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
            pacman.move(maze)
            for ghost in ghosts:
                ghost.move(maze)
            
            # Verificar colisiones
            check_pellets(pacman, maze)
            check_ghost_collision(pacman, ghosts)
            
            # Dibujar
            screen.fill(BLACK)
            draw_maze(screen, maze)
            pacman.draw(screen)
            for ghost in ghosts:
                ghost.draw(screen)
            show_score(screen, SCORE)
            
            pygame.display.flip()
        else:
            # Mostrar pantalla de fin de juego
            if show_game_over_screen(screen, WIN, SCORE):
                # Reiniciar juego si el jugador presiona R
                pacman, ghosts, maze = reset_game()
            else:
                running = False
        
        # Controlar la velocidad del juego
        clock.tick(30)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()