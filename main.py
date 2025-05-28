import pygame
import sys
import random
import pygame
from pygame.locals import *

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GRAY = (230, 230, 230)
DARK_GRAY = (50, 50, 50)
TEAL = (0, 128, 128)
SOFT_BLUE = (100, 149, 237)
SOFT_RED = (188, 84, 84)
SOFT_GREEN = (106, 168, 79)
GOLD = (212, 175, 55)
BACKGROUND = (240, 240, 245)

# Game states
MENU = 0
NAME_INPUT = 1
PLAYING = 2
RESULT = 3
END_SCREEN = 4

class Game:
    def __init__(self):
        # Set up the display
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Rock, Paper, Scissors")
        self.clock = pygame.time.Clock()
        
        # Load fonts
        self.title_font = pygame.font.SysFont('Arial', 48, bold=True)
        self.font = pygame.font.SysFont('Arial', 36)
        self.small_font = pygame.font.SysFont('Arial', 24)
        
        # Game variables
        self.state = MENU
        self.player_name = ""
        self.input_active = False
        self.player_score = 0
        self.computer_score = 0
        self.player_choice = None
        self.computer_choice = None
        self.result = None
        
        # Load images with improved graphics
        self.rock_img = self.create_choice_image("ROCK", SOFT_RED)
        self.paper_img = self.create_choice_image("PAPER", SOFT_GREEN)
        self.scissors_img = self.create_choice_image("SCISSORS", SOFT_BLUE)
        
        # Create rectangles for choices
        self.rock_rect = self.rock_img.get_rect(center=(SCREEN_WIDTH//4, SCREEN_HEIGHT//2))
        self.paper_rect = self.paper_img.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.scissors_rect = self.scissors_img.get_rect(center=(3*SCREEN_WIDTH//4, SCREEN_HEIGHT//2))
    
    def create_choice_image(self, text, color):
        """Create a colored surface with text for each choice with improved graphics"""
        surf = pygame.Surface((150, 150), pygame.SRCALPHA)
        
        # Draw rounded rectangle with shadow effect
        pygame.draw.rect(surf, (*color, 220), (5, 5, 140, 140), border_radius=15)
        pygame.draw.rect(surf, (*color, 255), (0, 0, 140, 140), border_radius=15)
        
        # Add text with shadow for better visibility
        text_surf = self.font.render(text, True, BLACK)
        text_shadow = self.font.render(text, True, (*DARK_GRAY, 128))
        
        text_rect = text_surf.get_rect(center=(75, 75))
        shadow_rect = text_shadow.get_rect(center=(77, 77))
        
        surf.blit(text_shadow, shadow_rect)
        surf.blit(text_surf, text_rect)
        
        return surf
    
    def draw_text(self, text, font, color, x, y, align="center"):
        """Helper function to draw text on screen"""
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "center":
            text_rect.center = (x, y)
        elif align == "topleft":
            text_rect.topleft = (x, y)
        self.screen.blit(text_surface, text_rect)
    
    def menu_screen(self):
        """Display the main menu screen"""
        self.screen.fill(BACKGROUND)
        
        # Draw title with shadow for depth
        title_shadow = self.title_font.render("ROCK, PAPER, SCISSORS", True, DARK_GRAY)
        title_text = self.title_font.render("ROCK, PAPER, SCISSORS", True, TEAL)
        title_shadow_rect = title_shadow.get_rect(center=(SCREEN_WIDTH//2+2, 102))
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, 100))
        self.screen.blit(title_shadow, title_shadow_rect)
        self.screen.blit(title_text, title_rect)
        
        # Draw button with hover effect
        mouse_pos = pygame.mouse.get_pos()
        button_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 - 25, 200, 50)
        button_color = SOFT_BLUE if button_rect.collidepoint(mouse_pos) else TEAL
        pygame.draw.rect(self.screen, button_color, button_rect, border_radius=10)
        self.draw_text("Enter Your Name", self.font, WHITE, SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
        
        # Draw score if any games have been played
        if self.player_score > 0 or self.computer_score > 0:
            player_name = self.player_name if self.player_name else "Player"
            self.draw_text(f"{player_name}: {self.player_score} | Computer: {self.computer_score}", 
                          self.small_font, DARK_GRAY, SCREEN_WIDTH//2, SCREEN_HEIGHT - 50)
        
        # Check for mouse click to start game
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if button_rect.collidepoint(mouse_pos):
                    self.state = NAME_INPUT
    
    def name_input_screen(self):
        """Display the screen for entering player name"""
        self.screen.fill(BACKGROUND)
        self.draw_text("Enter Your Name:", self.font, TEAL, SCREEN_WIDTH//2, 100)
        
        # Draw input box
        input_box = pygame.Rect(SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2 - 25, 300, 50)
        box_color = SOFT_BLUE if self.input_active else TEAL
        pygame.draw.rect(self.screen, box_color, input_box, border_radius=5)
        pygame.draw.rect(self.screen, DARK_GRAY, input_box, 2, border_radius=5)
        
        # Display current input text
        text_surface = self.font.render(self.player_name, True, WHITE)
        text_rect = text_surface.get_rect(center=input_box.center)
        self.screen.blit(text_surface, text_rect)
        
        # Draw start button
        button_rect = pygame.Rect(SCREEN_WIDTH//2 - 75, SCREEN_HEIGHT//2 + 50, 150, 40)
        button_color = SOFT_GREEN if len(self.player_name) > 0 else DARK_GRAY
        pygame.draw.rect(self.screen, button_color, button_rect, border_radius=5)
        self.draw_text("Start Game", self.small_font, WHITE, SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 70)
        
        # Handle events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                # Check if input box clicked
                if input_box.collidepoint(event.pos):
                    self.input_active = True
                else:
                    self.input_active = False
                
                # Check if start button clicked and name entered
                if button_rect.collidepoint(event.pos) and len(self.player_name) > 0:
                    self.state = PLAYING
            elif event.type == KEYDOWN:
                if self.input_active:
                    if event.key == K_RETURN and len(self.player_name) > 0:
                        self.state = PLAYING
                    elif event.key == K_BACKSPACE:
                        self.player_name = self.player_name[:-1]
                    else:
                        # Limit name length to 15 characters
                        if len(self.player_name) < 15:
                            self.player_name += event.unicode
    
    def playing_screen(self):
        """Display the game screen where player makes a choice"""
        self.screen.fill(BACKGROUND)
        
        # Display player name
        player_name = self.player_name if self.player_name else "Player"
        self.draw_text(f"{player_name}, choose your move:", self.font, TEAL, SCREEN_WIDTH//2, 100)
        
        # Draw choice options with hover effect
        mouse_pos = pygame.mouse.get_pos()
        
        # Scale up choices on hover
        rock_scale = 1.1 if self.rock_rect.collidepoint(mouse_pos) else 1.0
        paper_scale = 1.1 if self.paper_rect.collidepoint(mouse_pos) else 1.0
        scissors_scale = 1.1 if self.scissors_rect.collidepoint(mouse_pos) else 1.0
        
        # Draw choices with scaling
        rock_img = pygame.transform.smoothscale(self.rock_img, 
                                              (int(self.rock_img.get_width() * rock_scale), 
                                               int(self.rock_img.get_height() * rock_scale)))
        paper_img = pygame.transform.smoothscale(self.paper_img, 
                                               (int(self.paper_img.get_width() * paper_scale), 
                                                int(self.paper_img.get_height() * paper_scale)))
        scissors_img = pygame.transform.smoothscale(self.scissors_img, 
                                                  (int(self.scissors_img.get_width() * scissors_scale), 
                                                   int(self.scissors_img.get_height() * scissors_scale)))
        
        rock_rect = rock_img.get_rect(center=self.rock_rect.center)
        paper_rect = paper_img.get_rect(center=self.paper_rect.center)
        scissors_rect = scissors_img.get_rect(center=self.scissors_rect.center)
        
        self.screen.blit(rock_img, rock_rect)
        self.screen.blit(paper_img, paper_rect)
        self.screen.blit(scissors_img, scissors_rect)
        
        # Check for player choice
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if rock_rect.collidepoint(mouse_pos):
                    self.player_choice = "rock"
                    self.get_computer_choice()
                    self.determine_winner()
                    self.state = RESULT
                elif paper_rect.collidepoint(mouse_pos):
                    self.player_choice = "paper"
                    self.get_computer_choice()
                    self.determine_winner()
                    self.state = RESULT
                elif scissors_rect.collidepoint(mouse_pos):
                    self.player_choice = "scissors"
                    self.get_computer_choice()
                    self.determine_winner()
                    self.state = RESULT
    
    def get_computer_choice(self):
        """Generate a random choice for the computer"""
        choices = ["rock", "paper", "scissors"]
        self.computer_choice = random.choice(choices)
    
    def determine_winner(self):
        """Determine the winner based on player and computer choices"""
        if self.player_choice == self.computer_choice:
            self.result = "It's a tie!"
        elif (self.player_choice == "rock" and self.computer_choice == "scissors") or \
             (self.player_choice == "paper" and self.computer_choice == "rock") or \
             (self.player_choice == "scissors" and self.computer_choice == "paper"):
            self.result = "You win!"
            self.player_score += 1
        else:
            self.result = "Computer wins!"
            self.computer_score += 1
    
    def result_screen(self):
        """Display the result of the round"""
        self.screen.fill(BACKGROUND)
        
        # Get player name or default
        player_name = self.player_name if self.player_name else "Player"
        
        # Draw player and computer choices with icons
        choice_y = 120
        self.draw_text(f"{player_name} chose:", self.font, TEAL, SCREEN_WIDTH//4, choice_y - 40)
        self.draw_text("Computer chose:", self.font, TEAL, 3*SCREEN_WIDTH//4, choice_y - 40)
        
        # Draw mini versions of the choices
        player_choice_img = self.create_choice_image(self.player_choice.upper(), 
                                                   SOFT_RED if self.player_choice == "rock" else
                                                   SOFT_GREEN if self.player_choice == "paper" else SOFT_BLUE)
        comp_choice_img = self.create_choice_image(self.computer_choice.upper(), 
                                                 SOFT_RED if self.computer_choice == "rock" else
                                                 SOFT_GREEN if self.computer_choice == "paper" else SOFT_BLUE)
        
        # Scale down the images
        player_choice_img = pygame.transform.smoothscale(player_choice_img, (100, 100))
        comp_choice_img = pygame.transform.smoothscale(comp_choice_img, (100, 100))
        
        self.screen.blit(player_choice_img, player_choice_img.get_rect(center=(SCREEN_WIDTH//4, choice_y + 50)))
        self.screen.blit(comp_choice_img, comp_choice_img.get_rect(center=(3*SCREEN_WIDTH//4, choice_y + 50)))
        
        # Draw result with animation effect (pulsing)
        result_color = GOLD
        pulse = (pygame.time.get_ticks() % 1000) / 1000  # Value between 0 and 1
        pulse_scale = 1.0 + 0.1 * abs(pulse - 0.5) * 2  # Scale between 1.0 and 1.1
        
        result_text = self.title_font.render(self.result, True, result_color)
        result_text = pygame.transform.smoothscale(result_text, 
                                                 (int(result_text.get_width() * pulse_scale),
                                                  int(result_text.get_height() * pulse_scale)))
        result_rect = result_text.get_rect(center=(SCREEN_WIDTH//2, 250))
        self.screen.blit(result_text, result_rect)
        
        # Draw scores
        self.draw_text(f"{player_name}: {self.player_score} | Computer: {self.computer_score}", 
                      self.font, DARK_GRAY, SCREEN_WIDTH//2, 350)
        
        # Draw buttons for play again or end game
        button_y = 450
        button_width = 150
        button_height = 50
        button_spacing = 50
        
        yes_button = pygame.Rect(SCREEN_WIDTH//2 - button_width - button_spacing//2, button_y, button_width, button_height)
        no_button = pygame.Rect(SCREEN_WIDTH//2 + button_spacing//2, button_y, button_width, button_height)
        
        mouse_pos = pygame.mouse.get_pos()
        yes_color = SOFT_GREEN if yes_button.collidepoint(mouse_pos) else TEAL
        no_color = SOFT_RED if no_button.collidepoint(mouse_pos) else TEAL
        
        pygame.draw.rect(self.screen, yes_color, yes_button, border_radius=10)
        pygame.draw.rect(self.screen, no_color, no_button, border_radius=10)
        
        self.draw_text("Play Again", self.font, WHITE, yes_button.centerx, yes_button.centery)
        self.draw_text("End Game", self.font, WHITE, no_button.centerx, no_button.centery)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_y:
                    self.state = PLAYING
                elif event.key == K_n:
                    self.state = END_SCREEN
            elif event.type == MOUSEBUTTONDOWN:
                if yes_button.collidepoint(event.pos):
                    self.state = PLAYING
                elif no_button.collidepoint(event.pos):
                    self.state = END_SCREEN
    
    def end_screen(self):
        """Display the final score and end game message"""
        self.screen.fill(BACKGROUND)
        
        # Get player name or default
        player_name = self.player_name if self.player_name else "Player"
        
        # Draw game over text with shadow for depth
        title_shadow = self.title_font.render("Game Over!", True, DARK_GRAY)
        title_text = self.title_font.render("Game Over!", True, TEAL)
        title_shadow_rect = title_shadow.get_rect(center=(SCREEN_WIDTH//2+2, 152))
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, 150))
        self.screen.blit(title_shadow, title_shadow_rect)
        self.screen.blit(title_text, title_rect)
        
        # Draw final score in a box
        score_box = pygame.Rect(SCREEN_WIDTH//2 - 200, 220, 400, 100)
        pygame.draw.rect(self.screen, LIGHT_GRAY, score_box, border_radius=10)
        pygame.draw.rect(self.screen, DARK_GRAY, score_box, 2, border_radius=10)
        
        self.draw_text("Final Score:", self.font, DARK_GRAY, SCREEN_WIDTH//2, 250)
        self.draw_text(f"{player_name}: {self.player_score} | Computer: {self.computer_score}", 
                      self.font, DARK_GRAY, SCREEN_WIDTH//2, 290)
        
        # Determine and display result
        if self.player_score > self.computer_score:
            result_text = f"Congratulations {player_name}! You won the game!"
            result_color = SOFT_GREEN
        elif self.player_score < self.computer_score:
            result_text = "Computer won the game!"
            result_color = SOFT_RED
        else:
            result_text = "The game ended in a tie!"
            result_color = GOLD
        
        self.draw_text(result_text, self.font, result_color, SCREEN_WIDTH//2, 400)
        
        # Draw buttons for restart or quit
        button_y = 500
        button_width = 150
        button_height = 50
        button_spacing = 50
        
        restart_button = pygame.Rect(SCREEN_WIDTH//2 - button_width - button_spacing//2, button_y, button_width, button_height)
        quit_button = pygame.Rect(SCREEN_WIDTH//2 + button_spacing//2, button_y, button_width, button_height)
        
        mouse_pos = pygame.mouse.get_pos()
        restart_color = SOFT_GREEN if restart_button.collidepoint(mouse_pos) else TEAL
        quit_color = SOFT_RED if quit_button.collidepoint(mouse_pos) else TEAL
        
        pygame.draw.rect(self.screen, restart_color, restart_button, border_radius=10)
        pygame.draw.rect(self.screen, quit_color, quit_button, border_radius=10)
        
        self.draw_text("Restart", self.font, WHITE, restart_button.centerx, restart_button.centery)
        self.draw_text("Quit", self.font, WHITE, quit_button.centerx, quit_button.centery)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_r:
                    # Reset game
                    self.player_score = 0
                    self.computer_score = 0
                    self.state = MENU
                elif event.key == K_q:
                    pygame.quit()
                    sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if restart_button.collidepoint(event.pos):
                    # Reset game
                    self.player_score = 0
                    self.computer_score = 0
                    self.state = MENU
                elif quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
    
    def run(self):
        """Main game loop"""
        while True:
            if self.state == MENU:
                self.menu_screen()
            elif self.state == NAME_INPUT:
                self.name_input_screen()
            elif self.state == PLAYING:
                self.playing_screen()
            elif self.state == RESULT:
                self.result_screen()
            elif self.state == END_SCREEN:
                self.end_screen()
            
            pygame.display.update()
            self.clock.tick(FPS)
            
            # Handle quit event
            for event in pygame.event.get(QUIT):
                pygame.quit()
                sys.exit()

# Run the game
if __name__ == "__main__":
    game = Game()
    game.run()