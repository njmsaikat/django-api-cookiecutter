#!/bin/sh
# PostgreSQL backup script - Compressed, optimized for Duplicati

set -e

PROJECT_NAME="${PGDATABASE}"
EXTRACT_BASE="/var/www/backups/production-db/${PROJECT_NAME}_extracted"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS="${RETENTION_DAYS:-3}"

mkdir -p ${EXTRACT_BASE}

echo "[$(date)] [${PROJECT_NAME}] Starting backup..."

EXTRACT_DIR="${EXTRACT_BASE}/${TIMESTAMP}"
mkdir -p ${EXTRACT_DIR}

if pg_dump -h ${PGHOST} -U ${PGUSER} -d ${PGDATABASE} \
    --no-owner --no-acl \
    | gzip -9 > ${EXTRACT_DIR}/backup.sql.gz; then

    SIZE=$(du -h ${EXTRACT_DIR}/backup.sql.gz | cut -f1)
    echo "[$(date)] [${PROJECT_NAME}] ✓ Backup created: ${SIZE}"

    ln -sfn ${EXTRACT_DIR} ${EXTRACT_BASE}/latest

    find ${EXTRACT_BASE} -maxdepth 1 -type d -regex ".*/[0-9].*" -mtime +${RETENTION_DAYS} -exec rm -rf {} \;

    COUNT=$(find ${EXTRACT_BASE} -maxdepth 1 -type d -regex ".*/[0-9].*" | wc -l)
    TOTAL_SIZE=$(du -sh ${EXTRACT_BASE} | cut -f1)

    echo "[$(date)] [${PROJECT_NAME}] Total: ${COUNT} backups (${TOTAL_SIZE})"

    exit 0
else
    echo "[$(date)] [${PROJECT_NAME}] ✗ Backup FAILED!"
    exit 1
fi
