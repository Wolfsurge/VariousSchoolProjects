import pygame, random

pygame.init()
font = pygame.font.SysFont("chewy", 50)
font_small = pygame.font.SysFont("chewy", 25)

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
SCREEN_DIM = (SCREEN_WIDTH, SCREEN_HEIGHT)

SPEED = 2
GRAVITY = 0.2
JUMP_HEIGHT = 4

SPACE_RANGE = [20, 120]
WIDTH_RANGE = [100, 200]


CLOCK = pygame.time.Clock()
    
SCORE = 0
    
screen = None
    
sprites = []

class Player:
    def __init__(self, colour, width, height, floor):
        super().__init__()
        
        self.colour = colour
        
        self.gravity = 0
        self.floor = floor
        
        self.animations = [pygame.image.load("assets/running_1.png"), pygame.image.load("assets/running_2.png"), pygame.image.load("assets/running_3.png")]
        
        self.image = self.animations[0]
        self.rect = self.image.get_rect()
        
        self.jumping = False
        self.ducking = False
        
        self.timer = pygame.time.get_ticks()
        
    def update(self):
        self.jumping = self.gravity > 0
                
        if self.floor.colliding(self) and not self.jumping:
            self.gravity = 0
        else:
            self.gravity -= GRAVITY
            
        self.rect.y -= self.gravity
        
        if pygame.time.get_ticks() - self.timer > 500:
            self.timer = pygame.time.get_ticks()
            
            if self.image == self.animations[0]:
                self.image = self.animations[1]
            else:
                self.image = self.animations[0]
        
    def draw(self, surface):
        rect = self.rect
                 
        if self.ducking:
            rect = (self.rect.x, self.rect.y + 32, 51, 32)
            self.image = self.animations[2] 
        else:
            if self.image == self.animations[2]:
                self.image = self.animations[0]
            
        surface.blit(self.image, rect)

    def jump(self):
        if self.floor.colliding(self):
            self.gravity = JUMP_HEIGHT
            self.ducking = False
            
    def fall(self):  
        if not self.floor.colliding(self):
            self.gravity = JUMP_HEIGHT * -1

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
            x = block.x + block.width + random.randint(SPACE_RANGE[0], SPACE_RANGE[1])
        
        self.blocks.append(Block(self, x, self.y, random.randint(WIDTH_RANGE[0], WIDTH_RANGE[1]), 30))

    def colliding(self, player):
        for block in self.blocks:
            if block.intersects(player.rect):
                return True
               
        return False
        
class Button:
    def __init__(self, text, x, y, width, height):
        self.text = text
        self.x = x
        self.y = y 
        self.width = width
        self.height = height
        
    def update_and_render(self, surface) -> bool:
        mouse = pygame.mouse.get_pos()
        hovered = self.hovered(mouse[0], mouse[1])

        pygame.draw.rect(surface, (0, 0, 0), [self.x, self.y, self.width, self.height])

        text = font_small.render(self.text, True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.x + self.width / 2, self.y + self.height / 2))
        surface.blit(text, text_rect)

        pressed = pygame.mouse.get_pressed()

        if hovered and pressed[0]:
            return True
            
        keys = pygame.key.get_pressed()
               
        if (keys[pygame.K_RETURN] or keys[pygame.K_SPACE]):
            return True
        
        return False
        
    def hovered(self, mouseX, mouseY):
        return mouseX >= self.x and mouseX <= self.x + self.width and mouseY >= self.y and mouseY <= self.y + self.height
    
def increase_list(li, a):
    for i in range(len(li)):
        li[i] += a

def text(surface, text, x, y, colour):
    global font
    surface.blit(font.render(text, True, colour), (x, y))
    
def text_width(text):
    global font
    return font.size(text)[0]
    
def text_height(text):
    global font
    return font.size(text)[1]
    
play_again = Button("Play Again", SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 2 + 100, 200, 50)

floor = Floor(SCREEN_HEIGHT - 30, SCREEN_WIDTH)

player = Player([255, 0, 0], 32, 64, floor)
player.rect.x = 90
player.rect.y = SCREEN_HEIGHT / 2
    
def startup():
    global SCORE

    sprites.append(player)

    SCORE = 0
    player.gravity = 0
    floor.speed = 2

    floor.blocks.append(Block(floor, 0, SCREEN_HEIGHT - 30, 250, 30))
 
    player.rect.x = 50
    player.rect.y = 250
    
    alive = True
    
def main():
    global SPEED, SPACE_RANGE, WIDTH_RANGE, font, SCORE
    
    startup()
    
    screen = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption("Subway Surfers")

    font = pygame.font.SysFont(None, 24)
    
    sprites.append(player)
    
    running = True
    
    lastMillis = pygame.time.get_ticks()
    
    alive = True
        
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
               
            keys = pygame.key.get_pressed()
               
            if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and alive:
                player.jump()
                player.ducking = False
            elif keys[pygame.K_DOWN] and not player.floor.colliding(player) and alive:
                player.fall()
                player.ducking = False
                
                
        keys = pygame.key.get_pressed()   
              
        if keys[pygame.K_DOWN] and player.floor.colliding(player) and alive:
            player.ducking = True         
        else:
            player.ducking = False
              
        screen.fill((17, 128, 255))
        
        if alive:
            if player.rect.y + player.rect.height <= SCREEN_HEIGHT - 23:
                floor.update()
            
        floor.draw(screen)
                
        if alive:
            for sprite in sprites:
                sprite.update()
                
            if player.rect.y > SCREEN_HEIGHT:
                alive = False
        
        for sprite in sprites: 
            sprite.draw(screen)
            
        if not alive:
            text(screen, f"You survived {SCORE} seconds!", SCREEN_WIDTH / 2 - (text_width(f"You survived {SCORE} seconds!") / 2), SCREEN_HEIGHT / 2 - (text_height(f"You survived {SCORE} seconds!") / 2), (255, 255, 255))
            sprites.clear()
            
        
        # debug
        text(screen, f"Sco: {SCORE}", 5, 5, (255, 255, 255))
        text(screen, f"Spd: {SPEED}", 5, 25, (255, 255, 255))
        text(screen, f"Gra: {GRAVITY}", 5, 45, (255, 255, 255))
        
        if alive and pygame.time.get_ticks() - lastMillis >= 1000:
            SCORE += 1
            
            SPEED += 0.1
            increase_list(SPACE_RANGE, 3)
            increase_list(WIDTH_RANGE, 3)
            
            lastMillis = pygame.time.get_ticks()
            
        
        if not alive:
            if play_again.update_and_render(screen):
                alive = True
                startup()
                
        CLOCK.tick(60)
        
        pygame.display.flip()
                
    pygame.quit()


if __name__ == '__main__':
    main()
