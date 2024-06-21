import pygame
from setting import *
from support import import_img
from timer import Timer
from random import choice

class Player(pygame.sprite.Sprite):
    def __init__(self,groups,colision_sprite,interaction_sprites,pos,z):
        super().__init__(groups)
        #graphic
        self.import_assets()

        self.alive=True

        #animation
        self.status='Idle'
        self.index=0
        self.left_animation=False

        #image setup
        self.image=self.animations[self.status][self.index]
        self.rect=self.image.get_rect(center=pos)
        self.z=z
        self.hitbox=self.rect.copy().inflate(-12,-5)
        self.hitbox_b=self.rect.copy().inflate(-12,-25)
        self.rotation = 0



        #movment
        self.direction=pygame.math.Vector2()
        self.pos=pygame.math.Vector2(self.rect.center)
        self.speed=2
        self.gravity=0.2
        self.jump=-7
        self.double_jump=0
        self.wall_jump_x=0
        self.blocked_space=False


        #timer
        self.timer={'DoubleJump':Timer(200),
                    'AnimationDouble':Timer(200),
                    'Jumpx':Timer(200,self.walljump)}

        #colision
        self.colision_sprite=colision_sprite
        self.collision_ground=False
        self.side_colision=['right','left']

        #newlvl
        self.interaction_sprites=interaction_sprites
        self.newlvl_active=False
        self.restart=True

        #inventory
        self.items=0
        self.max_items=0

    def import_assets(self):
        self.animations={'Double jump':[],
                         'Fall':[],
                         'Hit':[],
                         'Idle':[],
                         'Jump':[],
                         'Run':[],
                         'Wall Jump':[]}

        self.random_character=choice(['Mask Dude','Ninja Frog','Pink Man','Virtual Guy'])
        for animation in self.animations.keys():
            path = 'Main Characters/'+self.random_character+'/' + animation+'.png'
            self.animations[animation]=import_img(path,32)

    def input(self):
        keys=pygame.key.get_pressed()
        if not self.restart and self.alive:
            if keys[pygame.K_d] and not self.side_colision=='right' and not self.timer['Jumpx'].active:
                self.direction.x=1
                self.left_animation=False
                self.side_colision='nic'
            elif keys[pygame.K_a] and not self.side_colision=='left' and not self.timer['Jumpx'].active:
                self.direction.x=-1
                self.left_animation=True
                self.side_colision='nic'
            else:
                self.direction.x=0

            #jump
            if keys[pygame.K_SPACE] and not self.blocked_space and self.double_jump<2 and not self.timer['DoubleJump'].active:
                self.timer['DoubleJump'].acitvation()
                if self.side_colision=='left':
                    self.direction.y=self.jump
                    self.wall_jump_x=1
                    self.timer['Jumpx'].acitvation()
                    self.collision_ground = False
                    self.side_colision='nic'
                    self.left_animation = False

                elif self.side_colision=='right':
                    self.direction.y=self.jump
                    self.wall_jump_x=-1
                    self.timer['Jumpx'].acitvation()
                    self.collision_ground = False
                    self.side_colision='nic'
                    self.left_animation = True

                else:
                    self.direction.y=self.jump
                    self.double_jump+=1
                    self.collision_ground = False
                    self.side_colision='nic'
                self.blocked_space = keys[pygame.K_SPACE]
            self.blocked_space = keys[pygame.K_SPACE]

            #plaforms down
            if keys[pygame.K_s]:
                self.hitbox_b=self.rect.copy().inflate(-self.rect.width,-self.rect.height)
            else:
                self.hitbox_b = self.rect.copy().inflate(-12, -25)

            if keys[pygame.K_RETURN]:
                interaction=pygame.sprite.spritecollide(self,self.interaction_sprites,False)
                if interaction and self.items>=self.max_items:
                    self.newlvl_active=True
                    self.direction.x=0
                    self.direction.y=0
                    self.restart=True

    def animate(self):
        self.index+=0.25
        if self.index>=len(self.animations[self.status]):
            if self.status=='Hit':
                self.index=len(self.animations[self.status])-1
            else:
                self.index=0

        self.image = self.animations[self.status][int(self.index)]
        if self.left_animation:
            self.image=pygame.transform.flip(self.image,True,False)

        if not self.alive:
            if self.left_animation:
                self.rotation-=1
            else:
                self.rotation+=1
            self.image=pygame.transform.rotate(self.image,self.rotation)

    def apply_gravity(self):
        if not self.status=='Wall Jump':
            self.gravity=0.3
            self.direction.y+=self.gravity
        elif self.status=='Wall Jump':
            self.gravity=0.5
            self.direction.y=self.gravity

    def walljump(self):
        self.pos.x+=self.wall_jump_x
        self.rect.x+=self.pos.x
        self.double_jump=1

    def colision_vertical(self):
        #vertical movment
        self.pos.y += self.direction.y
        self.hitbox.centery=self.pos.y
        self.rect.centery = self.hitbox.centery

        for sprite in self.colision_sprite.sprites():
            if sprite.hitbox.colliderect(self.hitbox):
                if sprite.z==Layer['Teren'] or sprite.z==Layer['Obramowanie']:
                    if self.direction.y>0:
                        self.hitbox.bottom=sprite.hitbox.top
                        self.pos.y = self.hitbox.centery
                        self.rect.centery = self.pos.y
                        self.direction.y=0
                        self.double_jump=0
                        self.collision_ground = True
                        self.side_colision='nic'


                    elif self.direction.y<0:
                        self.hitbox.top=sprite.hitbox.bottom
                        self.pos.y= self.hitbox.centery
                        self.rect.centery = self.pos.y
                        self.direction.y=0
                        self.double_jump=1
                        self.collision_ground = False

    def colsiosn_horinztontal(self):
        #horizontal movement
        self.pos.x+=self.direction.x*self.speed
        self.hitbox.centerx=self.pos.x
        self.rect.centerx=self.hitbox.centerx


        for sprite in self.colision_sprite.sprites():
            if sprite.hitbox.colliderect(self.hitbox):
                if sprite.z==Layer['Teren'] or sprite.z==Layer['Obramowanie'] or sprite.z==Layer["Box"]:
                    if self.direction.x>0:
                        self.hitbox.right=sprite.hitbox.left
                        self.pos.x = self.hitbox.centerx
                        self.rect.centerx = self.pos.x
                        self.double_jump=1
                        if not self.collision_ground:
                            self.side_colision='right'

                    elif self.direction.x<0:
                        self.hitbox.left=sprite.hitbox.right
                        self.pos.x = self.hitbox.centerx
                        self.rect.centerx = self.pos.x
                        self.double_jump=1
                        if not self.collision_ground:
                            self.side_colision='left'

    def colision_platfroms(self):
        self.hitbox_b.midbottom=self.hitbox.midbottom
        for sprite in self.colision_sprite.sprites():
            if sprite.z==Layer['Platformy']:
                if sprite.hitbox.colliderect(self.hitbox_b):
                    if self.direction.y>0:
                        self.hitbox.bottom=sprite.hitbox.top
                        self.pos.y=self.hitbox.centery
                        self.rect.centery=self.pos.y
                        self.direction.y=0
                        self.double_jump=0

    def wall_jump_rejestr(self):
        for sprite in self.colision_sprite.sprites():
            walljump_coll=sprite.rect.colliderect(self.rect) and self.direction.y>0 and self.side_colision!='nic' and not self.collision_ground
            if walljump_coll and self.alive:
                self.status='Wall Jump'

    def dmg_boxes(self):
        for sprite in self.colision_sprite.sprites():
            if sprite.hitbox.colliderect(self.hitbox):
                if sprite.z==Layer['Box']:
                    if self.status=='Fall' or self.status=='Wall Jump':
                            self.status='Fall'
                            self.direction.y=0
                            sprite.health-=1
                            self.direction.y = self.jump

                    if self.status=='Jump' or self.status=='Double jump':
                            sprite.health-=1
                            self.hitbox.top = sprite.hitbox.bottom
                            self.pos.y = self.hitbox.centery
                            self.rect.centery = self.pos.y
                            self.double_jump=2
                            self.direction.y=0

    def check_status(self):
        if self.alive:
            #run idle
            if self.direction.x>0 or self.direction.x<0:
                self.status='Run'
            else:
                self.status='Idle'

            #fall jump
            if self.direction.y>=1:
                self.status='Fall'
                self.side_colision='nic'
                self.collision_ground=False
            if self.direction.y<0:
                self.collision_ground=True
                self.status='Jump'

            #double jump
            if self.double_jump==2 and self.direction.y<0:
                self.status='Double jump'

    def dmg_from_enemy(self):
        if self.alive:
            for sprite in self.colision_sprite.sprites():
                if sprite.z==Layer['Enemy']:
                    if (sprite.hitbox.colliderect(self.hitbox) and not self.status=='Fall') and (sprite.hitbox.colliderect(self.hitbox) and not self.status=='Jump'):
                        self.direction.x=0
                        self.direction.y=0
                        self.hitbox=self.rect.copy().inflate(-self.rect.width,-self.rect.height)

                        self.max_rect_y=self.rect.copy()
                        self.max_rect_y.y-=30

                        self.direction.y =-3

                        self.index=0
                        self.status = 'Hit'
                        self.alive = False

        else:
            if self.rect.y<=self.max_rect_y.y:
                self.direction.y +=1

    def update_timer(self):
        for timer in self.timer.values():
            timer.update()

    def update(self):
        self.update_timer()
        self.animate()
        self.input()
        self.check_status()
        self.colsiosn_horinztontal()
        self.colision_vertical()
        self.colision_platfroms()
        self.wall_jump_rejestr()
        self.dmg_boxes()
        self.dmg_from_enemy()
        if self.alive:
            self.apply_gravity()


