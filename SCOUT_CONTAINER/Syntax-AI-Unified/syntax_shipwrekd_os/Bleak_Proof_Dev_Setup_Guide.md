
# Bleak-Proof Dev Setup Guide

## 1️⃣ Overview

This setup allows you to:

- Develop locally on Android using **Termux + code-server (VS Code in browser)**  
- Sync code with GitHub and optionally a **remote Linux VM** (Oracle Cloud Free Tier, Fly.io, or Railway)  
- Use **ChatGPT / Codex-like AI** for code generation and refactoring  
- Keep your dev environment portable, low-cost, and resilient  

## 2️⃣ Requirements

- Android device (ARM64 recommended)  
- Termux (install from **F-Droid**)  
- GitHub account  
- Optional: free Linux VPS (Oracle Cloud / Fly.io / Railway) for heavier builds  

## 3️⃣ One-Tap Installer Script

Save this as `bleak_full_setup.sh` in Termux:

\`\`\`bash
#!/data/data/com.termux/files/usr/bin/bash
# Bleak-Proof Dev Setup: Full One-Tap Installer

echo "🚀 Starting Bleak-Proof Dev Setup..."

# Update packages
pkg update -y && pkg upgrade -y

# Install core dev tools
pkg install -y git nodejs python openssh neovim wget tar

# SSH key setup
read -p "Enter your GitHub email: " GIT_EMAIL
ssh-keygen -t ed25519 -C "$GIT_EMAIL"
echo "📋 Your public key:"
cat ~/.ssh/id_ed25519.pub
echo "Copy this key to GitHub → Settings → SSH Keys → New Key"
read -p "Press Enter after adding your SSH key..."

# Git config
git config --global user.name "Bleak"
git config --global user.email "$GIT_EMAIL"

# Create project directories
mkdir -p ~/ModMind/mod_core ~/ModMind/equilex ~/ModMind/equinex ~/ModMind/co-witness ~/ModMind/firefly
mkdir -p ~/shipwrekd-os/system ~/shipwrekd-os/ai_drivers ~/shipwrekd-os/user_interface ~/shipwrekd-os/assets
mkdir -p ~/shared_libraries

# code-server setup
wget https://github.com/coder/code-server/releases/download/v4.20.1/code-server-4.20.1-linux-arm64.tar.gz
tar -xzf code-server-4.20.1-linux-arm64.tar.gz
cd code-server-4.20.1-linux-arm64
./code-server --bind-addr 0.0.0.0:8080 --auth none &

# Workspace template
cat > ~/ModMind.code-workspace <<EOL
{
  "folders": [
    { "path": "ModMind/mod_core" },
    { "path": "ModMind/equilex" },
    { "path": "ModMind/equinex" },
    { "path": "ModMind/co-witness" },
    { "path": "ModMind/firefly" },
    { "path": "shipwrekd-os/system" },
    { "path": "shipwrekd-os/ai_drivers" },
    { "path": "shipwrekd-os/user_interface" },
    { "path": "shipwrekd-os/assets" },
    { "path": "shared_libraries" }
  ],
  "settings": {
    "terminal.integrated.shell.linux": "/data/data/com.termux/files/usr/bin/bash",
    "files.autoSave": "afterDelay",
    "files.autoSaveDelay": 500,
    "editor.tabSize": 2,
    "editor.formatOnSave": true,
    "python.pythonPath": "/data/data/com.termux/files/usr/bin/python3",
    "eslint.enable": true
  }
}
EOL

echo "✅ Bleak-Proof Dev Setup Complete!"
echo "Open your browser → localhost:8080 to access VS Code Web."
\`\`\`

## 4️⃣ How to Use the Script

1. Open Termux  
2. Create the script file:

\`\`\`bash
nano bleak_full_setup.sh
\`\`\`

3. Paste the content from the “One-Tap Installer Script” section, save (`CTRL+O`, `ENTER`, `CTRL+X`)  
4. Make it executable:

\`\`\`bash
chmod +x bleak_full_setup.sh
\`\`\`

5. Run the script:

\`\`\`bash
bash bleak_full_setup.sh
\`\`\`

6. Enter GitHub email, copy SSH key to GitHub, then open browser → `localhost:8080`

## 5️⃣ Remote VM Integration (Optional)

- Oracle Cloud Free Tier / Fly.io / Railway  
- SSH into VM:  

\`\`\`bash
ssh ubuntu@YOUR_VM_IP
sudo apt update && sudo apt install git python3 nodejs npm
\`\`\`

- Optional: install `code-server` on VM  
- Auto-sync with Termux:  

\`\`\`bash
rsync -avz ~/ModMind/ ubuntu@YOUR_VM_IP:/home/ubuntu/ModMind/
rsync -avz ~/shipwrekd-os/ ubuntu@YOUR_VM_IP:/home/ubuntu/shipwrekd-os/
rsync -avz ~/shared_libraries/ ubuntu@YOUR_VM_IP:/home/ubuntu/shared_libraries/
\`\`\`

## 6️⃣ AI Dev Loop

- Use ChatGPT or OpenAI API to refactor / generate code  
- Copy output into VS Code workspace  

## 7️⃣ Recommended Project Structure

```
/home/bleak/
├── ModMind/
│   ├── mod_core/
│   ├── equilex/
│   ├── equinex/
│   ├── co-witness/
│   └── firefly/
├── shipwrekd-os/
│   ├── system/
│   ├── ai_drivers/
│   ├── user_interface/
│   └── assets/
└── shared_libraries/
```

## 8️⃣ Tips

- Keep Termux updated: `pkg update && pkg upgrade -y`  
- Use `tmux` or `screen` to keep code-server running in background  
- Optional: HTTPS + password for code-server for remote access  

## 9️⃣ Cost Breakdown

| Service | Cost | Notes |
|---------|------|-------|
| Termux | Free | Android local dev |
| Oracle Cloud | Free | Always Free ARM instance |
| GitHub | Free | Version control |
| code-server | Free | VS Code Web |
| ChatGPT API | Free / Paid | AI dev assistant |
