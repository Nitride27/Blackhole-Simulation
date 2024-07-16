import pygame
import math
import random
from pygame import mixer

# Initialize Pygame and mixer
pygame.init()
mixer.init()

# Screen dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Black Hole Simulation")

# Load and play background music
try:
    mixer.music.load("Interstellar.mp3")
    mixer.music.set_volume(1.0)  # Set volume to maximum
    mixer.music.play(-1)  # Loop the music
except pygame.error as e:
    print(f"Error loading music: {e}")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_GRAY = (50, 50, 50)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# Black hole properties
black_hole_pos = (width // 2, height // 2)
black_hole_radius = 50
black_hole_mass = 3000  # Arbitrary mass for gravity calculation

# Load background image
try:
    background = pygame.image.load("space.jpg")
    background = pygame.transform.scale(background, (width, height))
except pygame.error as e:
    print(f"Error loading background image: {e}")
    background = None

# Particle properties
num_particles = 30
particles = []

# Initialize particles
for _ in range(num_particles):
    x = random.randint(0, width)
    y = random.randint(0, height)
    particles.append([x, y, random.uniform(-2, 2), random.uniform(-2, 2)])

def draw_black_hole():
    pygame.draw.circle(screen, BLACK, black_hole_pos, black_hole_radius)
    for i in range(1, 5):
        pygame.draw.circle(screen, DARK_GRAY, black_hole_pos, black_hole_radius + i * 5, 2)
    for i in range(black_hole_radius + 20, black_hole_radius + 40, 2):
        color = YELLOW if i % 20 == 0 else ORANGE
        pygame.draw.circle(screen, color, black_hole_pos, i, 2)

def draw_particles():
    for particle in particles:
        pygame.draw.circle(screen, WHITE, (int(particle[0]), int(particle[1])), 10)

def apply_gravity():
    for particle in particles:
        dx = black_hole_pos[0] - particle[0]
        dy = black_hole_pos[1] - particle[1]
        distance = math.sqrt(dx**2 + dy**2)
        if distance < black_hole_radius:
            # Reset particle if it falls into the black hole
            particle[0] = random.randint(0, width)
            particle[1] = random.randint(0, height)
            particle[2] = random.uniform(-2, 2)
            particle[3] = random.uniform(-2, 2)
        else:
            force = black_hole_mass / (distance**2)
            angle = math.atan2(dy, dx)
            particle[2] += force * math.cos(angle)
            particle[3] += force * math.sin(angle)

def update_particles():
    for particle in particles:
        particle[0] += particle[2]
        particle[1] += particle[3]

# Main loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))
    if background:
        screen.blit(background, (0, 0))

    draw_black_hole()
    draw_particles()
    apply_gravity()
    update_particles()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
