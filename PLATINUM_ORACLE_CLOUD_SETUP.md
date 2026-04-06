# Oracle Cloud Free VM Setup Guide

**Deploy your AI Employee on Cloud 24/7**

---

## 🎯 Oracle Cloud Free Tier

**What you get:**
- Up to 4 ARM Ampere A1 Compute instances
- 24 GB RAM total
- 200 GB block storage total
- Always Free (no time limit)

---

## 📋 Step 1: Create Oracle Cloud Account

1. Go to: https://www.oracle.com/cloud/free/
2. Click "Start for free"
3. Fill in registration form
4. Verify identity (phone, credit card)
5. Wait for account activation (email)

---

## 📋 Step 2: Create SSH Key Pair

**On your local machine:**

```bash
# Generate SSH key
ssh-keygen -t rsa -b 2048 -f ~/.ssh/oci_key -N ""

# Private key: ~/.ssh/oci_key
# Public key: ~/.ssh/oci_key.pub
```

**Save the public key content** - you'll need it for the VM.

---

## 📋 Step 3: Create Cloud VM

### 3.1 Create Compartment (Optional)

1. Go to **Identity & Security** → **Compartments**
2. Click **Create Compartment**
3. Name: `ai-employee`

### 3.2 Create Instance

1. Go to **Compute** → **Instances**
2. Click **Create Instance**

**Configuration:**
- **Compartment:** Select yours
- **Instance Name:** `ai-employee-cloud`
- **Availability Domain:** Any (e.g., AD-1)
- **Image:** Oracle Linux 8 or Ubuntu 22.04
- **Shape:** VM.Standard.A1.Flex (ARM)
- **OCPUs:** 2
- **Memory:** 12 GB

**Networking:**
- **Virtual Cloud Network:** Create new (default)
- **Subnet:** Public
- **Assign Public IP:** ✅ Yes

**SSH Keys:**
- **SSH Keys:** Paste your public key content
- Or upload the .pub file

**Boot Volume:**
- **Size:** 50 GB (minimum)

**Cloud Init:** (Optional - auto setup)
```yaml
#cloud-config
package_update: true
packages:
  - docker
  - docker-compose
  - python3
  - python3-pip
  - git
users:
  - name: aiemployee
    ssh_authorized_keys:
      - <YOUR_PUBLIC_KEY>
    sudo: ALL=(ALL) NOPASSWD:ALL
    shell: /bin/bash
```

3. Click **Create**
4. Wait for instance to be RUNNING (2-5 minutes)

---

## 📋 Step 4: Configure Security List

### Allow Required Ports:

1. Go to **Networking** → **Virtual Cloud Networks**
2. Click your VCN
3. Click **Security Lists**
4. Click **Default Security List**

**Add Ingress Rules:**

| Source | IP Protocol | Source Port Range | Destination Port Range | Description |
|--------|-------------|-------------------|----------------------|-------------|
| 0.0.0.0/0 | TCP | All | 22 | SSH |
| 0.0.0.0/0 | TCP | All | 8069 | Odoo |
| 0.0.0.0/0 | TCP | All | 80 | HTTP |
| 0.0.0.0/0 | TCP | All | 443 | HTTPS |
| 0.0.0.0/0 | TCP | All | 8080 | PGAdmin |

---

## 📋 Step 5: Connect to VM

**Get Public IP from Oracle Console:**
- Go to **Compute** → **Instances**
- Copy the **Public IP Address**

**Connect via SSH:**
```bash
ssh -i ~/.ssh/oci_key opc@<PUBLIC_IP>

# Or for Ubuntu:
ssh -i ~/.ssh/oci_key ubuntu@<PUBLIC_IP>
```

---

## 📋 Step 6: Install Docker

```bash
# Update system
sudo yum update -y  # For Oracle Linux
# OR
sudo apt update -y  # For Ubuntu

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker

# Verify
docker --version
docker run hello-world
```

---

## 📋 Step 7: Install Docker Compose

```bash
# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Verify
docker-compose --version
```

---

## 📋 Step 8: Install Python & Dependencies

```bash
# Install Python
sudo yum install python3 python3-pip -y  # Oracle Linux
# OR
sudo apt install python3 python3-pip -y  # Ubuntu

# Install required packages
pip3 install --user python-dotenv requests facebook-sdk

# Verify
python3 --version
pip3 --version
```

---

## 📋 Step 9: Clone AI Employee Repository

```bash
# Create directory
mkdir -p /opt/ai-employee
cd /opt/ai-employee

# Clone your repository (or copy files)
git clone <YOUR_REPO_URL> .
# OR manually copy files

# Set permissions
sudo chown -R $USER:$USER /opt/ai-employee
chmod -R 755 /opt/ai-employee
```

---

## 📋 Step 10: Configure Environment

```bash
# Create .env file
cd /opt/ai-employee
nano .env

# Add your credentials:
FACEBOOK_PAGE_ACCESS_TOKEN=EAAN...
FACEBOOK_PAGE_ID=1004531386081562
FACEBOOK_APP_ID=969420109076481
```

---

## 📋 Step 11: Start Cloud Services

```bash
# Start Odoo
cd /opt/ai-employee/odoo
docker-compose up -d

# Start watchers (as background services)
nohup python3 /opt/ai-employee/AI_Employee_Vault/scripts/facebook_comment_watcher.py > /var/log/watcher.log 2>&1 &

# Verify
docker ps
ps aux | grep python
```

---

## 📋 Step 12: Setup Systemd Services (Auto-start)

### Create Cloud Orchestrator Service:

```bash
sudo nano /etc/systemd/system/ai-employee-cloud.service
```

**Content:**
```ini
[Unit]
Description=AI Employee Cloud Orchestrator
After=network.target docker.service
Requires=docker.service

[Service]
Type=simple
User=opc
WorkingDirectory=/opt/ai-employee
ExecStart=/usr/bin/python3 /opt/ai-employee/AI_Employee_Vault/scripts/cloud_orchestrator.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Enable and start:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable ai-employee-cloud
sudo systemctl start ai-employee-cloud
sudo systemctl status ai-employee-cloud
```

---

## 📋 Step 13: Setup HTTPS (Optional but Recommended)

### Install Nginx:

```bash
sudo yum install nginx -y  # Oracle Linux
# OR
sudo apt install nginx -y  # Ubuntu

sudo systemctl enable nginx
sudo systemctl start nginx
```

### Configure Nginx for Odoo:

```bash
sudo nano /etc/nginx/conf.d/odoo.conf
```

**Content:**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8069;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

### Get SSL Certificate (Let's Encrypt):

```bash
# Install Certbot
sudo yum install certbot python3-certbot-nginx -y  # Oracle Linux
# OR
sudo apt install certbot python3-certbot-nginx -y  # Ubuntu

# Get certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo systemctl enable certbot.timer
```

---

## 📋 Step 14: Setup Monitoring

### Health Check Script:

```bash
nano /opt/ai-employee/health_check.sh
```

**Content:**
```bash
#!/bin/bash
echo "=== AI Employee Health Check ==="
echo "Date: $(date)"
echo ""

# Check Docker containers
echo "Docker Containers:"
docker ps --format "table {{.Names}}\t{{.Status}}"
echo ""

# Check Odoo
if curl -s http://localhost:8069 > /dev/null; then
    echo "✅ Odoo: Running"
else
    echo "❌ Odoo: Not responding"
fi

# Check Python processes
echo ""
echo "Python Processes:"
ps aux | grep python | grep -v grep

# Check disk space
echo ""
echo "Disk Usage:"
df -h /
```

**Make executable:**
```bash
chmod +x /opt/ai-employee/health_check.sh
```

---

## 📋 Step 15: Setup Backup

### Backup Script:

```bash
nano /opt/ai-employee/backup.sh
```

**Content:**
```bash
#!/bin/bash
BACKUP_DIR="/opt/backups"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Backup Odoo database
docker exec odoo_postgres pg_dump -U odoo ai_employee_db > $BACKUP_DIR/odoo_db_$DATE.sql

# Backup vault (excluding secrets)
rsync -av --exclude='.env' --exclude='*.pem' /opt/ai-employee/AI_Employee_Vault/ $BACKUP_DIR/vault_$DATE/

# Keep only last 7 backups
find $BACKUP_DIR -type f -mtime +7 -delete

echo "Backup completed: $DATE"
```

**Schedule daily backup:**
```bash
crontab -e
```

**Add:**
```
0 2 * * * /opt/ai-employee/backup.sh
```

---

## ✅ Verification Checklist

- [ ] VM is RUNNING in Oracle Console
- [ ] SSH connection works
- [ ] Docker is installed
- [ ] Docker Compose is installed
- [ ] Python3 is installed
- [ ] Odoo container is running
- [ ] Port 8069 is accessible
- [ ] Security rules allow required ports
- [ ] Systemd service is running
- [ ] HTTPS is configured (if using domain)
- [ ] Backup script is scheduled

---

## 🔧 Useful Commands

```bash
# Check service status
sudo systemctl status ai-employee-cloud

# View logs
sudo journalctl -u ai-employee-cloud -f

# Restart service
sudo systemctl restart ai-employee-cloud

# Check Docker containers
docker ps

# View Odoo logs
docker logs odoo_community_19 -f

# Check disk usage
df -h

# Check memory usage
free -h

# Restart Odoo
cd /opt/ai-employee/odoo && docker-compose restart
```

---

**Your AI Employee is now running 24/7 on Oracle Cloud!** 🚀
