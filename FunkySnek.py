import random
import pygame

# list of colors
red = (255, 0, 0)
green = (0, 255, 0)
black = (0, 0, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)

class Point:
    def __init__(self, x=0, y=0, color=(0,0,0)):
        self.x = x
        self.y = y
        self.color = color
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

class Control:
    def __init__(self):
        self.movingLeft = self.movingDown = self.movingUp = self.movingRight = False
    def stop(self):
        self.movingLeft = self.movingDown = self.movingUp = self.movingRight = False
    def turnRight(self):
        self.stop()
        self.movingRight = True
    def turnLeft(self):
        self.stop()
        self.movingLeft = True
    def turnUp(self):
        self.stop()
        self.movingUp = True
    def turnDown(self):
        self.stop()
        self.movingDown = True        

class Game:
    def __init__(self, width=0, height=0, numX=0, numY=0):
        self.control = Control()
        self.snake = [Point(0, 0, green)]
        self.food = [Point(1, 1, red)]
        self.swidth = width//numX
        self.sheight = height//numY
        self.numX = numX
        self.numY = numY

    def generateFood(self):
        if len(self.food) == 0:
            y = random.randint(0, (self.numY-1))
            x = random.randint(0, (self.numX-1))
            r = random.randint(1,100)
            # 30% chance for three types of food
            if r <= 33:
                self.food.append(Point(x, y, red))
            elif r > 66:
               self.food.append(Point(x, y, yellow))  
            else:
                self.food.append(Point(x, y, blue)) 

    def getHead(self):
        return self.snake[len(self.snake) - 1]

    def checkFoodEaten(self):
        check = False;
        if len(self.food) == 0:
           self.generateFood() 
        if len(self.food) > 0:
            if self.food[0] == self.getHead(): #food is eaten

                # if blue food is "eaten" the snake teleports to and moves away from what was the tail
                if self.food[0].color == blue:
                    tail = self.snake[0] 
                    test = self.snake[1]
                    if test.y<tail.y:
                        self.control.turnDown()
                    if test.y>tail.y:
                        self.control.turnUp()
                    if test.x<tail.x:
                        self.control.turnRight()
                    if test.x>tail.x:
                        self.control.turnLeft()
                    self.snake.append(Point(tail.x, tail.y, green))
                    self.snake.pop(0)

                # if yellow food is "eaten" the snake becomes temporarily immortal from self collisions
                if self.food[0].color == yellow:
                    self.getHead().color = yellow

                self.food.pop(0)
                check = True

        return check

    def grow(self, x=0, y=0):
        self.snake.append(Point(x, y, green)) # grows in direction of new point
        if not self.checkFoodEaten():
            self.snake.pop(0) # removes the tail point if not eating

    def checkForYellow(self):
        check = False;
        for s in self.snake:
            if(s.color == yellow):
                check = True
        return check

    def checkSelfCollision(self):
        check = False;
        if not self.checkForYellow(): # immortal temporarily if yellow is eaten
            for s in self.snake:
                count = 0
                for c in self.snake:
                    if c == s:
                        count += 1
                if count > 1:
                    check = True
        return check

    def checkOutOfBounds(self, x=0, y=0):
        return y < 0 or x < 0 or y >= self.numY or x >= self.numX

    def checkDeadOrMoving(self):
        check = False
        head = self.getHead()
        x = 0
        y = 0
        if self.control.movingDown:
            y = head.y + 1
            x = head.x
        if self.control.movingUp:
            y = head.y - 1
            x = head.x
        if self.control.movingRight:
            y = head.y
            x = head.x + 1
        if self.control.movingLeft:
            y = head.y
            x = head.x - 1
        if self.checkOutOfBounds(x, y) or self.checkSelfCollision():
            check = True
        self.grow(x, y)
        return check

class gui:
    def __init__(self):
        pygame.init()
        width = 600
        height = 600
        game = Game(width, height, 20, 20)
        win = pygame.display.set_mode((width, height))
        running = True
        clock = pygame.time.Clock()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        game.control.turnLeft()
                    if event.key == pygame.K_RIGHT:
                        game.control.turnRight()
                    if event.key == pygame.K_UP:
                        game.control.turnUp()
                    if event.key == pygame.K_DOWN:
                        game.control.turnDown()
            win.fill(black)
            for p in game.snake:
                pygame.draw.rect(win, p.color, (p.x * game.swidth, p.y * game.swidth, game.swidth, game.sheight))
            for p in game.food:
                pygame.draw.rect(win, p.color, (p.x * game.swidth, p.y * game.swidth, game.swidth, game.sheight))
            if game.checkDeadOrMoving():
                running = False
            pygame.display.update()
            time = clock.tick(4)
        pygame.quit()


if __name__ == '__main__':
    run = gui()