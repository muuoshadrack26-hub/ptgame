import pygame
import os

pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2D Shooter")

# Defining game speed
clock = pygame.time.Clock()

# Defining player action variables
moving_left = False
moving_right = False
shoot=False


class Soldier(pygame.sprite.Sprite):
    def __init__(self, x, y, char_type, scale, direction):
        pygame.sprite.Sprite.__init__(self)
        self.char_type = char_type
        self.scale = scale
        self.direction = direction
        self.vel = 5
        self.alive = True
        self.jump = False
        self.flip = False
        self.health=50

        # Animation states
        self.action = 0  # 0: Idle, 1: Run, 2: Jump, 3: Death
        self.frame_index = 0  # Changed from 4 to 0 to prevent crash on small animation files
        self.animation_list = []
        self.update_time = pygame.time.get_ticks()
        #bullet variables
        self.bullet_cooldown=50
        self.ammo=30
        # Loading all the character types and animations
        animation_types = ["Idle", "Run", "Jump", "Death"]
        for animation in animation_types:
            temp_list = []
            path = f"shooter_assets/img/{self.char_type}/{animation}"
            number_of_frames = len(os.listdir(path))
            for i in range(number_of_frames):
                img = pygame.image.load(f"{path}/{i}.png").convert_alpha()
                img = pygame.transform.scale(img, (int(scale * img.get_width()), int(scale * img.get_height())))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        # FIX: Assign surface variables OUTSIDE the animation loop
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update_animation(self):
        ANIMATION_COOLDOWN = 100

        # Check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

        # If animation loop is complete
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0

        # Update image based on active frame
        self.image = self.animation_list[self.action][self.frame_index]

    def draw(self, surface):
        flipped_image = pygame.transform.flip(self.image, self.flip, False)
        surface.blit(flipped_image, self.rect)

    def move(self, moving_right, moving_left):
        dx = 0
        dy = 0

        # Assign movement variables if moving right or left
        if moving_left:
            dx = -self.vel
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.vel
            self.flip = False
            self.direction = 1

        # Updating rect coordinates
        self.rect.x += dx
        self.rect.y += dy

    def update_action(self, new_action):
        # FIX: Assign new action to self.action (not the other way around)
        if new_action != self.action:
            self.action=new_action
            # Reset animation settings for the new action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
    def shoot(self):
        if self.bullet_cooldown ==0 and self.ammo>0:
            self.bullet_cooldown=20

            bullet=Bullet(self.rect.centerx + (0.6 * self.rect.width * self.direction), self.rect.centery,
                            self.direction)
            bullet_grp.add(bullet)
            self.ammo-=1

class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y,direction):
        pygame.sprite.Sprite.__init__(self)
        self.vel=5
        self.direction=direction
        self.image=pygame.image.load("shooter_assets/img/icons/bullet.png")
        self.rect=self.image.get_rect()
        self.rect.center=(x,y)

    def update(self, *args, **kwargs):
        #move the bullet
        self.rect.x+=(self.direction * self.vel)

        #check if bullet and delete bullet when it crosses screen
        if self.rect.right <0 or self.rect.left>SCREEN_WIDTH:
            self.kill()
        #checking for collisions with charaters
        if pygame.sprite.spritecollide(soja,bullet_grp,False):
            if soja.alive:
                soja.health-=5
                self.kill()

        if pygame.sprite.spritecollide(enemy, bullet_grp, False):
            if enemy.alive:
                enemy.health -= 5
                self.kill()


# Class instances
soja = Soldier(200, 200, "player", 2, 1)
enemy=Soldier(250,200,"enemy",2,1)

#sprite groups
enemy_grp=pygame.sprite.Group()
bullet_grp=pygame.sprite.Group()

run = True
while run:
    clock.tick(60)
    screen.fill("silver")

    shoot =False

    # 1. Handle Input Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # FIX: Keep keyup checks nested inside the event loop
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                moving_left = False
            if event.key == pygame.K_RIGHT:
                moving_right = False

    # Continuous keyboard holds checked using get_pressed
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        moving_left = True
        moving_right=False
    if keys[pygame.K_RIGHT]:
        moving_right = True
        moving_left=False
    if keys[pygame.K_s]:
        shoot=True

    # 2. Update player actions / animations state based on movement status
    if soja.alive:
        if moving_left or moving_right:
            soja.update_action(1)  # 1 = Run
        else:
            soja.update_action(0)  # 0 = Idle
    if soja.bullet_cooldown>0:
        soja.bullet_cooldown-=1

    if shoot:
        soja.shoot()
    # 3. Apply physics movements and frame calculations
    bullet_grp.update()
    bullet_grp.draw(screen)
    soja.move(moving_right, moving_left)
    soja.update_animation()

    # 4. Render graphics updates
    soja.draw(screen)
    enemy.draw(screen)

    pygame.display.flip()

pygame.quit()
