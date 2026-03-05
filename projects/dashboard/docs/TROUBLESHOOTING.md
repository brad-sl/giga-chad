# Troubleshooting Guide

## Common Issues

### 1. Port Already in Use

**Error:** `Address already in use`

**Solution:**
```bash
# Find process on port 5000
lsof -i :5000

# Kill it
kill -9 <PID>

# Or use different port
export FLASK_PORT=5001
python3 projects/dashboard/app.py
```

### 2. Database Locked

**Error:** `database is locked`

**Solution:**
```bash
# Close any open connections
pkill -f "python3 projects/dashboard/app.py"

# Remove lock file
rm -f projects/dashboard/dashboard.db-journal

# Restart app
python3 projects/dashboard/app.py
```

### 3. WebSocket Connection Refused

**Error:** `WebSocket connection to ws://... failed`

**Solution:**
```bash
# Check Flask-SocketIO is installed
pip install flask-socketio python-socketio

# Check CORS settings in .env
SOCKETIO_CORS_ALLOWED_ORIGINS=*

# Restart app
python3 projects/dashboard/app.py
```

### 4. Missing Dependencies

**Error:** `ModuleNotFoundError: No module named '...'`

**Solution:**
```bash
# Reinstall dependencies
source venv/bin/activate
pip install -r projects/dashboard/requirements.txt
```

### 5. Browser Won't Connect

**Error:** Chrome shows "Cannot GET /"

**Solution:**
- Verify server is running: `curl http://localhost:5000`
- Check browser console (F12) for errors
- Try different browser
- Clear browser cache: Ctrl+Shift+Delete

### 6. Tests Fail

**Error:** `pytest: command not found`

**Solution:**
```bash
# Install test dependencies
pip install pytest pytest-flask

# Run tests with full path
python3 -m pytest projects/dashboard/tests/ -v
```

### 7. Database Migration Issues

**Error:** `Column not found` or schema mismatch

**Solution:**
```bash
# Backup current database
cp projects/dashboard/dashboard.db projects/dashboard/dashboard.db.old

# Delete and reinitialize
rm projects/dashboard/dashboard.db

# Run setup script (creates fresh DB)
bash setup.sh
```

### 8. Frontend Not Loading

**Error:** CSS/JS files 404

**Solution:**
- Check files exist: `ls -la projects/dashboard/static/`
- Verify Flask app.py has `static_folder` set
- Check console in browser (F12) for exact 404 paths
- Restart Flask: `Ctrl+C` then run app again

## Debug Mode

Enable verbose logging:

```bash
export FLASK_ENV=development
export FLASK_DEBUG=true
export FLASK_LOG_LEVEL=DEBUG

python3 projects/dashboard/app.py
```

This shows:
- All HTTP requests
- SQL queries
- WebSocket events
- Full stack traces

## Getting Help

1. Check error message carefully (usually tells you exactly what's wrong)
2. Search terminal output for "ERROR" or "CRITICAL"
3. Check browser console (F12 → Console tab)
4. Run tests: `pytest projects/dashboard/tests/ -v` (shows what works)
5. Try fresh setup: `bash setup.sh` (starts clean)

## Performance Issues

**Slow dashboard response:**
```bash
# Check if database is slow
sqlite3 projects/dashboard/dashboard.db "ANALYZE;"

# Restart Flask in production mode
FLASK_ENV=production python3 projects/dashboard/app.py
```

**WebSocket lag:**
- Reduce SOCKETIO_PING_INTERVAL in .env (25 is default)
- Check network latency: `ping localhost`
- Restart browser connection

## Reset Everything

```bash
# Complete reset (be careful!)
bash setup.sh  # Recreates venv, installs deps, fresh DB
source venv/bin/activate
python3 projects/dashboard/app.py
```
