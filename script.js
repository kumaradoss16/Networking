// Vibe Code Platform - JavaScript Functionality

class VibeCodePlatform {
    constructor() {
        this.currentProject = {
            html: '',
            css: '',
            js: ''
        };
        this.collaborators = ['You', 'Alex Chen'];
        this.deploymentId = this.generateId();
        
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.updatePreviewUrl();
        this.simulateCollaboratorActivity();
        this.checkBackendConnection();
    }

    async checkBackendConnection() {
        try {
            const response = await fetch('http://localhost:3001/health');
            if (response.ok) {
                const data = await response.json();
                this.updateConnectionStatus('connected', 'AI Backend Online');
                console.log('✅ AI Backend connected:', data);
            } else {
                throw new Error('Backend health check failed');
            }
        } catch (error) {
            this.updateConnectionStatus('disconnected', 'AI Backend Offline - Using Fallback');
            console.log('⚠️ AI Backend offline, using fallback mode');
        }
    }

    updateConnectionStatus(status, message) {
        // Update the status in the status bar
        const statusElement = document.querySelector('.status-left');
        if (statusElement) {
            const existingStatus = statusElement.querySelector('.ai-status');
            if (existingStatus) {
                existingStatus.remove();
            }
            
            const aiStatusElement = document.createElement('span');
            aiStatusElement.className = `status-item ai-status`;
            aiStatusElement.innerHTML = `
                <i class="fas fa-robot ${status === 'connected' ? 'text-green' : 'text-orange'}"></i>
                ${message}
            `;
            statusElement.appendChild(aiStatusElement);
        }
    }

    setupEventListeners() {
        // Generate button
        const generateBtn = document.getElementById('generateBtn');
        const vibeInput = document.getElementById('vibeInput');
        
        generateBtn.addEventListener('click', () => this.generateCode());
        
        // Allow Enter + Ctrl/Cmd to generate
        vibeInput.addEventListener('keydown', (e) => {
            if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
                this.generateCode();
            }
        });

        // Tab switching
        document.querySelectorAll('.tab').forEach(tab => {
            tab.addEventListener('click', (e) => this.switchTab(e.target.closest('.tab')));
        });

        // File switching
        document.querySelectorAll('.file-item').forEach(item => {
            item.addEventListener('click', (e) => this.switchFile(e.target.closest('.file-item')));
        });

        // Preview controls
        document.querySelector('.preview-btn[title="Refresh"]').addEventListener('click', () => {
            this.updatePreview();
        });

        document.querySelector('.preview-btn[title="Open in new tab"]').addEventListener('click', () => {
            this.openInNewTab();
        });

        // Deploy button
        document.querySelector('.btn-primary').addEventListener('click', () => {
            this.deployApp();
        });

        // Collaborate button
        document.querySelector('.btn-secondary').addEventListener('click', () => {
            this.showCollaboration();
        });

        // AI suggestions
        document.querySelectorAll('.suggestion-item').forEach(item => {
            item.addEventListener('click', (e) => this.applySuggestion(e.target.closest('.suggestion-item')));
        });
    }

    async generateCode() {
        const vibeInput = document.getElementById('vibeInput');
        const description = vibeInput.value.trim();
        
        if (!description) {
            this.showNotification('Please describe what you want to build!', 'warning');
            return;
        }

        if (description.length > 2000) {
            this.showNotification('Description is too long. Please keep it under 2000 characters.', 'warning');
            return;
        }

        this.showLoading(true, 'AI is analyzing your request...');
        
        try {
            // Try to call the real AI backend first
            const response = await this.callAIBackend(description);
            
            if (response.success) {
                this.updateCodeEditors(response.data);
                this.updatePreview();
                this.updateStatus(`Last generated: Just now (${response.source})`);
                
                const sourceText = response.source === 'openai' ? 'OpenAI GPT-4' : 'Mock AI';
                this.showNotification(`🤖 Code generated successfully using ${sourceText}! 🎉`, 'success');
                
                // Update AI suggestions based on generated code
                if (response.source === 'openai') {
                    this.updateAISuggestions(response.data);
                }
            } else {
                throw new Error(response.message || 'AI generation failed');
            }
        } catch (error) {
            console.error('AI generation error:', error);
            
            // Fallback to mock AI
            this.showLoading(true, 'Using fallback AI engine...');
            await this.delay(1000);
            
            try {
                const fallbackCode = this.mockAIEngine(description);
                this.updateCodeEditors(fallbackCode);
                this.updatePreview();
                this.updateStatus('Last generated: Just now (fallback)');
                this.showNotification('⚠️ Generated using fallback AI. For full AI features, configure OpenAI API key.', 'warning');
            } catch (fallbackError) {
                this.showNotification('❌ Failed to generate code. Please try again.', 'error');
            }
        } finally {
            this.showLoading(false);
        }
    }

    async callAIBackend(description) {
        const API_BASE_URL = 'http://localhost:3001';
        
        try {
            const response = await fetch(`${API_BASE_URL}/api/generate`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    description: description,
                    type: 'fullApp',
                    model: 'gpt-4'
                })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.message || `HTTP ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            // Network error or server not running
            if (error.name === 'TypeError' && error.message.includes('fetch')) {
                throw new Error('AI backend server not running. Starting fallback mode...');
            }
            throw error;
        }
    }

    async updateAISuggestions(generatedCode) {
        try {
            const response = await fetch('http://localhost:3001/api/suggest', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    code: JSON.stringify(generatedCode),
                    type: 'fullApp'
                })
            });

            if (response.ok) {
                const result = await response.json();
                if (result.success && result.suggestions) {
                    this.displayAISuggestions(result.suggestions);
                }
            }
        } catch (error) {
            console.log('Could not fetch AI suggestions:', error.message);
        }
    }

    displayAISuggestions(suggestions) {
        const suggestionsContainer = document.querySelector('.ai-suggestions');
        if (!suggestionsContainer) return;

        // Clear existing suggestions
        suggestionsContainer.innerHTML = '';

        // Add new AI suggestions
        suggestions.forEach((suggestion, index) => {
            const suggestionItem = document.createElement('div');
            suggestionItem.className = 'suggestion-item';
            suggestionItem.innerHTML = `
                <i class="fas fa-robot"></i>
                <span>${suggestion}</span>
            `;
            suggestionItem.addEventListener('click', () => this.applySuggestion(suggestionItem));
            suggestionsContainer.appendChild(suggestionItem);
        });
    }

    mockAIEngine(description) {
        // Simple keyword-based code generation
        const keywords = description.toLowerCase();
        
        if (keywords.includes('todo') || keywords.includes('task')) {
            return this.generateTodoApp(keywords);
        } else if (keywords.includes('calculator')) {
            return this.generateCalculator(keywords);
        } else if (keywords.includes('weather')) {
            return this.generateWeatherApp(keywords);
        } else if (keywords.includes('landing') || keywords.includes('homepage')) {
            return this.generateLandingPage(keywords);
        } else if (keywords.includes('chat') || keywords.includes('message')) {
            return this.generateChatApp(keywords);
        } else {
            return this.generateGenericApp(description);
        }
    }

    generateTodoApp(keywords) {
        const isDark = keywords.includes('dark');
        const theme = isDark ? 'dark' : 'light';
        
        return {
            html: `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Todo App</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body class="${theme}-theme">
    <div class="container">
        <h1>📝 My Todo App</h1>
        <div class="input-section">
            <input type="text" id="todoInput" placeholder="What needs to be done?">
            <button id="addBtn">Add Task</button>
        </div>
        <ul id="todoList" class="todo-list"></ul>
        <div class="stats">
            <span id="totalTasks">0 tasks</span>
            <button id="clearCompleted">Clear Completed</button>
        </div>
    </div>
</body>
</html>`,
            css: `* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    transition: all 0.3s ease;
}

.light-theme {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: #333;
}

.dark-theme {
    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
    color: #fff;
}

.container {
    max-width: 600px;
    margin: 50px auto;
    padding: 30px;
    background: rgba(255, 255, 255, 0.95);
    border-radius: 20px;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(10px);
}

.dark-theme .container {
    background: rgba(0, 0, 0, 0.3);
    border: 1px solid rgba(255, 255, 255, 0.1);
}

h1 {
    text-align: center;
    margin-bottom: 30px;
    font-size: 2.5em;
    background: linear-gradient(45deg, #667eea, #764ba2);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.input-section {
    display: flex;
    gap: 10px;
    margin-bottom: 30px;
}

#todoInput {
    flex: 1;
    padding: 15px;
    border: 2px solid #ddd;
    border-radius: 10px;
    font-size: 16px;
    transition: all 0.3s ease;
}

#todoInput:focus {
    outline: none;
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.dark-theme #todoInput {
    background: rgba(255, 255, 255, 0.1);
    border-color: rgba(255, 255, 255, 0.2);
    color: white;
}

#addBtn {
    padding: 15px 25px;
    background: linear-gradient(45deg, #667eea, #764ba2);
    color: white;
    border: none;
    border-radius: 10px;
    cursor: pointer;
    font-weight: 600;
    transition: all 0.3s ease;
}

#addBtn:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
}

.todo-list {
    list-style: none;
    margin-bottom: 20px;
}

.todo-item {
    display: flex;
    align-items: center;
    padding: 15px;
    margin-bottom: 10px;
    background: rgba(255, 255, 255, 0.5);
    border-radius: 10px;
    transition: all 0.3s ease;
}

.dark-theme .todo-item {
    background: rgba(255, 255, 255, 0.1);
}

.todo-item:hover {
    transform: translateX(5px);
}

.todo-item.completed {
    opacity: 0.6;
    text-decoration: line-through;
}

.todo-text {
    flex: 1;
    margin-left: 10px;
}

.delete-btn {
    background: #e74c3c;
    color: white;
    border: none;
    padding: 5px 10px;
    border-radius: 5px;
    cursor: pointer;
    transition: all 0.3s ease;
}

.delete-btn:hover {
    background: #c0392b;
    transform: scale(1.1);
}

.stats {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-top: 20px;
    border-top: 1px solid rgba(0, 0, 0, 0.1);
}

.dark-theme .stats {
    border-top-color: rgba(255, 255, 255, 0.1);
}

#clearCompleted {
    background: transparent;
    border: 2px solid #667eea;
    color: #667eea;
    padding: 8px 16px;
    border-radius: 5px;
    cursor: pointer;
    transition: all 0.3s ease;
}

#clearCompleted:hover {
    background: #667eea;
    color: white;
}`,
            js: `class TodoApp {
    constructor() {
        this.todos = [];
        this.init();
    }

    init() {
        this.todoInput = document.getElementById('todoInput');
        this.addBtn = document.getElementById('addBtn');
        this.todoList = document.getElementById('todoList');
        this.totalTasks = document.getElementById('totalTasks');
        this.clearCompleted = document.getElementById('clearCompleted');

        this.addBtn.addEventListener('click', () => this.addTodo());
        this.todoInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.addTodo();
        });
        this.clearCompleted.addEventListener('click', () => this.clearCompletedTodos());
        
        this.loadFromStorage();
        this.render();
    }

    addTodo() {
        const text = this.todoInput.value.trim();
        if (!text) return;

        const todo = {
            id: Date.now(),
            text: text,
            completed: false,
            createdAt: new Date()
        };

        this.todos.unshift(todo);
        this.todoInput.value = '';
        this.saveToStorage();
        this.render();
        this.animateAdd();
    }

    toggleTodo(id) {
        this.todos = this.todos.map(todo => 
            todo.id === id ? { ...todo, completed: !todo.completed } : todo
        );
        this.saveToStorage();
        this.render();
    }

    deleteTodo(id) {
        this.todos = this.todos.filter(todo => todo.id !== id);
        this.saveToStorage();
        this.render();
    }

    clearCompletedTodos() {
        this.todos = this.todos.filter(todo => !todo.completed);
        this.saveToStorage();
        this.render();
    }

    render() {
        this.todoList.innerHTML = '';
        
        this.todos.forEach(todo => {
            const li = document.createElement('li');
            li.className = \`todo-item \${todo.completed ? 'completed' : ''}\`;
            li.innerHTML = \`
                <input type="checkbox" \${todo.completed ? 'checked' : ''} 
                       onchange="todoApp.toggleTodo(\${todo.id})">
                <span class="todo-text">\${todo.text}</span>
                <button class="delete-btn" onclick="todoApp.deleteTodo(\${todo.id})">🗑️</button>
            \`;
            this.todoList.appendChild(li);
        });

        this.updateStats();
    }

    updateStats() {
        const total = this.todos.length;
        const completed = this.todos.filter(todo => todo.completed).length;
        this.totalTasks.textContent = \`\${total} tasks (\${completed} completed)\`;
    }

    saveToStorage() {
        localStorage.setItem('todos', JSON.stringify(this.todos));
    }

    loadFromStorage() {
        const saved = localStorage.getItem('todos');
        this.todos = saved ? JSON.parse(saved) : [];
    }

    animateAdd() {
        const items = this.todoList.children;
        if (items.length > 0) {
            items[0].style.animation = 'slideIn 0.3s ease';
        }
    }
}

// Initialize the app
const todoApp = new TodoApp();

// Add some CSS animation
const style = document.createElement('style');
style.textContent = \`
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
\`;
document.head.appendChild(style);`
        };
    }

    generateCalculator(keywords) {
        return {
            html: `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Calculator</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="calculator">
        <div class="display">
            <input type="text" id="display" readonly>
        </div>
        <div class="buttons">
            <button class="btn clear" onclick="clearDisplay()">C</button>
            <button class="btn operator" onclick="deleteLast()">⌫</button>
            <button class="btn operator" onclick="appendToDisplay('/')">/</button>
            <button class="btn operator" onclick="appendToDisplay('*')">×</button>
            
            <button class="btn" onclick="appendToDisplay('7')">7</button>
            <button class="btn" onclick="appendToDisplay('8')">8</button>
            <button class="btn" onclick="appendToDisplay('9')">9</button>
            <button class="btn operator" onclick="appendToDisplay('-')">-</button>
            
            <button class="btn" onclick="appendToDisplay('4')">4</button>
            <button class="btn" onclick="appendToDisplay('5')">5</button>
            <button class="btn" onclick="appendToDisplay('6')">6</button>
            <button class="btn operator" onclick="appendToDisplay('+')">+</button>
            
            <button class="btn" onclick="appendToDisplay('1')">1</button>
            <button class="btn" onclick="appendToDisplay('2')">2</button>
            <button class="btn" onclick="appendToDisplay('3')">3</button>
            <button class="btn equals" onclick="calculate()" rowspan="2">=</button>
            
            <button class="btn zero" onclick="appendToDisplay('0')">0</button>
            <button class="btn" onclick="appendToDisplay('.')">.</button>
        </div>
    </div>
</body>
</html>`,
            css: `* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Arial', sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    padding: 20px;
}

.calculator {
    background: #2c3e50;
    border-radius: 20px;
    padding: 25px;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
    max-width: 350px;
    width: 100%;
}

.display {
    margin-bottom: 20px;
}

#display {
    width: 100%;
    height: 80px;
    background: #1a252f;
    border: none;
    border-radius: 10px;
    font-size: 2em;
    color: white;
    text-align: right;
    padding: 0 20px;
    box-shadow: inset 0 4px 8px rgba(0, 0, 0, 0.3);
}

.buttons {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 15px;
}

.btn {
    height: 70px;
    border: none;
    border-radius: 15px;
    font-size: 1.5em;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.2s ease;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
}

.btn:active {
    transform: translateY(0);
}

.btn:not(.operator):not(.clear):not(.equals) {
    background: #34495e;
    color: white;
}

.operator {
    background: #e67e22;
    color: white;
}

.clear {
    background: #e74c3c;
    color: white;
}

.equals {
    background: #27ae60;
    color: white;
    grid-row: span 2;
}

.zero {
    grid-column: span 2;
}`,
            js: `let currentInput = '';
let operator = '';
let previousInput = '';

function appendToDisplay(value) {
    const display = document.getElementById('display');
    
    if (['+', '-', '*', '/'].includes(value)) {
        if (currentInput !== '') {
            if (previousInput !== '' && operator !== '') {
                calculate();
            }
            previousInput = currentInput;
            operator = value;
            currentInput = '';
        }
    } else {
        currentInput += value;
    }
    
    updateDisplay();
}

function updateDisplay() {
    const display = document.getElementById('display');
    if (currentInput !== '') {
        display.value = currentInput;
    } else if (operator !== '') {
        display.value = previousInput + ' ' + operator;
    } else {
        display.value = previousInput;
    }
}

function clearDisplay() {
    currentInput = '';
    operator = '';
    previousInput = '';
    document.getElementById('display').value = '';
}

function deleteLast() {
    if (currentInput !== '') {
        currentInput = currentInput.slice(0, -1);
    }
    updateDisplay();
}

function calculate() {
    if (previousInput !== '' && currentInput !== '' && operator !== '') {
        const prev = parseFloat(previousInput);
        const current = parseFloat(currentInput);
        let result;
        
        switch (operator) {
            case '+':
                result = prev + current;
                break;
            case '-':
                result = prev - current;
                break;
            case '*':
                result = prev * current;
                break;
            case '/':
                result = current !== 0 ? prev / current : 'Error';
                break;
            default:
                return;
        }
        
        currentInput = result.toString();
        operator = '';
        previousInput = '';
        updateDisplay();
    }
}

// Add keyboard support
document.addEventListener('keydown', function(event) {
    if (event.key >= '0' && event.key <= '9' || event.key === '.') {
        appendToDisplay(event.key);
    } else if (['+', '-', '*', '/'].includes(event.key)) {
        appendToDisplay(event.key);
    } else if (event.key === 'Enter' || event.key === '=') {
        calculate();
    } else if (event.key === 'Escape' || event.key === 'c' || event.key === 'C') {
        clearDisplay();
    } else if (event.key === 'Backspace') {
        deleteLast();
    }
});`
        };
    }

    generateGenericApp(description) {
        return {
            html: `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Generated App</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="container">
        <header>
            <h1>🚀 Your Generated App</h1>
            <p>Based on: "${description}"</p>
        </header>
        
        <main>
            <div class="feature-card">
                <h2>🎯 Core Features</h2>
                <ul>
                    <li>Modern responsive design</li>
                    <li>Interactive user interface</li>
                    <li>Clean and accessible code</li>
                    <li>Mobile-friendly layout</li>
                </ul>
            </div>
            
            <div class="demo-section">
                <h2>🎨 Interactive Demo</h2>
                <button id="demoBtn" class="demo-button">Click me!</button>
                <div id="output" class="output"></div>
            </div>
        </main>
        
        <footer>
            <p>Generated by VibeCode AI ✨</p>
        </footer>
    </div>
</body>
</html>`,
            css: `* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    padding: 20px;
}

.container {
    max-width: 800px;
    margin: 0 auto;
    background: rgba(255, 255, 255, 0.95);
    border-radius: 20px;
    overflow: hidden;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(10px);
}

header {
    background: linear-gradient(45deg, #667eea, #764ba2);
    color: white;
    padding: 40px;
    text-align: center;
}

header h1 {
    font-size: 2.5em;
    margin-bottom: 10px;
}

header p {
    opacity: 0.9;
    font-style: italic;
}

main {
    padding: 40px;
}

.feature-card {
    background: #f8f9fa;
    border-radius: 15px;
    padding: 30px;
    margin-bottom: 30px;
    border-left: 5px solid #667eea;
}

.feature-card h2 {
    color: #333;
    margin-bottom: 20px;
}

.feature-card ul {
    list-style: none;
}

.feature-card li {
    padding: 10px 0;
    border-bottom: 1px solid #eee;
    position: relative;
    padding-left: 20px;
}

.feature-card li:before {
    content: '✓';
    position: absolute;
    left: 0;
    color: #27ae60;
    font-weight: bold;
}

.demo-section {
    text-align: center;
}

.demo-section h2 {
    margin-bottom: 30px;
    color: #333;
}

.demo-button {
    background: linear-gradient(45deg, #667eea, #764ba2);
    color: white;
    border: none;
    padding: 15px 30px;
    border-radius: 50px;
    font-size: 1.2em;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
}

.demo-button:hover {
    transform: translateY(-3px);
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
}

.output {
    margin-top: 20px;
    padding: 20px;
    background: #e8f4f8;
    border-radius: 10px;
    min-height: 60px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 500;
}

footer {
    background: #2c3e50;
    color: white;
    text-align: center;
    padding: 20px;
}`,
            js: `// Interactive demo functionality
document.addEventListener('DOMContentLoaded', function() {
    const demoBtn = document.getElementById('demoBtn');
    const output = document.getElementById('output');
    
    const messages = [
        "🎉 Welcome to your generated app!",
        "✨ This was created using AI magic!",
        "🚀 Ready to build something amazing?",
        "💡 The possibilities are endless!",
        "🎯 Your idea brought to life!"
    ];
    
    let messageIndex = 0;
    
    demoBtn.addEventListener('click', function() {
        output.textContent = messages[messageIndex];
        messageIndex = (messageIndex + 1) % messages.length;
        
        // Add some animation
        output.style.animation = 'none';
        output.offsetHeight; // Trigger reflow
        output.style.animation = 'fadeIn 0.5s ease';
    });
    
    // Initial message
    output.textContent = "Click the button above to see the magic! ✨";
});

// Add CSS animation
const style = document.createElement('style');
style.textContent = \`
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
\`;
document.head.appendChild(style);`
        };
    }

    updateCodeEditors(code) {
        document.getElementById('htmlCode').textContent = code.html;
        document.getElementById('cssCode').textContent = code.css;
        document.getElementById('jsCode').textContent = code.js;
        
        this.currentProject = code;
    }

    updatePreview() {
        const iframe = document.getElementById('preview');
        const htmlContent = `
            <html>
                <head>
                    <style>${this.currentProject.css}</style>
                </head>
                <body>
                    ${this.currentProject.html.replace(/<\/?html[^>]*>|<\/?head[^>]*>|<\/?body[^>]*>/gi, '').replace(/<link[^>]*>/gi, '')}
                    <script>${this.currentProject.js}</script>
                </body>
            </html>
        `;
        
        iframe.srcdoc = htmlContent;
    }

    switchTab(tab) {
        // Remove active class from all tabs and editors
        document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
        document.querySelectorAll('.editor').forEach(e => e.classList.remove('active'));
        
        // Add active class to clicked tab
        tab.classList.add('active');
        
        // Show corresponding editor
        const fileType = tab.dataset.file;
        const editor = document.getElementById(`${fileType}Editor`);
        if (editor) {
            editor.classList.add('active');
        }
    }

    switchFile(fileItem) {
        document.querySelectorAll('.file-item').forEach(item => item.classList.remove('active'));
        fileItem.classList.add('active');
        
        // Here you could load different file contents
        this.showNotification(`Switched to ${fileItem.textContent}`, 'info');
    }

    async deployApp() {
        this.showLoading(true, 'Deploying your app...');
        
        await this.delay(3000);
        
        this.deploymentId = this.generateId();
        this.updatePreviewUrl();
        this.showNotification('🚀 App deployed successfully!', 'success');
        this.updateStatus('Last deployed: Just now');
        
        this.showLoading(false);
    }

    showCollaboration() {
        const modal = this.createModal(`
            <h2>👥 Collaboration</h2>
            <div class="collaborator-list">
                ${this.collaborators.map(name => `
                    <div class="collaborator">
                        <div class="avatar">${name.charAt(0)}</div>
                        <span>${name}</span>
                        <span class="status online">online</span>
                    </div>
                `).join('')}
            </div>
            <input type="email" placeholder="Invite by email..." class="invite-input">
            <button class="btn-primary">Send Invitation</button>
        `);
        
        modal.querySelector('.invite-input').focus();
    }

    applySuggestion(suggestionItem) {
        const suggestion = suggestionItem.textContent.trim();
        this.showNotification(`Applied suggestion: ${suggestion}`, 'success');
        
        // Simulate applying the suggestion
        setTimeout(() => {
            if (suggestion.includes('responsive')) {
                this.showNotification('Added responsive breakpoints to CSS', 'info');
            } else if (suggestion.includes('accessibility')) {
                this.showNotification('Improved accessibility with ARIA labels', 'info');
            }
        }, 1000);
    }

    showLoading(show, message = 'AI is generating your code...') {
        const overlay = document.getElementById('loadingOverlay');
        const messageEl = overlay.querySelector('h3');
        messageEl.textContent = message;
        
        if (show) {
            overlay.classList.remove('hidden');
        } else {
            overlay.classList.add('hidden');
        }
    }

    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.innerHTML = `
            <span>${message}</span>
            <button onclick="this.parentElement.remove()">×</button>
        `;
        
        // Add styles if not exists
        if (!document.querySelector('#notification-styles')) {
            const style = document.createElement('style');
            style.id = 'notification-styles';
            style.textContent = `
                .notification {
                    position: fixed;
                    top: 20px;
                    right: 20px;
                    padding: 15px 20px;
                    border-radius: 8px;
                    color: white;
                    z-index: 1001;
                    display: flex;
                    align-items: center;
                    gap: 10px;
                    animation: slideIn 0.3s ease;
                    max-width: 400px;
                }
                .notification.success { background: #27ae60; }
                .notification.error { background: #e74c3c; }
                .notification.warning { background: #f39c12; }
                .notification.info { background: #3498db; }
                .notification button {
                    background: none;
                    border: none;
                    color: white;
                    cursor: pointer;
                    font-size: 18px;
                    padding: 0;
                    width: 20px;
                    height: 20px;
                }
            `;
            document.head.appendChild(style);
        }
        
        document.body.appendChild(notification);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            if (notification.parentElement) {
                notification.remove();
            }
        }, 5000);
    }

    createModal(content) {
        const modal = document.createElement('div');
        modal.className = 'modal-overlay';
        modal.innerHTML = `
            <div class="modal">
                ${content}
                <button class="modal-close" onclick="this.closest('.modal-overlay').remove()">×</button>
            </div>
        `;
        
        // Add modal styles if not exists
        if (!document.querySelector('#modal-styles')) {
            const style = document.createElement('style');
            style.id = 'modal-styles';
            style.textContent = `
                .modal-overlay {
                    position: fixed;
                    top: 0;
                    left: 0;
                    right: 0;
                    bottom: 0;
                    background: rgba(0, 0, 0, 0.8);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    z-index: 1002;
                }
                .modal {
                    background: #161b22;
                    border-radius: 12px;
                    padding: 30px;
                    max-width: 500px;
                    width: 90%;
                    position: relative;
                    color: #c9d1d9;
                }
                .modal h2 {
                    margin-bottom: 20px;
                    color: #58a6ff;
                }
                .modal-close {
                    position: absolute;
                    top: 15px;
                    right: 15px;
                    background: none;
                    border: none;
                    color: #8b949e;
                    cursor: pointer;
                    font-size: 20px;
                }
                .collaborator-list {
                    margin-bottom: 20px;
                }
                .collaborator {
                    display: flex;
                    align-items: center;
                    gap: 10px;
                    padding: 10px 0;
                    border-bottom: 1px solid #30363d;
                }
                .avatar {
                    width: 32px;
                    height: 32px;
                    border-radius: 50%;
                    background: #58a6ff;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-weight: bold;
                    color: white;
                }
                .status.online {
                    color: #27ae60;
                    font-size: 12px;
                }
                .invite-input {
                    width: 100%;
                    padding: 10px;
                    margin-bottom: 15px;
                    border: 1px solid #30363d;
                    border-radius: 6px;
                    background: #0d1117;
                    color: #c9d1d9;
                }
            `;
            document.head.appendChild(style);
        }
        
        document.body.appendChild(modal);
        return modal;
    }

    updatePreviewUrl() {
        const url = `https://vibeapp-${this.deploymentId}.vibeCode.app`;
        document.getElementById('previewUrl').textContent = url;
    }

    updateStatus(status) {
        const statusItem = document.querySelector('.status-right .status-item:first-child');
        statusItem.innerHTML = `<i class="fas fa-clock"></i> ${status}`;
    }

    openInNewTab() {
        const iframe = document.getElementById('preview');
        const newWindow = window.open('', '_blank');
        newWindow.document.write(iframe.srcdoc);
        newWindow.document.close();
    }

    generateId() {
        return Math.random().toString(36).substr(2, 8);
    }

    simulateCollaboratorActivity() {
        setInterval(() => {
            if (Math.random() < 0.1) { // 10% chance every interval
                this.showNotification(`${this.collaborators[1]} made changes to the project`, 'info');
            }
        }, 30000); // Check every 30 seconds
    }

    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}

// Initialize the platform
document.addEventListener('DOMContentLoaded', () => {
    new VibeCodePlatform();
});