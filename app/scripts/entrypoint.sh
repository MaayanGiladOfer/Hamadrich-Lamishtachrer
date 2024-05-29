#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Wait for the database to be ready
/base/app/scripts/wait-for-it.sh db:3306 -- echo "Database is up"

# Initialize, migrate, and upgrade the database
flask db init || true  # Ignore error if the migration directory already exists
flask db migrate -m "Initial migration." || true  # Ignore error if migration already exists
flask db upgrade

# Execute the command passed as arguments to the script
exec "$@"