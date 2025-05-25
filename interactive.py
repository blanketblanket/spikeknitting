'''
This file contains functions to create buttons and sliders with images that change on hover.

Dependencies: Pygame 
Install: python3 -m pip install -U pygame --user
For more information: https://www.pygame.org/wiki/GettingStarted
'''
import pygame
import math

class Button():
    '''
        Class for interactive button. 
        When drawn, returns true when clicked.

        To make this class I started by following a button tutorial by Rustam (Coding with Russ)
        but extended from that with the addition of a hoverstate
        and distinguishing between a click on the button vs coincidental pressed mouse,
        https://www.youtube.com/watch?v=G8MYGDf_9ho
    '''
    def __init__ (self, screen, x, y, img, hover_img):
        self.screen = screen #the screen the button will to be drawn to
        self.x = x #top left coordinate
        self.y = y #top left coordinate
        self.img = img # initial image
        self.hover_img = hover_img #image when button is hovered pver
        #size of button is based on the initial image
        w = img.get_width()
        h = img.get_height()
        self.area = pygame.Rect(x, y, w, h) #setting collision area
        self.hover = False
        self.previouslypressed = False
    
    def draw(self) -> bool:
        '''
            Draws button.
            Returns true when button is pressed.
        '''
        pressed = False
        clicked = False

        #if mouse is over the button, display the hover image.
        if self.area.collidepoint(pygame.mouse.get_pos()):
            self.screen.blit(self.hover_img, (self.x, self.y))
            if pygame.mouse.get_pressed()[0] == 1:
                pressed = True
        else:
            self.screen.blit(self.img, (self.x, self.y))
        
        # distinguishes between whether the mouse was dragged over while being held,
        # or if the user clicked on this button intentionally.
        if pressed and not self.previouslypressed:
            clicked = True
        if pygame.mouse.get_pressed()[0] == 1:
            self.previouslypressed = True
        else:
            self.previouslypressed = False
        return clicked
    
class Slider():
    '''
    Class for interactive slider that allows user to select from an ordered range of values. 
    When drawn, returns true when clicked.
    '''
    def __init__(self, screen, scene_manager, label, x, y, slider_img, hover_img, bar_img, values):
        self.screen = screen 
        self.scene_manager = scene_manager
        self.x = x # top left coordinate of slider bar
        self.y = y # top left coordinate of slider bar
        self.label = label 

        self.slider_img = slider_img # image of slider button before hover
        self.slider_size = self.slider_img.get_size()[0]/2
        self.slider_posX = x # default slider position is the beginning.
        self.slider_posY = y-self.slider_size+20
        self.hover_img = hover_img
        
        # default value is first value.
        self.values = values
        self.value = values[0]

        self.bar_img = bar_img
        self.len = self.bar_img.get_size()[0] #length of slider follows the bar image
        # calculate the size of each step in the bar, so the slider snaps to the nearest value.
        steps = []
        for n in range(len(values)):
            steps.append(x + n*( self.len/ (len(values)-1)))
        self.steps = steps
        # uses previous mouse position instead of current mouse position 
        # so you feel like you're dragging something
        self.pMouseX = 0

        self.clicked = False


    def draw(self):
        '''
            Draws slider, snaps slider to nearest value
            Return current value of slider.
        '''
        # draw the bar 
        self.screen.blit(self.bar_img, (self.x, self.y))
        # label the bottom value, the top value and the current value
        top = self.values[-1]
        bottom = self.values[0]
        bottom_label = self.scene_manager.h2.render(f'{bottom}', True, (0,0,0))
        self.screen.blit(bottom_label, (self.x-bottom_label.get_size()[0]/2, self.y+self.slider_size+15))
        top_label = self.scene_manager.h2.render(f'{top}', True, (0,0,0))
        self.screen.blit(top_label, (self.x+self.len-bottom_label.get_size()[0]/2, self.y+self.slider_size+15))
        value_label = self.scene_manager.h1.render(f'{self.label}{self.value}', True, (0,0,0))
        self.screen.blit(value_label, (self.x+self.len/2-value_label.get_size()[0]/2, self.y-self.slider_size-15))

        #calculate the distance of the mouse from the slider, to be used later
        mouse_pos = pygame.mouse.get_pos()
        dist_mouse = math.sqrt((mouse_pos[0] - self.slider_posX)**2 + (mouse_pos[1] - self.slider_posY-self.slider_size)**2)

        #if the slider was previously clicked, make the slider follow the mouse x position
        if self.clicked:
            self.slider_posX = mouse_pos[0]
            # stop the slider when it reaches either end of the bar
            if self.slider_posX > self.x + self.len:
                self.slider_posX = self.x + self.len
            if self.slider_posX < self.x :
                self.slider_posX = self.x
            # draw the hover image 
            self.screen.blit(self.hover_img, (self.slider_posX-self.slider_size, self.slider_posY))
            #upon letting go of the mouse, snap the slider to the nearest value
            if pygame.mouse.get_pressed()[0] != 1:
                self.clicked = False
                smallest_diff = abs(self.slider_posX-self.steps[0])
                index_closest = 0
                for n in range(len(self.steps)):
                    if abs(self.slider_posX - self.steps[n]) < smallest_diff:
                        index_closest = n
                        smallest_diff = abs(self.slider_posX - self.steps[n])
                self.slider_posX = self.steps[index_closest]
                self.value = self.values[index_closest]
        # if the slider hasn't been clicked but the mouse is hovering, draws the hover img and accept any clicks
        elif dist_mouse < self.slider_size:
            self.screen.blit(self.hover_img, (self.slider_posX-self.slider_size, self.slider_posY))
            if pygame.mouse.get_pressed()[0] == 1:
                self.clicked = True       
        #else draw the initial image.
        else:
            self.screen.blit(self.slider_img, (self.slider_posX-self.slider_size, self.slider_posY))
        self.pMouseX = mouse_pos[0] #set value of previous frame's mouse position, so the slider trails behind mouse

        return self.value 
