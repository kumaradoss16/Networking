const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const { RateLimiterMemory } = require('rate-limiter-flexible');
const OpenAI = require('openai');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3001;

// Security middleware
app.use(helmet());
app.use(cors({
    origin: process.env.ALLOWED_ORIGINS?.split(',') || ['http://localhost:8000'],
    credentials: true
}));
app.use(express.json({ limit: '10mb' }));

// Rate limiting
const rateLimiter = new RateLimiterMemory({
    keyPrefix: 'middleware',
    points: process.env.RATE_LIMIT_MAX_REQUESTS || 50,
    duration: process.env.RATE_LIMIT_WINDOW_MS || 900, // 15 minutes
});

// OpenAI client
const openai = new OpenAI({
    apiKey: process.env.OPENAI_API_KEY,
});

// Rate limiting middleware
const rateLimitMiddleware = async (req, res, next) => {
    try {
        await rateLimiter.consume(req.ip);
        next();
    } catch (rejRes) {
        res.status(429).json({
            error: 'Too many requests',
            message: 'Rate limit exceeded. Please try again later.',
            retryAfter: Math.round(rejRes.msBeforeNext / 1000)
        });
    }
};

// Code generation prompts
const SYSTEM_PROMPTS = {
    html: `You are an expert HTML developer. Generate clean, semantic, modern HTML code based on the user's description. 
    Include proper DOCTYPE, meta tags, and structure. Make it responsive and accessible. 
    Only return the HTML code, no explanations.`,
    
    css: `You are an expert CSS developer. Generate modern, responsive CSS code that matches the user's description. 
    Use modern CSS features like flexbox, grid, animations, and CSS variables. 
    Make it visually appealing and mobile-friendly. Only return the CSS code, no explanations.`,
    
    javascript: `You are an expert JavaScript developer. Generate clean, modern JavaScript code that implements the functionality described by the user. 
    Use ES6+ features, proper error handling, and good practices. 
    Make it interactive and user-friendly. Only return the JavaScript code, no explanations.`,
    
    fullApp: `You are an expert full-stack developer. Based on the user's description, generate a complete web application with HTML, CSS, and JavaScript.
    Return a JSON object with three properties: "html", "css", and "javascript".
    Make it modern, responsive, accessible, and fully functional.
    
    The response format should be:
    {
        "html": "<!DOCTYPE html>...",
        "css": "/* CSS styles */...",
        "javascript": "// JavaScript code..."
    }`
};

// Health check endpoint
app.get('/health', (req, res) => {
    res.json({ 
        status: 'healthy', 
        timestamp: new Date().toISOString(),
        version: '1.0.0'
    });
});

// Generate code endpoint
app.post('/api/generate', rateLimitMiddleware, async (req, res) => {
    try {
        const { description, type = 'fullApp', model = 'gpt-4' } = req.body;

        if (!description || description.trim().length === 0) {
            return res.status(400).json({
                error: 'Invalid input',
                message: 'Description is required and cannot be empty'
            });
        }

        if (description.length > 2000) {
            return res.status(400).json({
                error: 'Invalid input',
                message: 'Description is too long. Maximum 2000 characters allowed.'
            });
        }

        // Check if OpenAI API key is configured
        if (!process.env.OPENAI_API_KEY || process.env.OPENAI_API_KEY === 'your_openai_api_key_here') {
            // Fallback to mock AI if no API key
            console.log('No OpenAI API key configured, using mock AI');
            const mockResponse = generateMockResponse(description);
            return res.json({
                success: true,
                data: mockResponse,
                source: 'mock',
                timestamp: new Date().toISOString()
            });
        }

        const systemPrompt = SYSTEM_PROMPTS[type] || SYSTEM_PROMPTS.fullApp;
        
        const completion = await openai.chat.completions.create({
            model: model,
            messages: [
                {
                    role: "system",
                    content: systemPrompt
                },
                {
                    role: "user",
                    content: `Create a ${type === 'fullApp' ? 'complete web application' : type} based on this description: ${description}`
                }
            ],
            max_tokens: 4000,
            temperature: 0.7,
        });

        const generatedContent = completion.choices[0].message.content;
        
        let responseData;
        if (type === 'fullApp') {
            try {
                // Try to parse as JSON first
                responseData = JSON.parse(generatedContent);
            } catch (parseError) {
                // If JSON parsing fails, create a structured response
                responseData = parseCodeFromText(generatedContent);
            }
        } else {
            responseData = { [type]: generatedContent };
        }

        res.json({
            success: true,
            data: responseData,
            source: 'openai',
            model: model,
            tokens: completion.usage?.total_tokens || 0,
            timestamp: new Date().toISOString()
        });

    } catch (error) {
        console.error('Error generating code:', error);
        
        // Fallback to mock AI on error
        const mockResponse = generateMockResponse(req.body.description);
        
        res.status(500).json({
            success: false,
            error: 'Code generation failed',
            message: error.message,
            fallback: mockResponse,
            timestamp: new Date().toISOString()
        });
    }
});

// Suggest improvements endpoint
app.post('/api/suggest', rateLimitMiddleware, async (req, res) => {
    try {
        const { code, type = 'general' } = req.body;

        if (!code || code.trim().length === 0) {
            return res.status(400).json({
                error: 'Invalid input',
                message: 'Code is required for suggestions'
            });
        }

        // Mock suggestions if no API key
        if (!process.env.OPENAI_API_KEY || process.env.OPENAI_API_KEY === 'your_openai_api_key_here') {
            const mockSuggestions = [
                'Add responsive design with media queries',
                'Improve accessibility with ARIA labels',
                'Add error handling for better user experience',
                'Optimize performance with lazy loading',
                'Add animations for better UX'
            ];
            return res.json({
                success: true,
                suggestions: mockSuggestions.slice(0, 3),
                source: 'mock'
            });
        }

        const completion = await openai.chat.completions.create({
            model: 'gpt-4',
            messages: [
                {
                    role: "system",
                    content: "You are a code review expert. Analyze the provided code and suggest 3-5 specific improvements. Focus on best practices, performance, accessibility, and user experience. Return a JSON array of suggestion strings."
                },
                {
                    role: "user",
                    content: `Analyze this ${type} code and suggest improvements:\n\n${code}`
                }
            ],
            max_tokens: 1000,
            temperature: 0.5,
        });

        const suggestions = JSON.parse(completion.choices[0].message.content);

        res.json({
            success: true,
            suggestions: suggestions,
            source: 'openai',
            timestamp: new Date().toISOString()
        });

    } catch (error) {
        console.error('Error generating suggestions:', error);
        res.status(500).json({
            success: false,
            error: 'Suggestion generation failed',
            message: error.message
        });
    }
});

// Helper function to parse code from text response
function parseCodeFromText(text) {
    const result = { html: '', css: '', javascript: '' };
    
    // Try to extract code blocks
    const htmlMatch = text.match(/```html\n([\s\S]*?)\n```/i) || text.match(/<html[\s\S]*<\/html>/i);
    const cssMatch = text.match(/```css\n([\s\S]*?)\n```/i) || text.match(/\/\*[\s\S]*?\*\/|[^{}]*\{[^{}]*\}/);
    const jsMatch = text.match(/```javascript\n([\s\S]*?)\n```/i) || text.match(/```js\n([\s\S]*?)\n```/i);
    
    if (htmlMatch) result.html = htmlMatch[1] || htmlMatch[0];
    if (cssMatch) result.css = cssMatch[1] || cssMatch[0];
    if (jsMatch) result.javascript = jsMatch[1] || jsMatch[0];
    
    // If no structured code found, create a basic app
    if (!result.html && !result.css && !result.javascript) {
        return generateMockResponse(text);
    }
    
    return result;
}

// Mock response generator (fallback)
function generateMockResponse(description) {
    const keywords = description.toLowerCase();
    
    if (keywords.includes('todo') || keywords.includes('task')) {
        return {
            html: `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Todo App</title>
</head>
<body>
    <div class="container">
        <h1>🤖 AI-Powered Todo App</h1>
        <div class="input-section">
            <input type="text" id="todoInput" placeholder="What needs to be done?">
            <button id="addBtn">Add Task</button>
        </div>
        <ul id="todoList"></ul>
    </div>
</body>
</html>`,
            css: `* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: 'Arial', sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 20px; }
.container { max-width: 600px; margin: 0 auto; background: white; border-radius: 15px; padding: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); }
h1 { text-align: center; margin-bottom: 30px; color: #333; }
.input-section { display: flex; gap: 10px; margin-bottom: 20px; }
#todoInput { flex: 1; padding: 12px; border: 2px solid #ddd; border-radius: 8px; font-size: 16px; }
#addBtn { padding: 12px 20px; background: #667eea; color: white; border: none; border-radius: 8px; cursor: pointer; }
#todoList { list-style: none; }
.todo-item { padding: 10px; margin: 5px 0; background: #f8f9fa; border-radius: 5px; display: flex; justify-content: space-between; align-items: center; }`,
            javascript: `const todoInput = document.getElementById('todoInput');
const addBtn = document.getElementById('addBtn');
const todoList = document.getElementById('todoList');
let todos = [];

addBtn.addEventListener('click', addTodo);
todoInput.addEventListener('keypress', (e) => { if (e.key === 'Enter') addTodo(); });

function addTodo() {
    const text = todoInput.value.trim();
    if (!text) return;
    
    const todo = { id: Date.now(), text, completed: false };
    todos.push(todo);
    todoInput.value = '';
    renderTodos();
}

function deleteTodo(id) {
    todos = todos.filter(todo => todo.id !== id);
    renderTodos();
}

function toggleTodo(id) {
    todos = todos.map(todo => todo.id === id ? {...todo, completed: !todo.completed} : todo);
    renderTodos();
}

function renderTodos() {
    todoList.innerHTML = todos.map(todo => \`
        <li class="todo-item \${todo.completed ? 'completed' : ''}">
            <span onclick="toggleTodo(\${todo.id})" style="cursor: pointer; \${todo.completed ? 'text-decoration: line-through; opacity: 0.6;' : ''}">\${todo.text}</span>
            <button onclick="deleteTodo(\${todo.id})" style="background: #e74c3c; color: white; border: none; padding: 5px 10px; border-radius: 3px; cursor: pointer;">Delete</button>
        </li>
    \`).join('');
}`
        };
    }
    
    // Default generic app
    return {
        html: `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Generated App</title>
</head>
<body>
    <div class="container">
        <header>
            <h1>🤖 AI-Generated Application</h1>
            <p>Based on: "${description}"</p>
        </header>
        <main>
            <div class="feature-section">
                <h2>✨ AI-Powered Features</h2>
                <div class="demo-area">
                    <button id="demoBtn" class="demo-button">Try the AI Magic!</button>
                    <div id="output" class="output"></div>
                </div>
            </div>
        </main>
    </div>
</body>
</html>`,
        css: `* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: 'Inter', sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }
.container { max-width: 800px; margin: 0 auto; background: rgba(255,255,255,0.95); backdrop-filter: blur(10px); min-height: 100vh; }
header { background: linear-gradient(45deg, #667eea, #764ba2); color: white; padding: 40px; text-align: center; }
h1 { font-size: 2.5em; margin-bottom: 10px; }
main { padding: 40px; }
.feature-section { text-align: center; }
.demo-button { background: linear-gradient(45deg, #667eea, #764ba2); color: white; border: none; padding: 15px 30px; border-radius: 25px; font-size: 1.2em; cursor: pointer; margin-bottom: 20px; transition: transform 0.2s; }
.demo-button:hover { transform: translateY(-2px); }
.output { padding: 20px; background: #f8f9fa; border-radius: 10px; margin-top: 20px; min-height: 100px; display: flex; align-items: center; justify-content: center; }`,
        javascript: `document.addEventListener('DOMContentLoaded', function() {
    const demoBtn = document.getElementById('demoBtn');
    const output = document.getElementById('output');
    
    const responses = [
        '🎉 AI magic in action!',
        '✨ Code generated successfully!',
        '🚀 Your app is ready!',
        '💡 AI-powered development!',
        '🎯 Built with artificial intelligence!'
    ];
    
    let index = 0;
    
    demoBtn.addEventListener('click', function() {
        output.textContent = responses[index];
        index = (index + 1) % responses.length;
        output.style.animation = 'fadeIn 0.5s ease';
    });
    
    output.textContent = 'Click the button to see AI in action! 🤖';
});

const style = document.createElement('style');
style.textContent = '@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }';
document.head.appendChild(style);`
    };
}

// Error handling middleware
app.use((error, req, res, next) => {
    console.error('Unhandled error:', error);
    res.status(500).json({
        success: false,
        error: 'Internal server error',
        message: process.env.NODE_ENV === 'development' ? error.message : 'Something went wrong'
    });
});

// 404 handler
app.use((req, res) => {
    res.status(404).json({
        success: false,
        error: 'Not found',
        message: 'The requested endpoint does not exist'
    });
});

app.listen(PORT, () => {
    console.log(`🚀 VibeCode AI Server running on port ${PORT}`);
    console.log(`🔗 Health check: http://localhost:${PORT}/health`);
    console.log(`🤖 AI Status: ${process.env.OPENAI_API_KEY && process.env.OPENAI_API_KEY !== 'your_openai_api_key_here' ? 'OpenAI Enabled' : 'Mock AI Mode'}`);
});