# 🐳 Odoo on Docker - Complete Setup Guide

**Status:** Docker needs to be started

---

## ⚠️ ISSUE: Docker is Not Running

**Error:**
```
error during connect: Get "http://%2F%2F.%2Fpipe%2FdockerDesktopLinuxEngine/...
The system cannot find the file specified.
```

**This means:** Docker Desktop is not running on your computer.

---

## ✅ HOW TO FIX

### Step 1: Start Docker Desktop

**Option A: From Start Menu**
1. Press **Windows Key**
2. Type **"Docker Desktop"**
3. Click **Docker Desktop**
4. Wait for it to start (whale icon in system tray will turn green)

**Option B: From Desktop**
1. Find Docker Desktop icon on desktop
2. Double-click to open
3. Wait for it to start

**Option C: From Command**
```bash
"C:\Program Files\Docker\Docker\Docker Desktop.exe"
```

---

### Step 2: Wait for Docker to Start

**You'll know it's ready when:**
- ✅ Docker icon in system tray turns **green**
- ✅ No more "Docker is starting" message
- ✅ You can run: `docker ps`

---

### Step 3: Verify Docker is Running

```bash
docker ps
```

**Expected:** List of containers (might be empty)

---

### Step 4: Start Odoo

```bash
cd D:\Download\working_hackthoon_zero_0\odoo
docker-compose up -d
```

**Expected:**
```
[+] Running 3/3
 ✔ Container odoo_postgres      Started
 ✔ Container odoo_community_19  Started
 ✔ Container odoo_pgadmin       Started
```

---

### Step 5: Verify Odoo is Running

```bash
# Check containers
docker-compose ps

# Or
docker ps
```

**Expected:**
```
CONTAINER ID   IMAGE          STATUS
xxxxx          odoo:19.0      Up
xxxxx          postgres:15    Up
xxxxx          pgadmin4       Up
```

---

### Step 6: Access Odoo

**Open in your browser:**
```
http://localhost:8069
```

**You should see:** Odoo login/setup page!

---

## 🎯 Quick Commands

### Start Odoo:
```bash
cd D:\Download\working_hackthoon_zero_0\odoo
docker-compose up -d
```

### Stop Odoo:
```bash
cd D:\Download\working_hackthoon_zero_0\odoo
docker-compose down
```

### Check Status:
```bash
cd D:\Download\working_hackthoon_zero_0\odoo
docker-compose ps
```

### View Logs:
```bash
cd D:\Download\working_hackthoon_zero_0\odoo
docker-compose logs -f
```

### Restart Odoo:
```bash
cd D:\Download\working_hackthoon_zero_0\odoo
docker-compose restart
```

---

## 🔧 Troubleshooting

### Docker Won't Start:

1. **Check if Docker is installed:**
   ```bash
   docker --version
   ```

2. **If not installed, download:**
   ```
   https://www.docker.com/products/docker-desktop/
   ```

3. **Install Docker Desktop**
4. **Restart your computer**
5. **Try again**

### Odoo Won't Start:

1. **Check Docker is running:**
   ```bash
   docker ps
   ```

2. **Check ports are free:**
   - Port 8069 (Odoo)
   - Port 5432 (PostgreSQL)
   - Port 8080 (PGAdmin)

3. **View logs:**
   ```bash
   cd odoo
   docker-compose logs odoo
   ```

---

## ✅ Verification Checklist

After starting Odoo, verify:

- [ ] Docker Desktop is running (green whale icon)
- [ ] `docker ps` shows containers
- [ ] `docker-compose ps` shows 3 containers Up
- [ ] Can access http://localhost:8069
- [ ] Odoo setup page appears

---

## 🎉 After Odoo is Running

**Your AI Employee will have:**

| Component | Status |
|-----------|--------|
| Facebook | ✅ Working |
| Instagram | ✅ Working |
| Twitter | ✅ Working |
| Gmail | ✅ Working |
| **Odoo** | ✅ **Running on Docker** |
| LinkedIn | ⚠️ Scripts Complete |

---

**Next:** Start Docker Desktop, then run `docker-compose up -d` in the odoo folder! 🚀
