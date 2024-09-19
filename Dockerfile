# Build stage
FROM python:3.12-alpine AS build

WORKDIR /app

# Install build dependencies and dos2unix in a single RUN command
RUN apk add --no-cache gcc musl-dev libffi-dev dos2unix

# Copy requirements early to leverage Docker cache if they do not change
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Ensure crontab is set up properly
COPY crontab /etc/crontabs/root

# Create the log directory and files with appropriate permissions in one layer
RUN mkdir -p /var/log && \
    touch /var/log/cron.log /var/log/cron.error.log && \
    chmod 666 /var/log/cron.log /var/log/cron.error.log

# Convert the crontab and entrypoint.sh files to Unix line endings in a single RUN command
RUN dos2unix /etc/crontabs/root /entrypoint.sh

# Runtime stage
FROM python:3.12-alpine

WORKDIR /app

# Install runtime dependencies, including Redis server and Supervisor
RUN apk add --no-cache libffi dos2unix redis supervisor && \
    mkdir -p /var/log && \
    touch /var/log/cron.log /var/log/cron.error.log && \
    chmod 666 /var/log/cron.log /var/log/cron.error.log

# Copy Python environment from build stage to final stage
COPY --from=build /usr/local/lib/python3.12 /usr/local/lib/python3.12
COPY --from=build /usr/local/bin /usr/local/bin

# Copy application files from the build stage
COPY --from=build /app /app

# Copy necessary files for cron jobs
COPY --from=build /etc/crontabs/root /etc/crontabs/root

# Install the app in editable mode
RUN pip install -e .

# Expose the necessary ports
EXPOSE 8080 8082 6379

# Supervisor configuration
COPY supervisord.conf /etc/supervisord.conf

# Set the entrypoint to start supervisord
ENTRYPOINT ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]
