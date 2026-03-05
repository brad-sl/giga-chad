# Dashboard Setup & Usage

## Quick Start

```bash
# 1. Run setup
bash setup.sh

# 2. Activate environment
source venv/bin/activate

# 3. Start dashboard
python3 projects/dashboard/app.py

# 4. Open browser
# http://localhost:5000
```

## System Requirements
- Python 3.8+
- pip
- git
- ~500MB disk space

## Project Structure

```
projects/dashboard/
├── app.py                 # Flask server + API endpoints
├── models.py              # SQLAlchemy ORM models
├── database.py            # Database schema
├── socketio_config.py     # WebSocket configuration
├── events.py              # Event system
├── static/
│   ├── websocket.js       # WebSocket client
│   ├── index.html         # Dashboard UI
│   ├── app.js             # Frontend logic
│   └── styles.css         # Styling
├── requirements.txt       # Python dependencies
└── tests/
    ├── test_api.py        # API endpoint tests
    └── test_websocket.py  # WebSocket tests
```

## Available Commands

```bash
make setup      # Full setup
make run        # Start server
make test       # Run all tests
make test-api   # Test API only
make test-ws    # Test WebSocket only
make clean      # Clean build artifacts
make docs       # Show docs location
```

## Configuration

Edit `.env` file:
```
FLASK_ENV=development
FLASK_DEBUG=true
DATABASE_URL=sqlite:///dashboard.db
SECRET_KEY=your-secret-key-here
SOCKETIO_PING_INTERVAL=25
SOCKETIO_PING_TIMEOUT=60
```

## Troubleshooting

See TROUBLESHOOTING.md for common issues.

## API Documentation

See API.md for endpoint details.

## Deployment

See DEPLOYMENT.md for production setup.
