# 🛠️ Detailed Setup Guide

## System Requirements

### Minimum Requirements
- CPU: 2 cores
- RAM: 4GB
- Storage: 500MB free space
- OS: Windows 10+, macOS 10.14+, Linux (Ubuntu 18.04+)

### Recommended
- CPU: 4+ cores
- RAM: 8GB+
- GPU: Any dedicated GPU (for smoother 3D rendering)
- Display: 1920x1080 or higher

---

## Step-by-Step Installation

### 1. Install Python

#### Windows
```powershell
# Download from python.org or use winget
winget install Python.Python.3.11

# Verify installation
python --version
```

#### macOS
```bash
# Using Homebrew
brew install python@3.11

# Verify
python3 --version
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3.11 python3-pip

# Verify
python3 --version
```

### 2. Install Node.js

#### Windows
```powershell
# Download from nodejs.org or use winget
winget install OpenJS.NodeJS.LTS

# Verify
node --version
npm --version
```

#### macOS
```bash
brew install node

# Verify
node --version
npm --version
```

#### Linux
```bash
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt install -y nodejs

# Verify
node --version
npm --version
```

### 3. Clone/Download Project

```bash
# If using Git
git clone https://github.com/yourusername/rampage-refactor.git
cd rampage-refactor

# OR download ZIP and extract
unzip rampage-refactor.zip
cd rampage-refactor
```

### 4. Backend Setup

```bash
cd backend

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Start backend
python server.py
```

You should see:
```
🦖 Rampage Refactor Backend
🚀 WebSocket server running on ws://localhost:8765
📡 HTTP server running on http://localhost:8765
✨ Ready to scan codebases!
```

### 5. Frontend Setup

**Open a NEW terminal window** (keep backend running)

```bash
cd frontend

# Install dependencies
npm install
# OR with yarn:
yarn install

# Copy environment template
cp .env.example .env

# Start frontend
npm start
# OR with yarn:
yarn start
```

Your browser should automatically open to `http://localhost:3000`

---

## Verification Checklist

✅ **Backend running?**
```bash
curl http://localhost:8765/health
# Should return: {"status":"healthy"}
```

✅ **Frontend loaded?**
- Open http://localhost:3000 in browser
- Should see "Code City Apocalypse" interface

✅ **WebSocket connected?**
- Look for green "Connected" status in UI
- Check browser console (F12) - no red errors

✅ **Can scan folders?**
- Click "Scan Codebase"
- Enter a test folder path
- Should see buildings appear

---

## Common Issues

### "Port 8765 already in use"

**Kill existing process:**
```bash
# Linux/macOS
lsof -ti:8765 | xargs kill -9

# Windows PowerShell
Get-Process -Id (Get-NetTCPConnection -LocalPort 8765).OwningProcess | Stop-Process
```

**OR change port:**
Edit `backend/.env`:
```env
PORT=8766
```

And `frontend/.env`:
```env
REACT_APP_BACKEND_URL=http://localhost:8766
```

### "Module not found" errors

```bash
# Backend
cd backend
pip install -r requirements.txt --force-reinstall

# Frontend
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### "WebSocket connection failed"

1. Make sure backend is running
2. Check browser console for errors
3. Try disabling browser extensions (ad blockers)
4. Check firewall settings

### Permission errors on Linux/macOS

```bash
# If you get permission errors scanning folders
sudo python server.py

# OR give your user read permissions
sudo chmod -R +r /path/to/folder/to/scan
```

---

## Development Mode

### Hot Reload (Auto-restart on code changes)

**Backend:**
```bash
cd backend
pip install watchdog
python server.py --reload
```

**Frontend:**
```bash
cd frontend
npm start  # Already has hot reload
```

### Debug Mode

**Backend:**
Edit `backend/.env`:
```env
DEBUG=true
LOG_LEVEL=debug
```

**Frontend:**
```bash
REACT_APP_DEBUG=true npm start
```

---

## Production Deployment

### Build Frontend

```bash
cd frontend
npm run build
# Creates optimized build in frontend/build/
```

### Run Backend in Production

```bash
cd backend
pip install gunicorn
gunicorn server:app --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8765
```

### Serve Frontend

Option 1: Using Python
```bash
cd frontend/build
python -m http.server 3000
```

Option 2: Using Nginx
```nginx
server {
    listen 80;
    server_name your-domain.com;
    root /path/to/frontend/build;
    
    location / {
        try_files $uri /index.html;
    }
    
    location /api {
        proxy_pass http://localhost:8765;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

---

## Next Steps

1. Read [API Documentation](API.md)
2. Try scanning your first codebase
3. Customize city appearance (see `frontend/src/config.js`)
4. Report bugs or request features

---

**Need more help?** Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
