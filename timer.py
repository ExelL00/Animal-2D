import pygame

class Timer:
    def __init__(self,duration,func=None):
        self.start_timer=0
        self.active=False
        self.duration=duration
        self.func=func

    def acitvation(self):
        self.active=True
        self.start_timer=pygame.time.get_ticks()

    def deactivation(self):
        self.active=False
        self.start_timer=0

    def update(self):
        current_time=pygame.time.get_ticks()
        if self.func and self.start_timer != 0:
            self.func()
        if current_time-self.start_timer>=self.duration:
            self.deactivation()