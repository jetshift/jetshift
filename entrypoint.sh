#!/bin/sh

# Start cron
crond -f &

# Start luigid
luigid --port 8082 &

# Start the Flask app with Waitress
waitress-serve --host=0.0.0.0 --port=80 web.main:app &

# Start Redis server
redis-server &

# Start RQ worker (if needed)
rq worker --url redis://localhost:6379 &

# Wait for all background processes to finish
wait
