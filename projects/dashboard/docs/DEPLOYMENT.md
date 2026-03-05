# Deployment Guide

## Local Development

### Prerequisites
- Python 3.8+
- pip
- Virtual environment

### Step 1: Clone & Setup
```bash
git clone https://github.com/brad-sl/giga-chad.git
cd giga-chad
bash setup.sh
source venv/bin/activate
```

### Step 2: Configure
```bash
cp .env.example .env
# Edit .env as needed (optional for local dev)
```

### Step 3: Run
```bash
python3 projects/dashboard/app.py
```

Server starts on `http://localhost:5000`

### Step 4: Test
```bash
pytest projects/dashboard/tests/ -v
```

## Production Deployment

### Prerequisites
- Ubuntu 20.04+ or similar Linux
- Python 3.8+
- Nginx (reverse proxy)
- Systemd (for service management)

### Recommended Architecture
```
Client Browser
    ↓
Nginx (port 80/443)
    ↓
Gunicorn (port 8000)
    ↓
Flask App
    ↓
SQLite DB
```

### Setup Steps

1. **Clone repository**
```bash
git clone https://github.com/brad-sl/giga-chad.git /opt/dashboard
cd /opt/dashboard
```

2. **Create virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r projects/dashboard/requirements.txt
pip install gunicorn
```

3. **Configure production .env**
```bash
cp .env.example .env
# Edit .env:
# - FLASK_ENV=production
# - SECRET_KEY=<random-secure-key>
# - DATABASE_URL=sqlite:///dashboard.db
```

4. **Create Systemd service**

Create `/etc/systemd/system/dashboard.service`:
```ini
[Unit]
Description=Orchestrator Dashboard
After=network.target

[Service]
User=www-data
WorkingDirectory=/opt/dashboard
ExecStart=/opt/dashboard/venv/bin/gunicorn \
  --workers 4 \
  --bind 127.0.0.1:8000 \
  projects.dashboard.app:create_app()
Restart=on-failure
RestartSec=10s

[Install]
WantedBy=multi-user.target
```

5. **Enable & start service**
```bash
sudo systemctl daemon-reload
sudo systemctl enable dashboard
sudo systemctl start dashboard
```

6. **Configure Nginx**

Create `/etc/nginx/sites-available/dashboard`:
```nginx
upstream dashboard {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://dashboard;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

Enable & reload:
```bash
sudo ln -s /etc/nginx/sites-available/dashboard /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

7. **SSL with Let's Encrypt (recommended)**
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

8. **Monitor**
```bash
sudo systemctl status dashboard
sudo tail -f /var/log/syslog | grep dashboard
```

## Database Management

### Backup
```bash
cp projects/dashboard/dashboard.db projects/dashboard/dashboard.db.backup
```

### Migration
If schema changes, restart the app (it auto-migrates on startup).

## Monitoring & Logging

Configure syslog in `/etc/rsyslog.d/30-dashboard.conf`:
```
:programname, isequal, "dashboard" /var/log/dashboard.log
```

## Scaling Considerations

- Single instance: Handles ~100 runs/day easily
- Multiple instances: Use load balancer (Nginx) + shared database
- WebSocket: Requires sticky sessions (Nginx handles this)

## Health Check

```bash
curl http://localhost:5000/api/metrics/overview
```

Should return 200 with metrics JSON.
