# LastSignal - Deployment Guide

## 🚀 Deploy to Render

### Quick Deploy

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

### Manual Deployment Steps

1. **Fork/Clone this repository** to your GitHub account

2. **Sign up for Render** at https://render.com

3. **Create a new Web Service**:
   - Go to Render Dashboard
   - Click "New +" → "Web Service"
   - Connect your GitHub repository

4. **Configure the service**:
   - **Name**: `lastsignal-game` (or your choice)
   - **Environment**: `Python 3`
   - **Region**: Choose your preferred region
   - **Branch**: `main` or your PR branch
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn -w 4 -b 0.0.0.0:$PORT server_web:app`

5. **Environment Variables** (Optional):
   - `LASTSIGNAL_AI_ENABLED`: `true` (to enable AI features)
   - `OPENAI_API_KEY`: Your OpenAI API key (if using AI features)
   - `PYTHON_VERSION`: `3.11.0`

6. **Deploy**: Click "Create Web Service"

Your game will be live at: `https://your-service-name.onrender.com`

---

## 📋 Build and Start Commands

### For Render Deployment

**Build Command:**
```bash
pip install -r requirements.txt
```

**Start Command:**
```bash
gunicorn -w 4 -b 0.0.0.0:$PORT server_web:app
```

### For Local Development

**Install dependencies:**
```bash
pip install -r requirements.txt
```

**Start server:**
```bash
python server_web.py
```

Then open: `http://localhost:8080`

---

## 🎮 Game Versions

### Standard 2D UI
Access at: `/` or `/index.html`
- Classic 2D interface
- Works on all devices
- Lightweight

### 3D Enhanced UI
Access at: `/index_3d.html`
- Three.js 3D visualization
- Animated faction nodes
- Custom GLB model support
- Immersive experience

---

## 🎨 Custom 3D Models

### Upload Your Own GLB Models

The 3D version supports custom GLB/GLTF models for faction nodes!

**Steps:**
1. Create or download a GLB/GLTF 3D model
2. Open the 3D game interface
3. Click "📦 Upload GLB/GLTF Model" in the System Status panel
4. Select your `.glb` or `.gltf` file
5. Your model will replace a faction node!

**Model Requirements:**
- Format: GLB or GLTF
- Recommended size: < 5MB
- Recommended poly count: < 50k triangles
- Will be auto-scaled to fit the scene

**Free 3D Model Resources:**
- [Sketchfab](https://sketchfab.com/feed) - Free GLB models
- [Poly Haven](https://polyhaven.com/) - Free CC0 3D assets
- [Blender](https://www.blender.org/) - Create your own (export as GLB)

---

## 🔧 Architecture

### Files Structure

```
lastsignal/
├── server_web.py          # Flask web server for deployment
├── game.py                # Core game engine
├── ai_engine.py           # AI-powered features
├── server.py              # CLI multiplayer server
├── index.html             # 2D game UI
├── index_3d.html          # 3D game UI with Three.js
├── requirements.txt       # Python dependencies
├── render.yaml            # Render deployment config
└── docs/
    ├── README.md
    ├── AI_FEATURES.md
    ├── ARCHITECTURE.md
    └── QUICKSTART.md
```

### API Endpoints

The web server exposes REST API for game functionality:

- `GET /api/health` - Health check
- `GET /api/sessions` - List active game sessions
- `POST /api/sessions` - Create new session
- `POST /api/sessions/{id}/join` - Join session
- `POST /api/sessions/{id}/start` - Start game
- `GET /api/sessions/{id}/state` - Get game state
- `POST /api/sessions/{id}/action` - Process player action
- `POST /api/sessions/{id}/round` - Process round
- `GET /api/sessions/{id}/status` - Check game over status

---

## 🌐 Production Configuration

### Environment Variables

```bash
# Required for deployment
PORT=8080                           # Auto-set by Render

# Optional - AI Features
LASTSIGNAL_AI_ENABLED=true         # Enable AI features
OPENAI_API_KEY=sk-...              # Your OpenAI API key

# Optional - Configuration
PYTHON_VERSION=3.11.0              # Python version
RENDER=true                         # Auto-set by Render
```

### Performance

- **Free Tier**: Suitable for 1-10 concurrent players
- **Starter Tier**: Recommended for 10-50 players
- **Memory Usage**: ~200MB base, +50MB per active game session
- **Cold Start**: ~15-30 seconds on free tier

### Scaling

For production use:
1. Upgrade to Starter tier or higher
2. Enable auto-scaling (paid plans)
3. Add Redis for session management (recommended for >100 players)
4. Enable CDN for static assets

---

## 🧪 Testing Deployment

### Test Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run server
python server_web.py

# Test in browser
open http://localhost:8080
open http://localhost:8080/index_3d.html
```

### Test API Endpoints

```bash
# Health check
curl http://localhost:8080/api/health

# Create session
curl -X POST http://localhost:8080/api/sessions \
  -H "Content-Type: application/json" \
  -d '{"max_players": 4, "game_duration": 300}'

# List sessions
curl http://localhost:8080/api/sessions
```

---

## 🐛 Troubleshooting

### Common Issues

**Issue**: Build fails on Render
- **Solution**: Verify `requirements.txt` is in root directory
- Check Python version compatibility

**Issue**: 3D models not loading
- **Solution**: Check file size (< 5MB recommended)
- Verify GLB/GLTF format
- Check browser console for errors

**Issue**: Game not starting
- **Solution**: Clear browser cache
- Check browser console for errors
- Verify API endpoints are accessible

**Issue**: Slow performance
- **Solution**: Use 2D interface for low-end devices
- Reduce particle count in 3D version
- Upgrade Render plan

### Support

For issues or questions:
1. Check documentation: [AI_FEATURES.md](AI_FEATURES.md), [ARCHITECTURE.md](ARCHITECTURE.md)
2. Review game logs in Render dashboard
3. Open an issue on GitHub

---

## 📱 Mobile Support

Both 2D and 3D versions are responsive:
- Touch controls supported
- Auto-adjusting UI for small screens
- Optimized for mobile browsers

Recommended browsers:
- Chrome/Edge (best performance)
- Firefox (good support)
- Safari (basic support)

---

## 🎯 Next Steps

1. **Deploy**: Follow the Render deployment steps above
2. **Customize**: Upload your own 3D models
3. **Enable AI**: Add OpenAI API key for full AI features
4. **Share**: Share your game URL with friends
5. **Compete**: Play multiplayer matches!

---

**Live Demo**: [Coming Soon]

**Documentation**: See [README.md](README.md) for game mechanics and strategy

**AI Features**: See [AI_FEATURES.md](AI_FEATURES.md) for AI integration details

---

Made with 💚 for the LastSignal community
