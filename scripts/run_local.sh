
#!/bin/bash
set -e
echo "Starting uvicorn server on http://0.0.0.0:8000"
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
