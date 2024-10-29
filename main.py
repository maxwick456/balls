# Imports
import pygame  # type: ignore
import sys
import random
import time

# Initialize Pygame
pygame.init()

# Set Screen Dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ball Simulation")

# Define Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]

# Circle Variables
circle_center = (WIDTH // 2, HEIGHT // 2)
circle_radius = 250

# Ball Variables
ball_radius = 20
ball_pos = [WIDTH // 2, HEIGHT // 2]
ball_velocity = [random.choice([-5, 5]), random.choice([-5, 5])]
ball_color = random.choice(colors)

# Load Sound
pygame.mixer.init()  # Initialize the mixer
sound_file = "symphony.mp3"  # Replace with your sound file path
pygame.mixer.music.load(sound_file)

# Timer Variables
last_hit_time = time.time()
hit_threshold = 0.005  # 5 milliseconds

# Loop The Game
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Ball Movement
    ball_pos[0] += ball_velocity[0]
    ball_pos[1] += ball_velocity[1]

    # Check for collision with the circle boundary and reflect the velocity
    dist_x = ball_pos[0] - circle_center[0]
    dist_y = ball_pos[1] - circle_center[1]
    distance = (dist_x**2 + dist_y**2)**0.5

    if distance + ball_radius >= circle_radius:
        # Normalize Distance Vector
        normal = [dist_x / distance, dist_y / distance]

        # Calculate Dot Product
        velocity_dot_normal = ball_velocity[0] * normal[0] + ball_velocity[1] * normal[1]

        # Reflect Ball Velocity Vector
        ball_velocity[0] -= 2 * velocity_dot_normal * normal[0]
        ball_velocity[1] -= 2 * velocity_dot_normal * normal[1]

        # Set Position To Ensure Ball Stays In The Circle
        ball_pos[0] = circle_center[0] + (circle_radius - ball_radius) * normal[0]
        ball_pos[1] = circle_center[1] + (circle_radius - ball_radius) * normal[1]

        # Update last hit time
        last_hit_time = time.time()

    # Check if 5 ms have passed since the last hit
    if time.time() - last_hit_time > hit_threshold:
        # Play the sound if not already playing
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play()

    # Clear Screen
    screen.fill(BLACK)

    # Draw Circle Perimeter
    pygame.draw.circle(screen, WHITE, circle_center, circle_radius, 2)

    # Draw The Ball
    pygame.draw.circle(screen, ball_color, ball_pos, ball_radius)

    # Update Display
    pygame.display.flip()

    # Set Frame Rate
    pygame.time.Clock().tick(60)

# Outside Main Loop
pygame.quit()
sys.exit()