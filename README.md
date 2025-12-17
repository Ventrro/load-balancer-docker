\# Load Balancing Aplikasi dengan Docker dan Traefik



Project ini mengimplementasikan load balancing menggunakan Docker dan Traefik.



\## Authors

\*\*Nama:\*\* Muhammad Abdillah Martadinata 

\*\*NPM:\*\* 062430701451

\*\*Kelas:\*\* 3CD



\*\*Nama:\*\* Celsya Intan Kinanti

\*\*NPM:\*\* 062430701443

\*\*Kelas:\*\* 3CD



\*\*Nama:\*\* Fathir Muhammad Evantra

\*\*NPM:\*\* 06243070144

\*\*Kelas:\*\* 3CD





\## Teknologi

\- Docker \& Docker Compose

\- Traefik v2.10 (Load Balancer)

\- Python 3.11 + Flask (Backend)



\## Arsitektur

```

Internet → Traefik (Port 80, 8080) → Backend1, Backend2, Backend3

```



\## Cara Menjalankan



\### Prerequisites

\- Docker Desktop terinstall

\- Port 80 dan 8080 tersedia



\### Instalasi

```bash

\# Clone repository

git clone https://github.com/username/load-balancer-docker.git

cd load-balancer-docker



\# Build dan start

docker compose up --build -d



\# Check status

docker compose ps

```



\### Testing

\- Backend: http://localhost

\- Dashboard: http://localhost:8080



\### Stop

```bash

docker compose down

```



\## ✅ Fitur

✅ 3 Backend containers  

✅ Load balancing (round-robin)  

✅ Service discovery otomatis  

✅ Health checks  

✅ Traefik dashboard  



\## 📊 Testing Load Balancer



Request beberapa kali dan lihat hostname berubah:

```powershell

for ($i=1; $i -le 10; $i++) {

&nbsp;   curl http://localhost

}

```



\## Troubleshooting



\*\*Port 80 sudah digunakan:\*\*

```bash

\# Ganti port di docker-compose.yml

ports:

&nbsp; - "8000:80"

```



\*\*Container tidak start:\*\*

```bash

docker compose logs traefik

docker compose logs backend1

```



\## Repository

https://github.com/Ventrro/load-balancer-docker

