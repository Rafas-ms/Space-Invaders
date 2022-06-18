import pygame
import random
import math
from pygame import mixer, K_LEFT, K_RIGHT

# Inicializando o Pygame
pygame.init()

# Criando a tela
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width,
                                  screen_height))

# FPS
FPS = 60
FPS_CLOCK = pygame.time.Clock()

# Definindo o titulo da tela
pygame.display.set_caption("UNIBH Space Invaders")

# Som de fundo
mixer.music.load('data/background.wav')
mixer.music.play()




# Classe para o plano de fundo
class Background(pygame.sprite.Sprite):
    def __init__(self):
        self.img_path = ""
        self.bgY = 0
        self.bgX = 0

    def render(self):
        img = pygame.image.load(self.img_path)
        screen.blit(img, (self.bgX, self.bgY))

    def setBackground(self,img_path):
        self.img_path = img_path

# Instanciando o plano de fundo
background = Background()
background.setBackground("data/jogo1.jpg")


# Classe para o jogador
class Player(pygame.sprite.Sprite):
    def __init__(self):
        self.image = pygame.image.load("data/spaceship.png")
        self.rect = self.image.get_rect()

        # Position and direction
        self.player_X = 370
        self.player_Y = 523
        self.player_Xchange = 0

    def create(self):
        screen.blit(self.image, (self.player_X - 16, self.player_Y + 10))

    def move(self):
        # Returns the current key presses
        pressed_keys = pygame.key.get_pressed()
        # Accelerates the player in the direction of the key press
        if pressed_keys[K_LEFT]:
            self.player_Xchange = -5
        if pressed_keys[K_RIGHT]:
            self.player_Xchange = 5

    def stop(self):
        self.player_Xchange = 0


    def update_move(self):
        self.player_X += self.player_Xchange

    def getPlayer_X(self):
        return self.player_X

    def getPlayer_Y(self):
        return self.player_Y

    def setPlayer_X(self,player_x):
        self.player_X = player_x


# Instanciando o jogador
player = Player()


#Classe para a munição
class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        self.bullet_X = 0
        self.bullet_Y = 500
        self.img = ""
        self.bullet_state = "rest"

    def setSkin(self,img_path):
        self.img = pygame.image.load(img_path)


    def draw(self):
        screen.blit(self.img, (self.bullet_X, self.bullet_Y))
        self.bullet_state = "fire"

    def sound(self):
        bullet_sound = mixer.Sound('data/bullet.wav')
        bullet_sound.play()

    def setBullet_X(self,player_X):
        self.bullet_X = player_X

    def setBullet_Y(self,bullet_y):
        self.bullet_Y = bullet_y

    def getBullet_Y(self):
        return self.bullet_Y

    def getBullet_X(self):
        return self.bullet_X

    def setBullet_state(self,bullet_state):
        self.bullet_state = bullet_state

    def getBullet_state(self):
        return self.bullet_state

    def update_bullet(self):
        self.bullet_Y -= 40


#Instanciando a munição
bullet = Bullet()
bullet.setSkin("data/laser2.png")


#Classe para o inimigo
class Invader(pygame.sprite.Sprite):

    def __init__(self):
         self.invaderImage = []
         self.invader_X = []
         self.invader_Y = []
         self.invader_Xchange = []
         self.invader_Ychange = []
         self.no_of_invaders = 12
         self.skin = ""


    def setSkin(self,skin_path):
        self.skin = skin_path
        self.invaderImage = []
        for num in range(self.no_of_invaders):
            self.invaderImage.append(pygame.image.load(self.skin))
            self.invader_X.append(random.randint(64, 737))
            self.invader_Y.append(random.randint(30, 180))
            self.invader_Xchange.append(4)
            self.invader_Ychange.append(50)


    def create(self,i):
        screen.blit(self.invaderImage[i], (self.invader_X[i],self.invader_Y[i]))

    def getNo_of_invaders(self):
        return self.no_of_invaders

    def setNo_of_invaders(self,i):
        self.no_of_invaders = i

    def update_move(self,i):
        self.invader_X[i] += self.invader_Xchange[i]

    def getInvader_X(self,i):
        return self.invader_X[i]

    def getInvader_Y(self,i):
        return self.invader_Y[i]

    def setInvader_X(self,i,Xchange):
        self.invader_X[i] = Xchange

    def setInvader_Y(self,i,Ychange):
        self.invader_Y[i] = Ychange

    def getInvader_Xchange(self,i):
        return self.invader_Xchange[i]

    def setInvader_Xchange(self,i,Xchange):
        self.invader_Xchange[i] = Xchange

    def update_hight(self,i):
        self.invader_Y[i] += invader.invader_Ychange[i]



#Instanciando o inimigo
invader = Invader()
invader.setSkin("data/alien1.png")



# Conceito de colisão
def isCollision(x1, x2, y1, y2):
    distance = math.sqrt((math.pow(x1 - x2, 2)) +
                         (math.pow(y1 - y2, 2)))
    if distance <= 50:
        return True
    else:
        return False



#Classe para a pontuação e para os niveis
class Score(pygame.sprite.Sprite):

    def __init__(self):
         self.score_val = 0
         self.scoreX = 5
         self.scoreY = 5
         self.levelX = 5
         self.levelY = 30
         self.superX = 5
         self.superY = 60
         self.liberaSuper = 0
         self.font = pygame.font.Font('freesansbold.ttf', 20)
         self.game_over_font = pygame.font.Font('freesansbold.ttf', 64)
         self.level = 1
         self.kill = 1

    def show_score(self):
        score = self.font.render("Points: " + str(self.score_val), True, (255, 255, 255))
        lvl = self.font.render("Level: " + str(self.level), True, (255, 255, 255))
        screen.blit(score, (self.scoreX, self.scoreY))
        screen.blit(lvl, (self.levelX, self.levelY))
        if self.liberaSuper == 1:
            super = self.font.render("Aperte 'E' para ativar a explosão galática ", True, (255, 255, 255))
            screen.blit(super, (self.superX, self.superY))



    def game_over(self):
        game_over_text = self.game_over_font.render("GAME OVER",
                                               True, (255, 255, 255))
        screen.blit(game_over_text, (190, 250))

    def win(self):
        win = self.font.render("Parabéns você salvou a galáxia Anima!",
                                               True, (255, 255, 255))
        screen.blit(win, (190, 250))

    def addScore(self):
        self.score_val += self.kill

    def getScore(self):
        return  self.score_val

    def getLevel(self):
        return  self.level

    def addLevel(self):
        self.level += 1

    def setKill(self, kill):
        self.kill = kill

    def addSuper(self):
        self.liberaSuper = 1




# Instanciando o score
score = Score()



# Quantidade de cargas para explosão galactia
charge = 1

# game loop
running = True
while running:
    # RGB
    screen.fill((0, 0, 0))
    background.render()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Captura das teclas do teclado e suas funções
        #Movimento do player
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.move()
            if event.key == pygame.K_RIGHT:
                player.move()

            #Gatilho para atirar
            if event.key == pygame.K_SPACE:
                if bullet.getBullet_state() == "rest":
                    bullet.setBullet_X(player.getPlayer_X())
                    bullet.draw()
                    bullet.sound()

            # Condição para utilizar a explosão galactia
            if event.key == pygame.K_e and score.getLevel() == 4 and charge == 1:
                for i in range(10):
                    score.addScore()
                    invader.setInvader_X(i, random.randint(64, 736))
                    invader.setInvader_Y(i, random.randint(30, 200))
                    invader.setInvader_Xchange(i, invader.getInvader_Xchange(i) * -1)
                    mixer.music.load('data/super.wav')
                    mixer.music.play()

                charge -= 1

        # Parar o movimento do player
        if event.type == pygame.KEYUP:
            player.stop()

    #Controlando a munição
    if bullet.getBullet_Y() <= 0:
        bullet.setBullet_Y(600)
        bullet.setBullet_state("rest")
    if bullet.getBullet_state() == "fire":
        bullet.draw()
        bullet.update_bullet()

    # Criando os Alienigenas e ajustando sua posição
    for i in range(invader.getNo_of_invaders()):

        #Condição para o game over
        if invader.getInvader_Y(i) >= 450:
            if abs(player.getPlayer_X() - invader.getInvader_X(i)) < 80:
                for j in range(invader.getNo_of_invaders()):
                    invader.setInvader_Y(j,2000)
                    explosion_sound = mixer.Sound('data/explosion.wav')
                    explosion_sound.play()
                score.game_over()
                break

        #Definindo limites para a movimentação do inimigo
        if invader.getInvader_X(i) >= 735 or invader.getInvader_X(i) <= 0:
            invader.setInvader_Xchange(i,invader.getInvader_Xchange(i) * -1)
            invader.update_hight(i)

        # Colisão
        collision = isCollision(bullet.getBullet_X(), invader.getInvader_X(i),
                                bullet.getBullet_Y(), invader.getInvader_Y(i))

        #Consequencias da colisão
        if collision:
            score.addScore()
            bullet.setBullet_Y(600)
            bullet.setBullet_state("rest")
            invader.setInvader_X(i,random.randint(64, 736))
            invader.setInvader_Y(i,random.randint(30, 200))
            invader.setInvader_Xchange(i,invader.getInvader_Xchange(i) * -1)

            #Mudança do level
            if score.getScore() == 26:
                score.addLevel()
                background.setBackground("data/jogo2.jpg")
                invader.setSkin("data/alien2.png")
            if score.getScore() == 81:
                score.addLevel()
                background.setBackground("data/jogo3.jpg")
                invader.setSkin("data/alien3.png")
                bullet.setSkin("data/laser3.png")
                score.setKill(4)
            if score.getScore() == 153:
                score.addSuper()
                score.addLevel()
                background.setBackground("data/jogo4.jpg")
                invader.setSkin("data/alien4.png")
                bullet.setSkin("data/laser1.png")
                score.setKill(8)


        invader.create(i)

    #Condição para a vitoria
    if score.getScore() >= 200:
        invader.setNo_of_invaders(0)
        score.win()





    # Limitando a movimentação do player
    if player.getPlayer_X() <= 16:
        player.setPlayer_X(16)
    elif player.getPlayer_X() >= 750:
        player.setPlayer_X(750)

    # Adicionando movimento nas entidades
    player.update_move()
    for i in range(invader.getNo_of_invaders()):
        invader.update_move(i)



    #Criando o jogador
    player.create()

    #Mostrando Score
    score.show_score()


    pygame.display.update()
    FPS_CLOCK.tick(FPS)
