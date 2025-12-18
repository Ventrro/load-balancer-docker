Load Balancing Aplikasi dengan Docker dan Traefik

Project ini mengimplementasikan load balancing menggunakan Docker dan Traefik sebagai reverse proxy untuk mendistribusikan traffic ke beberapa backend container.

👥 Authors

Nama: Muhammad Abdillah Martadinata  
NIM: 062430701451  
Kelas: 3CD

Nama: Celsya Intan Kinanti  
NIM: 062430701443  
Kelas: 3CD  

Nama: Fathir Muhammad Evantra  
NIM: 062430701445  
Kelas: 3CD    


📋 Daftar Isi

- [Deskripsi Project](#deskripsi-project)
- [Teknologi yang Digunakan](#teknologi-yang-digunakan)
- [Fitur](#fitur)
- [Cara Instalasi](#cara-instalasi)
- [Cara Penggunaan](#cara-penggunaan)
- [Testing Load Balancer](#testing-load-balancer)
- [Troubleshooting](#troubleshooting)
- [Author](#author)

🎯 Deskripsi Project

Project ini mendemonstrasikan implementasi load balancing dengan menggunakan:
- **Traefik v2.10** sebagai reverse proxy dan load balancer
- **3 backend containers** yang menjalankan aplikasi Flask sederhana
- **Docker Compose** untuk orchestration

Load balancer secara otomatis mendistribusikan incoming requests ke multiple backend containers menggunakan round-robin algorithm.

🛠 Teknologi yang Digunakan

- Docker Desktop (Windows)
- Traefik v2.10 (Load Balancer)
- Python** 3.11
- Flask** (Web Framework)

✅ Fitur

- ✅ Load balancing otomatis dengan 3 backend containers
- ✅ Round-robin distribution
- ✅ Traefik dashboard untuk monitoring
- ✅ Health checks otomatis
- ✅ Fault tolerance

🚀 Cara Instalasi

Lihat [INSTALLATION.md] untuk panduan instalasi lengkap.

Quick Start

```powershell
# 1. Navigate ke project directory
cd load-balancer-docker

# 2. Build dan start containers
docker compose build
docker compose up -d

# 3. Test
curl http://localhost

📖 Cara Penggunaan

Mengakses Aplikasi

Backend Application:
- URL: `http://localhost`
- Response: JSON dengan informasi container

Traefik Dashboard:
- URL: `http://localhost:8080`
- Dashboard untuk monitoring status services

API Endpoints

GET /
Endpoint utama yang menampilkan informasi container.

Request:
```powershell
curl http://localhost
```

Response:
```json
{
  "message": "Hello from backend!",
  "hostname": "backend1",
  "container_id": "a1b2c3d4e5f6",
  "status": "running"
}
```

GET /health
Health check endpoint.

Request:
```powershell
curl http://localhost/health
```

Response:
```json
{
  "status": "healthy"
}
```

🧪 Testing Load Balancer

Test 1: Multiple Requests

Jalankan request beberapa kali untuk melihat load balancing bekerja:

```powershell
for ($i=1; $i -le 10; $i++) {
    curl http://localhost
    Write-Host ""
}
```

Expected Result:  
Anda akan melihat `hostname` berubah-ubah antara backend1, backend2, dan backend3.

Test 2: Load Balancing dengan Hostname

```powershell
for ($i=1; $i -le 10; $i++) {
    $result = curl http://localhost | ConvertFrom-Json
    Write-Host "Request $i -> $($result.hostname)"
}
```

Test 3: Container Failure Simulation

Test bagaimana load balancer menangani failure:

```powershell
Stop satu backend
docker compose stop backend1

Test masih bisa akses
curl http://localhost

Start kembali
docker compose start backend1
```

🔧 Commands

Basic Commands

```powershell
# Start services
docker compose up -d

# Stop services
docker compose down

# Check status
docker compose ps

# View logs
docker compose logs -f

# Restart service
docker compose restart backend1
```

❗ Troubleshooting

Issue 1: Port 80 Already in Use

Solusi:
```powershell
# Check process using port 80
netstat -ano | findstr :80

# Kill process (ganti <PID> dengan nomor PID)
taskkill /PID <PID> /F
```

Atau ganti port di `docker-compose.yml`:
```yaml
ports:
  - "8000:80"  # Ganti 80 ke 8000
```

### Issue 2: Container Tidak Start

Solusi:
```powershell
# Check logs
docker compose logs

# Rebuild
docker compose build --no-cache
docker compose up -d
```

Issue 3: 404 Not Found

Solusi:
```powershell
# Verify containers running
docker compose ps

# Check Traefik dashboard
# Buka http://localhost:8080

# Restart Traefik
docker compose restart traefik
```

Issue 4: Traefik Connection Error

Gejala:
```
Provider connection error
```

Solusi:
1. Buka Docker Desktop → Settings → General
2. Centang: "Expose daemon on tcp://localhost:2375 without TLS"
3. Apply & Restart
4. Restart containers: `docker compose restart`

📝 Struktur Project

```
load-balancer-docker/
├── README.md
├── INSTALLATION.md
├── docker-compose.yml
├── .gitignore
└── backend/
    ├── Dockerfile
    └── app.py
```

📄 License

Project ini dibuat untuk keperluan project.

---

Repository: https://github.com/Ventrro/load-balancer-docker  
