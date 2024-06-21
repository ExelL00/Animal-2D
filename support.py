import pygame
from os import walk
from csv import reader

def import_img(path,pixel_size):
    img=pygame.image.load(path).convert_alpha()
    size=img.get_size()
    surface_list=[]
    if size[0]>pixel_size:
        title_num_x=size[0]
        for x in range(0,title_num_x,pixel_size):
            surface=pygame.Surface((pixel_size,pixel_size), flags=pygame.SRCALPHA)
            surface.blit(img,(0,0),pygame.Rect(x,0,pixel_size,pixel_size))
            surface_list.append(surface)
        return surface_list
    else:
        surface_list.append(img)
        return surface_list
def import_img_two_diff_sizes(path,pixel_size,pixelsize_two):
    img=pygame.image.load(path).convert_alpha()
    size=img.get_size()
    surface_list=[]
    if size[0]>pixel_size:
        title_num_x=size[0]
        for x in range(0,title_num_x,pixel_size):
            surface=pygame.Surface((pixel_size,pixelsize_two), flags=pygame.SRCALPHA)
            surface.blit(img,(0,0),pygame.Rect(x,0,pixel_size,pixelsize_two))
            surface_list.append(surface)
        return surface_list
    else:
        surface_list.append(img)
        return surface_list

def import_csv(path):
    with open(path) as map:
        terrain_range=[]
        Enemy_range=reader(map,delimiter=',')
        for row in Enemy_range:
            terrain_range.append(list(row))
        return terrain_range