/**
 * @jest-environment jsdom
 */

// Import the script to test
// Note: In a real project, you would need to make the script modular
// and export functions to test them properly

describe('Snake Game DOMContentLoaded Callback', () => {
  // Mock DOM elements
  let mockCanvas, mockCtx, mockScoreElement, mockHighScoreElement, mockStartBtn;
  let mockUpBtn, mockDownBtn, mockLeftBtn, mockRightBtn;

  // Mock localStorage
  let localStorageMock;

  // Store the DOMContentLoaded callback
  let domContentLoadedCallback;

  // Mock setInterval and clearInterval
  let originalSetInterval;
  let originalClearInterval;
  let intervalId = 999;

  beforeEach(() => {
    // Create a fresh document for each test
    document.body.innerHTML = `
      <canvas id="gameCanvas" width="400" height="400"></canvas>
      <div id="score">0</div>
      <div id="highScore">0</div>
      <button id="startBtn">Start Game</button>
      <button id="upBtn">Up</button>
      <button id="downBtn">Down</button>
      <button id="leftBtn">Left</button>
      <button id="rightBtn">Right</button>
    `;

    // Mock canvas and context
    mockCtx = {
      fillStyle: '',
      fillRect: jest.fn(),
      strokeStyle: '',
      strokeRect: jest.fn(),
      font: '',
      textAlign: '',
      fillText: jest.fn()
    };

    mockCanvas = document.getElementById('gameCanvas');
    mockCanvas.getContext = jest.fn().mockReturnValue(mockCtx);

    // Mock DOM elements
    mockScoreElement = document.getElementById('score');
    mockHighScoreElement = document.getElementById('highScore');
    mockStartBtn = document.getElementById('startBtn');
    mockUpBtn = document.getElementById('upBtn');
    mockDownBtn = document.getElementById('downBtn');
    mockLeftBtn = document.getElementById('leftBtn');
    mockRightBtn = document.getElementById('rightBtn');

    // Mock localStorage
    localStorageMock = {
      getItem: jest.fn().mockReturnValue('10'),
      setItem: jest.fn()
    };
    Object.defineProperty(window, 'localStorage', { value: localStorageMock });

    // Mock setInterval and clearInterval
    originalSetInterval = window.setInterval;
    originalClearInterval = window.clearInterval;

    window.setInterval = jest.fn(() => intervalId);
    window.clearInterval = jest.fn();

    // Capture the DOMContentLoaded callback
    const originalAddEventListener = document.addEventListener;
    document.addEventListener = jest.fn((event, callback) => {
      if (event === 'DOMContentLoaded') {
        domContentLoadedCallback = callback;
      } else {
        return originalAddEventListener.call(document, event, callback);
      }
    });

    // Load the script to capture the callback
    jest.isolateModules(() => {
      require('../script.js');
    });

    // Execute the callback to initialize the game
    if (domContentLoadedCallback) {
      domContentLoadedCallback();
    }
  });

  afterEach(() => {
    // Restore original functions
    window.setInterval = originalSetInterval;
    window.clearInterval = originalClearInterval;

    // Clear all mocks
    jest.clearAllMocks();
  });

  test('DOMContentLoaded callback is registered', () => {
    expect(document.addEventListener).toHaveBeenCalledWith('DOMContentLoaded', expect.any(Function));
  });

  test('initializes game variables and elements correctly', () => {
    // Check if canvas context was requested
    expect(mockCanvas.getContext).toHaveBeenCalledWith('2d');

    // Check if high score was retrieved from localStorage
    expect(localStorageMock.getItem).toHaveBeenCalledWith('snakeHighScore');

    // Check if high score element was updated
    expect(mockHighScoreElement.textContent).toBe('10');
  });

  test('registers event listeners for keyboard controls', () => {
    // Check if keydown event listener was added
    expect(document.addEventListener).toHaveBeenCalledWith('keydown', expect.any(Function));
  });

  test('registers event listeners for button controls', () => {
    // Check if click event listeners were added to buttons
    const clickListeners = mockStartBtn.onclick !== null &&
                          mockUpBtn.onclick !== null &&
                          mockDownBtn.onclick !== null &&
                          mockLeftBtn.onclick !== null &&
                          mockRightBtn.onclick !== null;

    expect(clickListeners).toBeTruthy();
  });

  test('starts game when start button is clicked', () => {
    // Simulate clicking the start button
    mockStartBtn.click();

    // Game interval should be set
    expect(window.setInterval).toHaveBeenCalled();

    // Button text should change
    expect(mockStartBtn.textContent).toBe('Restart Game');
  });

  test('changes direction when arrow keys are pressed', () => {
    // Start the game first
    mockStartBtn.click();

    // Create a keydown event for the right arrow key
    const keydownEvent = new KeyboardEvent('keydown', { key: 'ArrowRight' });

    // Dispatch the event
    document.dispatchEvent(keydownEvent);

    // We can't directly test internal variables, but we can verify the event was processed
    expect(keydownEvent.defaultPrevented).toBeTruthy();
  });

  test('changes direction when direction buttons are clicked', () => {
    // Start the game first
    mockStartBtn.click();

    // Simulate clicking the right button
    mockRightBtn.click();

    // We can't directly test internal variables, but we can verify the game is still running
    expect(mockStartBtn.textContent).toBe('Restart Game');
  });

  test('draws initial game state', () => {
    // Check if canvas was drawn on
    expect(mockCtx.fillRect).toHaveBeenCalled();
  });

  test('restarts game when start button is clicked again', () => {
    // Start the game
    mockStartBtn.click();

    // Clear mocks
    jest.clearAllMocks();

    // Click start button again
    mockStartBtn.click();

    // Should clear previous interval and set a new one
    expect(window.clearInterval).toHaveBeenCalled();
    expect(window.setInterval).toHaveBeenCalled();
  });
});