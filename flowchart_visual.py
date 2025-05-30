import pygame
import sys

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
TEAL = (0, 128, 128)
SOFT_BLUE = (100, 149, 237)
SOFT_RED = (188, 84, 84)
SOFT_GREEN = (106, 168, 79)
BACKGROUND = (240, 240, 245)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Rock, Paper, Scissors - Flow Diagram")
clock = pygame.time.Clock()

# Load fonts
title_font = pygame.font.SysFont('Arial', 24, bold=True)
font = pygame.font.SysFont('Arial', 16)

# Define states and their positions
states = [
    {"name": "Game Start", "pos": (400, 50), "color": TEAL},
    {"name": "Menu Screen", "pos": (400, 150), "color": SOFT_BLUE},
    {"name": "Name Input Screen", "pos": (400, 250), "color": SOFT_BLUE},
    {"name": "Playing Screen", "pos": (400, 350), "color": SOFT_BLUE},
    {"name": "Result Screen", "pos": (400, 450), "color": SOFT_BLUE},
    {"name": "End Screen", "pos": (400, 600), "color": SOFT_RED},
    {"name": "Game Exit", "pos": (600, 700), "color": SOFT_RED}
]

# Define connections between states
connections = [
    {"from": 0, "to": 1, "text": "Start"},
    {"from": 1, "to": 2, "text": "Click 'Enter Your Name'"},
    {"from": 2, "to": 3, "text": "Type name & Click 'Start Game'"},
    {"from": 3, "to": 4, "text": "Select Rock/Paper/Scissors"},
    {"from": 4, "to": 3, "text": "Click 'Play Again' or Press Y", "offset": (-150, 0)},
    {"from": 4, "to": 5, "text": "Click 'End Game' or Press N"},
    {"from": 5, "to": 1, "text": "Click 'Restart' or Press R", "offset": (-150, 0)},
    {"from": 5, "to": 6, "text": "Click 'Quit' or Press Q"}
]

def draw_state(state):
    """Draw a state box with text"""
    x, y = state["pos"]
    width, height = 180, 60
    rect = pygame.Rect(x - width//2, y - height//2, width, height)
    
    # Draw rounded rectangle
    pygame.draw.rect(screen, state["color"], rect, border_radius=15)
    pygame.draw.rect(screen, BLACK, rect, 2, border_radius=15)
    
    # Draw state name
    text = title_font.render(state["name"], True, WHITE)
    text_rect = text.get_rect(center=(x, y))
    screen.blit(text, text_rect)

def draw_arrow(start_pos, end_pos, text, offset=(0, 0)):
    """Draw an arrow between states with text"""
    # Apply offset if provided
    start_x, start_y = start_pos
    end_x, end_y = end_pos
    
    # Calculate direction and adjust start/end points
    dx, dy = end_x - start_x, end_y - start_y
    length = ((dx ** 2) + (dy ** 2)) ** 0.5
    
    if length > 0:
        dx, dy = dx / length, dy / length
    
    # Apply offset to the line
    offset_x, offset_y = offset
    
    # Draw the line
    pygame.draw.line(screen, BLACK, 
                    (start_x + offset_x, start_y + 30 + offset_y), 
                    (end_x + offset_x, end_y - 30 + offset_y), 2)
    
    # Draw arrowhead
    arrow_size = 10
    angle = math.atan2(end_y - start_y, end_x - start_x)
    end_point = (end_x + offset_x, end_y - 30 + offset_y)
    
    pygame.draw.polygon(screen, BLACK, [
        end_point,
        (end_point[0] - arrow_size * math.cos(angle - math.pi/6),
         end_point[1] - arrow_size * math.sin(angle - math.pi/6)),
        (end_point[0] - arrow_size * math.cos(angle + math.pi/6),
         end_point[1] - arrow_size * math.sin(angle + math.pi/6)),
    ])
    
    # Draw text
    if text:
        mid_x = (start_x + end_x) / 2 + offset_x
        mid_y = (start_y + 30 + end_y - 30) / 2 + offset_y
        
        text_surf = font.render(text, True, BLACK)
        text_rect = text_surf.get_rect(center=(mid_x, mid_y))
        
        # Add background to text for better readability
        padding = 5
        bg_rect = pygame.Rect(text_rect.x - padding, text_rect.y - padding,
                             text_rect.width + padding*2, text_rect.height + padding*2)
        pygame.draw.rect(screen, BACKGROUND, bg_rect)
        
        screen.blit(text_surf, text_rect)

# Import math for arrow calculations
import math

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Fill the background
    screen.fill(BACKGROUND)
    
    # Draw title
    title = title_font.render("Rock, Paper, Scissors - Game Flow Diagram", True, BLACK)
    screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 10))
    
    # Draw all connections first (so they appear behind states)
    for conn in connections:
        from_state = states[conn["from"]]
        to_state = states[conn["to"]]
        offset = conn.get("offset", (0, 0))
        draw_arrow(from_state["pos"], to_state["pos"], conn["text"], offset)
    
    # Draw all states
    for state in states:
        draw_state(state)
    
    # Draw legend
    legend_y = 730
    pygame.draw.rect(screen, TEAL, (50, legend_y, 20, 20), border_radius=5)
    pygame.draw.rect(screen, SOFT_BLUE, (50, legend_y + 30, 20, 20), border_radius=5)
    pygame.draw.rect(screen, SOFT_RED, (50, legend_y + 60, 20, 20), border_radius=5)
    
    screen.blit(font.render("Start/End Points", True, BLACK), (80, legend_y + 2))
    screen.blit(font.render("Game States", True, BLACK), (80, legend_y + 32))
    screen.blit(font.render("Exit Points", True, BLACK), (80, legend_y + 62))
    
    # Update the display
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()