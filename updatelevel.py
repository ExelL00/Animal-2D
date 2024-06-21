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

        # tsountrack
        self.tracks = ['Audio/Win/PitcherPerfectTheme.wav',
                       'Audio/Win/VictoryLap.wav']
        self.current_track = 0

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

    def play_music(self):
        pygame.mixer.music.load(self.tracks[self.current_track])
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play()
        self.current_track += 1
        if self.current_track == len(self.tracks):
            self.current_track = 0

    def last_level_end(self):
        if self.color==255:
            pygame.mixer.music.stop()
        if not pygame.mixer.music.get_busy():
            self.play_music()

        self.display_surf.fill((self.color,self.color,self.color),special_flags=pygame.BLEND_RGB_MULT)

        self.color+=self.speed
        if self.color<=0:
            self.color=0
            self.font = pygame.font.Font('Text/Painterz.ttf', 100)
            self.font_surf = self.font.render("THE END", True, 'White')
            x=self.display_surf.get_size()[0]/2-self.font_surf.get_size()[0]/2
            y=self.display_surf.get_size()[1]/2-self.font_surf.get_size()[1]/2
            self.display_surf.blit(self.font_surf, (x,y))
            self.font = pygame.font.Font('Text/Painterz.ttf', 25)
            self.font_surf = self.font.render("Tworcy:", True, 'White')
            self.display_surf.blit(self.font_surf, (x+x/2-50,y+100))
            self.font_surf = self.font.render("Robert Harasiuk i Wiktor Bebacz:", True, 'White')
            self.display_surf.blit(self.font_surf, (x+20,y+120))






