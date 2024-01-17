import pygame
from player import Player
from setting import *
from pytmx.util_pygame import load_pygame
from sprites import Generic,Fruit,Animate,Boxes
from overlayer import Overlayer
from support import import_img,import_csv
from updatelevel import UpdateLevel
from random import choice
from enemy import Enemy


class Level:
    def __init__(self):
        self.display_surface=pygame.display.get_surface()
        self.lvl=1
        #groups
        self.all_sprites=CameraGroup()
        self.collision_sprites=pygame.sprite.Group()
        self.interaction_sprites=pygame.sprite.Group()
        self.range_enemy_sprites=pygame.sprite.Group()

        #restart
        self.restart=True
        self.color=0
        self.speed_blend=2
        #setup
        self.setup()


        #overlayer
        self.overlayer=Overlayer(self.player)

        #update lvl
        self.updatelevel=UpdateLevel(self.player,self.all_sprites,self.reset)

    def setup(self):
        tmx_data=load_pygame('Data/Level'+' '+str(self.lvl)+'/Mapa.tmx')
        self.background_random=choice(['Blue','Brown','Gray','Pink','Purple','Yellow'])
        self.background_img=pygame.image.load('Background/'+self.background_random+'.png').convert_alpha()


        layer_s=['Obramowanie','Background','Obramowanie v2','Teren','Platformy','Start','Checkpoint','Checkpoint_object',
                    'Owoce','Box','Enemy_range','Enemy']
        layer_name=[]
        for layer in layer_s:
            for layer_data in tmx_data.layernames:
                if layer==layer_data:
                    layer_name.append(layer)

        for layer in layer_name:
            if layer=='Obramowanie':
                    for x,y,surf in tmx_data.get_layer_by_name(layer).tiles():
                        Generic(surf,(x * title_size,y * title_size),[self.all_sprites,self.collision_sprites],Layer['Obramowanie'])

            if layer=='Background':
                for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
                    Generic(surf, (x * title_size, y * title_size), self.all_sprites ,Layer['Background'])

            if layer=='Obramowanie v2':
                    for x,y,surf in tmx_data.get_layer_by_name(layer).tiles():
                        Generic(surf,(x * title_size,y * title_size),[self.all_sprites,self.collision_sprites],Layer['Obramowanie'])

                #terrain
            if layer=='Teren':
                    for x,y,surf in tmx_data.get_layer_by_name(layer).tiles():
                        Generic(surf,(x * title_size,y * title_size),[self.all_sprites,self.collision_sprites],Layer['Teren'])

                #platformy
            if layer=='Platformy':
                    for x,y,surf in tmx_data.get_layer_by_name(layer).tiles():
                        surf_p=pygame.Surface((16,5.5))
                        surf_p.blit(surf,(0,0))
                        Generic(surf_p,(x * title_size,y * title_size),[self.all_sprites,self.collision_sprites],Layer['Platformy'])

                #Start
            if layer=='Start':
                    for x,y,surf in tmx_data.get_layer_by_name(layer).tiles():
                        surf=import_img('Items/Checkpoints/Start/Start (Moving) (64x64).png',64)
                        x=x*title_size
                        y=y*title_size-45
                        self.pos_player=(x+40,y)
                        Animate(surf,(x,y),self.all_sprites,Layer['Teren'])

                #checkpoint
            if layer=='Checkpoint':
                    for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
                        surf=pygame.image.load('Items/Checkpoints/Checkpoint/Checkpoint (No Flag).png').convert_alpha()
                        x=x*title_size
                        y=y*title_size-45
                        self.player = Player(self.all_sprites, self.collision_sprites, self.interaction_sprites,
                                             (self.pos_player), Layer['Gracz'])
                        Generic(surf, (x,y), self.all_sprites, Layer['Checkpoint'])

            if layer=='Checkpoint_object':
                    for obj in tmx_data.get_layer_by_name(layer):
                        surf=pygame.Surface((48,48),flags=pygame.SRCALPHA)
                        Generic(surf, (obj.x+15,obj.y+2), self.interaction_sprites, Layer['Checkpoint_obj'])


            #Owoce
            if layer=='Owoce':
                    for x,y,surf in tmx_data.get_layer_by_name(layer).tiles():
                        y=y-1
                        Fruit((x * title_size,y * title_size),self.all_sprites,self.player,Layer['Owoce'])

            #box
            if layer=='Box':
                for obj in tmx_data.get_layer_by_name(layer):
                    Boxes(obj.name, obj.image, (obj.x, obj.y), [self.all_sprites, self.collision_sprites], self.player,Layer['Box'])

            #enemyrange
            if layer=='Enemy_range':
                csv='Data/Level'+' '+str(self.lvl)+'/Mapa_Enemy_range.csv'
                data_csv=import_csv(csv)

                surf=pygame.Surface((16,16), flags=pygame.SRCALPHA)


                for row_index,row in enumerate(data_csv):
                    for col_index, val in enumerate(row):
                        if val!='-1':
                            #print(val) #id 1 or 3
                            Generic(surf,(col_index*title_size,row_index*title_size),[self.all_sprites,self.range_enemy_sprites],Layer['Enemy_range'],val)


            #enemy
            if layer=='Enemy':
                for obj in tmx_data.get_layer_by_name(layer):
                    Enemy((obj.x,obj.y-8),obj.name,self.player, self.all_sprites,self.collision_sprites,self.range_enemy_sprites, Layer['Enemy'])

        #background
        for i in range(0,SCREEN_WIDTH,64):
            for j in range(-64,SCREEN_HEIGHT,64):
                Generic(self.background_img,(i,j),self.all_sprites,Layer['Background_animation'])

    def animation_background(self):
        for sprite in self.all_sprites.sprites():
            if sprite.z==Layer['Background_animation']:
                sprite.rect.y+=1
                if sprite.rect.y>SCREEN_HEIGHT+30:
                    sprite.rect.y=-64

    def reset(self):
        for sprite in self.all_sprites.sprites():
            sprite.kill()
        for sprite in self.interaction_sprites.sprites():
            sprite.kill()

        if self.player.alive:
            self.lvl+=1
        self.setup()

        self.restart=True

        self.overlayer = Overlayer(self.player)
        self.updatelevel = UpdateLevel(self.player, self.all_sprites, self.reset)

    def run(self):
        self.all_sprites.custom_draw()
        self.all_sprites.update()
        self.animation_background()
        self.overlayer.display()
        self.updatelevel.update_chechpoint()

        if self.restart:
            self.display_surface.fill((self.color,self.color,self.color),special_flags=pygame.BLEND_RGB_MULT)

            self.color+=self.speed_blend
            if self.color>=255:
                self.color=0
                self.restart=False
                self.player.restart=self.restart

        if not self.player.alive:
            self.updatelevel.next_level()
        if self.player.newlvl_active:
            self.updatelevel.next_level()

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surf=pygame.display.get_surface()
    def custom_draw(self):
        for layer in Layer.values():
            for sprite in self.sprites():
                if layer==sprite.z:
                    self.display_surf.blit(sprite.image, sprite.rect)


                    # hitbox_surf=pygame.Surface((sprite.hitbox.width,sprite.hitbox.height))
                    # hitbox_surf.fill('red')
                    # self.display_surf.blit(hitbox_surf,sprite.hitbox)
                    #
                    # if hasattr(sprite, 'hitbox_b'):
                    #     hitbox_b_surf = pygame.Surface((sprite.hitbox_b.width, sprite.hitbox_b.height))
                    #     hitbox_b_surf.fill('blue')
                    #     self.display_surf.blit(hitbox_b_surf, sprite.hitbox_b)




