import pygame
from support import import_img
from setting import *
from timer import Timer
from random import choice,randint
from sprites import Generic

class Enemy(pygame.sprite.Sprite):
    def __init__(self,pos,name,player,all_sprites,colision_sprites,range_enemy_sprites,z):
        super().__init__(all_sprites,colision_sprites)
        #setup
        self.name=name
        self.bullets_sprites=pygame.sprite.Group()
        #sizeimg
        if self.name=='Chicken':
            self.size_img=32
            self.hp=1
        elif self.name=='AngryPig':
            self.size_img=36
            self.hp=2
        elif self.name=='Bee':
            self.size_img=36
            self.hp=1

        self.import_assets()
        self.all_sprites = all_sprites
        self.colision_sprites=colision_sprites
        self.range_enemy_sprites=range_enemy_sprites
        self.player=player

        #img
        self.status='Idle'
        self.index=0
        self.image=self.animations[self.status][self.index]
        self.rect=self.image.get_rect(topleft=pos)
        self.hitbox=self.rect.copy().inflate(-self.rect.width * 0.2, -self.rect.height * 0.4)
        self.z=z
        self.side=False
        self.rotation = 0

        #movment
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        if self.name=='Chicken':
            self.speed=3
        elif self.name=='AngryPig':
            self.speed=1
        elif self.name=='Bee':
            self.direction.y=int(choice([1,-1]))
            self.direction.x = int(choice([1, -1]))
            self.speed=1
            self.run=False
            self.speed=2


        #timer
        self.timer={'Idle':Timer(500),
                    'Attack':Timer(1000)}
        self.attack_bee=self.timer['Attack'].active

        self.hit_pig=False
        self.alive=True

    def import_assets(self):
        if self.name=='Chicken':
            self.animations = {'Idle': [],
                               'Run': [],
                               'Hit': []}
        elif self.name=='AngryPig':
            self.animations = {'Idle': [],
                               'Run': [],
                               'Hit': [],
                               'Hit2':[],
                               'Walk':[]}
        elif self.name=='Bee':
            self.animations = {'Idle': [],
                               'Hit': [],
                               'Attack': [],
                               'BulletPieces':[],
                               'Bullet':[]}


        for img in self.animations.keys():
            path='Enemies/'+str(self.name)+'/'+img+'.png'
            self.animations[img]=import_img(path,self.size_img)

    def animation(self):
        if self.name=='Bee':
            self.index+=0.15
        else:
            self.index+=0.25
        if self.index>=len(self.animations[self.status]):
            if self.status == 'Hit':
                self.index = len(self.animations[self.status])-1
            else:
                self.index=0
        self.image=self.animations[self.status][int(self.index)]

        if self.side:
            self.image=pygame.transform.flip(self.image,True,False)

        if not self.alive:
            if self.side:
                self.rotation+=1
            else:
                self.rotation-=1
            self.image=pygame.transform.rotate(self.image,self.rotation)

    def movment(self):
        if self.alive and self.name=='Chicken':
            if self.player.rect.x<self.max_range_x and self.player.rect.x>self.min_range_x and self.max_range_y<self.player.rect.y and self.min_range_y>self.player.rect.y:
                if self.player.hitbox.x>self.hitbox.x:
                    self.direction.x=1
                    self.side=True
                else:
                    self.direction.x=-1
                    self.side=False
            else:
                if self.name=='Chicken':
                    self.direction.x=0

        if self.alive and self.name == 'AngryPig':
            if self.side and not self.timer['Idle'].active:
                self.direction.x=1
            elif not self.side and not self.timer['Idle'].active:
                self.direction.x=-1


    def colision_horizontal(self):
        self.pos.x += self.direction.x * self.speed
        self.hitbox.centerx = self.pos.x
        self.rect.centerx = self.hitbox.centerx



        for sprite in self.range_enemy_sprites.sprites():
            if self.hitbox.colliderect(sprite.hitbox):
                if self.name=='Bee':
                    if self.direction.x<0:
                        self.hitbox.left = sprite.hitbox.right
                        self.pos.x = self.hitbox.centerx
                        self.rect.centerx = self.pos.x
                        self.direction.x*=-1


                    elif self.direction.x>0:
                        self.hitbox.right = sprite.hitbox.left
                        self.pos.x = self.hitbox.centerx
                        self.rect.centerx = self.pos.x
                        self.direction.x*=-1
                if self.name=='AngryPig':
                    if self.direction.x<0:
                        self.side=True
                        if self.hp!=1:
                            self.direction.x=0
                            self.timer['Idle'].acitvation()
                    elif self.direction.x>0:
                        self.side=False
                        if self.hp!=1:
                            self.direction.x=0
                            self.timer['Idle'].acitvation()

    def colision_vertical(self):
        self.pos.y += self.direction.y * self.speed
        self.hitbox.centery=self.pos.y
        self.rect.centery = self.hitbox.centery

        for sprite in self.range_enemy_sprites.sprites():
            if self.hitbox.colliderect(sprite.hitbox):
                if self.name=='Bee':
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                        self.pos.y = self.hitbox.centery
                        self.rect.centery = self.pos.y
                        self.direction.y *= -1


                    elif self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom
                        self.pos.y = self.hitbox.centery
                        self.rect.centery = self.pos.y
                        self.direction.y *= -1

    def check_player_in_range(self):
        x=[]
        y=[]

        for sprite in self.range_enemy_sprites.sprites():
            if hasattr(sprite,'id'):
                if sprite.z==Layer['Enemy_range'] and sprite.id=='3':
                    x.append(sprite.rect.x)
                    y.append(sprite.rect.y)
        if len(x)!=0:
            self.max_range_x=max(x)
            self.min_range_x=min(x)
            self.max_range_y=min(y)
            self.min_range_y=max(y)

    def status_check(self):
        if self.direction.x!=0:
            if self.name=='Chicken':
                self.status = 'Run'
            if self.name=='AngryPig':
                if self.hit_pig:
                    self.status='Hit2'
                    self.speed=3
                    if self.index>=len(self.animations[self.status])-1:
                        self.hit_pig=False
                elif not self.hit_pig:
                    self.status= 'Walk' if self.hp>1 else 'Run'
        else:
            if self.name=='Chicken':
                self.status = 'Idle'

            if self.hit_pig:
                    self.status='Hit2'
                    self.speed=3
                    if self.index>=len(self.animations[self.status])-1:
                        self.index=len(self.animations[self.status])-1
                        if not self.timer['Idle'].active:
                            self.hit_pig=False

            else:
                self.status = 'Idle'

        if self.name=='Bee':
            if self.direction!=0 and not self.attack_bee:
                self.status='Idle'

        if not self.alive:
            self.status='Hit'

    def bullet_bee(self):
        if self.alive and self.name=='Bee':
            if randint(0,100)<1 and not self.timer['Attack'].active:
                self.timer['Attack'].acitvation()
                self.index=0
            self.attack_bee = self.timer['Attack'].active


            if self.attack_bee and len(self.bullets_sprites)<1:
                self.status='Attack'
                x=self.rect.centerx-8
                y=self.rect.centery
                if self.index>=4:
                    Generic(self.animations['Bullet'][0],(x,y),[self.all_sprites,self.bullets_sprites,self.colision_sprites],Layer['Enemy'])

            if len(self.bullets_sprites)>0:
                for sprite in self.bullets_sprites.sprites():
                    sprite.rect.y+=3
                    sprite.hitbox.y=sprite.rect.y

                    if sprite.rect.y>SCREEN_HEIGHT:
                        sprite.kill()

    def dmg_from_player(self):
        if self.alive and self.hp>0:
            if self.hitbox.colliderect(self.player.hitbox):
                if self.player.status=='Fall':
                    self.player.direction.y=self.player.jump
                    self.hp-=1
                    if self.name=='AngryPig':
                        self.hit_pig=True
                    self.index=0

                    if self.hp<=0:
                        self.player.direction.y = self.player.jump
                        self.speed=2
                        self.direction.x = 0
                        self.direction.y = 0
                        self.hitbox = self.rect.copy().inflate(-self.rect.width, -self.rect.height)

                        self.max_rect_y = self.rect.copy()
                        self.max_rect_y.y -= 40

                        if self.name=='Bee':
                            self.direction.y=-2
                        else:
                            self.direction.y = -1

                        self.index = 0
                        self.alive=False
        else:
            if self.rect.y<=self.max_rect_y.y:
                if self.name == 'Bee':
                    self.direction.y=2
                else:
                    self.direction.y=1

    def timer_update(self):
        for timer in self.timer.values():
            timer.update()

    def update(self):
        self.check_player_in_range()
        self.animation()
        self.movment()
        self.colision_horizontal()
        self.colision_vertical()
        self.status_check()
        self.dmg_from_player()
        self.bullet_bee()
        self.timer_update()
        if self.rect.y>SCREEN_HEIGHT+40:
            self.kill()
