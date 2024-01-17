import pygame
from setting import *
from support import import_img
from random import choice,randint
from player import Player

class Generic(pygame.sprite.Sprite):
    def __init__(self,surf,pos,groups,z,id=0):
        super().__init__(groups)
        self.image=surf
        self.rect=self.image.get_rect(topleft=pos)
        self.z=z
        self.id=id


        if z==Layer['Obramowanie']:
            self.hitbox = self.rect.copy().inflate(-self.rect.width*0.9, -self.rect.height * 0.9)
        elif z==Layer['Teren']:
            self.hitbox = self.rect.copy().inflate(-self.rect.width*0.2, -self.rect.height * 0.25)
        elif z==Layer['Platformy']:
            self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.2, -self.rect.height*0.2)
        else:
            self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.5, -self.rect.height * 0.5)

class Animate(Generic):
    def __init__(self,surfs,pos,groups,z,stabile_speed=False):

        self.surfs=surfs
        self.z=z
        self.index=0
        self.speed= 0.25 if stabile_speed else randint(2,4)/10

        super().__init__(surf=surfs[self.index],
                         pos=pos,
                         groups=groups,
                         z=z)
    def animation(self):
        self.index += self.speed
        if self.index >= len(self.surfs):
            self.index = 0
            if self.z==Layer['Temporary']:
                self.kill()
        self.image = self.surfs[int(self.index)]
    def update(self):
        self.animation()

class Fruit(Animate):
    def __init__(self,pos,groups,player,z):
        self.import_assets()
        self.player=player
        self.fruit_groups=pygame.sprite.Group()

        self.player.max_items+=1


        self.pos=pos
        self.z=z
        self.fruit=choice([f for f in self.fruits_animation.keys()])

        super().__init__(surfs=self.fruits_animation[self.fruit],
                         pos=self.pos,
                         groups=[groups,self.fruit_groups],
                         z=z,)
        self.hitbox=self.rect.copy().inflate(-self.rect.width*0.5,-self.rect.height*0.55)

    def import_assets(self):
        self.fruits_animation = {'Apple': [],
                           'Bananas': [],
                           'Cherries': [],
                           'Kiwi': [],
                           'Melon': [],
                           'Orange': [],
                           'Pineapple': [],
                           'Strawberry': []}

        for img in self.fruits_animation.keys():
            path='Items/Fruits/'+img+'.png'
            self.fruits_animation[img]=import_img(path,32)

        self.death_fuit=import_img('Items/Fruits/Collected.png',32)

    def colision(self):
        for sprite in self.fruit_groups.sprites():
            if sprite.hitbox.colliderect(self.player.hitbox):
                self.player.items+=1
                Animate(surfs=self.death_fuit,
                        pos=sprite.rect.topleft,
                        groups=self.groups(),
                        z=Layer['Temporary'],
                        stabile_speed=True)
                self.kill()

    def update(self):
        self.animation()
        self.colision()

class Boxes(Generic):
    def __init__(self,name,surf,pos,groups,player,z):
        self.import_assets()
        super().__init__(surf,pos,groups,z)

        self.player=player
        self.break_box_sprites=pygame.sprite.Group()
        self.all_sprites=groups[1]
        self.pos=pos
        self.health=int(name)
        self.surf=surf
        self.direction_y=0
        self.gravity=0.3

        self.alive=True

    def import_assets(self):
        self.hit_box=import_img('Items/Boxes/Box1/Hit (28x24).png',28)
        self.break_box=import_img('Items/Boxes/Box1/Break.png',28)

    def check_death(self):
        if self.health<=0:
            self.flags=Animate(self.hit_box,self.pos,self.groups()[0],Layer['Temporary'])
            x = round(self.pos[0])
            y = round(self.pos[1])
            self.random_x = randint(x - 30, x + 30)
            self.image = self.break_box[0]
            self.z = Layer['Temporary']
            self.rect = self.image.get_rect(topleft=(self.random_x, y))
            self.break_box_sprites.add(self)
            for i in range(1, 4):
                self.random_x = randint(x - 30, x + 30)
                self.random_y = randint(y - 30, y + 40)
                self.break_box_sprites.add(
                    Generic(self.break_box[i], (self.random_x, self.random_y), self.groups()[0], Layer['Temporary']))
            self.alive=False

    def break_box_pos(self):
        self.direction_y+=self.gravity
        for sprite in self.break_box_sprites.sprites():
            sprite.rect.y+=self.direction_y
            if round(self.pos[0]<=round(sprite.rect.x)):
                sprite.rect.x+=1
            else:
                sprite.rect.x-=1

            if sprite.rect.y>SCREEN_HEIGHT+40:
                sprite.kill()

    def update(self):
        if self.alive:
            self.check_death()

        if self.break_box_sprites.sprites():
            self.break_box_pos()




