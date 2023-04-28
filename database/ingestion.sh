#!/bin/bash
set -e

# Cria as bases
psql -d "$POSTGRES_DB" -U "$POSTGRES_USER"  -c "\i utfpr_chatbot/DDL/CAMPUS.sql"
psql -d "$POSTGRES_DB" -U "$POSTGRES_USER"  -c "\i utfpr_chatbot/DDL/ENROLLMENT_PHASE.sql"
psql -d "$POSTGRES_DB" -U "$POSTGRES_USER"  -c "\i utfpr_chatbot/DDL/ENROLLMENT_SCHEDULE.sql"
psql -d "$POSTGRES_DB" -U "$POSTGRES_USER"  -c "\i utfpr_chatbot/DDL/INTERNSHIP_INFO.sql"
psql -d "$POSTGRES_DB" -U "$POSTGRES_USER"  -c "\i utfpr_chatbot/DDL/INTERNSHIP_TYPE.sql"
psql -d "$POSTGRES_DB" -U "$POSTGRES_USER"  -c "\i utfpr_chatbot/DDL/INTERNSHIP_TEXT.sql"

# Carrega os dados
psql -d "$POSTGRES_DB" -U "$POSTGRES_USER"  -c "\copy CAMPUS from '/utfpr_chatbot/data/CAMPUS.csv' DELIMITER ';' CSV HEADER ENCODING 'latin1'"
psql -d "$POSTGRES_DB" -U "$POSTGRES_USER"  -c "\copy ENROLLMENT_PHASE from '/utfpr_chatbot/data/ENROLLMENT_PHASE.csv' DELIMITER ';' CSV HEADER ENCODING 'latin1'"
psql -d "$POSTGRES_DB" -U "$POSTGRES_USER"  -c "\copy ENROLLMENT_SCHEDULE from '/utfpr_chatbot/data/ENROLLMENT_SCHEDULE.csv' DELIMITER ';' CSV HEADER ENCODING 'latin1'"
psql -d "$POSTGRES_DB" -U "$POSTGRES_USER"  -c "\copy INTERNSHIP_INFO from '/utfpr_chatbot/data/INTERNSHIP_INFO.csv' DELIMITER ';' CSV HEADER ENCODING 'latin1'"
psql -d "$POSTGRES_DB" -U "$POSTGRES_USER"  -c "\copy INTERNSHIP_TYPE from '/utfpr_chatbot/data/INTERNSHIP_TYPE.csv' DELIMITER ';' CSV HEADER ENCODING 'latin1'"
psql -d "$POSTGRES_DB" -U "$POSTGRES_USER"  -c "\copy INTERNSHIP_TEXT from '/utfpr_chatbot/data/INTERNSHIP_TEXT.csv' DELIMITER ';' CSV HEADER ENCODING 'latin1'"
