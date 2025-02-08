import pygame
import time

class StressBar:
    def __init__(self, x, y, width=90, height=600, max_stress=100):
        """
        Initializes the stress bar.

        Parameters:
            x (int): X position of the bar.
            y (int): Y position of the bar.
            width (int): Width of the bar.
            height (int): Max height of the bar.
            max_stress (int): Maximum stress value.
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.max_stress = max_stress
        self.current_stress = 0
        self.color = (128, 0, 128)
        self.active = False
        self.sound_time = 0.0
        self.last_update_time = 0.0
        pygame.font.init()
        self.font = pygame.font.Font(None, 48)

    def start(self):
        """
        Activates stress increase (should be called when game starts).
        """
        self.active = True
        self.last_update_time = time.time()  # Start the timer

    def update(self):
        """
        Increases stress automatically every second (only if activated).
        """
        if self.active:
            current_time = time.time()
            if current_time - self.last_update_time >= 0.7:  # timer for the augmentation
                self.current_stress = min(self.max_stress, self.current_stress + 1)  # Increase %
                self.last_update_time = current_time  # Reset timer
            if current_time - self.sound_time >= 10.0 / ((1 + self.current_stress) * 0.1): # timer for the sound
                pygame.mixer.init()
                pygame.mixer.music.load("assets/music/stress_bar_sound.mp3")
                pygame.mixer.music.play(0)
                self.sound_time = current_time

    def change_stress(self, change):
        """
        Manually increase or decrease stress.
        Parameters:
            change (float): Positive to increase, negative to decrease.
        """
        self.current_stress = max(0, min(self.max_stress, self.current_stress + change))

    def draw(self, screen):
        """
        Draws the stress bar on the screen.
        Parameters:
            screen (pygame.Surface): The game screen.
        """
        filled_height = (self.current_stress / self.max_stress) * self.height

        # Draw the stress bar (grows upwards)
        pygame.draw.rect(screen, self.color,
                         (self.x, self.y + self.height - filled_height, self.width, filled_height))

        pygame.draw.rect(screen, (255, 255, 0), (self.x, self.y, self.width, self.height), 3)
        stress_text = f"{self.current_stress:.0f}%"
        text_surface = self.font.render(stress_text, 1, (255, 255, 255))  # White
        text_x = self.x + (self.width // 2) - (text_surface.get_width() // 2)
        text_y = self.y - 35  # Position above the bar
        screen.blit(text_surface, (text_x, text_y))
