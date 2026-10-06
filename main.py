import pygame
import  os
pygame.init()
SCREEN_WIDTH=800
SCREEN_HEIGHT=600
screen=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

#defining game speed
clock=pygame.time.Clock()
#defining player action variables
moving_left=False
moving_right=False


class soldier(pygame.sprite.Sprite):
    def __init__(self,x,y,char_type,scale,direction):
        pygame.sprite.Sprite.__init__(self)
        self.x=x
        self.y=y
        self.speed=5
        self.scale=scale
        self.vel=5
        self.counter=0
        self.alive=True
        self.action=0
        self.jump = False
        self.flip = False
        #animation states
        self.frame_index = 4
        self.animation_list = []
        self.char_type = char_type
        self.update_time=pygame.time.get_ticks()


        #loading all the character types and animations
        animation_type=["Idle","Run","Jump","Death"]
        for animation in animation_type:
            temp_list=[]
            number_of_frames=len(os.listdir(f"shooter_assets/img/{self.char_type}/{animation}"))
            for i in range(number_of_frames):
                img=pygame.image.load(f"shooter_assets/img/{self.char_type}/{animation}/{i}.png").convert_alpha()
                img=pygame.transform.scale(img,(int(scale *img.get_width()),int(scale*img.get_height())))
                temp_list.append(img)

            self.animation_list.append(temp_list)
            self.image=self.animation_list[self.action][self.frame_index]
            self.rect=self.image.get_rect()
            self.rect.center=(x,y)
            self.direction=direction

    def update_animation(self):
        #animation cooldown
        ANIMATION_COOLDOWN=100
        #update image based on  last frame
        self.image=self.animation_list[self.action][self.frame_index]
        #check if enough time has passed since the last update
        if pygame.time.get_ticks()-self.update_time>ANIMATION_COOLDOWN:
            self.update_time=pygame.time.get_ticks()
            self.frame_index+=1
        #if animation loop is complete
        if self.frame_index>=len(self.animation_list[self.action]):
            self.frame_index=0
    def draw(self,surface):
        flipped_image=pygame.transform.flip(self.image,self.flip,False)
        surface.blit(flipped_image,self.rect)

    def move(self,moving_right,moving_left):
        #reset movement variables
        dx=0
        dy=0
        #assign movement variables if moving right or left
        if moving_left:
            dx=-self.vel
            self.flip=True
            self.direction=-1
        if moving_right:
            dx = self.vel
            self.flip = False
            self.direction = 1
        #updatimg rect coordinates
        self.rect.x+=dx
        self.rect.y+=dy

    def update(self, *args, **kwargs):
       pass

    def update_action(self,new_action):
        if new_action !=self.action:
            new_action=self.action

            #updating animation settings
            self.frame_index=0
            self.update_time=pygame.time.get_ticks()





#class instances
soja=soldier(200,200,"player",2,1)
run=True
while run:
    clock.tick(60)
    screen.fill("silver")

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
    if keys[pygame.K_RIGHT]:
        moving_right = True

    # 2. Update player actions / animations state based on movement status
    if soja.alive:
        if moving_left or moving_right:
            soja.update_action(1)  # 1 = Run
        else:
            soja.update_action(0)  # 0 = Idle

    # 3. Apply physics movements and frame calculations
    soja.move(moving_right, moving_left)
    soja.update_animation()

    # 4. Render graphics updates
    soja.draw(screen)

    pygame.display.flip()

pygame.quit()
