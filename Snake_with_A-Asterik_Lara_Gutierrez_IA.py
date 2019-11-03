import pygame
import sys
import random
import time

#Developers: - Rodrigo Lara
#            - Cesar Gutierrez
#      -------------------------------
#
#                Snake Game 
#                   with
#           A Asterisk Algortihm
#
#      -------------------------------

class Nodo():
    def __init__(self, pariente=None, posicion=None):
        self.pariente = pariente
        self.posicion = posicion

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, otro):
        return self.posicion == otro.posicion

def Astar(mapa, inicio, objetivo):
    Nodo_incio = Nodo(None, inicio)
    Nodo_incio.g = Nodo_incio.h = Nodo_incio.f = 0
    Nodo_fin = Nodo(None, objetivo)
    Nodo_fin.g = Nodo_fin.h = Nodo_fin.f = 0
    lista_abierta = []
    lista_cerrada = []
    lista_abierta.append(Nodo_incio)
    while len(lista_abierta) > 0:
        Nodo_actual = lista_abierta[0]
        index_actual = 0
        for index, item in enumerate(lista_abierta):
            if item.f < Nodo_actual.f:
                Nodo_actual = item
                index_actual = index

        lista_abierta.pop(index_actual)
        lista_cerrada.append(Nodo_actual)

        if Nodo_actual == Nodo_fin:
            path = []
            current = Nodo_actual
            while current is not None:
                path.append(current.posicion)
                current = current.pariente
            return path[::-1]

        sucesores = []
        for pos in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: # adyacentes

            Nodo_posicion = (Nodo_actual.posicion[0] + pos[0], Nodo_actual.posicion[1] + pos[1])
            if Nodo_posicion[0] > (len(mapa) - 1) or Nodo_posicion[0] < 0 or Nodo_posicion[1] > (len(mapa[len(mapa)-1]) -1) or Nodo_posicion[1] < 0:
                continue

            if mapa[Nodo_posicion[0]][Nodo_posicion[1]] != 0:
                continue

            nuevo_Nodo = Nodo(Nodo_actual, Nodo_posicion)

            sucesores.append(nuevo_Nodo)

        for sucesor in sucesores:

            for closed_child in lista_cerrada:
                if sucesor == closed_child:
                    continue

            sucesor.g = Nodo_actual.g + 1
            sucesor.h = ((sucesor.posicion[0] - Nodo_fin.posicion[0]) ** 2) + ((sucesor.posicion[1] - Nodo_fin.posicion[1]) ** 2)
            sucesor.f = sucesor.g + sucesor.h

            for open_Nodo in lista_abierta:
                if sucesor == open_Nodo and sucesor.g > open_Nodo.g:
                    continue

            lista_abierta.append(sucesor)
##########################
class Snake():
    def __init__(self,x,y):
        self.position = [x,y]
        self.body = [[x,y],[x-10,y],[x-20,y]]
        self.direction = "Derecha"
        self.changueDirectionTo = self.direction

    def changueDirTo(self,direccion):
        if direccion == "Derecha" and not self.direction == "Izquierda":
            self.direction = "Derecha"
        if direccion == "Izquierda" and not self.direction == "Derecha":
            self.direction = "Izquierda"
        if direccion == "Arriba" and not self.direction == "Abajo":
            self.direction = "Arriba"
        if direccion == "Abajo" and not self.direction == "Arriba":
            self.direction = "Abajo"
    def move(self, foodPos):
        if self.direction == "Derecha":
            self.position[0] +=10 
        if self.direction == "Izquierda":
            self.position[0] -=10
        if self.direction == "Arriba":
            self.position[1] -=10
        if self.direction == "Abajo":
            self.position[1] +=10
        self.body.insert(0,list(self.position)) 
        if self.position == foodPos: 
            return 1 #True
        else:
            self.body.pop()
            return 0 #False
    def checkCollision(self):
        x=self.position[0]
        y=self.position[1]
        if x>490 or x<0:
            return 1
        elif y>490 or y<0:
            return 1
        #for bodyPart in self.body[1:]:
            #if self.position == bodyPart:
             #   return 1
        return 0
    def getHeadPos(self):
        return self.position
    def getBody(self):
        return self.body

class FoodSpawer():
    def __init__(self):
        self.position =[random.randrange(1,50)*10,
                        random.randrange(1,50)*10]
        self.isFoodOnScreen = True

    def spawnFood(self):
        if self.isFoodOnScreen == False:
            self.position =[random.randrange(1,50)*10,
                        random.randrange(1,50)*10]
            self.isFoodOnScreen = True
        return self.position

    def setFoodOnScreen(self,b):
        self.isFoodOnScreen = b
class Mapa:
    mapa = []
    
    def __init__(self):
        for i in range(50):
            self.fil=[]
            for j in range(50):
                self.fil.append(0)
            self.mapa.append(self.fil)
    def getMapa(self):
        return self.mapa
    def gameOver(self,score,score2):
        result=""
        if (score==score2):
            result="EMPATE!"
        if (score>score2):
            result="GANADOR: IA || LA IA DOMINARA EL MUNDO!"
        if (score<score2):
            result="GANADOR: HUMANO"

        pygame.display.set_caption(result)

        Fin=True
        while Fin:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    Fin=False
        pygame.quit()
        sys.exit()
def main():
    #Mapa (Matriz)
    MAPA=Mapa()
    mapa=MAPA.getMapa()
    
    #Mapa (Pygame)
    window = pygame.display.set_mode((500,500))
    pygame.display.set_caption('A* with Snake')
    fps = pygame.time.Clock()

    #Comida
    foodSpawner = FoodSpawer()
    
    #IA
    snake = Snake(100,50)
    score = 0
    inicio = (int(snake.getHeadPos()[0]/10),int(snake.getHeadPos()[1]/10))
    objetivo = (int(foodSpawner.spawnFood()[0]/10),int(foodSpawner.spawnFood()[1]/10))
    
    #Humano
    snake2 = Snake(100,100)
    score2 = 0

    window.fill(pygame.Color(225,225,225))

    while True:
        camino = Astar(mapa, inicio, objetivo) 
        snake_x = snake.getHeadPos()[0] 
        snake_y = snake.getHeadPos()[1]
        #IA
        for (x,y) in camino:
            if x>snake_x:
                snake.changueDirTo('Derecha')
            if x<snake_x:
                snake.changueDirTo('Izquierda')
            if y>snake_y:
                snake.changueDirTo('Abajo')
            if y<snake_y:
                snake.changueDirTo('Arriba')
            snake_x=x
            snake_y=y
        #Humano
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameOver();
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    snake2.changueDirTo('Derecha')
                if event.key == pygame.K_LEFT:
                    snake2.changueDirTo('Izquierda')
                if event.key == pygame.K_UP:
                    snake2.changueDirTo('Arriba')
                if event.key == pygame.K_DOWN:
                    snake2.changueDirTo('Abajo')
        
        foodPos = foodSpawner.spawnFood() # Retorna posicion de comida

        #IA
        if(snake.move(foodPos)==1): # Si hay colision
            score+=1
            foodSpawner.setFoodOnScreen(False)
        #Humano
        if(snake2.move(foodPos)==1): # Si hay colision
            score2+=1
            foodSpawner.setFoodOnScreen(False)
        
        window.fill(pygame.Color(225,225,225))

        for x in range(50):
            for y in range(50):
                if(mapa[x][y]==0):
                    pygame.draw.rect(window,pygame.Color(194, 186, 186),
                                 pygame.Rect(x*10,y*10,10,10),1)# x,y,ancho,alto
                if(mapa[x][y]==1):
                    pygame.draw.rect(window,pygame.Color(0, 0, 0),
                                 pygame.Rect(x*10,y*10,10,10))# x,y,ancho,alto
        #IA
        for pos in snake.getBody():
            pygame.draw.rect(window,pygame.Color(0,225,0),
                             pygame.Rect(pos[0],pos[1],10,10))# x,y,ancho,alto
        #Humano
        for pos in snake2.getBody():
            pygame.draw.rect(window,pygame.Color(0,0,225),
                             pygame.Rect(pos[0],pos[1],10,10))# x,y,ancho,alto
        

        #Dibujar Comida
        pygame.draw.rect(window,pygame.Color(225,0,0),
                             pygame.Rect(foodPos[0],foodPos[1],10,10))
        #IA
        if (snake.checkCollision()==1):
            MAPA.gameOver(score,score2)
        #Humano
        if (snake2.checkCollision()==1):
            MAPA.gameOver(score,score2)

        #Puntaje
        pygame.display.set_caption("IA | Score :" + str(score) + " Humano | Score :" +str(score2))
        pygame.display.flip()
        fps.tick(24)

        #Nodo
        inicio = (int(snake.getHeadPos()[0]/10),int(snake.getHeadPos()[1]/10))
        objetivo = (int(foodPos[0]/10),int(foodPos[1]/10))
      
if __name__ == '__main__':
    main()
