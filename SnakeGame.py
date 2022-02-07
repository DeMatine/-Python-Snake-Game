import os
import time;
import keyboard;
import random;

class Vector2:
    def __init__(self, x, y, b = ""):
        self.x = x;
        self.y = y;
        self.b = "o";
        self.x_l = 0;
        self.y_l = 0;

isRunning = True;
gameEnd = False;
render = False;

width = 25;
height = 18;

image = [];
image = [0 for i in range(width * height)];

startPos = Vector2(5,5);
snake = [Vector2(0,0)];
snake_index = int(0);

direction = "right";
bounds = "+"
snake_head = "0";
snake_body = "o";
background = " ";

food = "*";
foodValue = 0;
foodPos = Vector2(0,0);

def Start():
    global background;
    global foodPos;
    global endGame;

    endGame = False;
    
    for i in range(width*height):
        image[i] = background;
    snake[0] = startPos;
    startFood = Vector2(random.randint(0, width-1), random.randint(0, height-1));

    while(startFood ==  startPos):
        startFood = Vector2(random.randint(0, width-1), random.randint(0, height-1));
        
    if startPos != startFood:
        foodPos = startFood;
        image[startFood.x + startFood.y * width] = food;
Start();

def Render():
    global gameEnd;
    global foodPos;
    print(bounds * (width+4));
    print("Snake Game: ");   
    print(bounds * (width+4));
    xx = "";
    yy = 0;
    if gameEnd == False:
        for y in range(height):
            for x in range(width):        
                xx += image[x + y * width];
                if(x == width-1):
                  print(bounds+" "+xx+" "+bounds);
                  xx = "";
    else:
        print("End Game!");
    image[foodPos.x + foodPos.y * width] = food;
    print(bounds * (width+4));

def changeDir(dir):
    global direction;
    
    if((dir == "up" and direction is "down") == False
       and (dir == "down" and direction is "up") == False
       and (dir == "left" and direction is "right") == False
       and (dir == "right" and direction is "left") == False):
        direction = dir;

def clamp(obj, min, max):
    if obj <= min:
        obj = min;
    if obj >= max:
        obj = max;
    return obj;
def genFood():
    global foodPos;
    randX = random.randint(0, width-1);
    randY = random.randint(0, height-1);
    foodPos = Vector2(randX, randY);

def snakeMove(moveDir):
    global background;
    global snake_index;
    global snake;
    global foodValue;
    global foodPos;
    global image;

    lastPos = Vector2(snake[0].x, snake[0].y);

    snk = snake[snake_index];
    
    image[snk.x + snk.y * width] = background;

    if snake_index == 0:
        snake[0].x_l = snake[0].x;
        snake[0].y_l = snake[0].y;
        
        if snake[snake_index].x <= width-1:
            snake[snake_index].x += moveDir.x;
            snake[snake_index].x = clamp(snake[snake_index].x, 0, width-1);
                
        if snake[snake_index].y <= height-1:
            snake[snake_index].y += moveDir.y;
            snake[snake_index].y = clamp(snake[snake_index].y, 0, height-1);
    else:
        snake[snake_index].x_l = snake[snake_index].x;
        snake[snake_index].y_l = snake[snake_index].y;
        snake[snake_index].x = snake[snake_index-1].x_l;
        snake[snake_index].y = snake[snake_index-1].y_l;
       

    image[snk.x + snk.y * width] = snake[snake_index].b;
    
    if snake_index < len(snake)-1:
        snake_index += 1;
    elif snake_index == len(snake)-1:
        snake_index = 0;

    if(snake[0].x == foodPos.x and snake[0].y == foodPos.y):
        foodValue += 1;
        snake.append(Vector2(lastPos.x, lastPos.y, snake_body));
        genFood();

    for i in range(0, int(len(snake))):
        if i > 0 and snake[0].x == snake[i].x and snake[0].y == snake[i].y:
            endGame();

def endGame():
    global isRunning;
    global gameEnd;
    isRunning = False;
    gameEnd = True;

hsize = 0;

def Game():
    global snake;
    global direction;
    global snake_head;
    global hsize;
    
    mv = Vector2(0,0);

    snake[0].b = snake_head;
    
    if keyboard.is_pressed("up arrow"):
        changeDir("up");
    if keyboard.is_pressed("down arrow"):
        changeDir("down");
    if keyboard.is_pressed("left arrow"):
        changeDir("left");
    if keyboard.is_pressed("right arrow"):
        changeDir("right");
    if keyboard.is_pressed("w"):
           hsize += 1;
           
    if direction == "up":
        snakeMove(Vector2(0,-1));
    if direction == "down":
        snakeMove(Vector2(0,1));
    if direction == "left":
        snakeMove(Vector2(-1,0));
    if direction == "right":
        snakeMove(Vector2(1,0));

def current_milli_time():
    return round(time.time() * 1000)

fps = 0;
lastTimer = current_milli_time();
lastTime = time.time_ns();
nsPerTick = 1000000000/60.0;
delta = 0;

while isRunning is True:
    try:
        now = time.time_ns();
        delta += (now-lastTime)/nsPerTick;
        lastTime = now;
        rnd = False;
        
        while(delta >= 1):
            delta -= 1;
            rnd = True;

        if rnd == True:
            fps += 1;
            print("");
            Game();
            Render();
            print("Food: " + str(foodValue));
        
        if current_milli_time() - lastTimer >= 1000:
            lastTimer += 1000;
            fps = 0;

    except Exception as ext:
        print("Error>>> " + ext);
        os.system("pause");
    

input();
