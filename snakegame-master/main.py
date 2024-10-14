import pygame
import random
import asyncio
import sys

pygame.init()
pygame.mixer.init()

gameWindow = pygame.display.set_mode((500, 500))
pygame.display.set_caption("snakegame")


bgImg = pygame.image.load("bgimg.jpeg")
bgImg = pygame.transform.scale(bgImg, (500, 500)).convert_alpha()
gameOver = pygame.image.load("gameover.jpg")
gameOver = pygame.transform.scale(gameOver, (500, 500)).convert_alpha()
gamePlay = pygame.image.load("gameplay.png")
gamePlay = pygame.transform.scale(gamePlay, (500, 500)).convert_alpha()
mouseTapped = 0

async def main():
    global mouseTapped
    gameWindow.blit(bgImg, (0, 0))
    pygame.display.update()
    
    gameStarted = False
    
    while not gameStarted:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseTapped += 1
                if mouseTapped >= 2:
                    gameStarted = True

        await asyncio.sleep(0)  
    await game()

async def game():
    with open("highscore.txt", "r") as f:
        highScore = int(f.read())

    sizeXSnake = 10
    posXSnake = 40
    posYSnake = 40
    posXFood = random.randint(30, 250)
    posYFood = random.randint(30, 250)
    foodSize = 10
    velocityX = 0
    velocityY = 0
    lastDirection = None
    score = 0
    snakeLength = 1
    snakeList = []
    toGiveScore = "score: 0"
    fontLarge = pygame.font.SysFont(None, 50)
    fontSmall = pygame.font.SysFont(None, 20)
    quitGame = False
    exitGame = False
    red = (255, 0, 0)
    blue = (250, 0, 255)
    silver = (192, 192, 192)
    clock = pygame.time.Clock()

    def drawSnake(gameWindow, color, snakeList, size):
        for posXSnake, posYSnake in snakeList:
            pygame.draw.circle(gameWindow, color, [posXSnake, posYSnake], size)

    def scoreChanger(font, text, color, x, y):
        showText = font.render(text, True, color)
        gameWindow.blit(showText, [x, y])

    # Game loop
    while not exitGame:
        if quitGame:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exitGame = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        await main()
                        return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    await main()
                    return

            gameWindow.blit(gameOver, (0, 0))
            scoreChanger(fontLarge, f"score:{score}", silver, 180, 400)
            scoreChanger(fontLarge, f"highscore:{highScore}", silver, 140, 450)
            scoreChanger(fontLarge, f"Tap to play again", silver, 110, 50)
            with open("highscore.txt", "w") as f:
                f.write(f"{highScore}")
            pygame.display.update()

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exitGame = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    centerX, centerY = 250, 250
                    
                    if x > centerX and abs(x - posXSnake) > abs(y - posYSnake):
                        if lastDirection != "left":
                            velocityX = 4
                            velocityY = 0
                            lastDirection = "right"
                    elif x < centerX and abs(x - posXSnake) > abs(y - posYSnake):
                        if lastDirection != "right":
                            velocityX = -4
                            velocityY = 0
                            lastDirection = "left"
                    elif y > centerY:
                        if lastDirection != "up":
                            velocityX = 0
                            velocityY = 4
                            lastDirection = "down"
                    elif y < centerY:
                        if lastDirection != "down":
                            velocityX = 0
                            velocityY = -4
                            lastDirection = "up"

            posXSnake = posXSnake + velocityX
            posYSnake = posYSnake + velocityY

            if abs(posXSnake - posXFood) < 20 and abs(posYSnake - posYFood) < 20:
                pygame.mixer.music.load('beep.ogg')
                pygame.mixer.music.play()
                score += 10
                snakeLength += 3
                toGiveScore = f"score: {score}"
                posXFood = random.randint(30, 250)
                posYFood = random.randint(30, 250)

            gameWindow.blit(gamePlay, (0, 0))
            scoreChanger(fontSmall, toGiveScore, red, 10, 10)
            if score > highScore:
                highScore = score

            highScoreToShow = f"highscore: {highScore}"
            scoreChanger(fontSmall, highScoreToShow, red, 400, 10)

            temp = [posXSnake, posYSnake]
            snakeList.append(temp)

            if len(snakeList) > snakeLength:
                del snakeList[0]

            if posXSnake <= 0 or posXSnake >= 500 or posYSnake <= 0 or posYSnake >= 500:
                pygame.mixer.music.load('collison.ogg')
                pygame.mixer.music.play()
                quitGame = True

            if temp in snakeList[:-1]:
                pygame.mixer.music.load('collison.ogg')
                pygame.mixer.music.play()
                quitGame = True

            drawSnake(gameWindow, blue, snakeList, sizeXSnake)
            pygame.draw.circle(gameWindow, red, [posXFood, posYFood], foodSize)
            pygame.display.update()
            clock.tick(30)

        await asyncio.sleep(0)

    pygame.quit()

asyncio.run(main())
