import pygame
import random
import math

pygame.init()

# class allows for the creating the maximum and minimum amounts for the list to be ranged for sorting
# class also allows for providing the colors and fonts and set width and height for the screen and etc

class DrawInformation:
    black = 0,0,0
    white = 255,255,255
    green = 0,255,0
    red = 255,0,0
    
    font = pygame.font.SysFont('timesnewroman', 20)
    l_font = pygame.font.SysFont('timesnewroman', 40)
   
    gradient = [(128, 128, 128), (160,160,160), (192,192,192)]
    
    background_color = white
    
    side_pad = 100
    top_pad = 150
    
    
    def __init__(self, width, height, lst) -> None:
        self.width = width
        self.height = height
       
        
        #setsup the window of pygame (visual is setup)
        self.window = pygame.display.set_mode((width, height))
        #name of the window
        pygame.display.set_caption("Sorting Algorithm Visualization")
        
        #class function to setup lists for sorting
        self.set_list(lst)
        
    def set_list(self, lst):
        self.lst = lst
        self.max_value = max(lst)
        self.min_val = min(lst)
        
        self.pixel_width = round((self.width - self.side_pad) / len(lst))
        
        self.pixel_height = math.floor((self.height - self.top_pad)/(self.max_value - self.min_val))
        
        self.start_x = self.side_pad // 2
        
# function is used to display the visualizer
       
def dra_info(inf_draw):
    inf_draw.window.fill(inf_draw.background_color)
    
    controls = inf_draw.font.render("R : Reset | Space : Sorting | A : Ascending | D : Descending", 1, inf_draw.black) 
    inf_draw.window.blit(controls, ( inf_draw.width/2 - controls.get_width()/2,5))
    
    sorting = inf_draw.font.render("I : Insertion Sort | B : Bubble Sort", 1, inf_draw.black)
    inf_draw.window.blit(sorting, (inf_draw.width/2 - sorting.get_width()/ 2, 35))
    draw_list(inf_draw)
    #this opens the window
    pygame.display.update()  
    
# function is used to display the list into rectangles / bars
def draw_list(draw_info, color_positions = {}, clear_background = False):
    lst = draw_info.lst
    if clear_background:
        clear_rect = (draw_info.side_pad//2, draw_info.top_pad, draw_info.width - draw_info.side_pad, draw_info.height - draw_info.top_pad)
        pygame.draw.rect(draw_info.window, draw_info.background_color, clear_rect)
    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.pixel_width
        y = draw_info.height - (val - draw_info.min_val) * draw_info.pixel_height
        
        
        color = draw_info.gradient[i%3]
        
        if i in color_positions:
            color = color_positions[i]
        
        pygame.draw.rect(draw_info.window, color, (x,y, draw_info.pixel_width, draw_info.height))
        
    if clear_background:
        pygame.display.update()        
# function is used to generate the list that will later be displayed       
def generate_starting_list(n, min_val, max_val):
    lst = []
    
    for _ in range(n):
        value = random.randint(min_val, max_val)
        lst.append(value)
        
    return lst

def bubble_sort(draw_info, ascending = True):
    #retrieve the list for sorting 
    lst = draw_info.lst
    
    for i in range(len(lst) - 1):
        for j in range(len(lst) - 1 - i):
            num1 = lst[j]
            num2 = lst[j+1]
            
            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                lst[j], lst[j+1] = lst[j+1], lst[j]
                draw_list(draw_info, {j:draw_info.green, j+1: draw_info.red}, True)
                
                yield True
    return lst


            
    
def main():
    run = True
    #this generates how fast the loop can run for pygame
    clock = pygame.time.Clock()
    
    n = 50
    min_val = 0
    max_val = 100
    
    sorting = False
    ascending = True
    
    
    sorting_alg = bubble_sort
    sorting_alg_name = "Bubble Sort"
    sort_alg_gen = None
    
    lst = generate_starting_list(n , min_val, max_val)
    draw_info_pygame = DrawInformation(800, 600, lst)
    while run:
        clock.tick(60)
        
        if sorting:
            try:
                next(sort_alg_gen)
            except StopIteration:
                sorting = False
        else:
        
            dra_info(draw_info_pygame)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type != pygame.KEYDOWN:
                continue
            
            #if the person presses the 'r' key on the keyboard it resets the list into a new one
            if event.key == pygame.K_r:
                lst = generate_starting_list(n , min_val, max_val)
                draw_info_pygame.set_list(lst)
                sorting = False
                
            #allows for the sorting to begin when pressing the space key
            elif event.key == pygame.K_SPACE and sorting == False:
                sorting = True
                sort_alg_gen = sorting_alg(draw_info_pygame, ascending)
             
            #allows for the sorting simulator to sort in a ascending order  
            elif event.key == pygame.K_a and not sorting:
                ascending = True
                
            #allows for the sorting alogrithm to sort in descending order
            elif event.key == pygame.K_d and not sorting:
                ascending = False
            
            
            
             
                
    pygame.quit()
    
    
if __name__ == "__main__":
    main()