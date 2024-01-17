import pygame
from setting import *
from support import import_img
class Overlayer:
    def __init__(self,player):
        self.player=player
        self.display_surafce=pygame.display.get_surface()

        self.font=pygame.font.Font('Menu/Text/Painterz.ttf',30)
        self.font_surf=self.font.render(str(player.items),True,'White')
        self.slash_surf=self.font.render('/',True,'White')
        self.max_items_surf=self.font.render(str(self.player.max_items),True,'White')
        self.pos_slash=68
        self.pos_max_items=83

        self.fruits_animation = {'Apple': [],
                                 'Bananas': [],
                                 'Cherries': [],
                                 'Kiwi': []}


        self.selected_pos=0
        for img in self.fruits_animation.keys():
            path = 'Items/Fruits/' + img + '.png'
            self.fruits_animation[img] = import_img(path,32)

        #menu
        path='Menu/Text/Numbers.png'
        self.numbers_menu=[]
    def display(self):
        #surfs
        for img in self.fruits_animation.keys():
            self.selected_pos+=1
            self.display_surafce.blit(self.fruits_animation[img][0],(Pos_Overlayer[self.selected_pos]))
            if self.selected_pos>=4:
                self.selected_pos=0

        #lyrics
        self.font_surf = self.font.render(str(self.player.items), True, 'White')
        self.display_surafce.blit(self.font_surf, (50, 573))
        self.display_surafce.blit(self.slash_surf,(self.pos_slash,573))
        self.display_surafce.blit(self.max_items_surf,(self.pos_max_items,573))

        if self.player.items>=10:
            self.pos_slash=83
            self.pos_max_items=99

