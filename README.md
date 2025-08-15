# 🤖 VibeCode AI Platform

A revolutionary AI-powered coding platform that transforms natural language descriptions into fully functional web applications. Experience the future of "vibe coding" with real OpenAI integration!

## ✨ Features

### 🎯 **AI-Powered Code Generation**
- **Real OpenAI Integration**: Uses GPT-4 for intelligent code generation
- **Natural Language Processing**: Describe your app in plain English
- **Multi-Language Support**: Generates HTML, CSS, and JavaScript simultaneously
- **Smart Fallbacks**: Mock AI engine when OpenAI isn't available

### 🎨 **Professional Interface**
- **GitHub-Style UI**: Modern dark theme with professional aesthetics
- **Live Code Preview**: See your generated apps instantly
- **Multi-Tab Editor**: Switch between HTML, CSS, and JavaScript
- **Real-Time Collaboration**: Simulated team coding experience

### 🚀 **Advanced Features**
- **One-Click Deployment**: Simulate app deployment with shareable URLs
- **AI Suggestions**: Get intelligent code improvement recommendations
- **Rate Limiting**: Production-ready API protection
- **Error Handling**: Graceful fallbacks and user-friendly error messages

## 🛠️ Setup Instructions

### Prerequisites
- Node.js (v14 or higher)
- Python 3 (for client server)
- OpenAI API Key (optional but recommended)

### 1. Install Dependencies
```bash
# Install Node.js dependencies
npm install

# Or if you prefer yarn
yarn install
```

### 2. Environment Configuration
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=sk-your-actual-openai-api-key-here
```

### 3. Start the AI Backend Server
```bash
# Start the Express.js AI backend
npm start

# Or for development with auto-reload
npm run dev
```

The AI backend will run on `http://localhost:3001`

### 4. Start the Frontend Client
```bash
# In a new terminal, start the frontend
npm run client

# Or manually:
python3 -m http.server 8000
```

The frontend will be available at `http://localhost:8000`

## 🎮 Usage

### Basic Usage
1. **Open the Platform**: Navigate to `http://localhost:8000`
2. **Describe Your App**: Type a natural language description like:
   - `"Create a todo app with dark theme"`
   - `"Build a calculator with modern design"`
   - `"Make a landing page for my startup"`
3. **Generate Code**: Click "Generate Code" or press `Ctrl+Enter`
4. **Preview & Deploy**: See your app live in the preview panel

### Advanced Features
- **Switch Code Views**: Click HTML/CSS/JS tabs to see generated code
- **Deploy Simulation**: Click "Deploy" to simulate app deployment
- **Get AI Suggestions**: AI automatically suggests improvements (with OpenAI)
- **Collaborate**: Click "Collaborate" to see team features

## 🔧 API Endpoints

### `POST /api/generate`
Generate code based on natural language description.

**Request:**
```json
{
  "description": "Create a todo app with dark theme",
  "type": "fullApp",
  "model": "gpt-4"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "html": "<!DOCTYPE html>...",
    "css": "/* CSS styles */...",
    "javascript": "// JavaScript code..."
  },
  "source": "openai",
  "tokens": 1250,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### `POST /api/suggest`
Get AI-powered code improvement suggestions.

**Request:**
```json
{
  "code": "{ html: '...', css: '...', javascript: '...' }",
  "type": "fullApp"
}
```

### `GET /health`
Check backend service health.

## 🤖 AI Modes

### 1. **OpenAI Mode** (Recommended)
- **Requirements**: Valid OpenAI API key in `.env`
- **Features**: Full GPT-4 powered code generation
- **Quality**: Production-ready, intelligent code
- **Limitations**: Requires API costs

### 2. **Mock AI Mode** (Fallback)
- **Requirements**: No API key needed
- **Features**: Template-based code generation
- **Quality**: Good for demos and testing
- **Limitations**: Limited app types, no dynamic suggestions

## 🔐 Security Features

- **Rate Limiting**: 50 requests per 15 minutes per IP
- **Input Validation**: Description length limits and sanitization
- **CORS Protection**: Configurable allowed origins
- **Helmet Security**: Standard security headers
- **Error Handling**: No sensitive data leakage

## 🎯 Example Prompts

Try these example descriptions:

### Todo Applications
- `"Create a todo app with dark theme and animations"`
- `"Build a task manager with categories and due dates"`
- `"Make a simple to-do list with local storage"`

### Calculators
- `"Build a scientific calculator with modern design"`
- `"Create a simple calculator with keyboard support"`
- `"Make a tip calculator for restaurants"`

### Landing Pages
- `"Create a landing page for a SaaS startup"`
- `"Build a portfolio website for a designer"`
- `"Make a product launch page with call-to-action"`

### Interactive Apps
- `"Create a weather app with animations"`
- `"Build a chat interface with modern styling"`
- `"Make a quiz app with score tracking"`

## 🐛 Troubleshooting

### Backend Not Connecting
1. Check if Node.js server is running on port 3001
2. Verify no firewall blocking localhost:3001
3. Check browser console for connection errors

### OpenAI Not Working
1. Verify API key is correctly set in `.env`
2. Check OpenAI account has available credits
3. Ensure API key has proper permissions

### Frontend Issues
1. Clear browser cache and cookies
2. Check if port 8000 is available
3. Try different browsers

## 📦 Production Deployment

### Backend Deployment
1. Set production environment variables
2. Use process manager (PM2, Docker)
3. Configure reverse proxy (Nginx)
4. Set up HTTPS certificates

### Frontend Deployment
1. Build optimized assets
2. Configure CDN for static files
3. Set up proper caching headers

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details.

## 🌟 Acknowledgments

- OpenAI for providing the GPT-4 API
- The open-source community for inspiration
- Modern web development practices and tools

---

**Built with ❤️ for the future of coding**

🚀 Experience the magic of AI-powered development today!
