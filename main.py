import pygame, random

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
SCREEN_DIM = (SCREEN_WIDTH, SCREEN_HEIGHT)

SPEED = 2
GRAVITY = 0.2
JUMP_HEIGHT = 4

CLOCK = pygame.time.Clock()
    
screen = None
    
sprites = []

class Player:
    def __init__(self, colour, width, height, floor):
        super().__init__()
        
        self.colour = colour
        
        self.gravity = 0
        self.floor = floor
        
        self.image = pygame.Surface([width, height])
        self.image.fill(colour)
        self.image.set_colorkey(colour)
        
        pygame.draw.rect(self.image, colour, [0, 0, width, height])
        
        self.rect = self.image.get_rect()
        
        self.jumping = False
        
    def update(self):
        self.jumping = self.gravity > 0
                
        if self.floor.colliding(self) and not self.jumping:
            self.gravity = 0
        else:
            self.gravity -= GRAVITY
            
        self.rect.y -= self.gravity
        
    def draw(self, surface):
        pygame.draw.rect(surface, self.colour, self.rect)
        
    def jump(self):
        if self.floor.colliding(self):
            self.gravity = JUMP_HEIGHT

class Block:
    def __init__(self, floor, x, y, width, height):
        self.floor = floor
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
    def intersects(self, rect):
        x2 = rect.x + rect.width
        y2 = rect.y + rect.height
        
        if self.x >= x2 or rect.x >= self.get_max_x():
            return False
            
        if self.y >= y2 or rect.y >= self.get_max_y():
            return False  
            
        return True
        
    def contains(self, x, y):
        return x >= self.x and x <= self.get_max_x() and y >= self.y and y <= self.get_max_y()
        
    def get_max_x(self):
        return self.x + self.width
        
    def get_max_y(self):
        return self.y + self.height

class Floor:
    def __init__(self, y, screen_width):
        self.y = y
        self.screen_width = screen_width
        self.blocks = []

    def update(self): 
        while len(self.blocks) < 5:
            self.add_random_block()
        
        while self.blocks[0].get_max_x() < 0:
            self.blocks.pop(0)
        
        while self.blocks[len(self.blocks) - 1].get_max_x() < self.screen_width:
            self.add_random_block()
            
        for block in self.blocks:
            block.x -= SPEED
            
    def draw(self, surface):
        for block in self.blocks:
            pygame.draw.rect(surface, (0, 0, 255), (block.x, block.y, block.width, block.height))
        
    def add_random_block(self):
        x = 0
        
        if len(self.blocks) > 0:
            block = self.blocks[len(self.blocks) - 1]
            x = block.x + block.width + random.randint(20, 70)
        
        self.blocks.append(Block(self, x, self.y, random.randint(100, 200), 30))

    def colliding(self, player):
        for block in self.blocks:
            if block.intersects(player.rect):
                return True
               
        return False
    
def main():
    global SPEED
    
    pygame.init()
    
    screen = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption("Subway Surfers")
    
    floor = Floor(SCREEN_HEIGHT - 30, SCREEN_WIDTH)
    floor.blocks.append(Block(floor, 0, SCREEN_HEIGHT - 30, 250, 30))
    
    player = Player([255, 0, 0], 32, 64, floor)
    player.rect.x = 90
    player.rect.y = SCREEN_HEIGHT / 2
    
    sprites.append(player)
    
    running = True
    
    lastMillis = pygame.time.get_ticks()
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                player.jump()
                
        screen.fill((0, 0, 0))
        
        if player.rect.y + player.rect.height <= SCREEN_HEIGHT - 28:
            floor.update()
            
        floor.draw(screen)
                
        for sprite in sprites:
            sprite.update()
                
        for sprite in sprites: 
            sprite.draw(screen)
                
        if pygame.time.get_ticks() - lastMillis >= 1000:
            SPEED += 0.1
            lastMillis = pygame.time.get_ticks()
                
        CLOCK.tick(60)
        
        pygame.display.flip()
                
    pygame.quit()

if __name__ == '__main__':
    main()