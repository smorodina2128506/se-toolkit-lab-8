#!/bin/bash
set -e

# If running as root but APP_UID is set, switch to that user
if [ "$(id -u)" = "0" ]; then
    # Create home directory if it doesn't exist
    if [ ! -d "/home/appuser" ]; then
        mkdir -p /home/appuser
        chown ${APP_UID:-1000}:${APP_GID:-1000} /home/appuser
    fi
    
    # Fix ownership of app directory if needed
    chown -R ${APP_UID:-1000}:${APP_GID:-1000} /app/nanobot 2>/dev/null || true
    
    exec gosu ${APP_UID:-1000} "$@"
fi

exec "$@"
