import pygame
import sys
import time 
from pygame import mixer 

pygame.init()

# Music Set Up

mixer.init()
start_screen_music = "music/start_screen_music.mp3"
game_music = "music/chinese_music.mp3"
end_credits = "music/end_credits.mp3"
mixer.music.load(start_screen_music)
mixer.music.set_volume(0.7)
mixer.music.play(-1)  # Loop indefinitely
end_credits_music_playing = False

def switch_music(track):
    if mixer.music.get_busy():
        mixer.music.stop()
    mixer.music.load(track)
    mixer.music.play(-1)  # Loop forever

# Load dialogue sound 
dialogue_sound = mixer.Sound("music/dialogue_sound.mp3")
dialogue_sound.set_volume(1.0)
dialogue_sound_played = False

# Load game over sound 
game_over_sound = mixer.Sound("music/game_over_sound.mp3")
game_over_sound.set_volume(1.0)
game_over_sound_played = False

# Screen setup
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("The Legend of the Sage King")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
RED = (255, 0, 0)

# loading up the various backgrounds
cover_background = pygame.image.load("screens/start_screen.png")  
cover_background = pygame.transform.scale(cover_background, (SCREEN_WIDTH, SCREEN_HEIGHT))

laozi_background = pygame.image.load("screens/laozi_screen.png") 
laozi_background = pygame.transform.scale(laozi_background, (SCREEN_WIDTH, SCREEN_HEIGHT))

mengzi_background = pygame.image.load("screens/mengzi_screen.png")  
mengzi_background = pygame.transform.scale(mengzi_background, (SCREEN_WIDTH, SCREEN_HEIGHT))

lordshang_background = pygame.image.load("screens/lord_shang_screen.png")
lordshang_background = pygame.transform.scale(lordshang_background, (SCREEN_WIDTH, SCREEN_HEIGHT))

mozi_background = pygame.image.load("screens/mozi_screen.png")  
mozi_background = pygame.transform.scale(mozi_background, (SCREEN_WIDTH, SCREEN_HEIGHT))

throne_background = pygame.image.load("screens/throne_room.png")
throne_background = pygame.transform.scale(throne_background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Loading Pixel Font
smaller_pixel_font = pygame.font.Font("fonts/PressStart2P-Regular.ttf", 11)  
small_pixel_font = pygame.font.Font("fonts/PressStart2P-Regular.ttf", 15)  
pixel_font = pygame.font.Font("fonts/PressStart2P-Regular.ttf", 16)  
large_pixel_font = pygame.font.Font("fonts/PressStart2P-Regular.ttf", 24)  
larger_pixel_font = pygame.font.Font("fonts/PressStart2P-Regular.ttf", 30)  
chinese_font = pygame.font.Font("fonts/Kashima Demo 2.ttf", 30) 

# Game states
STATE_START = 0
STATE_NAME_INPUT = 1
STATE_GAMEPLAY = 2
STATE_GAME_OVER = 3
STATE_OUT_OF_TURNS = 4

game_state = STATE_START

game_over_reason = ""
next_npc = False

npcs = [
    {
        "name": "Farmer",
        "sprite_sheet": "npcs/npc_farmer.png",
        "question": "Farmer: A drought has been plaguing our nation, My King! What should we do?",
        "choices": [
            ("Let nature take its course, the rains shall come.", {"morale": +10, "resources": -10, "population": -10}),          # Laozi's Daoism
            ("Organize communal labor to share the burden.", {"morale": +10, "population": +10, "resources": -10}), # Mengzi's Confucianism
            ("Punish those who don’t meet the quotas.", {"resources": +15, "morale": -15, "population": +5}),      # Lord Shang's Legalism
            ("Distribute resources equally.", {"morale": +15, "population": +10, "resources": -10}),               # Mozi's Mohism
        ],
    },
    {
        "name": "Priest",
        "sprite_sheet": "npcs/npc_priest.png",
        "question": "Priest: The temple is in ruins, and the gods have been quiet since. What should we do?",
        "choices": [
            ("Embrace simplicity. Worship can happen under the open sky.", {"morale": +15, "resources": -10}),      
            ("Rally the community to restore the temple to honor tradition.", {"morale": +15, "population": +10, "resources": -10}),
            ("Enforce a tithe from every citizen to fund the temple's restoration.", {"resources": +15, "morale": -15, "population": -10}),
            ("Build a modest temple with shared labor and equal contributions.", {"morale": +15, "population": +10, "resources": -10}),
        ],
    },
    {
        "name": "Scholar",
        "sprite_sheet": "npcs/npc_scholar.png",
        "question": "Scholar: Our queen is asking us to design a new curriculum for the kingdom's curriculum. What should we prioritize?",
        "choices": [
            ("Teach students to observe nature and embrace simplicity.", {"morale": +10}), 
            ("Focus on classical texts to instill leadership and filial piety.", {"morale": +15, "resources": -5}),
            ("Prioritize practical skills like law, agriculture, and strength.", {"resources": +15, "morale": -10, "population": +10}),
            ("Teach universal love, and practice education to foster equality.", {"morale": +10, "population": +10, "resources": -15}),
        ],
    },
    {
        "name": "Soldier",
        "sprite_sheet": "npcs/npc_soldier.png",
        "question": "Soldier: The general has tasked you with training new recruits. What should you emphasize?",
        "choices": [
            ("Teach them to flow like water in combat, over using brute strength.", {"morale": +10, "resources": -10, "population": +5}),
            ("Instill loyalty, discipline, and moral purpose to protect the people.", {"morale": +15, "resources": -10}),
            ("Focus on strict obedience and severe punishment for mistakes.", {"resources": +10, "morale": -15, "population": -10}),
            ("Train all equally, and prioritize defensive tactics to minimize loss.", {"morale": +10, "population": +10, "resources": -10}),
        ],
    },
    {
        "name": "Artisan",
        "sprite_sheet": "npcs/npc_artisan.png",
        "question": "Artisan: A royal order has been placed for a grand statue. How should you approach the task?",
        "choices": [
            ("Create something simple and harmonious, reflecting the natural world.", {"morale": +10, "resources": -10}),
            ("Incorporate traditional symbols that honor the kingdom’s history.", {"morale": +15, "resources": -10}),
            ("Work quickly and efficiently, meeting strict deadlines.", {"resources": +10, "morale": -15}),
            ("Ensure the statue provides value to all, not just the elite.", {"morale": +15, "population": +5, "resources": -15}),
        ],
    },
    {
        "name": "Healer",
        "sprite_sheet": "npcs/npc_healer.png",
        "question": "Healer: The king has fallen ill, and the court is looking to you for a cure. What is your approach?",
        "choices": [
            ("Focus on restoring the king’s balance through natural remedies.", {"morale": +10, "resources": -5}),
            ("Consult ancient medical texts and work with others to find a cure.", {"morale": +10, "resources": -5}),
            ("Focus all available resources on the king’s recovery.", {"resources": -15, "morale": -10, "population": -10}),
            ("Balance the king’s treatment with the needs of the other sick people.", {"morale": +10, "population": +10, "resources": -10}),
        ],
    },
    {
        "name": "Noble",
        "sprite_sheet": "npcs/npc_noble.png",
        "question": "Noble: A rival noble family is gaining influence. How should you respond?",
        "choices": [
            ("Avoid direct confrontation; let events unfold naturally.", {"morale": +10, "resources": -5}),
            ("Seek dialogue to find common ground and strengthen alliances.", {"morale": +15, "resources": +5}),
            ("Undermine them through strict enforcement of laws and gain power.", {"resources": +15, "morale": -15, "population": -10}),
            ("Work together to ensure that the people benefit.", {"morale": +10, "population": +10, "resources": +10}),
        ],
    },
    {
        "name": "Peasant",
        "sprite_sheet": "npcs/npc_peasant.png",
        "question": "Peasant: My harvest has failed this season. What should I do?",
        "choices": [
            ("Accept the natural cycle and prepare for better seasons ahead.", {"morale": +5, "resources": -5, "population": -10}),
            ("Rely on the community to share resources and support each other.", {"morale": +15, "population": +5, "resources": -5}),
            ("Work harder and find ways to meet your quotas despite the challenges.", {"resources": +15, "morale": -15, "population": +5}),
            ("Advocate for equal redistribution of food from wealthier households.", {"morale": +10, "population": +10, "resources": -10}),
        ],
    },
    {
        "name": "Advisor",
        "sprite_sheet": "npcs/npc_advisor.png",
        "question": "Advisor: Our kingdom has surplus resources this year! How should we invest these resources?",
        "choices": [
            ("Preserve the resources.", {"resources": +10, "morale": -10, "population:": -10}),
            ("Invest in public infrastructure like schools", {"morale": +15, "population": +10, "resources": -15}),
            ("Invest in training soldiers and building defenses", {"resources": +15, "morale": -10, "population": -10}),
            ("Distribute resources equally across regions", {"morale": +15, "population": +10, "resources": -10}),
        ],
    },
    {
        "name": "General",
        "sprite_sheet": "npcs/npc_general.png",
        "question": "General: A neighboring state is amassing troops near our borders. My King, should we prepare for war?",
        "choices": [
            ("Only act if directly attacked, avoid provoking them.", {"morale": +5, "resources": -5, "population": +5}),
            ("Seek diplomacy and emphasize peace.", {"morale": +15, "resources": -10}),
            ("Secure borders and ensure enemy cannot threaten us.", {"resources": +10, "morale": -10, "population": -10}),
            ("Offer aid or resources to reduce hostilities", {"morale": +15, "population": +10, "resources": -10}),
        ],
    },
    {
        "name": "Villager",
        "sprite_sheet": "npcs/npc_villager.png",
        "question": "Villager: Our crops have failed, and we have no food to feed our families. My King, can the kingdom provide aid to help?",
        "choices": [
            ("Nature has its rhythms, think of a way to align yourself to it.", {"morale": -10, "population": -10, "resources": -5}),
            ("It is the ruler’s duty to act with benevolence, so provide food.", {"morale": +15, "population": +10, "resources": -10}),
            ("Villagers can contribute labor in exchange for food.", {"resources": +10, "morale": -10, "population": -10}),
            ("Divert resources from wealthier regions to provide immediate relief.", {"morale": +15, "population": +10, "resources": -10}),
        ],
    },
    {
        "name": "Merchant",
        "sprite_sheet": "npcs/npc_merchant.png",
        "question": "Merchant: A rare foreign silk promises wealth but harms workers and the land. Shall we trade it?",
        "choices": [
            ("Allow merchants to trade as they see fit.", {"resources": +10, "morale": -10}),
            ("Set strict guidelines for trade between merchants and producers.", {"morale": +15, "resources": -10}),
            ("Impose high taxes on merchants and use strict monitoring.", {"resources": +10, "morale": -15, "population": -10}),
            ("Trade is not permitted as it perpetuates inequality.", {"morale": +10, "resources": -10}),
        ],
    },
    {
        "name": "Scribe",
        "sprite_sheet": "npcs/npc_scribe.png",
        "question": "Scribe: Preserving historical texts require a lot of resources. My King, should we prioritize saving these texts?",
        "choices": [
            ("Preserve only what is essential and let go of the rest.", {"morale": +10, "resources": -10}),
            ("Preserve the texts diligently as they are vital for our posterity.", {"morale": +15, "resources": -10}),
            ("Preserve only the texts that reinforce law and order.", {"resources": +10, "morale": -10, "population": -10}),
            ("Focus resources on initiatives that benefit everyone.", {"morale": +15, "population": +10, "resources": -5}),
        ],
    },
    {
        "name": "Philosopher",
        "sprite_sheet": "npcs/npc_philosopher.png",
        "question": "Philosopher: Should we prioritize harmony, moral cultivation, strict governance, or universal welfare when ruling?",
        "choices": [
            ("The purpose of ruling is to harmonize with the Way.", {"morale": +15, "resources": +10}),
            ("It is important to invest in education and rituals to instill morality.", {"morale": +15, "resources": -10}),
            ("We should enforce strict laws and punish disobedience.", {"resources": +10, "morale": -5, "population": +10}),
            ("We should promote impartial care by distributing resources equally", {"morale": +15, "population": +10, "resources": -10}),
        ],
    },
    {
        "name": "Blacksmith",
        "sprite_sheet": "npcs/npc_blacksmith.png",
        "question": "Blacksmith: A surge in demand for weapons has strained our resources. My King, how should we proceed?",
        "choices": [
            ("Let the market decide. Let nature take its course.", {"morale": +10, "resources": -10}),
            ("Organize the blacksmiths into guilds to manage production and share the burden.", {"morale": +15, "population": +10, "resources": +5}),
            ("Increase production by extending work hours and enforcing strict quotas.", {"resources": +10, "morale": -15, "population": +10}),
            ("Distribute resources equally among blacksmiths to ensure fair wages and prevent inequality.", {"morale": +15, "population": +10, "resources": -10}),
        ],
    },
]


# for end of game count
laozi_points = 0
mengzi_points = 0
lord_shang_points = 0
mozi_points = 0

# max turns = number of npcs
max_turns = len(npcs)
turn_count = 0
current_npc_index = 0

# Getting the sprites of the npcs to display
npc_spritesheet = pygame.image.load(npcs[current_npc_index]["sprite_sheet"]).convert_alpha()

FRAME_WIDTH = npc_spritesheet.get_width() // 12 
FRAME_HEIGHT = npc_spritesheet.get_height() // 8

# Function to extract frames from the sprite sheet
def get_frames(sheet, num_frames, row):
    frames = []
    for i in range(num_frames):
        frame = sheet.subsurface(pygame.Rect(i * FRAME_WIDTH, row * FRAME_HEIGHT, FRAME_WIDTH, FRAME_HEIGHT))
        frame = pygame.transform.scale(frame, (FRAME_WIDTH * 4, FRAME_HEIGHT * 4))  
        frames.append(frame)
    return frames

# getting walking frames
npc_frames = get_frames(pygame.image.load(npcs[current_npc_index]["sprite_sheet"]).convert_alpha(), 4, row=1)

# npc position and animation
npc_x, npc_y = -50, SCREEN_HEIGHT - (FRAME_HEIGHT * 2) - 100  
npc_speed = 1.5
frame_index = 0
animation_timer = pygame.time.get_ticks()
FRAME_DELAY = 100
npc_arrived = False

def draw_multiline_text(text, font, color, x, y, max_width):
    words = text.split(' ')
    lines = []
    current_line = words[0]
    
    for word in words[1:]:
        if font.size(current_line + ' ' + word)[0] < max_width:
            current_line += ' ' + word
        else:
            lines.append(current_line)
            current_line = word
    lines.append(current_line)
    
    for i, line in enumerate(lines):
        line_surface = font.render(line, True, color)
        screen.blit(line_surface, (x, y + i * font.get_height()))

def draw_dialogue_box(question, choices, x, y, width, height):

    # draws background
    pygame.draw.rect(screen, BLACK, (x, y, width*1, height*1.5))
    pygame.draw.rect(screen, WHITE, (x, y, width*1, height*1.5), 2)

    # draws question text
    max_text_width = width - 20
    draw_multiline_text(question, small_pixel_font, WHITE, x + 10, y + 10, max_text_width)

    # draws choices below question
    choice_y = y + 50 + len(question.split('\n')) * pixel_font.get_height()
    for i, choice in enumerate(choices):
        choice_text = f"{i + 1}. {choice}"
        text_surface = smaller_pixel_font.render(choice_text, True, WHITE)
        screen.blit(text_surface, (x + 10, choice_y))
        choice_y += smaller_pixel_font.get_height() + 10

def draw_end_game_box(question, x, y, width, height):    
    # draws background
    pygame.draw.rect(screen, BLACK, (x, y, width*1, height*1.5))
    pygame.draw.rect(screen, WHITE, (x, y, width*1, height*1.5), 2)

    # Draw the question text
    max_text_width = width - 20
    draw_multiline_text(question, pixel_font, WHITE, x + 10, y + 10, max_text_width)

# draws dynamic resource bar
def draw_resource_bar(name, x, y, value, max_value=100):
    bar_width, bar_height = 250, 20

    # background bar 
    pygame.draw.rect(screen, GRAY, (x, y, bar_width, bar_height), border_radius=10)

    # dynamic foreground bar (fill)
    fill_width = int((value / max_value) * bar_width)
    red = min(255, max(0, 255 - int(255 * value / max_value)))  # Red when low
    green = min(255, max(0, int(255 * value / max_value)))     # Green when high
    bar_color = (red, green, 0)

    pygame.draw.rect(screen, bar_color, (x, y, fill_width, bar_height), border_radius=10)

    # renders pixel text
    text_surface = pixel_font.render(f"{name}: {value}/{max_value}", True, WHITE)

    # positions
    text_x = x
    text_y = y - 15  
    screen.blit(text_surface, (text_x, text_y))

# for the sage king name
def draw_decorative_box(text, font, color, x, y, padding, bg_color, border_color, ornament_image=None):
    text_surface = font.render(text, True, color)

    # get dimensions
    text_width, text_height = text_surface.get_size()
    box_width = text_width + 2 * padding
    box_height = text_height + 2 * padding
    box_x = x - padding
    box_y = y - padding

    # draw box and border
    pygame.draw.rect(screen, bg_color, (box_x, box_y, box_width, box_height), border_radius=15)
    pygame.draw.rect(screen, border_color, (box_x, box_y, box_width, box_height), 2, border_radius=15)

    # ornament images at corners
    if ornament_image:
        ornament = pygame.image.load(ornament_image).convert_alpha()
        ornament = pygame.transform.scale(ornament, (padding, padding))
        screen.blit(pygame.transform.rotate(ornament, 270), (box_x+5, box_y+5))  # top left
        screen.blit(pygame.transform.rotate(ornament, 180), (box_x + box_width - padding - 7, box_y +7))  # top right
        screen.blit(pygame.transform.rotate(ornament, 90), (box_x + box_width - padding -10, box_y + box_height - padding -5))  # bottom right
        screen.blit(ornament, (box_x + 2, box_y + box_height - padding - 8))  # bottom left

    screen.blit(text_surface, (x, y))


# checks resource limits and game over conditions
def check_resources():
    global morale, resources, population, game_state, game_over_reason

    # cap resources at 100
    morale = min(100, morale)
    resources = min(100, resources)
    population = min(100, population)

    # check for game over conditions
    if resources <= 0:
        game_over_reason = "A resource shortage led to starvation. The kingdom has fallen."
        game_state = STATE_GAME_OVER
    elif morale <= 0:
        game_over_reason = "The people rebelled against your rule. The kingdom has collapsed."
        game_state = STATE_GAME_OVER
    elif population <= 0:
        game_over_reason = "Poor decisions caused the kingdom's downfall. It is the end."
        game_state = STATE_GAME_OVER



# main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # start of game, switches to music and sets metrics
        if game_state == STATE_START:
            if event.type == pygame.KEYDOWN:
                switch_music(game_music)  
                game_state = STATE_NAME_INPUT

            player_name = ""
            input_box = pygame.Rect(200, 300, 400, 50)

            # metrics
            morale = 75
            resources = 75
            population = 75


        elif game_state == STATE_NAME_INPUT:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  
                    if player_name.strip() == "":
                        player_name = "Sage King"  # default name if none
                    game_state = STATE_GAMEPLAY
                elif event.key == pygame.K_BACKSPACE:  
                    player_name = player_name[:-1]
                else:  
                    player_name += event.unicode

        # game play state, switches to game music and acccounts for choices
        elif game_state == STATE_GAMEPLAY:
            if not mixer.music.get_busy():
                switch_music(game_music)
            if npc_arrived and event.type == pygame.KEYDOWN:
                dialogue_sound_played = False
                npc = npcs[current_npc_index]
                if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                    choice_index = event.key - pygame.K_1  
                    if choice_index < len(npc["choices"]):
                        # apply choice effects
                        choice = npc["choices"][choice_index]
                        effects = choice[1]
                        morale += effects.get("morale", 0)
                        resources += effects.get("resources", 0)
                        population += effects.get("population", 0)

                        # increment philosopher counts
                        if choice_index == 0:
                            laozi_points += 1
                        elif choice_index == 1:
                            mengzi_points += 1
                        elif choice_index == 2:
                            lord_shang_points += 1
                        elif choice_index == 3:
                            mozi_points += 1

                # moving on to next npc
                npc_arrived = False
                npc_x = -50
                turn_count += 1
            
                check_resources()
                if game_state == STATE_GAME_OVER:
                    break
                current_npc_index+=1

                # check if all turns are done
                if current_npc_index >= max_turns:
                    game_state = STATE_OUT_OF_TURNS
                    break
                npc_frames = get_frames(pygame.image.load(npcs[current_npc_index]["sprite_sheet"]).convert_alpha(), 4, row=1)

        # if game over or out of turns, player can restart game or exit
        elif game_state == STATE_GAME_OVER or game_state == STATE_OUT_OF_TURNS:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1: 
                    # reset game variables
                    game_over_sound.stop() 
                    game_state = STATE_START
                    game_over_sound_played = False  
                    end_credits_music_playing = False
                    switch_music(start_screen_music)
                    current_npc_index = 0
                    # reset points
                    laozi_points = 0
                    mengzi_points = 0
                    lord_shang_points = 0
                    mozi_points = 0
                # end game
                elif event.key == pygame.K_2: 
                    running = False     

    # renders based on game state
    if game_state == STATE_START:
        screen.blit(cover_background, (0, 0))
        start_text = large_pixel_font.render("PRESS ANY KEY TO CONTINUE", True, WHITE)
        screen.blit(start_text, (100, 500))

    elif game_state == STATE_NAME_INPUT:
        screen.fill(BLACK)
        prompt_text = pixel_font.render("Enter your name, Sage King:", True, WHITE)
        screen.blit(prompt_text, (200, 200))
        pygame.draw.rect(screen, WHITE, input_box, 2)
        name_surface = pixel_font.render(player_name, True, WHITE)
        screen.blit(name_surface, (input_box.x + 10, input_box.y + 10))

    elif game_state == STATE_GAMEPLAY:
        screen.blit(throne_background, (0, 0))
        draw_decorative_box(
            f"Welcome, {player_name}",
            large_pixel_font,  # Use Chinese-style font
            (255, 215, 0),  # Gold color for text
            50 + 10,
            50 + -10,
            padding=15,
            bg_color=BLACK,  # Dark gray background
            border_color=(255, 69, 0),  # Red border resembling cinnabar
            ornament_image="assets/corner_ornament.png"  # Decorative ornament
        )

        # draw resource bars
        draw_resource_bar("Morale", 50, 100, morale)
        draw_resource_bar("Population", 50, 150, population)
        draw_resource_bar("Resources", 50, 200, resources)

        # animates the npc to walk to middle of screen
        if npc_x < 200:
            npc_x += npc_speed
            if pygame.time.get_ticks() - animation_timer > FRAME_DELAY:
                frame_index = (frame_index + 1) % len(npc_frames)
                animation_timer = pygame.time.get_ticks()
        else:
            npc_arrived = True

        # draws npc
        screen.blit(npc_frames[frame_index], (npc_x, npc_y))

        # plays dialogue sound when npc gets close
        if npc_x > 150 and not dialogue_sound_played:
                dialogue_sound.play()
                dialogue_sound_played = True

        # renders choice box
        if npc_arrived:
            npc = npcs[current_npc_index]
            dialogue_question = npc["question"]
            dialogue_choices = [choice[0] for choice in npc["choices"]]
            draw_dialogue_box(dialogue_question, dialogue_choices, 0, SCREEN_HEIGHT - 350, SCREEN_WIDTH, 120)

        # display turn counter
        turn_counter_text = pixel_font.render(f"Turn: {current_npc_index + 1}/{max_turns}", True, WHITE)
        turn_counter_x = SCREEN_WIDTH - turn_counter_text.get_width() - 10  
        turn_counter_y = 10  
        screen.blit(turn_counter_text, (turn_counter_x, turn_counter_y))

    elif game_state == STATE_GAME_OVER:
        if not game_over_sound_played:
            # plays game over sound if not played
            mixer.music.stop()  
            game_over_sound.play() 
            game_over_sound_played = True 
        
        screen.fill(BLACK)

        game_over_text = larger_pixel_font.render("GAME OVER", True, RED)
        game_over_x = (SCREEN_WIDTH - game_over_text.get_width()) // 2
        game_over_y = (SCREEN_HEIGHT // 2) - 150
        screen.blit(game_over_text, (game_over_x, game_over_y))

        reason_x = 50 
        reason_y = game_over_y + 80
        max_text_width = SCREEN_WIDTH - 100  
        draw_multiline_text(game_over_reason, pixel_font, WHITE, reason_x, reason_y, max_text_width)

        continue_text = pixel_font.render("Would you like to start again? (Yes - 1, No - 2)", True, WHITE)
        screen.blit(continue_text, (SCREEN_WIDTH // 2 - continue_text.get_width() // 2, SCREEN_HEIGHT // 2 + 20))
        
    
    elif game_state == STATE_OUT_OF_TURNS:
        # switch to end credits musics
        if not end_credits_music_playing: 
            switch_music(end_credits)
            end_credits_music_playing = True  

        # determines whihc philosopher screen to display at the end based on max of decisions
        if max(laozi_points, mengzi_points, lord_shang_points, mozi_points) == laozi_points:
            screen.blit(laozi_background, (0, 0))
            explanation = "Laozi's Daoism: Decisions that emphasize the Way, nonaction, and thus allowing natural harmony to guide the state will align with this path."
            dialogue_question = "You embodied the Way of Laozi with " + str(laozi_points) + " decisions."
        elif max(laozi_points, mengzi_points, lord_shang_points, mozi_points) == mengzi_points:
            screen.blit(mengzi_background, (0, 0))
            explanation = "Mengzi's Confucianism: Decisions that emphasize benevolence and the moral cultivation of rulers and individuals will align with this path."
            dialogue_question = "You embodied the Way of Mengzi with " + str(mengzi_points) + " decisions."
        elif max(laozi_points, mengzi_points, lord_shang_points, mozi_points) == lord_shang_points:
            screen.blit(lordshang_background, (0, 0))
            explanation = "Lord Shang's Legalism: Decisions that embody a system of strict laws and rewards and punishments will be found under this path."
            dialogue_question = "You embodied the Way of Lord Shang with " + str(lord_shang_points) + " decisions."
        elif max(laozi_points, mengzi_points, lord_shang_points, mozi_points) == mozi_points:
            screen.blit(mozi_background, (0, 0))
            explanation = "Mozi's Mohism: Decisions that are focused on universal love and impartial care will be found under this school of thought."
            dialogue_question = "You embodied the Way of Mozi with " + str(mozi_points) + " decisions."
        
        draw_end_game_box(explanation, 0, SCREEN_HEIGHT -550, SCREEN_WIDTH, 60)
        draw_end_game_box(dialogue_question, 0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 60)

        continue_text = pixel_font.render("Would you like to start again? (Yes - 1, No - 2)", True, WHITE)
        screen.blit(continue_text, (SCREEN_WIDTH // 2 - continue_text.get_width() // 2, SCREEN_HEIGHT - 50))
 


    pygame.display.flip()
    pygame.time.Clock().tick(60)