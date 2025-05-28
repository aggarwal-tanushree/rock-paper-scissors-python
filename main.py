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
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)

# Game states
MENU = 0
PLAYING = 1
RESULT = 2
END_SCREEN = 3

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
        self.player_score = 0
        self.computer_score = 0
        self.player_choice = None
        self.computer_choice = None
        self.result = None
        
        # Load images
        self.rock_img = self.create_choice_image("ROCK", RED)
        self.paper_img = self.create_choice_image("PAPER", GREEN)
        self.scissors_img = self.create_choice_image("SCISSORS", BLUE)
        
        # Create rectangles for choices
        self.rock_rect = self.rock_img.get_rect(center=(SCREEN_WIDTH//4, SCREEN_HEIGHT//2))
        self.paper_rect = self.paper_img.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.scissors_rect = self.scissors_img.get_rect(center=(3*SCREEN_WIDTH//4, SCREEN_HEIGHT//2))
    
    def create_choice_image(self, text, color):
        """Create a colored surface with text for each choice"""
        surf = pygame.Surface((150, 150))
        surf.fill(color)
        text_surf = self.font.render(text, True, WHITE)
        text_rect = text_surf.get_rect(center=(75, 75))
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
        self.screen.fill(PURPLE)
        self.draw_text("ROCK, PAPER, SCISSORS", self.title_font, YELLOW, SCREEN_WIDTH//2, 100)
        self.draw_text("Click to start the game", self.font, WHITE, SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
        self.draw_text(f"Player Score: {self.player_score} | Computer Score: {self.computer_score}", 
                      self.small_font, WHITE, SCREEN_WIDTH//2, SCREEN_HEIGHT - 50)
        
        # Check for mouse click to start game
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                self.state = PLAYING
    
    def playing_screen(self):
        """Display the game screen where player makes a choice"""
        self.screen.fill(PURPLE)
        self.draw_text("Choose your move:", self.font, WHITE, SCREEN_WIDTH//2, 100)
        
        # Draw choice options
        self.screen.blit(self.rock_img, self.rock_rect)
        self.screen.blit(self.paper_img, self.paper_rect)
        self.screen.blit(self.scissors_img, self.scissors_rect)
        
        # Check for player choice
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.rock_rect.collidepoint(mouse_pos):
                    self.player_choice = "rock"
                    self.get_computer_choice()
                    self.determine_winner()
                    self.state = RESULT
                elif self.paper_rect.collidepoint(mouse_pos):
                    self.player_choice = "paper"
                    self.get_computer_choice()
                    self.determine_winner()
                    self.state = RESULT
                elif self.scissors_rect.collidepoint(mouse_pos):
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
        self.screen.fill(PURPLE)
        self.draw_text(f"You chose: {self.player_choice.upper()}", self.font, WHITE, SCREEN_WIDTH//2, 100)
        self.draw_text(f"Computer chose: {self.computer_choice.upper()}", self.font, WHITE, SCREEN_WIDTH//2, 150)
        self.draw_text(self.result, self.title_font, YELLOW, SCREEN_WIDTH//2, 250)
        self.draw_text(f"Player Score: {self.player_score} | Computer Score: {self.computer_score}", 
                      self.font, WHITE, SCREEN_WIDTH//2, 350)
        self.draw_text("Play again? (Y/N)", self.font, WHITE, SCREEN_WIDTH//2, 450)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_y:
                    self.state = PLAYING
                elif event.key == K_n:
                    self.state = END_SCREEN
    
    def end_screen(self):
        """Display the final score and end game message"""
        self.screen.fill(PURPLE)
        self.draw_text("Game Over!", self.title_font, YELLOW, SCREEN_WIDTH//2, 150)
        self.draw_text(f"Final Score:", self.font, WHITE, SCREEN_WIDTH//2, 250)
        self.draw_text(f"Player: {self.player_score} | Computer: {self.computer_score}", 
                      self.font, WHITE, SCREEN_WIDTH//2, 300)
        
        if self.player_score > self.computer_score:
            result_text = "You won the game!"
        elif self.player_score < self.computer_score:
            result_text = "Computer won the game!"
        else:
            result_text = "The game ended in a tie!"
        
        self.draw_text(result_text, self.font, YELLOW, SCREEN_WIDTH//2, 400)
        self.draw_text("Press R to restart or Q to quit", self.small_font, WHITE, SCREEN_WIDTH//2, 500)
        
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
    
    def run(self):
        """Main game loop"""
        while True:
            if self.state == MENU:
                self.menu_screen()
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