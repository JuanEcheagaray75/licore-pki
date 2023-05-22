#!/bin/bash

DB_NAME="measures"

sqlite3 "$DB_NAME.sqlite3" << EOF
CREATE TABLE measures(
    seq_id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    aud_id TEXT,
    measured_timestamp DATETIME,
    measure_type INTEGER,
    measure REAL
);
EOF