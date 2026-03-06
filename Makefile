.PHONY: help setup install run test clean docs

help:
	@echo "Orchestrator Dashboard - Available targets:"
	@echo "  make setup       - Full setup (venv + deps + DB)"
	@echo "  make install     - Install dependencies only"
	@echo "  make run         - Start dashboard (localhost:5000)"
	@echo "  make test        - Run all tests"
	@echo "  make test-api    - Test backend API only"
	@echo "  make test-ws     - Test WebSocket only"
	@echo "  make clean       - Clean build artifacts"
	@echo "  make docs        - Build documentation"

setup:
	bash setup.sh

install:
	pip install -r projects/dashboard/requirements.txt

run:
	python3 projects/dashboard/app.py

test:
	pytest projects/dashboard/tests/ -v

test-api:
	pytest projects/dashboard/tests/test_api.py -v

test-ws:
	pytest projects/dashboard/tests/test_websocket.py -v

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf projects/dashboard/*.db
	rm -rf venv/

docs:
	@echo "📖 Documentation ready in docs/"
	@echo "   - README.md (setup & usage)"
	@echo "   - API.md (endpoint docs)"
	@echo "   - DEPLOYMENT.md (deployment guide)"
	@echo "   - TROUBLESHOOTING.md (common issues)"
