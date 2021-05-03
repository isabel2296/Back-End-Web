#!/bin/sh

sqlite3 ./var/timelines.db < ./sqlFiles/timelines.sql
sqlite3 ./var/clients.db < ./sqlFiles/clients.sql