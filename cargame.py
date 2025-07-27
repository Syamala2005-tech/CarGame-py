import pygame 
from pygame.locals import * 
import random 
pygame.init() 
#create a window 
width=500 
height=500 
screen_size=(width,height) 
screen=pygame.display.set_mode(screen_size) 
pygame.display.set_caption("car Game") 
#RGB colours 
white=(255,255,255) 
green=(76,208,56) 
red=(200,0,0) 
black=(0,0,0) 
yellow=(255,232,0) 
#game settings 
gameover=False 
speed=1.5 
score=0 
#markers size 
marker_width=10 
marker_height=50 
#read and edge markers 
road=(100,0,300,height) 
left_edge_marker=(95,0,marker_width,height) 
right_edge_marker=(395,0,marker_width,height) 
 
#coordinates of lanes 
left_lane=150 
center_lane=250 
right_lane=350 
lanes=[left_lane,center_lane,right_lane] 
 
#for animating movements of the lane makers 
lane_marker_move_y=0 
 
class Vehicle(pygame.sprite.Sprite): 
 
    def __init__(self, image, x, y): 
        pygame.sprite.Sprite.__init__(self) 
 
        #scale the image down so it fits in the lane 
        image_scale =45 / image.get_rect().width 
        new_width=int(image.get_rect().width * image_scale) 
        new_height = int(image.get_rect().height * image_scale) 
        self.image = pygame.transform.scale(image,(new_width, new_height)) 
 
        self.rect = self.image.get_rect() 
        self.rect.center =[x,y] 
 
class PlayerVehicle(Vehicle): 
 
    def __init__(self, x, y): 
        image = pygame.image.load(r"C:\Users\kavur\Desktop\Screenshot 2024-11-02 193729.png") 
        super().__init__(image, x, y) 
#players starting coordinates 
player_x = 250 
player_y = 400 
#create the players car 
player_group = pygame.sprite.Group() 
player = PlayerVehicle(player_x, player_y) 
player_group.add(player) 
#load the other vehile images 
image_filename = [
    r"C:\Users\kavur\Desktop\Screenshot 2024-11-02 193740.png",
    r"C:\Users\kavur\Desktop\Screenshot 2024-11-02 193755.png",
    r"C:\Users\kavur\Desktop\Screenshot 2024-11-02 193749.png"
]
vehicle_image = []
for image_filename in image_filename: 
image = pygame.image.load(image_filename) 
vehicle_image.append(image) 
#sprite group for vrhicles 
vehicle_group = pygame.sprite.Group() 
#load the crsh image 
crash = pygame.image.load(r"C:\Users\kavur\Desktop\Screenshot 2024-11-02 234343.png") 
crash_rect = crash.get_rect() 
#game loop 
clock=pygame.time.Clock() 
fps=120#frames for second 
running=True 
while running: 
 
    clock.tick(fps) 
 
    for event in pygame.event.get(): 
        if event.type==QUIT: 
            running=False 
             
#move the players car using the left or right arrow key 
        if event.type== KEYDOWN: 
 
            if event.key ==K_LEFT and player.rect.center[0] > left_lane: 
                player.rect.x -= 100 
            elif event.key == K_RIGHT and player.rect.center[0] < right_lane: 
                player.rect.x += 100 
                 
            #check if there is a swipe collision after changing lanes 
            if v in vehicle_group: 
                if pygame.sprite.collide_rect(player, v): 
 
                    gameover = True 
 
                    #place the players next to vehicle 
                    #and determine where to positioned the crash image 
                    if event.key ==K_LEFT: 
                        player.rect.left = v.rect.right 
                        crash_rect.center = [player.rect.left,(player.rect.center[1] + v.rect.center[1]) /2] 
                    elif event.key == K_RIGHT: 
                        player.rect.right = v.rect.left 
                        crash_rect.center = [player.rect.right, (player.rect.center[1] + v.rect.center[1] / 2)] 
                     
    screen.fill(green) 
 
    #draw a road 
    pygame.draw.rect(screen,white,road) 
 
    #draw the edge markers 
    pygame.draw.rect(screen,yellow,left_edge_marker) 
    pygame.draw.rect(screen,yellow,right_edge_marker) 
 
    #draw the line markers 
    lane_marker_move_y += speed*2 
    if  lane_marker_move_y >= marker_height*2: 
        lane_marker_move_y = 0 
    for y in range(marker_height* -2, height, marker_height*2): 
        pygame.draw.rect(screen, black, (left_lane+45,  y + lane_marker_move_y, marker_width, 
marker_height)) 
        pygame.draw.rect(screen, black,(center_lane+45, y + lane_marker_move_y, marker_width, 
marker_height)) 
 
    #draw the players car 
    player_group.draw(screen) 
 
    #add up to two vehicles 
    if len(vehicle_group) < 6: 
 
        #ensure there is enough gap between vehicles 
        add_vehicle = True 
        for v in vehicle_group: 
            if v.rect.top < height * 0.75: 
                add_vehicle = False 
 
        if add_vehicle: 
                 
                #select a random lane 
            lane = random.choice(lanes) 
 
                #select a random vehicle image 
            image = random.choice(vehicle_image) 
            new_vehicle = Vehicle(image, lane , -50) 
            vehicle_group.add(new_vehicle) 
 
        for v in vehicle_group: 
            v.rect.y += speed 
 
            #remove the vehicle once it is off the screen 
            if v.rect.top >= height: 
                v.kill() 
 
                #add to screen 
                score += 1 
 
                 #speed up the game after passing 5 vehicles 
                if score > 0 and score %5 ==0: 
                    speed += 1 
                  
        #draw the vehicles 
        vehicle_group.draw(screen) 
 
        #display the score 
        font = pygame.font.Font(pygame.font.get_default_font(), 16) 
        text = font.render('SCORE '+ str(score), True,white) 
        text_rect = text.get_rect() 
        text_rect.center = (50, 450) 
        screen.blit(text, text_rect) 
 
        #check if there is a head collision 
        if pygame.sprite.spritecollide(player, vehicle_group, True): 
            gameover = True 
            crash_rect.center = [player.rect.center[0], player.rect.top] 
 
        #display game over 
        if gameover: 
            screen.blit(crash, crash_rect) 
 
            pygame.draw.rect(screen,red, (0,50, width, 100)) 
 
            font = pygame.font.Font(pygame.font.get_default_font(), 16) 
            text = font.render('GAME OVER. Play Again? (Enter Y or N)',True, white) 
            text_rect = text.get_rect() 
            text_rect.center = (width / 2, 100) 
            screen.blit(text, text_rect) 
                                         
    pygame.display.update() 
     
    #check if player wants to play again 
    while gameover: 
        clock.tick(fps) 
 
        for event in pygame.event.get(): 
 
            if event.type ==QUIT: 
                gameover = False 
                running = False 
 
           # get the players input (y or n) 
            if event.type == KEYDOWN: 
                if event.key ==K_y: 
                    #reset the game 
                    gameover = False 
                    speed =1.5 
                    score = 0 
                    vehicle_group.empty() 
                    player.rect.center = [player_x, player_y] 
                elif event.key == K_n: 
                    #exit the loops 
                    gemeover = False 
                    running = False 
                     
 
pygame.quit()  
