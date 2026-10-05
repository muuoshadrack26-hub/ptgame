import os
import pygame

pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# defining game speed
clock = pygame.time.Clock()


class Soldier(pygame.sprite.Sprite):

  def __init__(self, x, y, char_type, scale, direction):
    pygame.sprite.Sprite.__init__(self)
    self.x = x
    self.y = y
    self.scale = scale
    self.char_type = char_type
    self.vel = 5
    self.counter = 0
    self.frame_index = 0
    self.animation_list = []
    self.action = 0

    # loading all the character types and animations
    animation_type = ["Idle", "Run", "Jump", "Death"]
    for animation in animation_type:
      temp_list = []
      path = f"shooter_assets/img/{self.char_type}/{animation}"
      try:
        number_of_frames = len(os.listdir(path))
      except FileNotFoundError:
        number_of_frames = 1  # Fallback if assets folder is missing during test

      for i in range(number_of_frames):
        img_path = f"{path}/{i}.png"
        if os.path.exists(img_path):
          img = pygame.image.load(img_path).convert_alpha()
        else:
          # Fallback surface if image file doesn't exist locally
          img = pygame.Surface((40, 40))
          img.fill((255, 0, 0))

        img = pygame.transform.scale(
            img,
            (
                int(scale * img.get_width()),
                int(scale * img.get_height()),
            ),
        )
        temp_list.append(img)

      self.animation_list.append(temp_list)

    # Ensure list has content to prevent IndexError
    if self.animation_list and self.animation_list[self.action]:
      self.image = self.animation_list[self.action][
          self.frame_index
          if self.frame_index < len(self.animation_list[self.action])
          else 0
      ]
    else:
      self.image = pygame.Surface((40, 40))

    self.rect = self.image.get_rect()
    self.rect.center = (x, y)
    self.direction = direction
    self.jump = False
    self.flip = False

  def update_action(self, new_action):
    if self.action != new_action:
      self.action = new_action
      self.frame_index = 0
      self.counter = 0

  def draw(self, surface):
    # Correctly flip self.image instead of the main screen surface
    flipped_image = pygame.transform.flip(self.image, self.flip, False)
    surface.blit(flipped_image, self.rect)


# class instances
soja = Soldier(200, 200, "player", 0.5, 1)
run = True
while run:
  screen.fill("green")

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False

  # Continuous key polling for movement
  keys = pygame.key.get_pressed()
  if keys[pygame.K_LEFT]:
    soja.rect.x -= soja.vel
    soja.flip = True
  if keys[pygame.K_RIGHT]:
    soja.rect.x += soja.vel
    soja.flip = False

  # render game here/ call functions
  soja.draw(screen)

  pygame.display.flip()
  clock.tick(60)

pygame.quit()


