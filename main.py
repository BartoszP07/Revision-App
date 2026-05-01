# Import modules
import pygame, sys, time

class app:
    def __init__(self):
        self.screen = pygame.display.set_mode((500, 500))
        pygame.display.set_caption("Revision")
        self.clock = pygame.time.Clock()
        self.delta_time = 0
        
    def quit_game(self):
        pygame.quit()
        sys.exit()
        
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game()
    
    def update(self):
        pass
    
    def draw(self):
        self.screen.fill((25, 25, 25))
        
    def run(self):
        while True:
            self.delta_time = self.clock.tick(60) / 1000
            
            self.events()
            self.update()
            self.draw()
            
            pygame.display.flip()
        
    
if __name__ == "__main__":
    a = app()
    a.run()