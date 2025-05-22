import tkinter as tk
import random

# Game constants
WIDTH = 700
HEIGHT = 700
SPEED = 100
SPACE_SIZE = 20
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"

class Snake:
    def __init__(self, canvas):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        # Create initial snake body
        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        # Create graphical representation of snake
        for x, y in self.coordinates:
            square = canvas.create_rectangle(
                x, y, x + SPACE_SIZE, y + SPACE_SIZE, 
                fill=SNAKE_COLOR, tag="snake"
            )
            self.squares.append(square)

class Food:
    def __init__(self, canvas):
        # Generate random position for food
        x = random.randint(0, (WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE
        
        self.coordinates = [x, y]
        
        # Create graphical representation of food
        canvas.create_oval(
            x, y, x + SPACE_SIZE, y + SPACE_SIZE,
            fill=FOOD_COLOR, tag="food"
        )

def next_turn(snake, food, canvas, score_label, window):
    # Get current head position
    x, y = snake.coordinates[0]

    # Update position based on direction
    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    # Update snake coordinates with new head position
    snake.coordinates.insert(0, [x, y])
    
    # Create new square for snake head
    square = canvas.create_rectangle(
        x, y, x + SPACE_SIZE, y + SPACE_SIZE,
        fill=SNAKE_COLOR
    )
    snake.squares.insert(0, square)

    # Check if food was eaten
    if x == food.coordinates[0] and y == food.coordinates[1]:
        # Update score
        global score
        score += 1
        score_label.config(text=f"Score: {score}")
        
        # Delete current food
        canvas.delete("food")
        
        # Create new food
        food = Food(canvas)
    else:
        # Remove last segment of snake
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    # Check for collisions
    if check_collisions(snake, canvas):
        game_over(canvas, window)
    else:
        # Schedule next turn
        window.after(SPEED, next_turn, snake, food, canvas, score_label, window)

def change_direction(new_direction):
    global direction

    # Prevent 180-degree turns
    if new_direction == 'left' and direction != 'right':
        direction = new_direction
    elif new_direction == 'right' and direction != 'left':
        direction = new_direction
    elif new_direction == 'up' and direction != 'down':
        direction = new_direction
    elif new_direction == 'down' and direction != 'up':
        direction = new_direction

def check_collisions(snake, canvas):
    x, y = snake.coordinates[0]

    # Check for wall collisions
    if x < 0 or x >= WIDTH:
        return True
    elif y < 0 or y >= HEIGHT:
        return True

    # Check for self collisions
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False

def game_over(canvas, window):
    canvas.create_text(
        WIDTH/2, HEIGHT/2,
        font=('consolas', 70),
        text="GAME OVER",
        fill="red",
        tag="gameover"
    )
    
    # Add restart button
    restart_button = tk.Button(
        window, 
        text="Restart", 
        font=('consolas', 20),
        command=lambda: restart_game(canvas, window, restart_button)
    )
    restart_button.place(x=WIDTH/2-50, y=HEIGHT/2+50)

def restart_game(canvas, window, restart_button):
    # Clear canvas
    canvas.delete("all")
    restart_button.destroy()
    
    # Reset score
    global score
    score = 0
    
    # Reset direction
    global direction
    direction = 'down'
    
    # Update score display
    score_label = tk.Label(
        window, 
        text=f"Score: {score}", 
        font=('consolas', 40),
        bg=BACKGROUND_COLOR,
        fg="white"
    )
    score_label.pack()
    
    # Create new game objects
    canvas = tk.Canvas(
        window, 
        bg=BACKGROUND_COLOR,
        height=HEIGHT, 
        width=WIDTH
    )
    canvas.pack()
    
    # Start new game
    snake = Snake(canvas)
    food = Food(canvas)
    
    window.after(SPEED, next_turn, snake, food, canvas, score_label, window)

# Initialize game
def start_game():
    window = tk.Tk()
    window.title("Snake Game")
    window.resizable(False, False)
    
    # Initialize score
    global score
    score = 0
    
    # Initialize direction
    global direction
    direction = 'down'
    
    # Create score display
    score_label = tk.Label(
        window, 
        text=f"Score: {score}", 
        font=('consolas', 40),
        bg=BACKGROUND_COLOR,
        fg="white"
    )
    score_label.pack()
    
    # Create game canvas
    canvas = tk.Canvas(
        window, 
        bg=BACKGROUND_COLOR,
        height=HEIGHT, 
        width=WIDTH
    )
    canvas.pack()
    
    # Bind keyboard controls
    window.bind('<Left>', lambda event: change_direction('left'))
    window.bind('<Right>', lambda event: change_direction('right'))
    window.bind('<Up>', lambda event: change_direction('up'))
    window.bind('<Down>', lambda event: change_direction('down'))
    
    # Create game objects
    snake = Snake(canvas)
    food = Food(canvas)
    
    # Start game loop
    window.after(SPEED, next_turn, snake, food, canvas, score_label, window)
    
    # Start main loop
    window.mainloop()

if __name__ == "__main__":
    try:
        print("Starting Snake Game with Tkinter...")
        start_game()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        print("Game closed")