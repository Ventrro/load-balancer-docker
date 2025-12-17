\# Panduan Instalasi (Windows)



\## Step 1: Install Docker Desktop

1\. Download: https://www.docker.com/products/docker-desktop

2\. Install dan restart

3\. Verify: `docker --version`



\## Step 2: Clone Project

```bash

git clone https://github.com/username/load-balancer-docker.git

cd load-balancer-docker

```



\## Step 3: Build \& Run

```bash

docker compose build

docker compose up -d

```



\## Step 4: Verify

\- Open: http://localhost

\- Dashboard: http://localhost:8080



\## Stop Services

```bash

docker compose down

```

