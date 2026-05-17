import pygame
import random
import math

# Initialize Pygame
pygame.init()
# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Futuristic AI Core")
clock = pygame.time.Clock()

# Colors
BG = (5, 5, 12)
CORE_COLOR = (24, 235, 255)
GLOW_COLOR = (0, 230, 255)
NODE_COLOR = (110, 255, 255)
WHITE = (255, 255, 255)

# Core parameters
CORE_CENTER = (WIDTH // 2, HEIGHT // 2)
CORE_RADIUS = 150
OUTER_RING_COUNT = 4
NODE_COUNT = 22
PARTICLE_COUNT = 120

# Particle state
particles = [
    {
        "angle": random.uniform(0, 2 * math.pi),
        "radius": random.uniform(CORE_RADIUS + 10, CORE_RADIUS + 90),
        "speed": random.uniform(0.003, 0.01),
        "size": random.randint(1, 3),
    }
    for _ in range(PARTICLE_COUNT)
]

# Node layout for the neural core
nodes = []
for i in range(NODE_COUNT):
    theta = (2 * math.pi / NODE_COUNT) * i
    ring = random.choice([0.5, 0.7, 0.9])
    distance = CORE_RADIUS * ring
    x = CORE_CENTER[0] + math.cos(theta) * distance
    y = CORE_CENTER[1] + math.sin(theta) * distance
    nodes.append({"pos": (x, y), "angle": theta, "distance": distance})


def draw_radial_glow(surface, center, radius, color, alpha, thickness):
    glow = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    pygame.draw.circle(glow, (*color, alpha), center, radius, thickness)
    surface.blit(glow, (0, 0), special_flags=pygame.BLEND_ADD)


def draw_core(surface, center, time):
    for i in range(5):
        radius = CORE_RADIUS - i * 18
        width = 4 if i == 0 else 1
        shade = max(40, int(180 - i * 30 + math.sin(time + i) * 15))
        pygame.draw.circle(surface, (shade, 255, 255), center, radius, width)

    # inner pulse
    pulse = CORE_RADIUS * 0.14 + math.sin(time * 2.2) * 6
    pygame.draw.circle(surface, CORE_COLOR, center, int(pulse))
    pygame.draw.circle(surface, WHITE, center, int(pulse / 2), 2)

    # soft glow layers
    draw_radial_glow(surface, center, CORE_RADIUS + 55, GLOW_COLOR, 22, 0)
    draw_radial_glow(surface, center, CORE_RADIUS + 18, CORE_COLOR, 48, 0)


def draw_ring(surface, center, radius, angle_offset, thickness):
    ring_color = (*GLOW_COLOR[:3], 90)
    glow = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    for segment in range(8):
        start = angle_offset + segment * (math.pi / 4)
        end = start + math.pi / 6
        points = []
        for a in [start, end]:
            x = center[0] + math.cos(a) * radius
            y = center[1] + math.sin(a) * radius
            points.append((x, y))
        pygame.draw.aaline(glow, ring_color, points[0], points[1])
    surface.blit(glow, (0, 0), special_flags=pygame.BLEND_ADD)
    pygame.draw.circle(surface, GLOW_COLOR, center, radius, thickness)


def draw_nodes(surface, time):
    for node in nodes:
        x, y = node["pos"]
        offset = math.sin(time * 1.2 + node["angle"] * 3) * 5
        radius = node["distance"] + offset
        nx = CORE_CENTER[0] + math.cos(node["angle"]) * radius
        ny = CORE_CENTER[1] + math.sin(node["angle"]) * radius
        pygame.draw.circle(surface, NODE_COLOR, (int(nx), int(ny)), 6)
        pygame.draw.circle(surface, WHITE, (int(nx), int(ny)), 2)
        for other in random.sample(nodes, 3):
            ox, oy = other["pos"]
            pygame.draw.aaline(surface, (*NODE_COLOR[:3], 60), (int(nx), int(ny)), (int(ox), int(oy)))


def draw_particles(surface, time):
    for particle in particles:
        particle["angle"] += particle["speed"]
        x = CORE_CENTER[0] + math.cos(particle["angle"]) * particle["radius"]
        y = CORE_CENTER[1] + math.sin(particle["angle"]) * particle["radius"]
        alpha = int(120 + math.sin(time * 3 + particle["angle"] * 8) * 80)
        glow = pygame.Surface((6, 6), pygame.SRCALPHA)
        pygame.draw.circle(glow, (*GLOW_COLOR, alpha), (3, 3), particle["size"])
        surface.blit(glow, (x - 3, y - 3), special_flags=pygame.BLEND_ADD)


def draw_background(surface):
    surface.fill(BG)
    for _ in range(4):
        x = random.randrange(0, WIDTH)
        y = random.randrange(0, HEIGHT)
        shade = random.randint(12, 35)
        screen.set_at((x, y), (shade, shade, shade))


def draw_ai_core(surface, time):
    draw_background(surface)
    draw_particles(surface, time)
    draw_core(surface, CORE_CENTER, time)

    for i in range(OUTER_RING_COUNT):
        ring_radius = CORE_RADIUS + 32 + i * 22
        draw_ring(surface, CORE_CENTER, ring_radius, time * 0.3 + i * 0.7, 2)

    draw_nodes(surface, time)

# Main loop
running = True
start_time = pygame.time.get_ticks() / 1000.0
while running:
    elapsed = pygame.time.get_ticks() / 1000.0 - start_time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    draw_ai_core(screen, elapsed)
    pygame.display.flip()
    clock.tick(60)
    
    

