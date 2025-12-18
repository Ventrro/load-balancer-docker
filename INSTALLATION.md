# Panduan Instalasi - Windows

Dokumen ini berisi langkah-langkah lengkap untuk menginstall dan menjalankan project load balancer di Windows.

## 📋 System Requirements

- **OS:** Windows 10/11
- **RAM:** 4 GB minimum
- **Storage:** 5 GB free space
- **Internet:** Untuk download Docker images

## 🐳 Step 1: Instalasi Docker Desktop

### Download Docker Desktop

1. Buka browser
2. Pergi ke: https://www.docker.com/products/docker-desktop
3. Klik **"Download for Windows"**
4. Tunggu download selesai (sekitar 500MB)

### Install Docker Desktop

1. Double-click file `Docker Desktop Installer.exe`
2. Centang **"Use WSL 2 instead of Hyper-V"**
3. Klik **"Ok"**
4. Tunggu instalasi selesai (5-10 menit)
5. Klik **"Close and restart"** jika diminta restart
6. Setelah restart, Docker Desktop akan otomatis buka

### First Time Setup

1. Accept terms and conditions
2. Tunggu Docker Engine start (icon whale di system tray berhenti bergerak)
3. Docker sudah siap digunakan

### Verify Docker Installation

Buka **PowerShell** (klik kanan Start → Windows PowerShell):

```powershell
# Check Docker version
docker --version

# Check Docker Compose version
docker compose version

# Test Docker
docker run hello-world
```

**Expected output:**
```
Docker version 24.x.x
Docker Compose version v2.x.x
Hello from Docker!
```

### Enable Docker Daemon (PENTING!)

1. Buka Docker Desktop
2. Klik **Settings (⚙️)**
3. Pergi ke tab **"General"**
4. **CENTANG:** ☑ "Expose daemon on tcp://localhost:2375 without TLS"
5. Klik **"Apply & Restart"**
6. Tunggu Docker restart selesai

## 🔧 Step 2: Instalasi Git

### Download Git

1. Pergi ke: https://git-scm.com/download/win
2. Download akan otomatis start
3. Tunggu download selesai

### Install Git

1. Double-click installer
2. Klik **"Next"** untuk semua options (gunakan default settings)
3. Klik **"Install"**
4. Klik **"Finish"**

### Verify dan Configure Git

Buka PowerShell baru:

```powershell
# Check Git version
git --version

# Configure Git
git config --global user.name "Nama Anda"
git config --global user.email "email@example.com"
```

## 📁 Step 3: Setup Project

### Create Project Directory

```powershell
# Navigate ke Documents
cd $HOME\Documents

# Create project folder
mkdir load-balancer-docker
cd load-balancer-docker

# Create backend folder
mkdir backend
```

### Create Backend Application

**Create file: `backend/app.py`**

```powershell
notepad backend\app.py
```

**Copy-paste code ini dan save:**

```python
from flask import Flask, jsonify
import socket
import os

app = Flask(__name__)

@app.route('/')
def home():
    hostname = socket.gethostname()
    container_id = os.environ.get('HOSTNAME', 'unknown')
    
    return jsonify({
        'message': 'Hello from backend!',
        'hostname': hostname,
        'container_id': container_id,
        'status': 'running'
    })

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

### Create Dockerfile

**Create file: `backend/Dockerfile`**

```powershell
notepad backend\Dockerfile
```

**Copy-paste code ini dan save:**

```dockerfile
FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir flask

COPY app.py .

EXPOSE 5000

CMD ["python", "app.py"]
```

### Create docker-compose.yml

**Create file: `docker-compose.yml`**

```powershell
notepad docker-compose.yml
```

**Copy-paste code ini dan save:**

```yaml
services:
  traefik:
    image: traefik:v2.10
    container_name: traefik
    command:
      - "--api.insecure=true"
      - "--providers.docker=true"
      - "--providers.docker.exposedbydefault=false"
      - "--entrypoints.web.address=:80"
    ports:
      - "80:80"
      - "8080:8080"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    networks:
      - web

  backend1:
    build: ./backend
    container_name: backend1
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.backend.rule=Host(`localhost`)"
      - "traefik.http.services.backend.loadbalancer.server.port=5000"
    networks:
      - web

  backend2:
    build: ./backend
    container_name: backend2
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.backend.rule=Host(`localhost`)"
      - "traefik.http.services.backend.loadbalancer.server.port=5000"
    networks:
      - web

  backend3:
    build: ./backend
    container_name: backend3
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.backend.rule=Host(`localhost`)"
      - "traefik.http.services.backend.loadbalancer.server.port=5000"
    networks:
      - web

networks:
  web:
    driver: bridge
```

### Create .gitignore

**Create file: `.gitignore`**

```powershell
notepad .gitignore
```

**Copy-paste code ini dan save:**

```
__pycache__/
*.py[cod]
.Python
*.log
.env
.vscode/
.idea/
.DS_Store
Thumbs.db
```

### Verify File Structure

```powershell
tree /F
```

**Expected structure:**
```
load-balancer-docker/
├── backend/
│   ├── app.py
│   └── Dockerfile
├── docker-compose.yml
└── .gitignore
```

## 🚀 Step 4: Build dan Run

### Build Docker Images

```powershell
# Pastikan di folder load-balancer-docker
docker compose build
```

Tunggu 2-5 menit untuk download Python image dan install Flask.

**Expected output:**
```
[+] Building 45.2s (10/10) FINISHED
Successfully built
```

### Start Containers

```powershell
docker compose up -d
```

**Expected output:**
```
[+] Running 4/4
 ✔ Network load-balancer-docker_web  Created
 ✔ Container traefik                 Started
 ✔ Container backend1                Started
 ✔ Container backend2                Started
 ✔ Container backend3                Started
```

### Check Container Status

```powershell
docker compose ps
```

**Expected output:**
```
NAME       IMAGE                 STATUS         PORTS
traefik    traefik:v2.10        Up             0.0.0.0:80->80/tcp, 0.0.0.0:8080->8080/tcp
backend1   ...                  Up             5000/tcp
backend2   ...                  Up             5000/tcp
backend3   ...                  Up             5000/tcp
```

**Semua container harus "Up"!**

## ✅ Step 5: Testing

### Test Backend Response

```powershell
curl http://localhost
```

**Expected output:**
```json
{
  "message": "Hello from backend!",
  "hostname": "backend1",
  "container_id": "abc123",
  "status": "running"
}
```

### Test Traefik Dashboard

Buka browser:
```
http://localhost:8080
```

Anda harus melihat Traefik dashboard dengan 3 backend servers.

### Test Load Balancing

```powershell
for ($i=1; $i -le 10; $i++) {
    $result = curl http://localhost | ConvertFrom-Json
    Write-Host "Request $i -> $($result.hostname)"
}
```

```

**Hostname berubah-ubah = Load balancing bekerja!** ✅

## 🛑 Stop Services

```powershell
# Stop all containers
docker compose down
```

## ❗ Troubleshooting

### Port 80 Sudah Digunakan

```powershell
# Check process
netstat -ano | findstr :80

# Kill process
taskkill /PID <PID> /F
```

### Docker Daemon Not Running

- Pastikan Docker Desktop terbuka dan running
- Check icon whale di system tray

### Traefik Connection Error

1. Docker Desktop → Settings → General
2. Centang: "Expose daemon on tcp://localhost:2375 without TLS"
3. Apply & Restart
4. `docker compose restart`

### Build Failed

```powershell
# Rebuild without cache
docker compose build --no-cache
docker compose up -d
```

---

**Instalasi selesai!** Baca [README.md](README.md) untuk dokumentasi lengkap.
