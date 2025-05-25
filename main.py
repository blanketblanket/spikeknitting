'''
An interactive applet that generates a repeating knitting pattern 
for a spike-textured knit.

This ended up as a GUI application and has to be run outside of the Ed environment.

Dependencies: Pygame 
Install: python3 -m pip install -U pygame --user
For more information: https://www.pygame.org/wiki/GettingStarted

Font: Delius
Designed by Natalia Raices
Copyright (c) 2010, 2011, Natalia Raices, 
Copyright (c) 2011, Igino Marini. (www.ikern.com|mail@iginomarini.com),
 with Reserved Font Names "Delia", "Delia Unicase", "Delius" and "Delius Unicase".
This Font Software is licensed under the SIL Open Font License, Version 1.1 . 
Source: https://fonts.google.com/specimen/Delius 
'''
import pygame
import interactive
import knitting
import sys

WINDOW_HEIGHT = 800
WINDOW_WIDTH = 1200

YARN_TO_NEEDLESIZE = {
    '2 ply': '1.5 mm',
    '4 ply': '2.5 mm',
    '5 ply': '3 mm',
    '8 ply': '3.75 mm',
    '10 ply': '4.5 mm',
    '12 ply': '5.5 mm',
    '14+ ply': '7mm'
}


class App:
    # Stores the different scenes and the settings for the GUI/initial loadstate.
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
        self.scene_manager = SceneManager('setting', '8 ply',  4, 4)
        self.setting_scene = Setting_Scene(self.screen, self.scene_manager)
        self.pattern_scene = Pattern_Scene(self.screen, self.scene_manager)
        self.scenes = {
            'setting': self.setting_scene,
            'pattern': self.pattern_scene
        }
        # The logic of the scene manager is based on a tutorial by Coding with Sphere
        # https://www.youtube.com/watch?v=r0ixaTQxsUI

    def run(self):
        #runs until window is closed.
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.flip()
            self.scenes[self.scene_manager.getScene()].run() 

class Setting_Scene:
    # The title and settings scene
    # Displays sliders to change pattern settings and a button to generate the pattern
    # Also shows you an example of the knitting results.
    def __init__(self, screen, scene_manager):
        self.screen = screen  
        self.scene_manager = scene_manager

        #load background and title images
        self.background_img = pygame.image.load('Images/background.jpg').convert()
        self.title_img = pygame.image.load('Images/title.png').convert_alpha()

        #load button to generate a pattern
        pattern_img = pygame.image.load('Images/pattern.png').convert_alpha()
        pattern_hover_img = pygame.image.load('Images/pattern_hover.png').convert_alpha()
        self.pattern_button = interactive.Button(self.screen, WINDOW_WIDTH-390, WINDOW_HEIGHT-205, pattern_img, pattern_hover_img)

        #load picture of finished knit (a hat) and its collision area for its hoverstate
        self.hat_img = pygame.image.load('Images/hat.png').convert_alpha()
        self.hat_area = pygame.Rect(55, WINDOW_HEIGHT-604, 600, 524)
        self.hat_hover = pygame.transform.rotate(pygame.image.load('Images/hat.png').convert_alpha(), 6)
        
        #load slider to control the size of the yarn
        s1_img = pygame.image.load('Images/slider1_img.png').convert_alpha()
        s1_hover_img = pygame.image.load('Images/slider1_hover_img.png').convert_alpha()
        s1_bar_img = pygame.image.load('Images/slider1_bar.png').convert_alpha()
        s1_range = ['2 ply', '4 ply', '5 ply', '8 ply', '10 ply', '12 ply', '14+ ply']
        self.yarn_slider = interactive.Slider(self.screen, self.scene_manager,'Yarn Weight: ', 740, 235, s1_img, s1_hover_img, s1_bar_img, s1_range)
        
        #load slider to control the spikiness of the pattern
        s2_img = pygame.image.load('Images/slider2_img.png').convert_alpha()
        s2_hover_img = pygame.image.load('Images/slider2_hover_img.png').convert_alpha()
        s2_bar_img = pygame.image.load('Images/slider2_bar.png').convert_alpha()
        s2_range = [2, 3, 4, 5, 6, 7, 8]
        self.height_slider = interactive.Slider(self.screen, self.scene_manager,'Spike Size: ', 740, 370, s2_img, s2_hover_img, s2_bar_img, s2_range)
        
        #load slider to control the distance between the spikes
        s3_img = pygame.image.load('Images/slider3_img.png').convert_alpha()
        s3_hover_img = pygame.image.load('Images/slider3_hover_img.png').convert_alpha()
        s3_bar_img = pygame.image.load('Images/slider3_bar.png').convert_alpha()
        s3_range = [1, 2, 3, 4]
        self.dist_slider = interactive.Slider(self.screen, self.scene_manager, 'Spike Distance: ', 740, 505, s3_img, s3_hover_img, s3_bar_img, s3_range)

    def run(self):
        '''
        function that draws the whole settings scene and manages interactivity/logic
        '''
        self.screen.fill((255,255,255))
        self.screen.blit(self.background_img, (0, 0))
        self.screen.blit(self.title_img, (0, 15))

        #display the hoverstate of the hat
        if self.hat_area.collidepoint(pygame.mouse.get_pos()):
            self.screen.blit(self.hat_hover, (20, WINDOW_HEIGHT-635))
        else:
            self.screen.blit(self.hat_img, (55, WINDOW_HEIGHT-604))
        
        #draws the sliders, sets the pattern params and passes them to the scene manager.
        yarn = self.yarn_slider.draw()
        height = self.height_slider.draw()
        dist = self.dist_slider.draw()
        self.scene_manager.setPattern(yarn, height, dist)

        # draws the pattern button and tells the scene manager to change the scene when pressed
        if self.pattern_button.draw():
            self.scene_manager.setScene('pattern')

class Pattern_Scene:
    # The scene displaying the final pattern and instructions on how to make it.
    def __init__(self, screen, scene_manager):
        self.screen = screen  
        self.scene_manager = scene_manager

        #load back button to go back to settings scene.
        back_img = pygame.image.load('Images/back.png').convert_alpha()
        back_hover_img = pygame.image.load('Images/back_hover.png').convert_alpha()
        self.back_button = interactive.Button(self.screen, WINDOW_WIDTH-240, 22, back_img, back_hover_img)

    def run(self):
        '''
        function that draws the whole pattern scene and manages interactivity
        '''
        #generate pattern based on parameters stored by the scene manager
        bump_height = self.scene_manager.getHeight()
        bump_distance = self.scene_manager.getDist()
        pattern = knitting.generate_pattern(bump_height, bump_distance)

        #draw the scene.
        self.screen.fill((255,255,255))
        self.draw_legend()
        self.draw_instructions(pattern)
        self.draw_pattern(pattern)

        #draws back button to go back to settings scene when pressed
        if self.back_button.draw():
            self.scene_manager.setScene('setting')


    def draw_legend(self):
        '''
        Function that draws 
        - the yarn description - based on information stored by the scene manager
        - recommended needle size - based on dictionary 
        - knitting pattern symbols and their meanings
        '''
        # draw yarn size and recommended needle size
        yarn = self.scene_manager.getYarn()
        yarn_desc = self.scene_manager.h2.render(f'Yarn: {yarn}', True, (0,0,0))
        self.screen.blit(yarn_desc, (50, 40))
        needle_desc = self.scene_manager.h2.render(f'Suggested Needle Size: {YARN_TO_NEEDLESIZE[yarn]}', True, (0,0,0))
        self.screen.blit(needle_desc, (50, 70))

        #begin drawing the legend
        legendtitle = self.scene_manager.h2.render('Diagram Legend', True, (0,0,0))
        self.screen.blit(legendtitle, (50, 115))

        #draw knit symbol and meaning
        rect = (50, 160, 20, 20)
        pygame.draw.rect(self.screen, (0,0,0), rect, 2)
        k1 = self.scene_manager.body.render('Knit one', True, (0,0,0))
        self.screen.blit(k1, (130, 160))

        # draw KYoK symbol and meaning
        pygame.draw.line(self.screen, (0,0,0), (55, 199), (60,211), 2)
        pygame.draw.line(self.screen, (0,0,0), (60, 199), (60,211), 2)
        pygame.draw.line(self.screen, (0,0,0), (65, 199), (60,211), 2)
        rect = (50, 195, 20, 20)
        pygame.draw.rect(self.screen, (0,0,0), rect, 2)
        kyok = self.scene_manager.body.render('KYoK: Knit one, yarn over', True, (0,0,0))
        self.screen.blit(kyok, (130, 195))
        kyok2 = self.scene_manager.body.render('knit one in same stitch', True, (0,0,0))
        self.screen.blit(kyok2, (130, 215))

        #draw SK2P symbol and meaning
        pygame.draw.line(self.screen, (0,0,0), (80, 253), (60,265), 2)
        pygame.draw.line(self.screen, (0,0,0), (80, 253), (80,265), 2)
        pygame.draw.line(self.screen, (0,0,0), (80, 253), (100,265), 2)
        rect = (49, 249, 22, 22)
        pygame.draw.rect(self.screen, (0,0,0), rect, 2)
        rect = (69, 249, 22, 22)
        pygame.draw.rect(self.screen, (0,0,0), rect, 2)
        rect = (89, 249, 22, 22)
        pygame.draw.rect(self.screen, (0,0,0), rect, 2)
        sk2p = self.scene_manager.body.render('SK2P: Slip one knitwise, knit two ', True, (0,0,0))
        self.screen.blit(sk2p, (130, 250))
        sk2p2 = self.scene_manager.body.render('together, pass slipped stitch over.', True, (0,0,0))
        self.screen.blit(sk2p2, (130, 270))

    def draw_instructions(self, pattern):
        '''
        function that takes a pattern and 
        draws instructions for it, aligned to bottom left of screen
        '''
        screen = self.screen
        h2 = self.scene_manager.h2
        body = self.scene_manager.body
        instructions = knitting.pattern_to_strarray(pattern)
        starting_point = WINDOW_HEIGHT - len(instructions)*20 - 50
        for n in range(len(instructions)):
            if n == 0: #the first line is always the heading 'Instructions'
                line = h2.render(instructions[n], True, (0,0,0))
                screen.blit(line, (50, starting_point-20))
            else:
                line = body.render(instructions[n], True, (0,0,0))
                screen.blit(line, (50, starting_point+n*20))

    def draw_pattern(self, pattern):
        '''
        function that takes a pattern and draws it from bottom right (row 1)
        to top (last row), depending on stitch.
        '''
        
        screen = self.screen
        #takes pattern height and width to scale pattern to window size
        pattern_height = len(pattern)
        pattern_width = pattern[0][0][1] + pattern[0][1][1] 
        scale = 700/(max(pattern_height,pattern_width)) 

        #for every row of the pattern...
        for n in range(len(pattern)):
            row = pattern[n]
            #start from the bottom of the pattern area...
            y = WINDOW_HEIGHT - scale * (n+1) -50  
            x = WINDOW_WIDTH - 750
            l_weight = 2 #line weight
            ofst = l_weight/2 #offset squares to accomodate for line weight
            # draw a box for every stitch in the pattern from left to right
            # note: pattern is drawn left to right but read by human right to left.
            for i in range(len(row)):
                stitch = row[i][0]
                count = row[i][1]
                if stitch == ' ':
                    x += scale * count
                elif stitch == 'kyok':
                    rect = pygame.Rect(x-ofst, y-ofst, scale + l_weight, scale + l_weight)
                    pygame.draw.rect(screen, (0,0,0), rect , l_weight)
                    pygame.draw.line(screen, (0,0,0), (x+scale/4, y+scale/4), (x+scale/2, y+scale*3/4), l_weight+1)
                    pygame.draw.line(screen, (0,0,0), (x+scale*3/4, y+scale/4), (x+scale/2, y+scale*3/4), l_weight+1)
                    pygame.draw.line(screen, (0,0,0), (x+scale/2, y+scale/4), (x+scale/2, y+scale*3/4), l_weight+1)
                    x += scale
                elif stitch == 'sk2p':
                    pygame.draw.line(screen, (0,0,0), (x+scale*3/2, y+scale/4), (x+scale*5/2, y+scale*3/4), l_weight+1)
                    pygame.draw.line(screen, (0,0,0), (x+scale*3/2, y+scale/4), (x+scale/2, y+scale*3/4), l_weight+1)
                    pygame.draw.line(screen, (0,0,0), (x+scale*3/2, y+scale/4), (x+scale*3/2, y+scale*3/4), l_weight+1)
                    rect = pygame.Rect(x-ofst, y-ofst, scale + l_weight, scale + l_weight)
                    pygame.draw.rect(screen, (0,0,0), rect , l_weight)
                    x += scale
                    rect = pygame.Rect(x-ofst, y-ofst, scale + l_weight, scale + l_weight)
                    pygame.draw.rect(screen, (0,0,0), rect , l_weight)
                    x += scale
                    rect = pygame.Rect(x-ofst, y-ofst, scale + l_weight, scale + l_weight)
                    pygame.draw.rect(screen, (0,0,0), rect , l_weight)
                    x += scale
                elif stitch == 'k':
                    for no in range(count):
                        rect = pygame.Rect(x-ofst, y-ofst, scale + l_weight, scale + l_weight)
                        pygame.draw.rect(screen, (0,0,0), rect , l_weight)
                        x += scale

class SceneManager:
    '''
        Manages which scene is currently active.
        Loads fonts and their settings.
        Stores information passed between scenes.
    '''
    def __init__(self, scene, yarn, bump_height, bump_dist):
        self.scene = scene
        self.yarn = yarn
        self.bump_height = bump_height
        self.bump_dist = bump_dist
        #load fonts
        self.h1 = pygame.font.Font('Delius-Regular.ttf', 30)
        self.h2 = pygame.font.Font('Delius-Regular.ttf', 24)
        self.body = pygame.font.Font('Delius-Regular.ttf', 16)

    def getScene(self):
        return self.scene
    
    def setScene(self, scene):
        self.scene = scene
    
    def getYarn(self):
        return self.yarn
    
    def getHeight(self):
        return self.bump_height
    
    def getDist(self):
        return self.bump_dist
    
    def setPattern(self, yarn, bump_height, bump_dist):
        self.yarn = yarn
        self.bump_height = bump_height
        self.bump_dist = bump_dist 

if __name__ == '__main__':
    app = App()
    app.run()
