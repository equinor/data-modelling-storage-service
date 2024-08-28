#!/bin/bash
set -e

# Connect to the default database and create the uuid-ossp extension
psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";"
