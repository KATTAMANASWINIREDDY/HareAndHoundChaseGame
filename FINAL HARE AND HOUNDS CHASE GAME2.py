import pygame
import sys
import pygame.mixer
import pyttsx3
import threading

pygame.init()
pygame.mixer.init()
WIDTH = 750
HEIGHT = 600
ROWS = 3
COLS = 5
CELL_SIZE = 150
screen = pygame.display.set_mode([WIDTH, HEIGHT],pygame.RESIZABLE)
pygame.display.set_caption('HARE HOUND CHASE GAME')
font = pygame.font.Font('freesansbold.ttf', 20)
timer = pygame.time.Clock()
fps = 60

hare_pieces=["hare"]
hound_pieces=["hound1","hound2","hound3"]
hare_locations = [(4,1)]
hound_locations = [(1, 0), (0, 1), (1,2)]
turn_step = 0
selection=100
valid_moves = []
hare_image = pygame.image.load("C:\\Users\\katta\\OneDrive\\Desktop\\FINAL HARE AND HOUND CHASE GAME\\IMAGES\\hareimage1.png")
hare_image = pygame.transform.scale(hare_image, (CELL_SIZE, CELL_SIZE))
hound_image = pygame.image.load("C:\\Users\\katta\\OneDrive\\Desktop\\FINAL HARE AND HOUND CHASE GAME\\IMAGES\\houndimage1.png")
hound_image = pygame.transform.scale(hound_image, (CELL_SIZE, CELL_SIZE))
captured_pieces_hare = []
captured_pieces_hound = []
buttonsound= pygame.mixer.Sound("C:\\Users\\katta\\OneDrive\\Desktop\\FINAL HARE AND HOUND CHASE GAME\\SOUNDS\\button sound.wav")
move_sound1 = pygame.mixer.Sound("C:\\Users\\katta\\OneDrive\\Desktop\\FINAL HARE AND HOUND CHASE GAME\\SOUNDS\\haresound.wav")
move_sound2 = pygame.mixer.Sound("C:\\Users\\katta\\OneDrive\\Desktop\\FINAL HARE AND HOUND CHASE GAME\\SOUNDS\\houndssound.wav")
congratulation_sound=pygame.mixer.Sound("C:\\Users\\katta\\OneDrive\\Desktop\\FINAL HARE AND HOUND CHASE GAME\\SOUNDS\\applause.wav")
background_image = pygame.image.load("C:\\Users\\katta\\OneDrive\\Desktop\\FINAL HARE AND HOUND CHASE GAME\\IMAGES\\background.png")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

def draw_board(screen):    
    for row in range(ROWS):
        for col in range(COLS):
            if row==0 and col==0:
                color="black"
            elif row==2 and col==0:
                color="black"
            elif row==0 and col==4:
                color="black"
            elif row==2 and col==4:
                color="black"
            else:
                color="gray"
            pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            for i in range(5):
                pygame.draw.line(screen, "black", (0, 150 * i), (750, 150 * i), 2)
                pygame.draw.line(screen, "black", (150 * i, 0), (150 * i, 450), 2)
                pygame.draw.rect(screen, 'gold', [0, 450, WIDTH, 150], 3)
            status_text = ['HARE: Select a Piece to Move!', 'HARE: Select a Destination!',
                        'HOUND: Select a Piece to Move!', 'HOUND: Select a Destination!']
            screen.blit(font.render(status_text[turn_step], True, 'black'), (10, 525))


def draw_pieces(screen):
    hare_x, hare_y = hare_locations[0]
    screen.blit(hare_image,(hare_x * CELL_SIZE, hare_y * CELL_SIZE))
    for hound_pos in hound_locations:
        hound_y, hound_x = hound_pos
        screen.blit(hound_image, (hound_y *CELL_SIZE, hound_x * CELL_SIZE))
                
def check_options(pieces,locations,turn):
    moves_list=[]
    all_moves_list=[]
    for i in range((len(pieces))):
        location=locations[i]
        piece=pieces[i]
        if piece=="hare":
            moves_list=check_hare(location,turn)
        elif piece=="hound1":
            moves_list=check_hound(location,turn,hound_locations)
        elif piece=="hound2":
            moves_list=check_hound(location,turn,hound_locations)
        elif piece=="hound3":
            moves_list=check_hound(location,turn,hound_locations)
        all_moves_list.append(moves_list)
    return all_moves_list

def check_hare(position,turn):
    moves_list=[]
    x, y = position
    if turn=="hare":
        if position==(4,1):
            if x-1>=0 and y-1>=0:                 #cross_right            
                moves_list.append((x-1, y-1))
            if x-1>=0 and y+1>=0:
                moves_list.append((x-1,y+1))      #cross-left   
            if x-1>=0:
                moves_list.append((x - 1, y))     #front
        elif  position in [(1,1),(3,1)]:
            if x + 1 >= 2:
                moves_list.append((x + 1, y))
            if x-1>=0:
                moves_list.append((x - 1, y))
            if y+1>=0:
                moves_list.append((x, y+1))         #down
            if y-1>=0:
                moves_list.append((x, y-1))         #up
        elif (2,2)==(x,y):
            if x-1>=0:
                moves_list.append((x - 1, y))     #front
            if x + 1 >= 2:
                moves_list.append((x + 1, y))
            if y-1>=0:
                moves_list.append((x, y-1))
        elif(2,0)==(x,y):
            if x-1>=0:
                moves_list.append((x - 1, y))     #front
            if x + 1 >= 2:
                moves_list.append((x + 1, y))
            if y+1>=0:
                moves_list.append((x, y+1))    
        elif (3,0)==(x,y):
            if x+1>=0 and y+1>=0:
                moves_list.append((x+1,y+1))
            if y+1>=0:
                moves_list.append((x, y+1))
            if x-1>=0:                             
                moves_list.append((x-1, y))
            if x-1>=0 and y+1>=0:
                moves_list.append((x-1,y+1))
        elif (3,2)==(x,y):
            if x-1>=0:
                moves_list.append((x - 1, y))
            if x-1>=0 and y+1>=0:
                moves_list.append((x+1 ,y-1))
            if y-1>=0:
                moves_list.append((x, y-1))
            if x-1>=0 and y-1>=0:                             
                moves_list.append((x-1, y-1))
        elif (1,2)==(x,y):
            if x + 1 >= 2:
                moves_list.append((x + 1, y))
            if x-1>=0 and y+1>=0:
                moves_list.append((x + 1 ,y-1))
            if y-1>=0:
                moves_list.append((x, y-1))  
            if x-1>=0 and y-1>=0:                           
                moves_list.append((x-1, y-1))
        elif (1,0)==(x,y):
            if y+1>=0:
                moves_list.append((x, y+1))
            if x + 1 >= 2:
                moves_list.append((x + 1, y))
            if x-1>=0 and y+1>=0:
                moves_list.append((x-1,y+1))      
            if x+1>=0 and y+1>=0:                             
                moves_list.append((x+1, y+1))
        elif (2,1)==(x,y):
            if x + 1 >= 2:
                moves_list.append((x + 1, y))
            if x-1>=0:
                moves_list.append((x - 1, y))
            if y-1>=0:
                moves_list.append((x, y-1))
            if y+1>=0:
                moves_list.append((x, y+1))
            if x+1>=0 and y+1>=0:                             
                moves_list.append((x+1, y+1))
            if x-1>=0 and y+1>=0:
                moves_list.append((x + 1 ,y-1))
            if x-1>=0 and y+1>=0:
                moves_list.append((x-1,y+1))
            if x-1>=0 and y-1>=0:
                moves_list.append((x-1,y-1))    
        else:
            if x-1>=0 and y-1>=0:                 #cross_right            
                moves_list.append((x-1, y-1))
            if x-1>=0 and y+1>=0:
                moves_list.append((x-1,y+1))      #cross-left   
            if x-1>=0:
                moves_list.append((x - 1, y))     #front
            if x + 1 >= 2:
                moves_list.append((x + 1, y))     #back
            if x - 1 >= 0:
                moves_list.append((x - 1, y))
            if x + 1 <= 2:
                moves_list.append((x + 1, y))
    return moves_list
 
def check_hound(position, turn, hound_locations):
    moves_list = []
    x, y = position
    def is_hound_occupied(pos):
        return pos in hound_locations   
    if (0, 1) == (x, y):
        if x + 1 <= 2 and not is_hound_occupied((x + 1, y)):
            moves_list.append((x + 1, y))                                         # front
        if x + 1 <= 2 and y + 1 <= 4 and not is_hound_occupied((x+1,y+1)):
            moves_list.append((x + 1, y + 1))                                     #cross-right
        if x + 1 >= 0 and y - 1<=4 and not is_hound_occupied((x+1,y-1)):
            moves_list.append((x + 1, y - 1))
    elif (1,0)==(x,y):
        if x + 1 <= 2 and not is_hound_occupied((x+1,y)):
            moves_list.append((x + 1, y))                                         #front
        if x + 1 <= 2 and y + 1 <= 4 and not is_hound_occupied((x+1,y+1)):
            moves_list.append((x + 1, y + 1))                                     #cross-right
        if y + 1 <= 4 and not is_hound_occupied((x,y+1)):
            moves_list.append((x, y + 1))                                         #side-right
    elif (1,2)==(x,y):
        if x + 1 <= 4 and not is_hound_occupied((x+1,y)):
            moves_list.append((x + 1, y))                                        #front
        if y + 1 <= 4 and not is_hound_occupied((x,y-1)):
            moves_list.append((x, y - 1))                                        #side left
        if x + 1 <= 2 and y + 1 <= 4 and not is_hound_occupied((x+1,y-1)):
            moves_list.append((x + 1, y - 1))                                    #cross-left
    elif (2,1)==(x,y):
        if x + 1 <= 4 and not is_hound_occupied((x+1,y)):
            moves_list.append((x + 1, y))                                       #front
        if x + 1 <= 4 and y + 1 <= 4 and not is_hound_occupied((x+1,y+1)):
            moves_list.append((x + 1, y + 1))                                   #cross right
        if x - 1 >= 0 and y + 1 <= 4 and not is_hound_occupied((x+1,y-1)):
            moves_list.append((x + 1, y - 1))                                  #cross left
        if y + 1 <= 4 and not is_hound_occupied((x,y-1)):
            moves_list.append((x, y - 1))                                      #side-left
        if y + 1 <= 4 and not is_hound_occupied((x,y-1)):
            moves_list.append((x, y + 1))                                     #side right
    elif(1,1)==(x,y):
        if x + 1 <= 4 and not is_hound_occupied((x+1,y)):
            moves_list.append((x + 1, y))         
        if y + 1 <= 4 and not is_hound_occupied((x,y+1)):
            moves_list.append((x, y + 1))
        if y + 1 <= 4 and not is_hound_occupied((x,y-1)):
            moves_list.append((x, y - 1))
    elif(2,0)==(x,y):
        if x + 1 <= 4 and not is_hound_occupied((x+1,y)):
            moves_list.append((x + 1, y))
        if y + 1 <= 4 and not is_hound_occupied((x,y+1)):
            moves_list.append((x, y + 1))
    elif(2,2)==(x,y):
        if x + 1 <= 4 and not is_hound_occupied((x+1,y)):
            moves_list.append((x + 1, y))
        if y + 1 <= 4 and not is_hound_occupied((x,y-1)):
            moves_list.append((x, y - 1))
    elif(3,0)==(x,y):
        if x + 1 <= 4 and y + 1 <= 4 and not is_hound_occupied((x+1,y+1)):
            moves_list.append((x + 1, y + 1))
        if y + 1 <= 4 and not is_hound_occupied((x,y+1)):
            moves_list.append((x, y + 1))
    elif(3,1)==(x,y):
        if x + 1 <= 4 and not is_hound_occupied((x+1,y)):
            moves_list.append((x + 1, y)) 
        if y + 1 <= 4 and not is_hound_occupied((x,y+1)):
            moves_list.append((x, y + 1))
        if y + 1 <= 4 and not is_hound_occupied((x,y-1)):
            moves_list.append((x, y - 1))
        
    elif(3,2)==(x,y):
        if y + 1 <= 4 and not is_hound_occupied((x,y-1)):
            moves_list.append((x, y - 1))
        if x - 1 >= 0 and y + 1 <= 4 and not is_hound_occupied((x+1,y-1)):
            moves_list.append((x + 1, y - 1))    
    else:
        if y + 1 <= 4 and not is_hound_occupied((x,y+1)):
            moves_list.append((x, y + 1))
        if x - 1 >= 0 and not is_hound_occupied((x-1,y)):
            moves_list.append((x - 1, y))
        if x + 1 <= 2 and not is_hound_occupied((x+1,y)):
            moves_list.append((x + 1, y))
        if x - 1 >= 0 and  y + 1 <= 4 and not is_hound_occupied((x-1,y+1)):
            moves_list.append((x - 1, y + 1))
        if x + 1 <= 2 and y + 1 <= 4 and not is_hound_occupied((x+1,y+1)):
            moves_list.append((x + 1, y + 1))

    return moves_list

def check_valid_moves():
    if turn_step < 2:
        options_list = hare_options
        opponent_positions = hound_locations
    else:
        options_list = hound_options
        opponent_positions = hare_locations
    valid_options = options_list[selection]
    valid_moves = []
    for move in valid_options:
        if move not in opponent_positions:
            valid_moves.append(move)
    return valid_moves

def draw_game_over(winner):
    pygame.draw.rect(screen, 'black', [200, 200, 400, 70])
    screen.blit(font.render(f'{winner} won the game!', True, 'white'), (210, 210))
    screen.blit(font.render(f'Press ENTER to Restart!', True, 'white'), (210, 240))

def check_hare_win():
    return hare_locations[0] == (0, 1)

def check_hounds_win():
    hare_location = hare_locations[0]
    if hare_location == (2, 0):
        hounds_winning_positions = [(3, 0), (2, 1), (1, 0)]
        return all(hound in hound_locations for hound in hounds_winning_positions)
    if hare_location == (2, 2):
        hounds_winning_positions = [(1, 2), (2, 1), (3, 2)]
        return all(hound in hound_locations for hound in hounds_winning_positions)
    if hare_location == (4, 1):
        hounds_winning_positions = [(3, 0), (3, 1), (3, 2)]
        return all(hound in hound_locations for hound in hounds_winning_positions)
    return False

    
def draw_valid(moves):
    if turn_step<2:
        color="red"
    else:
        color="blue"

    for i in range(len(moves)):
        pygame.draw.circle(screen,color,(moves[i][0]*150+75,moves[i][1]*150+75),5)

def read_text(text):
    engine = pyttsx3.init()
    engine.setProperty("rate", 230)
    engine.say(text)
    engine.runAndWait()

hound_options = check_options(hound_pieces, hound_locations, 'hound')
hare_options = check_options(hare_pieces, hare_locations, 'hare')
run = True
def intro_window():
    intro_screen = pygame.display.set_mode([WIDTH, HEIGHT])
    pygame.display.set_caption('HARE HOUND CHASE GAME - Intro')
    intro_background_image = pygame.image.load("C:\\Users\\katta\\OneDrive\\Desktop\\FINAL HARE AND HOUND CHASE GAME\\IMAGES\\overlook.png")
    intro_background_image = pygame.transform.scale(intro_background_image, (WIDTH, HEIGHT))
    next_button_image = pygame.image.load("C:\\Users\\katta\\OneDrive\\Desktop\\nextbutton.png")
    next_button_image = pygame.transform.scale(next_button_image, (80, 50))
    exit_button_image = pygame.image.load("C:\\Users\\katta\\OneDrive\\Desktop\\FINAL HARE AND HOUND CHASE GAME\\IMAGES\\exitbutton.png")
    exit_button_image = pygame.transform.scale(exit_button_image, (80, 50))
    intro_done = False
    while not intro_done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if 650 < event.pos[0] < 730 and 500 < event.pos[1] < 550:
                    buttonsound.play()
                    intro_done = True
                elif 100 < event.pos[0] < 780 and 500 < event.pos[1] < 550:
                    pygame.quit()
                    sys.exit()                  
        intro_screen.blit(intro_background_image, (0, 0))
        intro_screen.blit(next_button_image, (650, 500))
        intro_screen.blit(exit_button_image, (100, 500)) 
        
        pygame.display.flip()
intro_window()

def screen2():
    screen2_screen = pygame.display.set_mode([WIDTH,HEIGHT])
    pygame.display.set_caption('HARE HOUND CHASE GAME - 2')
    play_button_image = pygame.image.load("C:\\Users\\katta\\OneDrive\\Desktop\\FINAL HARE AND HOUND CHASE GAME\\IMAGES\\playbutton.png")
    play_button_image = pygame.transform.scale(play_button_image, (80, 50))
    instruction_button_image = pygame.image.load("C:\\Users\\katta\\OneDrive\\Desktop\\INSTRUCTIONS-button.png")
    instruction_button_image = pygame.transform.scale(instruction_button_image, (120, 80))
    screen2_done = False
    while not screen2_done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if 350 < event.pos[0] < 430 and 200 < event.pos[1] < 250:
                    buttonsound.play()
                    screen2_done = True
                elif 330 < event.pos[0] < 450 and 400 < event.pos[1] < 480:
                    buttonsound.play()
                    instructions = pygame.display.set_mode([WIDTH, HEIGHT])
                    pygame.display.set_caption('HARE HOUND CHASE GAME - Instructions')
                    # threading.Thread(target=read_text, args=(instruction_text,)).start()
                    instruction_text= """Instructions for Hare and Hounds Game:",
                                "                                         ",
                                "The game is played on a 3x5 grid.",
                                "The 'hare' starts at (4, 1), and the 'hounds' start at (1, 0), (0, 1), and (1, 2)",
                                "Players take turns moving their pieces.",
                                "Hounds can only move forward sides and diagonally to capture the hare.",
                                "The hare can move in any direction.",
                                "The hare wins if it sneaks across the hounds to the left of the board",
                                "The hounds win by trapping the hare so that it can't move.",
                                "Press PLAY to start the game.","""
                    threading.Thread(target=read_text, args=(instruction_text,)).start()
                    instructions_text = [
                                "Instructions for Hare and Hounds Game:",
                                "---------------------------------------",
                                "1. The game is played on a 3x5 grid.",
                                "2. The 'hare' starts at (4, 1), and the 'hounds' start at (1, 0), (0, 1), and (1, 2).",
                                "3. Players take turns moving their pieces.",
                                "4. Hounds can only move forward and diagonally to capture the hare.",
                                "5. The hare can move in any direction.",
                                "6. The hare wins if it sneaks across the hounds to the left of the board.",
                                "7. The hounds win by trapping the hare so that it can't move..",
                                "8. Press PLAY to start the game.",

                    ]

                    
                    font = pygame.font.Font(None, 24)
                    threading.Thread(target=read_text, args=(instruction_text,)).start()
                    play_button_image = pygame.image.load("C:\\Users\\katta\\OneDrive\\Desktop\\FINAL HARE AND HOUND CHASE GAME\\IMAGES\\playbutton.png")
                    play_button_image = pygame.transform.scale(play_button_image, (80, 50))
                    exit_button_image = pygame.image.load("C:\\Users\\katta\\OneDrive\\Desktop\\FINAL HARE AND HOUND CHASE GAME\\IMAGES\\exitbutton.png")
                    exit_button_image = pygame.transform.scale(exit_button_image, (80, 50))
                    instruction_done = False
                    while not instruction_done:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                                if 650 < event.pos[0] < 730 and 500 < event.pos[1] < 550:
                                    buttonsound.play()
                                    instruction_done = True
                                elif 100 < event.pos[0] < 180 and 500 < event.pos[1] < 550:
                                    pygame.quit()
                                    sys.exit()
                        instructions.fill((255, 255, 255))
                        instructions.blit(background_image, (0, 0))
                        instructions.blit(play_button_image, (650, 500))
                        instructions.blit(exit_button_image, (100, 500))
                        y_position = 100
                        for line in instructions_text:
                            text_surface = font.render(line, True, (0, 0, 0))
                            instructions.blit(text_surface, (50, y_position))
                            y_position += 30                       
                        pygame.display.flip()              
        screen2_screen.blit(background_image, (0, 0))
        screen2_screen.blit(play_button_image, (350, 200))
        screen2_screen.blit(instruction_button_image, (330, 400)) 
        
        pygame.display.flip()
screen2()

def exit_window(winner):
    exit_screen = pygame.display.set_mode([WIDTH, HEIGHT])
    pygame.display.set_caption('HARE HOUND CHASE GAME - Congratulations')
    congrats_hare = pygame.image.load("C:\\Users\\katta\\OneDrive\\Desktop\\FINAL HARE AND HOUND CHASE GAME\\IMAGES\\hare win.png")
    congrats_hare = pygame.transform.scale(congrats_hare, (750, 600))
    congrats_hounds=pygame.image.load("C:\\Users\\katta\\OneDrive\\Desktop\\FINAL HARE AND HOUND CHASE GAME\\IMAGES\\hounds win.png")
    congrats_hounds = pygame.transform.scale(congrats_hounds, (750, 600))
    exit_done = False
    while not exit_done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                exit_done = True
        if winner=="HARE":
            congratulation_sound.play()
            exit_screen.blit(congrats_hare, (0, 0))    
        elif winner=="HOUNDS":
            congratulation_sound.play()
            exit_screen.blit(congrats_hounds, (0, 0))
        pygame.display.flip()

while run:
    screen.fill("white")
    screen.blit(background_image, (0, 0))
    draw_board(screen)
    draw_pieces(screen)
    pygame.display.flip()
    if selection != 100:
        valid_moves=check_valid_moves()
        draw_valid(valid_moves)

    if check_hare_win():
        draw_game_over("HARE")
        print("Hare wins!")
        exit_window("HARE")
        run = False

    if check_hounds_win():
        draw_game_over("HOUNDS")
        print("Hounds win!")
        exit_window("HOUNDS")
        run = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
              run = False
        if event.type==pygame.MOUSEBUTTONDOWN and  event.button==1:
            x_coord=event.pos[0]//150
            y_coord=event.pos[1]//150
            click_coords=(x_coord,y_coord)
            if turn_step<=1:
                if click_coords in hare_locations:
                    selection=hare_locations.index(click_coords)
                    if turn_step==0:
                        turn_step=1
                if click_coords in valid_moves and selection!=100:
                    hare_locations[selection]=click_coords
                    if click_coords in hound_locations:
                        hound_piece=hound_locations.index(click_coords)
                        captured_pieces_hare.append(hound_pieces[hound_piece])
                        hound_locations.pop(hound_piece)
                    hound_options=check_options(hound_pieces,hound_locations,"hound")
                    hare_options=check_options(hare_pieces,hare_locations,"hare")
                    move_sound1.play()
                    turn_step=2
                    selection=100
                    valid_moves=[]
            if turn_step>1:
                if click_coords in hound_locations:
                    selection=hound_locations.index(click_coords)
                    if turn_step==2:
                        turn_step=3
                if click_coords in valid_moves and selection!=100:
                    hound_locations[selection]=click_coords
                    if click_coords in hare_locations:
                        hare_piece=hare_locations.index(click_coords)
                        captured_pieces_hound.append(hare_pieces[hare_piece])
                        hare_locations.pop(hare_piece)
                    hare_options=check_options(hare_pieces,hare_locations,"hare")
                    hound_options=check_options(hound_pieces,hound_locations,"hound")
                    move_sound2.play()
                    turn_step=0
                    selection=100
                    valid_moves=[]

    pygame.display.flip()

pygame.quit()