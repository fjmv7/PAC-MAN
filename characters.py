import pygame
import random
from constants import *

class PacMan:
    def __init__(self):
        self.x = 10 * CELL_SIZE + CELL_SIZE // 2
        self.y = 16 * CELL_SIZE + CELL_SIZE // 2
        self.radius = CELL_SIZE // 2
        self.direction = 0  # 0: derecha, 1: arriba, 2: izquierda, 3: abajo
        self.mouth_angle = 0
        self.mouth_open = True
        self.speed = PACMAN_SPEED
        
    def move(self, maze):
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
                
    def draw(self, screen):
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

class Ghost:
    def __init__(self, x, y, color):
        self.x = x * CELL_SIZE + CELL_SIZE // 2
        self.y = y * CELL_SIZE + CELL_SIZE // 2
        self.radius = CELL_SIZE // 2
        self.color = color
        self.direction = random.randint(0, 3)
        self.speed = GHOST_SPEED
        self.change_direction_counter = 0
        
    def move(self, maze):
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
                
    def draw(self, screen):
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