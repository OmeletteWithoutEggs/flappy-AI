import raylibpy as raylib
import random
import neuralNetworks
import concurrent.futures
import sys
 
class Pipe():
    def __init__(self,height,size):
        self.height = height
        self.size = size
        self.topRect = raylib.Rectangle(WIDTH,0,100,self.height-self.size/2)
        self.bottomRect = raylib.Rectangle(WIDTH-1,self.height+(self.size/2),100,HEIGHT)
    
    def update(self):
        self.topRect.x -= scrollSpeed
        self.bottomRect.x -= scrollSpeed
        
         

    def draw(self):
        raylib.draw_rectangle_rec(self.topRect,(1, 121, 110,255))
        raylib.draw_rectangle_rec(self.bottomRect,(1, 121, 110,255))


class Bird():
    def __init__(self,y,velY):
        self.x = 200
        self.y = y
        self.velY = velY
        self.size = 40
        self.brain = neuralNetworks.nNetwork((5,9,4,1))
        self.score = 0
        self.colour = [random.randint(0,255) for _ in range(3)] + [150]


    def jump(self):
        self.velY = jumpPower
    def update(self):
        self.velY += gravity
        self.y += self.velY
        if self.velY > maxSpeed:
            self.velY = maxSpeed
        inputs = [
            self.y / HEIGHT,
            self.velY / maxSpeed,
            pipes[0].topRect.x / WIDTH,
            pipes[0].topRect.height / HEIGHT,
            pipes[0].bottomRect.y / HEIGHT
        ]
        if self.brain.feedForward(inputs) > 0.5:
            if self.velY >= 0:
                self.jump()
        
        self.hitbox:raylib.Rectangle = raylib.Rectangle(self.x-20,self.y-20,40,40)

        self.score += 1#/(((pipes[0].height-self.y)**2)+0.00001)
        
    def draw(self):
        raylib.draw_circle(self.x,self.y,self.size//2,self.colour)


def render():
    raylib.begin_drawing()
    raylib.clear_background((0,0,0,255))

    for bird in birds:
        bird.draw()

    for pipe in pipes:
        pipe.draw()

    raylib.draw_text("bird population: " + str(len(birds)),10,10,18,(255,255,255,255))
    raylib.draw_text("top score: " +str(topTopScore),10,30,18,(255,255,255,255))
    raylib.draw_text("current score: "+str(topScore),10,50,18,(255,255,255,255))
    raylib.draw_text("frame count: "+str(frameCount),10,70,18,(255,255,255,255))
    raylib.draw_text("generation: "+str(generation),10,90,18,(255,255,255,255))
    raylib.end_drawing()

def updateChunk(chunk):
    for bird in chunk:
        bird.update()


WIDTH, HEIGHT = 1900, 1000
raylib.set_config_flags(raylib.FLAG_MSAA_4X_HINT)
raylib.init_window(WIDTH,HEIGHT,"flappy bird AI")
try:
    print(sys._is_gil_enabled())
except:
    print("gil is enabled")

frameCount = 0

executor = concurrent.futures.ThreadPoolExecutor(max_workers=16)

pipes :list[Pipe]= []
birds :list[Bird]= []
numBirds = 500

for _ in range(numBirds):
    birds.append(Bird(500,0))

scrollSpeed = 2
gravity = 0.3
maxSpeed = 8
jumpPower = -10
random.seed(1000)

generation = 0
topScore = 0
topTopScore = 0
lastScore = 0
while not raylib.window_should_close():
    
    if frameCount % 300 == 0:
        #pipes.append(Pipe(random.randint(400,600),random.randint(200,350)))
        pipes.append(Pipe(random.randint(200,800),max(300-topScore,250)))

    removes = []
    for pipe in pipes:
        if pipe.topRect.x+pipe.topRect.width < birds[0].x-birds[0].size//2:
            removes.append(pipe)
        else:
            pipe.update()

    for pipe in removes:
        pipes.remove(pipe)
        topScore += 1

    chunks = [birds[i::8] for i in range(8)]
    list(executor.map(updateChunk, chunks))

    for bird in birds[:]:
        if pipes:
            if raylib.check_collision_recs(bird.hitbox,pipes[0].topRect) or raylib.check_collision_recs(bird.hitbox,pipes[0].bottomRect):
                if lastScore < bird.score:
                    lastBird = bird
                    lastScore = bird.score
                birds.remove(bird)
        
            elif  bird.y < bird.size//2 or bird.y > HEIGHT-bird.size//2:
                if lastScore < bird.score:
                    lastBird = bird
                    lastScore = bird.score
                birds.remove(bird)


    if topScore > topTopScore:
        topTopScore = topScore

    render()
    
    frameCount += 1

    if len(birds) == 0:
        generation += 1
        print(topScore)
        pipes.clear()
        frameCount = 0
        #pipes.append(Pipe(random.randint(200,800),random.randint(200,300)))
        birds.clear()
        brains = lastBird.brain.evolve(numBirds,6000/max(lastScore**1.43,0.001))
        topScore = 0
        for i in range(numBirds):

            birds.append(Bird(500,0))
            
            birds[i].brain = brains[i]
        random.seed(1000)

                
