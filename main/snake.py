import pygame, random, webbrowser, sys, time

# Pygame initialization and initial configurations
pygame.init()

# Name of the game
pygame.display.set_caption('SMOKING SNAKE GAME 🐍')

# Screen size settings
width, height = 1000, 600
screen = pygame.display.set_mode((width, height))

# Game clock settings
clock = pygame.time.Clock()

# Definition of colors used
red = (255, 0, 0)
green = (0, 255, 0)
white = (255, 255, 255)
purple = (128, 0, 128)

# Setting the square (pixel) size of the game
square_size = 20

# Setting game speed
game_speed = 10

# Loading background music and setting it as loop
pygame.mixer.music.load('back1.mp3')
pygame.mixer.music.play(-1)
# Carrying the sound of eating the fruit
eat_sound = pygame.mixer.Sound('eat.wav') 

# Setting and configuring the background image
background = pygame.image.load("background.png")
background = pygame.transform.scale(background, (width, height))

background.set_alpha(128)

# Defining the function that will randomly generate the fruit in the game
def generate_fruit():
    fruit_x = round(random.randrange(0, width - square_size) / 20.0) * 20.0
    fruit_y = round(random.randrange(0, height - square_size) / 20.0) * 20.0
    return fruit_x, fruit_y

# Loading apple image
apple_image = pygame.image.load('apple.png')

# Defining the function that draws the fruit
def draw_fruit(size, fruit_x, fruit_y):
    # Drawing the image of the apple in the position of the fruit
    screen.blit(pygame.transform.scale(apple_image, (size + 8, size + 8)), (fruit_x, fruit_y))

# Defining the function that draws the snake
def draw_snake(size, pixels, color, eyes_color):
    for i, pixel in enumerate(pixels):
        pygame.draw.rect(screen, color, [pixel[0], pixel[1], size, size])
        if i == len(pixels) - 1:
            # Drawing eyes on the snake's head
            eye_size = size // 2
            pupil_size = eye_size // 2
            left_eye_pos = (pixel[0] + size // 4 - eye_size // 2, pixel[1] + size // 4 - eye_size // 2)
            right_eye_pos = (pixel[0] + 3 * size // 4 - eye_size // 2, pixel[1] + size // 4 - eye_size // 2)
            
            # Drawing the whites of the eyes
            pygame.draw.ellipse(screen, white, [left_eye_pos[0], left_eye_pos[1], eye_size, eye_size])
            pygame.draw.ellipse(screen, white, [right_eye_pos[0], right_eye_pos[1], eye_size, eye_size])
            
            # Drawing the pupils
            pygame.draw.ellipse(screen, eyes_color, [left_eye_pos[0] + pupil_size // 2, left_eye_pos[1] + pupil_size // 2, pupil_size, pupil_size])
            pygame.draw.ellipse(screen, eyes_color, [right_eye_pos[0] + pupil_size // 2, right_eye_pos[1] + pupil_size // 2, pupil_size, pupil_size])

            # Drawing the white stick in the snake's mouth
            tongue_length = size // 2
            tongue_width = size // 10
            tongue_pos = (pixel[0] + size // 2 - tongue_width // 2, pixel[1] - tongue_length)
            pygame.draw.rect(screen, white, [tongue_pos[0], tongue_pos[1], tongue_width, tongue_length])

# Defining the function that shows the score
def show_score(score):
    font = pygame.font.SysFont('Arial', 25)
    text = font.render(f'Score: {score}', False, white)
    screen.blit(text, [1, 1])

# Defining the function that shows the game over message
def game_over():
    game_over_font = pygame.font.SysFont('Arial', 50)
    game_over_text = game_over_font.render('GAME OVER', False, white)
    screen.blit(game_over_text, (width // 2 - 150, height // 2 - 30))

    continue_font = pygame.font.SysFont('Arial', 20)
    continue_text = continue_font.render('Press ENTER to continue', False, white)

    # Getting text dimensions
    continue_text_rect = continue_text.get_rect()

    # Centering text on the screen
    continue_text_rect.center = (width // 2, height // 2 + 25)
    screen.blit(continue_text, continue_text_rect)

    # Updating the screen
    pygame.display.update()

    waiting_input = True
    # Creating the function loop that ends the game
    while waiting_input:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting_input = False
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

# Defining the function gives the final reward. Here it is by default, upon reaching 50 points the player ends the game. You can change this amount of points in the condition of line 254 of the code when the final_reward function is called
def final_reward():
    webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    pygame.quit()
    sys.exit()

# Defining the function that creates the movement of the game's snake
def select_speed(key, velocity_x, velocity_y):
    if key == pygame.K_DOWN and not (velocity_x == 0 and velocity_y == -square_size):
        velocity_x = 0
        velocity_y = square_size
    elif key == pygame.K_UP and not (velocity_x == 0 and velocity_y == square_size):
        velocity_x = 0
        velocity_y = -square_size
    elif key == pygame.K_RIGHT and not (velocity_x == -square_size and velocity_y == 0):
        velocity_x = square_size
        velocity_y = 0
    elif key == pygame.K_LEFT and not (velocity_x == square_size and velocity_y == 0):
        velocity_x = -square_size
        velocity_y = 0

    return velocity_x, velocity_y

# Defining the function that runs the game
def run_game():
    while True:
        # Starting the song
        pygame.mixer.music.unpause()
        
        # Defining element position and size variables
        end_game = False

        x = width / 2
        y = height / 2

        velocity_x = 0
        velocity_y = 0

        snake_size = 1
        pixels = []

        fruit_x, fruit_y = generate_fruit()

        # Initializing Purple Snake
        purple_snake_size = 1
        purple_pixels = []
        purple_x = round(random.randrange(0, width - square_size) / 20.0) * 20.0
        purple_y = round(random.randrange(0, height - square_size) / 20.0) * 20.0
        purple_velocity_x = 0
        purple_velocity_y = 0

        # Creating the main game loop
        while not end_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    velocity_x, velocity_y = select_speed(event.key, velocity_x, velocity_y)

            screen.blit(background, (0, 0))

            # Drawing the fruit on the screen
            draw_fruit(square_size, fruit_x, fruit_y)

            # Checking collision with the fruit
            head_position = [x, y]
            if head_position[0] == fruit_x and head_position[1] == fruit_y:
                snake_size += 1
                fruit_x, fruit_y = generate_fruit()
                eat_sound.play() 

            # Checking for collision with the purple snake
            if head_position[0] == purple_x and head_position[1] == purple_y:
                end_game = True

            # Checking if the purple snake ate the fruit
            purple_head_position = [purple_x, purple_y]
            if purple_head_position[0] == fruit_x and purple_head_position[1] == fruit_y:
                purple_snake_size += 1
                purple_snake_size += 1
                fruit_x, fruit_y = generate_fruit()
                eat_sound.play() 

            # Updating the snake's position
            x += velocity_x
            y += velocity_y

            # Checking if the snake has left the screen
            if x >= width or x < 0 or y >= height or y < 0:
                end_game = True

            # Updating the snake's pixel list
            pixels.append([x, y])
            if len(pixels) > snake_size:
                del pixels[0]

            # Checking if the snake collided with itself
            for pixel in pixels[:-1]:
                if pixel == [x, y]:
                    end_game = True

            # Drawing the snake on the canvas
            draw_snake(square_size, pixels, green, (0, 0, 0))

             # Upgrading the purple snake's speed to move towards the fruit
            if purple_x < fruit_x:
                purple_velocity_x = square_size
                purple_velocity_y = 0
            elif purple_x > fruit_x:
                purple_velocity_x = -square_size
                purple_velocity_y = 0
            elif purple_y < fruit_y:
                purple_velocity_x = 0
                purple_velocity_y = square_size
            elif purple_y > fruit_y:
                purple_velocity_x = 0
                purple_velocity_y = -square_size

            # Updating the purple snake's position every two iterations
            if pygame.time.get_ticks() % 2 == 0:
                purple_x += purple_velocity_x
                purple_y += purple_velocity_y

            # Updating purple snake pixel list
            purple_pixels.append([purple_x, purple_y])
            if len(purple_pixels) > purple_snake_size:
                del purple_pixels[0]

            # Drawing the purple snake on the canvas
            draw_snake(square_size, purple_pixels, purple, red)

            # Showing the score on the screen
            show_score(snake_size - 1)

            # Updating the screen
            pygame.display.update()

            if snake_size == 51:
                final_reward()
                end_game = True

            # Setting game speed
            clock.tick(game_speed)

            # Checking if the game is over
            if end_game:
                # Showing game over message
                game_over()

                # Restarting the game
                run_game()

# Running the game
run_game()