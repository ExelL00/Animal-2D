import pygame
from setting import *
from support import import_img
from sprites import Animate

class UpdateLevel:
    def __init__(self,player,all_sprites,reset):
        self.display_surf=pygame.display.get_surface()
        self.player=player
        self.all_sprites=all_sprites
        self.checkpoint_activ=False
        self.surf=import_img('Items/Checkpoints/Checkpoint/Checkpoint (Flag Out) (64x64).png',64)
        self.reset=reset

        #newlvl
        self.color=255
        self.speed=-2

    def update_chechpoint(self):
        if self.player.items==self.player.max_items and not self.checkpoint_activ:
            for sprite in self.all_sprites.sprites():
                if sprite.z==Layer['Checkpoint']:
                    self.x=sprite.rect.x
                    self.y=sprite.rect.y
                    sprite.kill()
                    self.flags=Animate(self.surf,(self.x,self.y),self.all_sprites,Layer['Temporary'])
                    self.checkpoint_activ=True

        if self.checkpoint_activ:
            self.img_checkpoints = import_img('Items/Checkpoints/Checkpoint/Checkpoint (Flag Idle)(64x64).png', 64)

            if len(self.flags.groups()) == 0:
                self.flags=Animate(self.img_checkpoints, (self.x, self.y), self.all_sprites, Layer['Checkpoint'])

    def next_level(self):
        self.display_surf.fill((self.color,self.color,self.color),special_flags=pygame.BLEND_RGB_MULT)

        self.color+=self.speed
        if self.color<=0:
            self.color=0
            self.reset()





