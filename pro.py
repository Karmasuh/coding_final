import pygame
import random

# Initialize pygame
pygame.init()

win = pygame.display.set_mode((900, 800))
pygame.display.set_caption("Pokemon Gamma Emerald")

# Load assets (add paths to actual image files in your project directory)
walkRight = [pygame.image.load("./assets/B right walk.png"), pygame.image.load("./assets/brendan look right stand.png"), pygame.image.load("./assets/B look right walk.png")]
walkLeft = [pygame.image.load("./assets/B look left walk 1.png"), pygame.image.load("./assets/B look left stand.png"), pygame.image.load("./assets/B look left walk 2.png")]
walkUp = [pygame.image.load("./assets/brendan walk behind 1.png"), pygame.image.load("./assets/brendan look back stand.png"), pygame.image.load("./assets/brendan walk behind 2.png")]
walkDown = [pygame.image.load("./assets/Brendan walk 1.png"), pygame.image.load("./assets/standingBrendan.png"), pygame.image.load("./assets/brendand walk 2.png")]
bg = pygame.image.load("./assets/route 101.png")
bgTown = pygame.image.load("./assets/littleroot.png")
char = pygame.image.load("./assets/standingBrendan.png")
arena = pygame.image.load("./assets/arena.png")

# Game clock
clock = pygame.time.Clock()

# Character position and speed
x = 250  # Where object starts
y = 250  # Where object starts
vel = 6
walkCount = 0
left = False
right = False
up = False
down = False

# Hide the mouse cursor
pygame.mouse.set_visible(False)

# Rectangle definitions for collision detection (invisible)
rectangles = [
    pygame.Rect(65, 150, 210, 100),
    pygame.Rect(270, 140, 70, 90),
    pygame.Rect(170, 110, 120, 80),
    pygame.Rect(160, 200, 90, 80),
    pygame.Rect(550, 150, 210, 100),
    pygame.Rect(720, 140, 70, 100),
    pygame.Rect(590, 230, 190, 70),
    pygame.Rect(580, 90, 160, 70),
    pygame.Rect(560, 460, 200, 150),
    pygame.Rect(520, 420, 70, 130),
    pygame.Rect(560, 480, 200, 100),
    pygame.Rect(580, 420, 100, 100),
    pygame.Rect(80, 580, 200, 90),
    pygame.Rect(150, 640, 140, 90)
]

# Movement variables
distance_travelled = 0
yellow_screen_timer = 0

# Function to check if the mouse is inside any of the rectangles
def is_mouse_in_rect(mouse_pos, rects):
    for rect in rects:
        if rect.collidepoint(mouse_pos):
            return rect
    return None

# Game loop
run = True
while run:
    clock.tick(27)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Get the current mouse position
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Move the character based on arrow key input
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and x > 70:
        x -= vel
        left = True
        right = False
        down = False
        up = False
    elif keys[pygame.K_RIGHT] and x < 900 - 70:
        x += vel
        right = True
        left = False
        up = False
        down = False
    elif keys[pygame.K_UP] and y > 80:
        y -= vel
        up = True
        down = False
        right = False
        left = False
    elif keys[pygame.K_DOWN] and y < 800 - 100:
        y += vel
        up = False
        down = True
        right = False
        left = False
    else:
        up = False
        down = False
        right = False
        left = False

    # Lock mouse to the sprite position
    pygame.mouse.set_pos(x + 25, y + 25)  # Lock mouse to the center of the sprite

    # Check for yellow screen trigger only if the sprite is moving
    if yellow_screen_timer == 0 and (left or right or up or down):  # Only trigger if moving
        # Check if mouse is inside any rectangle
        current_rect = is_mouse_in_rect((mouse_x, mouse_y), rectangles)
        
        if current_rect:
            distance_travelled += vel
            if distance_travelled >= 50:
                if random.random() < 0.5:  # 50% chance to turn screen yellow
                    yellow_screen_timer = 60  # 1 second (60 FPS * 1 second)
                distance_travelled = 0

    # Handling yellow screen duration
    if yellow_screen_timer > 0:
        win.fill((255, 255, 0))  # Fill the screen with yellow
        yellow_screen_timer -= 1
    else:
        # Redraw the background
        win.blit(bg, (0, 0))  # Draw background

        # Drawing character sprite with walking animation
        if walkCount >= 3:
            walkCount = 0
        if left:
            win.blit(walkLeft[walkCount], (x, y))
            walkCount += 1
        elif right:
            win.blit(walkRight[walkCount], (x, y))
            walkCount += 1
        elif up:
            win.blit(walkUp[walkCount], (x, y))
            walkCount += 1
        elif down:
            win.blit(walkDown[walkCount], (x, y))
            walkCount += 1
        else:
            win.blit(char, (x, y))  # Draw character if not moving

    # Update the display
    pygame.display.update()

# Quit Pygame
pygame.quit()


class Pokemon:
    def __init__(self, name, hp, atk, defence, spAtk, spDef, spe, level, exp, type1, type2 = False):
        self.name = name
        self.level = level
        self.exp = exp
        self.type1 = type1
        self.type2 = type2
        self.stats = {
            'hp': hp,
            'atk':  atk,
            'defence': defence,
            'spAtk': spAtk,
            'spDef': spDef,
            'spe': spe,
            'hpIv': random.randrange(0, 32),
            'atkIv': random.randrange(0, 32),
            'defenceIv': random.randrange(0, 32),
            'spAtkIv': random.randrange(0, 32),
            'spDefIv': random.randrange(0, 32),
            'speIv': random.randrange(0, 32),
        }

    def statsCalculator(self, stat):
        if stat == 'hp':
            return (2 * self.stats['hp'] + self.stats['hpIv']) / 100 + self.level + 10
        elif stat == 'def':
            return ((2 * self.stats['def'] + self.stats['defIv']) // 100 + 5)
        elif stat == 'atk':
            return ((2 * self.stats['atk'] + self.stats['atkIv']) // 100 + 5)
        elif stat == 'spDef':
            return ((2 * self.stats['spDef'] + self.stats['spDefIv']) // 100 + 5)
        elif stat == 'spAtk':
            return ((2 * self.stats['spAtk'] + self.stats['spAtkIv']) // 100 + 5)
        elif stat == 'spe':
            return ((2 * self.stats['spe'] + self.stats['speIv']) // 100 + 5)

    def levelUp(self):
        if self.exp >= (0.8*(100**3))//1:
            return self.level + 1
        else: 
            return False



class Moves:
    
    def __init__(self, name, element, typing, power, accuracy, pp, effect):
        self.name = name
        self.element = element
        self.typing = typing
        self.power = power
        self.accuracy = accuracy
        self.pp = pp
        self.effect = effect
        self.pokemonData = Pokemon()

    def moveDmgCalculator(self):
        hitOrMiss = random.randrange(0, 100)
        damage = (((2 * self.pokemonData(self.level) // 5) * self.power * self.pokemonData.statsCalculator('atk') // self.pokemonData.statsCalculator('def')) // 50 + 2) * random.randrange(0.85, 1)
        if hitOrMiss > self.accuracy:
                return "The opposing pokemon evaded the move!"
        if hitOrMiss <= self.accuracy:
            if self.typing == 'Physical':
                return damage
            elif self.typing == 'Special':
                damage = (((2 * self.pokemonData(self.level) // 5) * self.power * self.pokemonData.statsCalculator('spAtk') // self.pokemonData.statsCalculator('spDefence')) // 50 + 2) * random.randrange(0.85, 1)
                return damage

class Combat:

    def __init__(self, pokemon1, pokemon2):
        self.pokemon1 = pokemon1
        self.pokemon2 = pokemon2
        self.pokemon1Stats = Pokemon()
        self.pokemon2Stats = Pokemon()
        self.pokemon1Moves = Moves()
        self.pokemon2Moves = Moves()
        
    def turnOrder(self):
        if self.pokemon1Stats.statsCalculator('spe') > self.pokemon2Stats.statsCalculator('spe'):
            return True #[self.pokemon1, self.pokemon2]
        elif self.pokemon1Stats.statsCalculator('spe') < self.pokemon2Stats.statsCalculator('spe'):
            return False #[self.pokemon2, self.pokemon1]
        else:
            return True #[self.pokemon1, self.pokemon2]
    
    # def actualCombat(self):
    #     while self.pokemon1Stats.statsCalculator('hp') > 0 and self.pokemon1Stats.statsCalculator('hp') > 0:
    #         if self.turnOrder() == True:
                

                
    
    # def winOrLose(self):
    #     if self.pokemon1Stats['hp'] <= 0:
    #         return True
    #     elif self.pokemon2Stats['hp'] <= 0:
    #         return False
    #     return "The battle is still ongoing."
    
    def gainEXP(self):
        if self.winOrLose() == True:
            return (1.25*(self.pokemon1.stats['level'] ** 3))//1 
        else: 
            return 0 


def importantNPCCombatLines (npcName): #these are the lines that npcs will use when you start the battle
    if npcName == "Roxanne":
        return "Congrats on making it this far now.... show my how you battle" #come back to this later and ask how to divide up 2 texts
    elif npcName == "Brawly":
        return "I'm Brawly Dewford city's gym leader you want to challenge me? Let's see what your made of! "
    elif npcName == "Watson":
        return "Battling youngsters like you are what I live for. Now I shall show you my electrifiying power!"
    elif npcName == "Flannery":
        return "Show me you and your pokemon's fiery passion for battle!"
    elif npcName == "Norman":
        return "Lets see how much you have grown from the last time I saw you"
    elif npcName == "Winona":
        return "Witness the elegant choreography of me and my bird pokemon!"
    elif npcName == "Tate and Liza":
        return "We don't need to talk because we can tell what each other is thinking" #come back and find out how to separate that line into parts
    elif npcName == "Wallace":
        return "I'm Wallace the Sootopolis city gym leader. I shall show you a performance of illusions in water by me and my pokemon"
    elif npcName == "Sidney":
        return "I like that look in your eyes, that's good real good lets have a thrilling battle in the pokemon league!"
    elif npcName == "Phoebe":
        return "I'm Phoebe of the elite 4. The bond I have with my pokemon is extremly tight, see if you can even inflict damage on my pokemon"
    elif npcName == "Glacia":
        return "I am Glacia of the elite 4, you better be careful, or else me and my pokemon might just freeze you in your tracks"
    elif npcName == "Drake":
        return "I am Drake the last of the elite 4, I hope you understand and trust your pokemon, because if you don't you will never beat me!"
    elif npcName == "Steven":
        return "I was hoping to see you here one day. I want you to show me everything you have learned on your adventure and I will show you my everything as well!"

existingPokemon = {
    'Treecko': (40, 45, 35, 65, 55, 70), #grass
    'Grovyle': (50, 65, 45, 85, 65, 95), #grass
    'Sceptile': (70, 85, 65, 105, 85, 120), #grass
    'Mega Sceptile': (70, 110, 75, 145, 85, 145), #dragon grass
    'Torchic': (45, 60, 40, 70, 50, 45), #fire
    'Combusken': (60, 85, 60, 85, 60, 55,),
    'Blaziken': (80, 120, 70, 110, 70, 80),
    'Mega Blaziken': (80, 160, 80, 130, 80, 100),
    'Mudkip': (50, 70, 50, 50, 50, 40),
    'Marshtomp': (70, 85, 70, 60, 70, 50),
    'Swampert': (100, 110, 90, 85, 90, 60),
    'Mega Swampert': (100, 150, 110, 95, 110, 70),
    'Poochyena': (35, 55, 35, 30, 30, 35),
    'Mightyena': (70, 90, 70, 60, 60, 70),
    'Zigzagoon': (38, 30, 41, 30, 41, 60),
    'Linoone': (78, 70, 61, 50, 61, 100),
    'Wurmple': (45, 45, 35, 20, 30, 20),
    'Silcoon': (50, 35, 55, 25, 25, 15),
    'Beautifly': (60, 70, 50, 100, 50, 65),
    'Cascoon': (50, 35, 55, 25, 25, 15),
    'Dustox': (60, 50, 70, 50, 90, 65),
    'Lotad': (40, 30, 30, 40, 50, 30),
    'Lombre': (60, 50, 50, 60, 70, 50),
    'Ludicolo': (80, 70, 70, 90, 100, 70),
    'Seedot': (40, 40, 50, 30, 30, 30),
    'Nuzleaf': (70, 70, 40, 60, 40, 60),
    'Shiftry': (90, 100, 60, 90, 60, 80),
    'Taillow': (40, 55, 30, 30, 30, 85),
    'Swellow': (60, 85, 60, 75, 50, 125),
    'Wingull': (40, 30, 30, 55, 30, 85),
    'Pelipper': (60, 50, 100, 95, 70, 65),
    'Ralts': (28, 25, 25, 45, 35, 40),
    'Kirlia': (38, 35, 35, 65, 55, 50),
    'Gardevoir': (68, 65, 65, 125, 115, 80),
    'Mega Gardevoir': (68, 85, 65, 165, 135, 100),
    'Gallade': (68, 125, 65, 65, 115, 80),
    'Mega Gallade': (68, 165, 95, 65, 115, 110),
    'Surskit': (40, 30, 32, 50, 52, 65),
    'Masquerain': (70, 60, 62, 100, 82, 80), 
    'Shroomish': (60, 40, 60, 40, 60, 35),
    'Breloom': (60, 130, 80, 60, 60, 70),
    'Slakoth': (60, 60, 60, 35, 35, 30), #normal
    'Vigoroth': (80, 80, 80, 55, 55, 90), #normal
    'Slaking': (150, 160, 100, 95, 65, 100), #normal
    'Abra': (25, 20, 15, 105, 55, 90), #psychic
    'Kadabra': (40, 35, 30, 120, 70, 105), #psychic
    'Nincada': (31, 45, 90, 30, 30, 40), #bug ground
    'Ninjask': (61, 90, 45, 50, 50, 160), #bug flying
    'Shedninja': (1, 90, 45, 30, 30, 40), #bug ghost
    'Whismur': (64, 51, 23, 51, 23, 28), #normal 20
    'Loudred': (84, 71, 43, 71, 43, 48), #normal 40
    'Exploud': (104, 91, 63, 91, 73, 68), #normal
    'Makuhita': (72, 60, 30, 20, 30, 25), #fighting 24
    'Hariyama': (144, 120, 60, 40, 60, 50), #fighting 
    'Goldeen': (45, 67, 60, 35, 50, 63), #water 33
    'Seaking': (80, 92, 65, 65, 80, 68), #water
    'Magikarp': (20, 10, 55, 15, 20, 80),# water 
    'Gyarados': (95, 125, 79, 60, 100, 81),# water flying
    'Mega Gyarados': (95, 155, 109, 70, 130, 81),#water dark
    'Marill': (70, 20, 50, 20, 50, 40),#water fairy
    'Azumarill': (100, 50, 80, 60, 80, 50),#water fairy
    'Geodude': (40, 80, 100, 30, 30, 20),#rock ground
    'Graveler': (55, 95, 115, 45, 45, 35),#rock ground
    'Golem': (80, 120, 130, 55, 65, 45),#rock ground
    'Nosepass': (30, 45, 135, 45, 90, 30),#rock
    'Probopass': (60, 55, 145, 75, 150, 40),#rock steel
    'Skitty': (50, 45, 45, 35, 35, 50),#normal
    'Delcatty': (70, 65, 65, 55, 55, 90),#normal
    'Zubat': (40, 45, 35, 30, 40, 55),#posion flying
    'Golbat': (75, 80, 70, 65, 75, 90),#poison flying
    'Crobat': (85, 90, 80, 70, 80, 130),#poison flying
    'Tentacool': (40, 40, 35, 50, 100, 70),#posion water
    'Tentacruel': (80, 70, 65, 80, 120, 100),#water poison
    'Sableye': (50, 75, 75, 65, 65, 50),#dark ghost
    'Mawile': (50, 85, 85, 55, 55, 50),#steel fairy
    'Mega Mawile': (50, 105, 125, 55, 95, 50),#steel fairy
    'Aron': (50, 70, 100, 40, 40, 30),#steel rock
    'Lairon': (60, 90, 140, 50, 50, 40),#steel rock
    'Aggron': (70, 110, 180, 60, 60, 50),#steel rock
    'Mega Aggron': (70, 140, 230, 60, 80, 50),#steel rock
    'Machop': (70, 80, 50, 35, 35, 35),#fighting
    'Machoke': (80, 100, 70, 50, 60, 45),#fighting
    'Machamp': (90, 130, 80, 65, 85, 55),#fighting
    'Meditite': (30, 40, 55, 40, 55, 60),#fight psychic
    'Medicham': (60, 60, 75, 60, 75, 80),#fight psychic
    'Mega Medicham': (60, 100, 85, 80, 85, 100),
    'Electrike': (40, 45, 40, 65, 40, 65),#electrike
    'Manectric': (70, 75, 60, 105, 60, 105),#electrike
    'Mega Manectric': (70, 75, 80, 135, 80, 135),
    'Plusle': (60, 50, 40, 85, 75, 95),
    'Minun': (60, 40, 50, 75, 85, 95),	
    'Magnemite': (25, 35, 70, 95, 55, 45),
    'Magneton': (50, 60, 95, 120, 70, 70),
    'Voltorb': (40, 30, 50, 55, 55, 100),
    'Electrode': (60, 50, 70, 80, 80, 150),
    'Volbeat': (65, 73, 75, 47, 85, 85),
    'Illumise': (65, 47, 75, 73, 85, 85),
    'Oddish': (45, 50, 55, 75, 65, 30),#grass poison
    'Gloom': (60, 65, 70, 85, 75, 40),
    'Vileplume': (75, 80, 85, 110, 90, 50),
    'Bellossom': (75, 80, 95, 90, 100, 50),#grass
    'Gulpin': (70, 43, 53, 43, 53, 40),#poison
    'Swalot': (100, 73, 83, 73, 83, 55),#poison
    'Carvanha': (45, 90, 20, 65, 20, 65),#water dark
    'Sharpedo': (70, 120, 40, 95, 40, 95),
    'Mega Sharpedo': (70, 140, 70, 110, 65, 105),
    'Wailmer': (130, 70, 35, 70, 35, 60), #water
    'Wailord': (170, 90, 45, 90, 45, 60),
    'Numel': (60, 60, 40, 65, 45, 35),#fire ground
    'Camerupt': (70, 100, 70, 105, 75, 40),
    'Mega Camerupt': (70, 120, 100, 145, 105, 20),
    'Torkoal': (70, 85, 140, 85, 70, 20),
    'Grimer': (80, 80, 50, 40, 50, 25),
    'Muk': (105, 105, 75, 65, 100, 50),
    'Koffing': (40, 65, 95, 60, 45, 35),
    'Weezing': (65, 90, 120, 85, 70, 60),
    'Spoink': (60, 25, 35, 70, 80, 60),
    'Grumpig': (80, 45, 65, 90, 110, 80),
    'Sandshrew': (50, 75, 85, 20, 30, 40),
    'Sandslash': (75, 100, 110, 45, 55, 65),
    'Spinda': (60, 60, 60, 60, 60, 60),
    'Skarmory': (65, 80, 140, 40, 70, 70),
    'Trapinch': (45, 100, 45, 45, 45, 10),#ground
    'Vibrava': (50, 70, 50, 50, 50, 70),#dragon ground
    'Flygon': (80, 100, 80, 80, 80, 100),
    'Cacnea': (50, 85, 40, 85, 40, 35),#grass
    'Cacturne': (70, 115, 60, 115, 60, 55),#grass dark
    'Swablu': (45, 40, 60, 40, 75, 50),#normal flying
    'Altaria': (75, 70, 90, 70, 105, 80),#dragon flying
    'Mega Altaria': (75, 110, 110, 110, 105, 80),#dragon fairy
    'Seviper': (73, 100, 60, 100, 60, 65), 
    'Solrock': (90, 95, 85, 55, 65, 70),#rock psychic
    'Barboach': (50, 48, 43, 46, 41, 60),#water ground
    'Whiscash': (110, 78, 73, 76, 71, 60),
    'Corphish': (43, 80, 65, 50, 35, 35),#water
    'Crawdaunt': (63, 120, 85, 90, 55, 55),#water dark
    'Baltoy': (40, 40, 55, 40, 70, 55),#ground psychic
    'Claydol': (60, 70, 105, 70, 120, 75),	
    'Lileep': (66, 41, 77, 61, 87, 23),#rock grass
    'Cradily': (86, 81, 97, 81, 107, 43),
    'Anorith': (45, 95, 50, 40, 50, 75),#rock bug
    'Armaldo': (75, 125, 100, 70, 80, 45),
    'Jigglypuff': (115, 45, 20, 45, 25, 20),#normal fairy
    'Wigglytuff': (140, 70, 45, 85, 50, 45),
    'Feebas': (20, 15, 20, 10, 55, 80),
    'Milotic': (95, 60, 79, 100, 125, 81),	
    'Staryu': (30, 45, 55, 70, 55, 85),
    'Starmie': (60, 75, 85, 100, 85, 115),#water psychic
    'Kecleon': (60, 90, 70, 60, 120, 40),
    'Shuppet': (44, 75, 35, 63, 33, 45),#ghost
    'Banette': (64, 115, 65, 83, 63, 65),
    'Mega Banette': (64, 165, 75, 93, 83, 75),
    'Duskull': (20, 40, 90, 30, 90, 25),
    'Dusclops': (40, 70, 130, 60, 130, 25),	
    'Tropius': (99, 68, 83, 72, 87, 51),#grass flying
    'Chimecho': (75, 50, 80, 95, 90, 65),
    'Absol': (65, 130, 60, 75, 60, 75),
    'Mega Absol': (65, 150, 60, 115, 60, 115),
    'Vulpix': (38, 41, 40, 50, 65, 65),
    'Ninetales': (73, 76, 75, 81, 100, 100),
    'Psyduck': (50, 52, 48, 65, 50, 55),
    'Golduck': (80, 82, 78, 95, 80, 85),
    'Wobbuffet': (190, 33, 58, 33, 58, 33),
    'Natu': (40, 50, 45, 70, 45, 70),#psychic flying
    'Xatu': (65, 75, 70, 95, 70, 95),
    'Phanpy': (90, 60, 60, 40, 40, 40),
    'Donphan': (90, 120, 120, 60, 60, 50),
    'Pinsir': (65, 125, 100, 55, 70, 85),
    'Mega Pinsir': (65, 155, 120, 65, 90, 105),#bug flying
    'Heracross': (80, 125, 75, 40, 95, 85),
    'Mega Heracross': (80, 185, 115, 40, 105, 75),
    'Rhyhorn': (80, 85, 95, 30, 30, 25),#rock ground
    'Rhydon': (105, 130, 120, 45, 45, 40),
    'Snorunt': (50, 50, 50, 50, 50, 50),
    'Glalie': (80, 80, 80, 80, 80, 80),
    'Mega Glalie': (80, 120, 80, 120, 80, 100),
    'Froslass': (70, 80, 70, 80, 70, 110),
    'Spheal': (70, 40, 50, 55, 50, 25),#water ice
    'Sealeo': (90, 60, 70, 75, 70, 45),
    'Walrein': (110, 80, 90, 95, 90, 65),	
    'Clamperl': (35, 64, 85, 74, 55, 32),
    'Relicanth': (100, 90, 130, 45, 65, 55),#water rock
    'Corsola': (65, 55, 95, 65, 95, 35),#water rock
    'Chinchou':	(75, 38, 38, 56, 56, 67),#water elec
    'Lantern': (125, 58, 58, 76, 76, 67),
    'Luvdisc': (43, 30, 55, 40, 65, 97),
    'Horsea': (30, 40, 70, 70, 25, 60),
    'Seadra': (55, 65, 95, 95, 45, 85),
    'Bagon': (45, 75, 60, 40, 30, 50),
    'Shelgon': (65, 95, 100, 60, 50, 50),
    'Salamence': (95, 135, 80, 110, 80, 100),
    'Mega Salamence': (95, 145, 130, 120, 90, 120),
    'Metagross': (80, 135, 130, 95, 90, 70),
    'Mega Metagross': (80, 145, 150, 105, 110, 110),
    'Primal Kyogre': (100, 150, 90, 180, 160, 90),
    'Primal Groudon': (100, 180, 160, 150, 90, 90),
    'Rayquaza': (105, 150, 90, 150, 90, 95),
    'Mega Rayquaza': (105, 180, 100, 180, 100, 115),
}

existingItems = {#type, what it does, cost
    'Antidote':	    ('Status', 'Poison',),
	'Awakening':	('Status', 'Sleep',),
	'Berry Juice':	('Heal',  20,),
	'Burn Heal':	('Status', 'Burn',),
	'Fresh Water':	('Heal',  50,),
	'Full Heal':	('Status', 'Status',),
	'Hyper Potion':	('Heal', 200,),
	'Max Potion':	('HealFull'),
	'Max Revive':	('ReviveFull'),
	'Paralyz Heal':	('Status', 'Paralysis',),
	'Potion':	    ('Heal', 20,),
	'Revival Herb':	('Revive'),
	'Revive':	    ('Revive'), 
	'Soda Pop':	    ('Heal', 60,),
	'Super Potion':	('Heal', 50,),
    'Pokeball':     ('Catch',),
    'Great ball':   ('Catch',),
    'Ultra ball':   ('Catch',),
    'Master ball':  ('Catch', ),
    'Rare candy':   ('Level up')
}

pokemonMoves = {
    "Treecko": {
        1: ["Pound"],
        3: ["Leafage"],
        6: ["Quick Attack"],
        9: ["Mega Drain"],
    },
    "Grovyle": {
        1: ["Leer"],
        1: ["Pound"],
        3: ["Leafage"],
        6: ["Quick Attack"],
        9: ["Mega Drain"],
    },
    "Sceptile": {
        1: ["Leer"],
        1: ["Pound"],
        3: ["Leafage"],
        6: ["Quick Attack"],
        9: ["Mega Drain"],
    },
    "Mudkip": {
        1: ["Tackle"],
        3: ["Water Gun"],
        9: ["Rock Smash"],
        12: ["Water Pulse"]
    },
    "Marshtomp": {
        1: ["Growl"],
        1: ["Tackle"],
        3: ["Water Gun"],
        9: ["Rock Smash"],
        12: ["Water Pulse"]
    },
    "Swampert": {
        1: ["Growl"],
        1: ["Tackle"],
        3: ["Water Gun"],
        9: ["Rock Smash"],
        12: ["Water Pulse"]
    },
    "Torchic": {
        1: ["Scratch"],
        3: ["Ember"],
        6: ["Flame Charge"],
        12: ["Aerial Ace"]
    },
    "Combusken": {
        1: ["Growl"],
        1: ["Scratch"],
        3: ["Ember"],
        6: ["Flame Charge"],
        12: ["Aerial Ace"]
    },
    "Blaziken": {
        1: ["Growl"],
        1: ["Scratch"],
        3: ["Ember"],
        6: ["Flame Charge"],
        12: ["Aerial Ace"]
    },
    "Zigzagoon": {
        1: ["Tackle"],
        3: ["Headbutt"]
    },
    "Poochyena": {
        1: ["Tackle"],
        3: ["Bite"]
    },
    "Wurmple": {
        1: ["Tackle"],
        2: ["Poison Sting"]
    }
}

# Pokémon Type Chart in Python
typeChart = {
    'Normal': {
        'Normal': 1, 'Fire': 1, 'Water': 1, 'Electric': 1, 'Grass': 1, 'Ice': 1, 'Fighting': 2, 'Poison': 1, 'Ground': 1, 'Flying': 1, 'Psychic': 1, 
        'Bug': 1, 'Rock': 1, 'Ghost': 0, 'Dragon': 1, 'Dark': 1, 'Steel': 1, 'Fairy': 1
    },
    'Fire': {
        'Normal': 1, 'Fire': 0.5, 'Water': 0.5, 'Electric': 1, 'Grass': 2, 'Ice': 2, 'Fighting': 1, 'Poison': 1, 'Ground': 1, 'Flying': 1, 'Psychic': 1, 
        'Bug': 2, 'Rock': 0.5, 'Ghost': 1,'Dragon': 0.5, 'Dark': 1, 'Steel': 2, 'Fairy': 1
    },
    'Water': {
        'Normal': 1, 'Fire': 2, 'Water': 0.5, 'Electric': 0.5, 'Grass': 0.5, 'Ice': 1, 'Fighting': 1, 'Poison': 1, 'Ground': 2, 'Flying': 1, 'Psychic': 1, 
        'Bug': 1, 'Rock': 2, 'Ghost': 1, 'Dragon': 0.5, 'Dark': 1, 'Steel': 1, 'Fairy': 1
    },
    'Electric': {
        'Normal': 1, 'Fire': 1, 'Water': 2, 'Electric': 0.5, 'Grass': 0.5, 'Ice': 1, 'Fighting': 1, 'Poison': 1, 'Ground': 0, 'Flying': 2, 'Psychic': 1, 
        'Bug': 1, 'Rock': 1, 'Ghost': 1, 'Dragon': 1, 'Dark': 1, 'Steel': 1, 'Fairy': 1
    },
    'Grass': {
        'Normal': 1, 'Fire': 0.5, 'Water': 2, 'Electric': 1, 'Grass': 0.5, 'Ice': 0.5, 'Fighting': 1, 'Poison': 1, 'Ground': 2, 'Flying': 0.5, 'Psychic': 1, 
        'Bug': 0.5, 'Rock': 2, 'Ghost': 1, 'Dragon': 0.5, 'Dark': 1, 'Steel': 0.5, 'Fairy': 1
    },
    'Ice': {
        'Normal': 1, 'Fire': 0.5, 'Water': 0.5, 'Electric': 1, 'Grass': 2, 'Ice': 0.5, 'Fighting': 1,'Poison': 1, 'Ground': 2, 'Flying': 2, 'Psychic': 1, 
        'Bug': 1, 'Rock': 1, 'Ghost': 1, 'Dragon': 2, 'Dark': 1, 'Steel': 0.5, 'Fairy': 1
    },
    'Fighting': {
        'Normal': 2, 'Fire': 1, 'Water': 1, 'Electric': 1, 'Grass': 1, 'Ice': 1, 'Fighting': 1, 'Poison': 1, 'Ground': 1, 'Flying': 0.5, 'Psychic': 0.5, 
        'Bug': 1, 'Rock': 2, 'Ghost': 0, 'Dragon': 1, 'Dark': 2, 'Steel': 2, 'Fairy': 0.5
    },
    'Poison': {
        'Normal': 1, 'Fire': 1, 'Water': 1, 'Electric': 1, 'Grass': 2, 'Ice': 1, 'Fighting': 1, 'Poison': 0.5, 'Ground': 1, 'Flying': 1, 'Psychic': 2, 
        'Bug': 1, 'Rock': 1, 'Ghost': 1, 'Dragon': 1, 'Dark': 1, 'Steel': 0, 'Fairy': 2
    },
    'Ground': {
        'Normal': 1, 'Fire': 2, 'Water': 1, 'Electric': 2, 'Grass': 0.5, 'Ice': 1, 'Fighting': 1, 'Poison': 2, 'Ground': 1, 'Flying': 0, 'Psychic': 1, 
        'Bug': 1, 'Rock': 2, 'Ghost': 1, 'Dragon': 1, 'Dark': 1, 'Steel': 2, 'Fairy': 1
    },
    'Flying': {
        'Normal': 1, 'Fire': 1, 'Water': 1, 'Electric': 0.5, 'Grass': 2, 'Ice': 1, 'Fighting': 2, 'Poison': 1, 'Ground': 1, 'Flying': 1, 'Psychic': 1, 
        'Bug': 2, 'Rock': 0.5, 'Ghost': 1, 'Dragon': 1, 'Dark': 1, 'Steel': 1, 'Fairy': 1
    },
    'Psychic': {
        'Normal': 1, 'Fire': 1, 'Water': 1, 'Electric': 1, 'Grass': 1, 'Ice': 1, 'Fighting': 1, 'Poison': 1, 'Ground': 1, 'Flying': 1, 'Psychic': 1, 
        'Bug': 1, 'Rock': 1, 'Ghost': 2, 'Dragon': 1, 'Dark': 0, 'Steel': 1, 'Fairy': 1
    },
    'Bug': {
        'Normal': 1, 'Fire': 0.5, 'Water': 1, 'Electric': 1, 'Grass': 2, 'Ice': 1, 'Fighting': 1, 'Poison': 1, 'Ground': 1, 'Flying': 0.5, 'Psychic': 2, 
        'Bug': 1, 'Rock': 1, 'Ghost': 1, 'Dragon': 1, 'Dark': 2, 'Steel': 0.5, 'Fairy': 0.5
    },
    'Rock': {
        'Normal': 1, 'Fire': 2, 'Water': 1, 'Electric': 1, 'Grass': 1, 'Ice': 2, 'Fighting': 0.5, 'Poison': 1, 'Ground': 1, 'Flying': 2, 'Psychic': 1, 
        'Bug': 2, 'Rock': 1, 'Ghost': 1, 'Dragon': 1, 'Dark': 1, 'Steel': 0.5, 'Fairy': 1
    },
    'Ghost': {
        'Normal': 0, 'Fire': 1, 'Water': 1, 'Electric': 1, 'Grass': 1, 'Ice': 1, 'Fighting': 0, 'Poison': 1, 'Ground': 1, 'Flying': 1, 'Psychic': 2, 
        'Bug': 1, 'Rock': 1, 'Ghost': 2, 'Dragon': 1, 'Dark': 1, 'Steel': 1, 'Fairy': 1
    },
    'Dragon': {
        'Normal': 1, 'Fire': 1, 'Water': 1, 'Electric': 1, 'Grass': 1, 'Ice': 1, 'Fighting': 1, 'Poison': 1, 'Ground': 1, 'Flying': 1, 'Psychic': 1, 
        'Bug': 1, 'Rock': 1, 'Ghost': 1, 'Dragon': 2, 'Dark': 1, 'Steel': 0.5, 'Fairy': 0
    },
    'Dark': {
        'Normal': 1, 'Fire': 1, 'Water': 1, 'Electric': 1, 'Grass': 1, 'Ice': 1, 'Fighting': 2, 'Poison': 1, 'Ground': 1, 'Flying': 1, 'Psychic': 2, 
        'Bug': 1, 'Rock': 1, 'Ghost': 2, 'Dragon': 1, 'Dark': 1, 'Steel': 1, 'Fairy': 0.5
    },
    'Steel': {
        'Normal': 1, 'Fire': 0.5, 'Water': 0.5, 'Electric': 0.5, 'Grass': 1, 'Ice': 2, 'Fighting': 2, 'Poison': 1, 'Ground': 1, 'Flying': 1, 'Psychic': 1, 
        'Bug': 1, 'Rock': 2, 'Ghost': 1, 'Dragon': 1, 'Dark': 1, 'Steel': 0.5, 'Fairy': 2
    },
    'Fairy': {
        'Normal': 1, 'Fire': 0.5, 'Water': 1, 'Electric': 1, 'Grass': 1, 'Ice': 1, 'Fighting': 2, 'Poison': 0.5, 'Ground': 1, 'Flying': 1, 'Psychic': 1, 
        'Bug': 1, 'Rock': 1, 'Ghost': 1, 'Dragon': 2, 'Dark': 2, 'Steel': 0.5, 'Fairy': 1
    }
}

existingMoves = {
'Aerial Ace': ('Flying', 'Physical', 60, 100, 20),
'Air Cutter': ('Flying', 'Special', 60, 95, 25),  # High critical hit ratio.
'Arm Thrust': ('Fighting', 'Physical', 15, 100, 20),  # Hits 2-5 times in one turn.
'Aromatherapy': ('Grass', 'Status', 0, 100, 5),
'Astonish': ('Ghost', 'Physical', 30, 100, 15),  # May cause flinching.
'Blast Burn': ('Fire', 'Special', 150, 90, 5),  # User must recharge next turn.
'Blaze Kick': ('Fire', 'Physical', 85, 90, 10),  # High critical hit ratio. May burn opponent.
'Block': ('Normal', 'Status', 0, 100, 5),  # Opponent cannot flee or switch.
'Bounce': ('Flying', 'Physical', 85, 85, 5),  # Springs up on first turn, attacks on second. May paralyze opponent.
'Brick Break': ('Fighting', 'Physical', 75, 100, 15),  # Breaks through Reflect and Light Screen barriers.
'Bulk Up': ('Fighting', 'Status', 0, 100, 20),  # Raises user's Attack and Defense.
'Bullet Seed': ('Grass', 'Physical', 25, 100, 30),  # Hits 2-5 times in one turn.
'Calm Mind': ('Psychic', 'Status', 0, 100, 20),  # Raises user's Special Attack and Special Defense.
'Camouflage': ('Normal', 'Status', 0, 100, 20),  # Changes user's type according to the location.
'Charge': ('Electric', 'Status', 0, 100, 20),  # Raises user's Special Defense and next Electric move's power increases.
'Cosmic Power': ('Psychic', 'Status', 0, 100, 20),  # Raises user's Defense and Special Defense.
'Covet': ('Normal', 'Physical', 60, 100, 25),  # Opponent's item is stolen by the user.
'Crush Claw': ('Normal', 'Physical', 75, 95, 10),  # May lower opponent's Defense.
'Dive': ('Water', 'Physical', 80, 100, 10),  # Dives underwater on first turn, attacks on second turn.
'Dragon Claw': ('Dragon', 'Physical', 80, 100, 15),
'Dragon Dance': ('Dragon', 'Status', 0, 100, 20),  # Raises user's Attack and Speed.
'Endeavor': ('Normal', 'Physical', 0, 100, 5),  # Reduces opponent's HP to same as user's.
'Eruption': ('Fire', 'Special', 150, 100, 5),  # Stronger when the user's HP is higher.
'Extrasensory': ('Psychic', 'Special', 80, 100, 20),  # May cause flinching.
'Facade': ('Normal', 'Physical', 70, 100, 20),  # Power doubles if user is burned, poisoned, or paralyzed.
'Fake Out': ('Normal', 'Physical', 40, 100, 10),  # User attacks first, foe flinches. Only usable on first turn.
'Fake Tears': ('Dark', 'Status', 0, 100, 20),  # Sharply lowers opponent's Special Defense.
'Feather Dance': ('Flying', 'Status', 0, 100, 15),  # Sharply lowers opponent's Attack.
'Flatter': ('Dark', 'Status', 0, 100, 15),  # Confuses opponent, but raises its Special Attack.
'Focus Punch': ('Fighting', 'Physical', 150, 100, 20),  # If the user is hit before attacking, it flinches instead.
'Frenzy Plant': ('Grass', 'Special', 150, 90, 5),  # User must recharge next turn.
'Grass Whistle': ('Grass', 'Status', 0, 55, 15),  # Puts opponent to sleep.
'Grudge': ('Ghost', 'Status', 0, 100, 5),  # If the user faints after using this move, the PP for the opponent's last move is depleted.
'Hail': ('Ice', 'Status', 0, 100, 10),  # Non-Ice types are damaged for 5 turns.
'Heat Wave': ('Fire', 'Special', 95, 90, 10),  # May burn opponent.
'Helping Hand': ('Normal', 'Status', 0, 100, 20),  # In Double Battles, boosts the power of the partner's move.
'Howl': ('Normal', 'Status', 0, 100, 40),  # Raises Attack of allies.
'Hydro Cannon': ('Water', 'Special', 150, 90, 5),  # User must recharge next turn.
'Hyper Voice': ('Normal', 'Special', 90, 100, 10),
'Ice Ball': ('Ice', 'Physical', 30, 90, 20),  # Doubles in power each turn for 5 turns.
'Icicle Spear': ('Ice', 'Physical', 25, 100, 30),  # Hits 2-5 times in one turn.
'Imprison': ('Psychic', 'Status', 0, 100, 10),  # Opponent is unable to use moves that the user also knows.
'Ingrain': ('Grass', 'Status', 0, 100, 20),  # User restores HP each turn. User cannot escape/switch.
'Iron Defense': ('Steel', 'Status', 0, 100, 15),  # Sharply raises user's Defense.
'Knock Off': ('Dark', 'Physical', 65, 100, 20),  # Removes opponent's held item for the rest of the battle.
'Leaf Blade': ('Grass', 'Physical', 90, 100, 15),  # High critical hit ratio.
'Leer': ('Normal', 'Status', 0, 100, 30),  # Lowers opponent's Defense.
'Luster Purge': ('Psychic', 'Special', 95, 100, 5),  # May lower opponent's Special Defense.
'Magic Coat': ('Psychic', 'Status', 0, 100, 15),  # Reflects moves that cause status conditions back to the attacker.
'Magical Leaf': ('Grass', 'Special', 60, 100, 20),  # Ignores Accuracy and Evasiveness.
'Memento': ('Dark', 'Status', 0, 100, 10),  # User faints, sharply lowers opponent's Attack and Special Attack.
'Metal Sound': ('Steel', 'Status', 0, 85, 40),  # Sharply lowers opponent's Special Defense.
'Meteor Mash': ('Steel', 'Physical', 90, 90, 10),  # May raise user's Attack.
'Mist Ball': ('Psychic', 'Special', 95, 100, 5),  # May lower opponent's Special Attack.
'Mud Shot': ('Ground', 'Special', 55, 95, 15),  # Lowers opponent's Speed.
'Mud Sport': ('Ground', 'Status', 0, 100, 15),  # Weakens the power of Electric-type moves.
'Muddy Water': ('Water', 'Special', 90, 85, 10),  # May lower opponent's Accuracy.
'Nature Power': ('Normal', 'Status', 0, 100, 20),  # Uses a certain move based on the current terrain.
'Needle Arm': ('Grass', 'Physical', 60, 100, 15),  # May cause flinching.
'Odor Sleuth': ('Normal', 'Status', 0, 100, 40),  # Resets opponent's Evasiveness, and allows Normal- and Fighting-type attacks to hit Ghosts.
'Overheat': ('Fire', 'Special', 130, 90, 5),  # Sharply lowers user's Special Attack.
'Poison Fang': ('Poison', 'Physical', 50, 100, 15),  # May badly poison opponent.
'Poison Tail': ('Poison', 'Physical', 50, 100, 25),  # High critical hit ratio. May poison opponent.
'Psycho Boost': ('Psychic', 'Special', 140, 90, 5),  # Sharply lowers user's Special Attack.
'Recycle': ('Normal', 'Status', 0, 100, 10),  # User's used hold item is restored.
'Refresh': ('Normal', 'Status', 0, 100, 20),  # Cures paralysis, poison, and burns.
'Revenge': ('Fighting', 'Physical', 60, 100, 10),  # Power increases if user was hit first.
'Rock Blast': ('Rock', 'Physical', 25, 90, 10),  # Hits 2-5 times in one turn.
'Rock Tomb': ('Rock', 'Physical', 60, 95, 15),  # Lowers opponent's Speed.
'Role Play': ('Psychic', 'Status', 0, 100, 10),  # User copies the opponent's Ability.
'Sand Tomb': ('Ground', 'Physical', 35, 85, 15),  # Traps opponent, damaging them for 4-5 turns.
'Secret Power': ('Normal', 'Physical', 70, 100, 20),  # Effects of the attack vary with the location.
'Shadow Punch': ('Ghost', 'Physical', 60, 100, 20),  # Ignores Accuracy and Evasiveness.
'Sheer Cold': ('Ice', 'Special', 0, 30, 5),  # One-Hit-KO, if it hits.
'Shock Wave': ('Electric', 'Special', 60, 100, 20),  # Ignores Accuracy and Evasiveness.
'Signal Beam': ('Bug', 'Special', 75, 100, 15),  # May confuse opponent.
'Silver Wind': ('Bug', 'Special', 60, 100, 5),  # May raise all stats of user at once.
'Skill Swap': ('Psychic', 'Status', 0, 100, 10),  # The user swaps Abilities with the opponent.
'Sky Uppercut': ('Fight', 'Physical', 85, 90, 15),  # Hits the opponent, even during Fly.
'Slack Off': ('Normal', 'Status', 0, 100, 5),  # User recovers half its max HP.
'Smelling Salts': ('Normal', 'Physical', 70, 100, 10),  # Power doubles if opponent is paralyzed, but cures it.
'Snatch': ('Dark', 'Status', 0, 100, 10),  # Steals the effects of the opponent's next move.
'Spit Up': ('Normal', 'Special', 0, 100, 10),  # Power depends on how many times the user performed Stockpile.
'Stockpile': ('Normal', 'Status', 0, 100, 20),  # Stores energy for use with Spit Up and Swallow.
'Superpower': ('Fight', 'Physical', 120, 100, 5),  # Lowers user's Attack and Defense.
'Swallow': ('Normal', 'Status', 0, 100, 10),  # The more times the user has performed Stockpile, the more HP is recovered.
'Tail Glow': ('Bug', 'Status', 0, 100, 20),  # Drastically raises user's Special Attack.
'Taunt': ('Dark', 'Status', 0, 100, 20),  # Opponent can only use moves that attack.
'Teeter Dance': ('Normal', 'Status', 0, 100, 20),  # Confuses all Pokémon.
'Tickle': ('Normal', 'Status', 0, 100, 20),  # Lowers opponent's Attack and Defense.
'Torment': ('Dark', 'Status', 0, 100, 15),  # Opponent cannot use the same move in a row.
'Trick': ('Psychic', 'Status', 0, 100, 10),  # Swaps held items with the opponent.
'Uproar': ('Normal', 'Special', 90, 100, 10),  # User attacks for 3 turns and prevents sleep.
'Volt Tackle': ('Electric', 'Physical', 120, 100, 15),  # User receives recoil damage. May paralyze opponent.
'Water Pulse': ('Water', 'Special', 60, 100, 20),  # May confuse opponent.
'Water Sport': ('Water', 'Status', 0, 100, 15),  # Weakens the power of Fire-type moves.
'Water Spout': ('Water', 'Special', 150, 100, 5),  # The higher the user's HP, the higher the damage caused.
'Will-O-Wisp': ('Fire', 'Status', 0, 85, 15),  # Burns opponent.
'Wish': ('Normal', 'Status', 0, 100, 10),  # The user recovers HP in the following turn.
'Yawn': ('Normal', 'Status', 0, 100, 10), 
'Absorb': ('Grass', 'Special', 20, 100, 25),  # User recovers half the HP inflicted on opponent.
'Acid': ('Poison', 'Special', 40, 100, 30),  # May lower opponent's Special Defense.
'Acid Armor': ('Poison', 'Status', 0, 100, 20),  # Sharply raises user's Defense.
'Agility': ('Psychic', 'Status', 0, 100, 30),  # Sharply raises user's Speed.
'Amnesia': ('Psychic', 'Status', 0, 100, 20),  # Sharply raises user's Special Defense.
'Aurora Beam': ('Ice', 'Special', 65, 100, 20),  # May lower opponent's Attack.
'Barrage': ('Normal', 'Physical', 15, 85, 20),  # Hits 2-5 times in one turn.
'Barrier': ('Psychic', 'Status', 0, 100, 20),  # Sharply raises user's Defense.
'Bind': ('Normal', 'Physical', 15, 85, 20,),  # Traps opponent, damaging them for 4-5 turns.
'Bite': ('Dark', 'Physical', 60, 100, 25),  # May cause flinching.
'Blizzard': ('Ice', 'Special', 110, 70, 5),  # May freeze opponent.
'Body Slam': ('Normal', 'Physical', 85, 100, 15),  # May paralyze opponent.
'Bubble': ('Water', 'Special', 40, 100, 30),  # May lower opponent's Speed.
'Bubble Beam': ('Water', 'Special', 65, 100, 20),  # May lower opponent's Speed.
'Clamp': ('Water', 'Physical', 35, 85, 15),  # Traps opponent, damaging them for 4-5 turns.
'Confuse Ray': ('Ghost', 'Status', 0, 100, 10),  # Confuses opponent.
'Confusion': ('Psychic', 'Special', 50, 100, 25),  # May confuse opponent.
'Crabhammer': ('Water', 'Physical', 100, 90, 10),  # High critical hit ratio.
'Cut': ('Normal', 'Physical', 50, 95, 30),
'Defense Curl': ('Normal', 'Status', 0, 100, 40),  # Raises user's Defense.
'Dig': ('Ground', 'Physical', 80, 100, 10),  # Digs underground on first turn, attacks on second. Can also escape from caves.
'Double Kick': ('Fight', 'Physical', 30, 100, 30),  # Hits twice in one turn.
'Double Slap': ('Normal', 'Physical', 15, 85, 10),  # Hits 2-5 times in one turn.
'Double-Edge': ('Normal', 'Physical', 120, 100, 15),  # User receives recoil damage.
'Drill Peck': ('Flying', 'Physical', 80, 100, 20),
'Earthquake': ('Ground', 'Physical', 100, 100, 10),  # Power is doubled if opponent is underground from using Dig.
'Ember': ('Fire', 'Special', 40, 100, 25),  # May burn opponent.
'Fire Blast': ('Fire', 'Special', 110, 85, 5),  # May burn opponent.
'Fire Punch': ('Fire', 'Physical', 75, 100, 15),  # May burn opponent.
'Fire Spin': ('Fire', 'Special', 35, 85, 15),  # Traps opponent, damaging them for 4-5 turns.
'Fissure': ('Ground', 'Physical', 0, 30, 5),  # One-Hit-KO, if it hits.
'Flamethrower': ('Fire', 'Special', 90, 100, 15),  # May burn opponent.
'Fly': ('Flying', 'Physical', 90, 95, 15),  # Flies up on first turn, attacks on second turn.
'Fury Attack': ('Normal', 'Physical', 15, 85, 20),  # Hits 2-5 times in one turn.
'Glare': ('Normal', 'Status', 0, 100, 30),  # Paralyzes opponent.
'Growl': ('Normal', 'Status', 0, 100, 40),  # Lowers opponent's Attack.
'Guillotine': ('Normal', 'Physical', 0, 30, 5),  # One-Hit-KO, if it hits.
'Gust': ('Flying', 'Special', 40, 100, 35),  # Hits Pokémon using Fly/Bounce/Sky Drop with double power.
'Harden': ('Normal', 'Status', 0, 100, 30),  # Raises user's Defense.
'Headbutt': ('Normal', 'Physical', 70, 100, 15),  # May cause flinching.
'Horn Attack': ('Normal', 'Physical', 65, 100, 25),
'Horn Drill': ('Normal', 'Physical', 0, 30, 5),  # One-Hit-KO, if it hits.
'Hydro Pump': ('Water', 'Special', 110, 80, 5),
'Hyper Beam': ('Normal', 'Special', 150, 90, 5),  # User must recharge next turn.
'Hyper Fang': ('Normal', 'Physical', 80, 90, 15),  # May cause flinching.
'Hypnosis': ('Psychic', 'Status', 0, 60, 20),  # Puts opponent to sleep.
'Ice Beam': ('Ice', 'Special', 90, 100, 10),  # May freeze opponent.
'Ice Punch': ('Ice', 'Physical', 75, 100, 15),  # May freeze opponent.
'Leech Life': ('Bug', 'Physical', 80, 100, 10),  # User recovers half the HP inflicted on opponent.
'Leech Seed': ('Grass', 'Status', 0, 90, 10),  # Drains HP from opponent each turn.
'Leer': ('Normal', 'Status', 0, 100, 30),  # Lowers opponent's Defense.
'Light Screen': ('Psychic', 'Status', 0, 100, 30),  # Halves damage from Special attacks for 5 turns.
'Low Kick': ('Fight', 'Physical', 0, 100, 20),  # The heavier the opponent, the stronger the attack.
'Meditate': ('Psychic', 'Status', 0, 100, 40),  # Raises user's Attack.
'Mega Drain': ('Grass', 'Special', 40, 100, 15),  # User recovers half the HP inflicted on opponent.
'Mega Kick': ('Normal', 'Physical', 120, 75, 5),
'Mega Punch': ('Normal', 'Physical', 80, 85, 20),
'Night Shade': ('Ghost', 'Special', 0, 100, 15),  # Inflicts damage equal to user's level.
'Peck': ('Flying', 'Physical', 35, 100, 35),
'Petal Dance': ('Grass', 'Special', 120, 100, 10),  # User attacks for 2-3 turns but then becomes confused.
'Pin Missile': ('Bug', 'Physical', 25, 95, 20),  # Hits 2-5 times in one turn.
'Poison Gas': ('Poison', 'Status', 0, 90, 40),  # Poisons opponent.
'Poison Powder': ('Poison', 'Status', 0, 75, 35),  # Poisons opponent.
'Poison Sting': ('Poison', 'Physical', 15, 100, 35),  # May poison the opponent.
'Pound': ('Normal', 'Physical', 40, 100, 35),
'Psychic': ('Psychic', 'Special', 90, 100),
'Quick Attack': ('Normal', 'Physical', 40, 100, 30),  # User attacks first.
'Razor Leaf': ('Grass', 'Physical', 55, 95, 25),  # High critical hit ratio.
'Razor Wind': ('Normal', 'Special', 80, 100, 10),  # Charges on first turn, attacks on second. High critical hit ratio.
'Recover': ('Normal', 'Status', 0, 100, 5),  # User recovers half its max HP.
'Reflect': ('Psychic', 'Status', 0, 100, 20),  # Halves damage from Physical attacks for 5 turns.
'Rest': ('Psychic', 'Status', 0, 100, 5),  # User sleeps for 2 turns, but user is fully healed.
'Roar': ('Normal', 'Status', 0, 100, 20),  # In battles, the opponent switches. In the wild, the Pokémon runs.
'Rock Slide': ('Rock', 'Physical', 75, 90, 10),  # May cause flinching.
'Rock Throw': ('Rock', 'Physical', 50, 90, 15),
'Rolling Kick': ('Fight', 'Physical', 60, 85, 15),  # May cause flinching.
'Scratch': ('Normal', 'Physical', 40, 100, 35),
'Screech': ('Normal', 'Status', 0, 85, 40),  # Sharply lowers opponent's Defense.
'Sing': ('Normal', 'Status', 0, 55, 15),  # Puts opponent to sleep.
'Sky Attack': ('Flying', 'Physical', 140, 90, 5),  # Charges on first turn, attacks on second. May cause flinching. High critical hit ratio.
'Slam': ('Normal', 'Physical', 80, 75, 20),
'Sleep Powder': ('Grass', 'Status', 0, 75, 15),  # Puts opponent to sleep.
'Sludge': ('Poison', 'Special', 65, 100, 20),  # May poison opponent.
'Smog': ('Poison', 'Special', 30, 70, 20),  # May poison opponent.
'Soft-Boiled': ('Normal', 'Status', 0, 100, 5),  # User recovers half its max HP.
'Solar Beam': ('Grass', 'Special', 120, 100, 10),  # Charges on first turn, attacks on second.
'Spore': ('Grass', 'Status', 0, 100, 15),  # Puts opponent to sleep.
'Stomp': ('Normal', 'Physical', 65, 100, 20),  # May cause flinching.
'Strength': ('Normal', 'Physical', 80, 100, 15),
'String Shot': ('Bug', 'Status', 0, 95, 40),  # Sharply lowers opponent's Speed.
'Struggle': ('Normal', 'Physical', 50, 100, 10000000),  # Only usable when all PP are gone. Hurts the user.
'Stun Spore': ('Grass', 'Status', 0, 75, 30),  # Paralyzes opponent.
'Substitute': ('Normal', 'Status', 0, 100, 10),  # Uses HP to create a decoy that takes hits.
'Super Fang': ('Normal', 'Physical', 0, 90, 10),  # Always takes off half of the opponent's HP.
'Supersonic': ('Normal', 'Status', 0, 55, 20),  # Confuses opponent.
'Surf': ('Water', 'Special', 90, 100, 15),  # Hits all adjacent Pokémon.
'Swift': ('Normal', 'Special', 60, 100, 20),  # Ignores Accuracy and Evasiveness.
'Swords Dance': ('Normal', 'Status', 0, 100, 20),  # Sharply raises user's Attack.
'Tackle': ('Normal', 'Physical', 40, 100, 35),
'Tail Whip': ('Normal', 'Status', 0, 100, 30),  # Lowers opponent's Defense.
'Take Down': ('Normal', 'Physical', 90, 85, 20),  # User receives recoil damage.
'Teleport': ('Psychic', 'Status', 0, 100, 20),  # Allows user to flee wild battles; also warps player to last PokéCenter.
'Thrash': ('Normal', 'Physical', 120, 100, 10),  # User attacks for 2-3 turns but then becomes confused.
'Thunder': ('Electric', 'Special', 110, 70, 10),  # May paralyze opponent.
'Thunder Punch': ('Electric', 'Physical', 75, 100, 15),  # May paralyze opponent.
'Thunder Shock': ('Electric', 'Special', 40, 100, 30),  # May paralyze opponent.
'Thunder Wave': ('Electric', 'Status', 0, 90, 20),  # Paralyzes opponent.
'Thunderbolt': ('Electric', 'Special', 90, 100, 15),  # May paralyze opponent.
'Toxic': ('Poison', 'Status', 0, 90, 10),  # Badly poisons opponent.
'Tri Attack': ('Normal', 'Special', 80, 100, 10),  # May paralyze, burn, or freeze opponent.
'Twineedle': ('Bug', 'Physical', 25, 100, 20, True, 2, 2),  # Hits twice in one turn. May poison opponent.
'Vine Whip': ('Grass', 'Physical', 45, 100, 25),
'Vise Grip': ('Normal', 'Physical', 55, 100, 30),
'Water Gun': ('Water', 'Special', 40, 100, 25),
'Waterfall': ('Water', 'Physical', 80, 100, 15),  # May cause flinching.
'Wing Attack': ('Flying', 'Physical', 60, 100, 35),
'Wrap': ('Normal', 'Physical', 15, 90, 20),
'Ancient Power': ('Rock', 'Special', 60, 100, 5),  # May raise all user's stats at once.
'Beat Up': ('Dark', 'Physical', 0, 100, 10),  # Each Pokémon in user's party attacks.
'Charm': ('Fairy', 'Status', 0, 100, 20),  # Sharply lowers opponent's Attack.
'Cotton Spore': ('Grass', 'Status', 0, 100, 40),  # Sharply lowers opponent's Speed.
'Cross Chop': ('Fight', 'Physical', 100, 80, 5),  # High critical hit ratio.
'Crunch': ('Dark', 'Physical', 80, 100, 15),  # May lower opponent's Defense.
'Detect': ('Fight', 'Status', 0, 100, 5),  # Protects the user, but may fail if used consecutively.
'Dragon Breath': ('Dragon', 'Special', 60, 100, 20),  # May paralyze opponent.
'Dynamic Punch': ('Fight', 'Physical', 100, 50, 5),  # Confuses opponent.
'Encore': ('Normal', 'Status', 0, 100, 5),  # Forces opponent to keep using its last move for 3 turns.
'Extreme Speed': ('Normal', 'Physical', 80, 100, 5),  # User attacks first.
'False Swipe': ('Normal', 'Physical', 40, 100, 40),  # Always leaves opponent with at least 1 HP.
'Feint Attack': ('Dark', 'Physical', 60, 100, 20),  # Ignores Accuracy and Evasiveness.
'Flail': ('Normal', 'Physical', 0, 100, 15),  # The lower the user's HP, the higher the power.
'Flame Wheel': ('Fire', 'Physical', 60, 100, 25),  # May burn opponent.
'Fury Cutter': ('Bug', 'Physical', 40, 95, 20),  # Power increases each turn.
'Future Sight': ('Psychic', 'Special', 120, 100, 10),  # Damage occurs 2 turns later.
'Giga Drain': ('Grass', 'Special', 75, 100, 10),  # User recovers half the HP inflicted on opponent.
'Heal Bell': ('Normal', 'Status', 0, 100, 5),  # Heals the user's party's status conditions.
'Icy Wind': ('Ice', 'Special', 55, 95, 15),  # Lowers opponent's Speed.
'Iron Tail': ('Steel', 'Physical', 100, 75, 15),  # May lower opponent's Defense.
'Mach Punch': ('Fight', 'Physical', 40, 100, 30),  # User attacks first.
'Megahorn': ('Bug', 'Physical', 120, 85, 10),
'Metal Claw': ('Steel', 'Physical', 50, 95, 35),  # May raise user's Attack.
'Milk Drink': ('Normal', 'Status', 0, 100, 5),  # User recovers half its max HP.
'Moonlight': ('Fairy', 'Status', 0, 100, 5),  # User recovers HP. Amount varies with the weather.
'Morning Sun': ('Normal', 'Status', 0, 100, 5),  # User recovers HP. Amount varies with the weather.
'Mud-Slap': ('Ground', 'Special', 20, 100, 10),  # Lowers opponent's Accuracy.
'Outrage': ('Dragon', 'Physical', 120, 100, 10),  # User attacks for 2-3 turns but then becomes confused.
'Present': ('Normal', 'Physical', 0, 90, 15),  # Either deals damage or heals.
'Protect': ('Normal', 'Status', 0, 100, 10),  # Protects the user, but may fail if used consecutively.
'Psych Up': ('Normal', 'Status', 0, 100, 10),  # Copies the opponent's stat changes.
'Pursuit': ('Dark', 'Physical', 40, 100, 20),  # Double power if the opponent is switching out.
'Rain Dance': ('Water', 'Status', 0, 100, 5),  # Makes it rain for 5 turns.
'Rapid Spin': ('Normal', 'Physical', 50, 100, 40),  # Raises user's Speed and removes entry hazards and trap move effects.
'Reversal': ('Fight', 'Physical', 0, 100, 15),  # The lower the user's HP, the higher the power.
'Rock Smash': ('Fight', 'Physical', 40, 100, 15),  # May lower opponent's Defense.
'Rollout': ('Rock', 'Physical', 30, 90, 20),  # Doubles in power each turn for 5 turns.
'Shadow Ball': ('Ghost', 'Special', 80, 100, 15),  # May lower opponent's Special Defense.
'Sludge Bomb': ('Poison', 'Special', 90, 100, 10),  # May poison opponent.
'Spark': ('Electric', 'Physical', 65, 100, 20),  # May paralyze opponent.
'Steel Wing': ('Steel', 'Physical', 70, 90, 25),  # May raise user's Defense.
'Sunny Day': ('Fire', 'Status', 0, 100, 5),  # Makes it sunny for 5 turns.
'Synthesis': ('Grass', 'Status', 0, 100, 5),  # User recovers HP. Amount varies with the weather.
'Triple Kick': ('Fight', 'Physical', 10, 90, 10),  # Hits thrice in one turn at increasing power.
'Twister': ('Dragon', 'Special', 40, 100, 20),  # May cause flinching. Hits Pokémon using Fly/Bounce with double power.
'Vital Throw': ('Fight', 'Physical', 70, 100, 10),  # User attacks last, but ignores Accuracy and Evasiveness.
'Whirlpool': ('Water', 'Special', 35, 85, 15),  # May cause trapping effect.
}
