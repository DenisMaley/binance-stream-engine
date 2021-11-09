#!/bin/bash

until nc -z ${RABBIT_HOST} ${RABBIT_PORT}; do
    echo "$(date) - waiting for rabbitmq..."
    sleep 1
done

sleep 5

echo "$(date) - Ready to launch the stream"

python runner.py
echo "$(date) - The streaming process has started"