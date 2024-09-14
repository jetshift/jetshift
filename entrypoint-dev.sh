#!/bin/sh

# Load environment variables from .env file
if [ -f .env ]; then
  export $(cat .env | grep -v '^#' | xargs)
fi

JOB_QUEUE=${JOB_QUEUE:-False}
CRON_JOB=${CRON_JOB:-False}

# Start luigid
luigid --port 8082 &

# Start Flask development server with hot-reload
flask run --host=0.0.0.0 --port=80 --reload &

# Start Redis server & RQ worker
if [ "$JOB_QUEUE" = "True" ]; then
  redis-server &
  rq worker --url redis://$REDIS_HOST:$REDIS_PORT &
fi

# Start cron
if [ "$CRON_JOB" = "True" ]; then
  crond -f &
fi

# Wait for all background processes to finish
wait
