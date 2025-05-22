document.addEventListener('DOMContentLoaded', () => {
    // Game canvas setup
    const canvas = document.getElementById('gameCanvas');
    const ctx = canvas.getContext('2d');
    
    // Game variables
    const gridSize = 20;
    const tileCount = canvas.width / gridSize;
    let snake = [];
    let food = {};
    let dx = 0;
    let dy = 0;
    let score = 0;
    let highScore = localStorage.getItem('snakeHighScore') || 0;
    let gameSpeed = 150; // milliseconds
    let gameInterval;
    let gameRunning = false;
    
    // DOM elements
    const scoreElement = document.getElementById('score');
    const highScoreElement = document.getElementById('highScore');
    const startBtn = document.getElementById('startBtn');
    const upBtn = document.getElementById('upBtn');
    const downBtn = document.getElementById('downBtn');
    const leftBtn = document.getElementById('leftBtn');
    const rightBtn = document.getElementById('rightBtn');
    
    // Update high score display
    highScoreElement.textContent = highScore;
    
    // Initialize game
    function initGame() {
        // Reset snake
        snake = [
            { x: 10, y: 10 }
        ];
        
        // Reset direction
        dx = 0;
        dy = 0;
        
        // Reset score
        score = 0;
        scoreElement.textContent = score;
        
        // Place food
        placeFood();
        
        // Clear any existing interval
        if (gameInterval) {
            clearInterval(gameInterval);
        }
        
        // Start game loop
        gameRunning = true;
        gameInterval = setInterval(gameLoop, gameSpeed);
        
        // Update button text
        startBtn.textContent = 'Restart Game';
    }
    
    // Place food at random position
    function placeFood() {
        food = {
            x: Math.floor(Math.random() * tileCount),
            y: Math.floor(Math.random() * tileCount)
        };
        
        // Make sure food doesn't appear on snake
        for (let i = 0; i < snake.length; i++) {
            if (food.x === snake[i].x && food.y === snake[i].y) {
                placeFood();
                break;
            }
        }
    }
    
    // Game loop
    function gameLoop() {
        // Move snake
        moveSnake();
        
        // Check collisions
        if (checkCollisions()) {
            gameOver();
            return;
        }
        
        // Check if food eaten
        checkFood();
        
        // Draw everything
        drawGame();
    }
    
    // Move snake
    function moveSnake() {
        // If no direction, don't move
        if (dx === 0 && dy === 0) return;
        
        // Create new head
        const head = { x: snake[0].x + dx, y: snake[0].y + dy };
        
        // Add new head to beginning of snake
        snake.unshift(head);
        
        // Remove tail if no food eaten
        if (head.x !== food.x || head.y !== food.y) {
            snake.pop();
        }
    }
    
    // Check collisions with walls or self
    function checkCollisions() {
        const head = snake[0];
        
        // Wall collisions
        if (head.x < 0 || head.x >= tileCount || head.y < 0 || head.y >= tileCount) {
            return true;
        }
        
        // Self collision (start from 1 to skip head)
        for (let i = 1; i < snake.length; i++) {
            if (head.x === snake[i].x && head.y === snake[i].y) {
                return true;
            }
        }
        
        return false;
    }
    
    // Check if food eaten
    function checkFood() {
        const head = snake[0];
        
        if (head.x === food.x && head.y === food.y) {
            // Increase score
            score++;
            scoreElement.textContent = score;
            
            // Update high score if needed
            if (score > highScore) {
                highScore = score;
                highScoreElement.textContent = highScore;
                localStorage.setItem('snakeHighScore', highScore);
            }
            
            // Place new food
            placeFood();
            
            // Increase speed slightly
            if (gameSpeed > 50 && score % 5 === 0) {
                clearInterval(gameInterval);
                gameSpeed -= 5;
                gameInterval = setInterval(gameLoop, gameSpeed);
            }
        }
    }
    
    // Game over
    function gameOver() {
        gameRunning = false;
        clearInterval(gameInterval);
        
        // Display game over
        ctx.fillStyle = 'rgba(0, 0, 0, 0.75)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        ctx.fillStyle = 'red';
        ctx.font = '30px Arial';
        ctx.textAlign = 'center';
        ctx.fillText('Game Over!', canvas.width / 2, canvas.height / 2 - 15);
        
        ctx.fillStyle = 'white';
        ctx.font = '20px Arial';
        ctx.fillText(`Score: ${score}`, canvas.width / 2, canvas.height / 2 + 15);
        ctx.fillText('Press Start to play again', canvas.width / 2, canvas.height / 2 + 45);
        
        startBtn.textContent = 'Start Game';
    }
    
    // Draw game
    function drawGame() {
        // Clear canvas
        ctx.fillStyle = '#222';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        // Draw food
        ctx.fillStyle = 'red';
        ctx.fillRect(food.x * gridSize, food.y * gridSize, gridSize, gridSize);
        
        // Draw snake
        snake.forEach((segment, index) => {
            // Head is green, body is slightly darker
            ctx.fillStyle = index === 0 ? '#4CAF50' : '#388E3C';
            ctx.fillRect(segment.x * gridSize, segment.y * gridSize, gridSize, gridSize);
            
            // Draw eyes on head
            if (index === 0) {
                ctx.fillStyle = 'white';
                
                // Position eyes based on direction
                if (dx === 1) { // Right
                    ctx.fillRect(segment.x * gridSize + gridSize - 7, segment.y * gridSize + 5, 4, 4);
                    ctx.fillRect(segment.x * gridSize + gridSize - 7, segment.y * gridSize + gridSize - 9, 4, 4);
                } else if (dx === -1) { // Left
                    ctx.fillRect(segment.x * gridSize + 3, segment.y * gridSize + 5, 4, 4);
                    ctx.fillRect(segment.x * gridSize + 3, segment.y * gridSize + gridSize - 9, 4, 4);
                } else if (dy === 1) { // Down
                    ctx.fillRect(segment.x * gridSize + 5, segment.y * gridSize + gridSize - 7, 4, 4);
                    ctx.fillRect(segment.x * gridSize + gridSize - 9, segment.y * gridSize + gridSize - 7, 4, 4);
                } else if (dy === -1) { // Up
                    ctx.fillRect(segment.x * gridSize + 5, segment.y * gridSize + 3, 4, 4);
                    ctx.fillRect(segment.x * gridSize + gridSize - 9, segment.y * gridSize + 3, 4, 4);
                } else { // Default (right)
                    ctx.fillRect(segment.x * gridSize + gridSize - 7, segment.y * gridSize + 5, 4, 4);
                    ctx.fillRect(segment.x * gridSize + gridSize - 7, segment.y * gridSize + gridSize - 9, 4, 4);
                }
            }
            
            // Draw grid lines
            ctx.strokeStyle = 'rgba(255, 255, 255, 0.1)';
            ctx.strokeRect(segment.x * gridSize, segment.y * gridSize, gridSize, gridSize);
        });
        
        // Draw grid
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.05)';
        for (let i = 0; i < tileCount; i++) {
            for (let j = 0; j < tileCount; j++) {
                ctx.strokeRect(i * gridSize, j * gridSize, gridSize, gridSize);
            }
        }
    }
    
    // Handle keyboard input
    document.addEventListener('keydown', (e) => {
        if (!gameRunning && e.key !== ' ' && e.key !== 'Enter') return;
        
        switch (e.key) {
            case 'ArrowUp':
                if (dy !== 1) { // Prevent moving directly opposite
                    dx = 0;
                    dy = -1;
                }
                e.preventDefault();
                break;
            case 'ArrowDown':
                if (dy !== -1) {
                    dx = 0;
                    dy = 1;
                }
                e.preventDefault();
                break;
            case 'ArrowLeft':
                if (dx !== 1) {
                    dx = -1;
                    dy = 0;
                }
                e.preventDefault();
                break;
            case 'ArrowRight':
                if (dx !== -1) {
                    dx = 1;
                    dy = 0;
                }
                e.preventDefault();
                break;
            case ' ':
            case 'Enter':
                if (!gameRunning) {
                    initGame();
                }
                e.preventDefault();
                break;
        }
    });
    
    // Handle button clicks
    startBtn.addEventListener('click', () => {
        initGame();
    });
    
    upBtn.addEventListener('click', () => {
        if (gameRunning && dy !== 1) {
            dx = 0;
            dy = -1;
        }
    });
    
    downBtn.addEventListener('click', () => {
        if (gameRunning && dy !== -1) {
            dx = 0;
            dy = 1;
        }
    });
    
    leftBtn.addEventListener('click', () => {
        if (gameRunning && dx !== 1) {
            dx = -1;
            dy = 0;
        }
    });
    
    rightBtn.addEventListener('click', () => {
        if (gameRunning && dx !== -1) {
            dx = 1;
            dy = 0;
        }
    });
    
    // Initial draw
    drawGame();
});