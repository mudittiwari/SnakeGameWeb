import pygame
import random
import asyncio
import sys

pygame.init()
pygame.mixer.init()

gamewindow = pygame.display.set_mode((500, 500))
pygame.display.set_caption("snakegame")

# Load images
bgimg = pygame.image.load("bgimg.jpg")
bgimg = pygame.transform.scale(bgimg, (500, 500)).convert_alpha()
gameover = pygame.image.load("gameover.jpg")
gameover = pygame.transform.scale(gameover, (500, 500)).convert_alpha()
gameplay = pygame.image.load("gameplay.png")
gameplay = pygame.transform.scale(gameplay, (500, 500)).convert_alpha()

async def main():
    # Display the start screen
    gamewindow.blit(bgimg, (0, 0))
    pygame.display.update()
    
    # Start screen loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    await game()  # Start the game
                    return
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Start game when the screen is tapped
                await game()
                return

        await asyncio.sleep(0)

async def game():
    with open("highscore.txt", "r") as f:
        highscore = int(f.read())

    sizex_snake = 10
    sizey_snake = 10
    posix_snake = 40
    posiy_snake = 40
    posix_food = random.randint(30, 250)
    posiy_food = random.randint(30, 250)
    food_size = 10
    velocity_x = 0
    velocity_y = 0
    score = 0
    snake_length = 1
    snake_list = []
    togivescore = "score:0"
    font = pygame.font.SysFont(None, 50)
    quit_game = False
    exit_game = False
    red = (255, 0, 0)
    blue = (250, 0, 255)
    silver = (192, 192, 192)
    clock = pygame.time.Clock()

    def drawsnake(gamewindow, color, snake_list, size):
        for posix_snake, posiy_snake in snake_list:
            pygame.draw.rect(gamewindow, color, [posix_snake, posiy_snake, size, size])

    def score_changer(text, color, x, y):
        showtext = font.render(text, True, color)
        gamewindow.blit(showtext, [x, y])

    # Game loop
    while not exit_game:
        if quit_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        await main()  # Restart game
                        return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    await main()
                    return

            gamewindow.blit(gameover, (0, 0))
            score_changer(f"score:{score}", silver, 180, 400)
            score_changer(f"highscore:{highscore}", silver, 140, 450)
            score_changer(f"Press enter or tap to play again", silver, 50, 50)
            pygame.display.update()

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    # Control snake based on tap/click position
                    center_x, center_y = 250, 250
                    if x > center_x and abs(x - posix_snake) > abs(y - posiy_snake):
                        velocity_x = 4
                        velocity_y = 0
                    elif x < center_x and abs(x - posix_snake) > abs(y - posiy_snake):
                        velocity_x = -4
                        velocity_y = 0
                    elif y > center_y:
                        velocity_x = 0
                        velocity_y = 4
                    elif y < center_y:
                        velocity_x = 0
                        velocity_y = -4

            posix_snake = posix_snake + velocity_x
            posiy_snake = posiy_snake + velocity_y

            if abs(posix_snake - posix_food) < 10 and abs(posiy_snake - posiy_food) < 10:
                pygame.mixer.music.load('beep.ogg')
                pygame.mixer.music.play()
                score += 10
                snake_length += 3
                togivescore = f"score:{score}"
                posix_food = random.randint(30, 250)
                posiy_food = random.randint(30, 250)

            gamewindow.blit(gameplay, (0, 0))
            score_changer(togivescore, red, 10, 0)
            if score > highscore:
                highscore = score

            highscore_to_show = f"highscore:{highscore}"
            score_changer(highscore_to_show, red, 250, 0)

            temp = [posix_snake, posiy_snake]
            snake_list.append(temp)

            if len(snake_list) > snake_length:
                del snake_list[0]

            if posix_snake <= 0 or posix_snake >= 500 or posiy_snake <= 0 or posiy_snake >= 500:
                pygame.mixer.music.load('collison.ogg')
                pygame.mixer.music.play()
                quit_game = True

            if temp in snake_list[:-1]:
                pygame.mixer.music.load('collison.mp3')
                pygame.mixer.music.play()
                quit_game = True

            drawsnake(gamewindow, blue, snake_list, sizex_snake)
            pygame.draw.rect(gamewindow, red, [posix_food, posiy_food, food_size, food_size])
            pygame.display.update()
            clock.tick(30)

        await asyncio.sleep(0)

    with open("highscore.txt", "w") as f:
        f.write(f"{highscore}")
    pygame.quit()

asyncio.run(main())
