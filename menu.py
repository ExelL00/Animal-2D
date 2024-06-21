import pygame,sys
from setting import *
from pytmx.util_pygame import load_pygame
from sprites import Generic,Animate
from support import import_img,import_img_two_diff_sizes
import cv2

class Menu:
    def __init__(self):
        self.display_surf = pygame.display.get_surface()
        self.menu_start=True
        tmx_data=load_pygame('Menu2/Menu.tmx')
        layer = ['Buttons', 'Players','Title']
        player_numer = 1
        self.button_cliked=surf = import_img_two_diff_sizes('Menu2/button_clicked.png', 32, 59)
        self.button_not_clicked = import_img_two_diff_sizes('Menu2/Button2.png', 32, 64)

        self.color=255
        self.speed_blend=-2

        self.enter_pressed = False
        self.spirites_menu = pygame.sprite.Group()
        self.interaction_button_sprites = pygame.sprite.Group()

        self.video=cv2.VideoCapture('Menu2/background.mp4')
        self.tracks = ['Audio/Menu/KleptoLindaTitles.wav',
                       'Audio/Menu/ChillMenu.wav']
        self.current_track = 0

        for layer in layer:
            if layer=='Title':
                for x,y,surf in tmx_data.get_layer_by_name(layer).tiles():
                    Generic(surf,(x * title_size,y * title_size), self.spirites_menu,'Title')

            if layer=='Buttons':
                index=0
                for x,y,surf in tmx_data.get_layer_by_name(layer).tiles():
                    Generic(surf,(x * title_size,y * title_size), self.spirites_menu,'Buttons'+str(index))
                    index+=1
                    if index==4:
                        index=0

                surf = pygame.Surface((120, 12), flags=pygame.SRCALPHA)
                Generic(surf, (x * title_size-96, 20 * title_size), self.interaction_button_sprites, 'Menu')

            if layer=='Players':
                for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
                    surf = import_img('Menu2/Player'+str(player_numer)+'.png', 64)
                    Animate(surf, (x * title_size,y * title_size), self.spirites_menu, 'Animeted_menu')
                    player_numer+=1


    def draw_menu(self):
        for sprite in self.spirites_menu.sprites():
            self.display_surf.blit(sprite.image, sprite.rect)
        for sprite in self.interaction_button_sprites.sprites():
            self.display_surf.blit(sprite.image, sprite.rect)

    def play_music(self):
        pygame.mixer.music.load(self.tracks[self.current_track])
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play()
        self.current_track+=1
        if self.current_track==len(self.tracks):
            self.current_track=0

    def input(self):
        keys = pygame.key.get_pressed()
        enter_pressed=False
        if keys[pygame.K_w]:
            for sprite in self.interaction_button_sprites.sprites():
                sprite.rect.y=350
        elif keys[pygame.K_s]:
            for sprite in self.interaction_button_sprites.sprites():
                sprite.rect.y = 425
        elif keys[pygame.K_RETURN]:
            for sprite in self.interaction_button_sprites.sprites():
                if sprite.rect.y == 425:
                    for events in pygame.event.get():
                        sys.exit(0)
                else:
                    self.enter_pressed = True

    def colision_to_click(self):
        for sprite in self.interaction_button_sprites.sprites():
            for sprite_menu in self.spirites_menu.sprites():
                if not sprite_menu.z=='Title' and not sprite_menu.z=='Animeted_menu':
                    if sprite.rect.colliderect(sprite_menu.rect):
                        if sprite_menu.z=='Buttons0':
                            sprite_menu.image=self.button_cliked[0]
                        elif sprite_menu.z=='Buttons3':
                            sprite_menu.image = self.button_cliked[2]
                        else:
                            sprite_menu.image = self.button_cliked[1]

                    else:
                        if sprite_menu.z=='Buttons0':
                            sprite_menu.image=self.button_not_clicked[0]
                        elif sprite_menu.z=='Buttons3':
                            sprite_menu.image = self.button_not_clicked[2]
                        else:
                            sprite_menu.image = self.button_not_clicked[1]

    def adding_subtiles_to_the_menu(self):
        self.font = pygame.font.Font('Text/Painterz.ttf', 90)
        self.font_surf = self.font.render("Animal 2D", True, 'White')
        x = self.display_surf.get_size()[0] / 2 - self.font_surf.get_size()[0] / 2
        y = self.display_surf.get_size()[1] / 2 - self.font_surf.get_size()[1] / 2
        self.display_surf.blit(self.font_surf, (x, y-60))
        self.font = pygame.font.Font('Text/Painterz.ttf', 40)
        self.font_surf = self.font.render("Play", True, 'White')
        self.display_surf.blit(self.font_surf, (x + x / 2 - 40, y + 75))
        self.font_surf = self.font.render("Quit", True, 'White')
        self.display_surf.blit(self.font_surf, (x + x / 2 - 30, y + 155))

    def reset(self):
        for sprite in self.spirites_menu.sprites():
            sprite.kill()
        for sprite in self.interaction_button_sprites.sprites():
            sprite.kill()
    def run(self):
        self.success, self.video_image = self.video.read()
        self.video_image=cv2.resize(self.video_image,(SCREEN_WIDTH,SCREEN_HEIGHT))
        if self.success:
            self.video_surf = pygame.image.frombuffer(self.video_image.tobytes(), self.video_image.shape[1::-1], "BGR")
        self.display_surf.blit(self.video_surf,(0,0))

        self.draw_menu()
        self.spirites_menu.update()
        self.adding_subtiles_to_the_menu()
        self.interaction_button_sprites.update()
        self.colision_to_click()
        self.input()
        if not pygame.mixer.music.get_busy():
            self.play_music()

        self.display_surf.fill((self.color, self.color, self.color), special_flags=pygame.BLEND_RGB_MULT)
        if self.enter_pressed == True:
            self.color += self.speed_blend
            if self.color<=0:
                self.color = 0
                self.reset()
                pygame.mixer.music.stop()
                self.menu_start=False

