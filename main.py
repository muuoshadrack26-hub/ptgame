import pygame
import  os
pygame.init()
SCREEN_WIDTH=800
SCREEN_HEIGHT=600
screen=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

#defining game speed
clock=pygame.time.Clock()


class soldier(pygame.sprite.Sprite):
    def __init__(self,x,y,char_type,scale,direction):
        pygame.sprite.Sprite.__init__(self)
        self.x=x
        self.y=y
        self.scale=scale
        self.vel=5
        self.counter=0
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

    def update(self, *args, **kwargs):
        keys=pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            soja.rect.x-=self.vel
            soja.flip=True
        if keys[pygame.K_RIGHT]:
            soja.rect.x+=self.vel
            soja.flip=False

#class instances
soja=soldier(200,200,"player",2,1)
run=True
while run:
    screen.fill("silver")
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False


    #render game here/ call functions
    soja.draw(screen)
    soja.update_animation()
    soja.update()


    pygame.display.flip()
    clock.tick(60)





pygame.quit()
