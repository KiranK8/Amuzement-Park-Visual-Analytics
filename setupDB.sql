# Usage from Command Line
# Go to your top-level data folder and do the following.
# Start sqlite.
# > sqlite3 dinofun.db
# Execute this script.
# sqlite> .read ../setupDB.sql

# Create a table for the movement of the visitors on Friday.
CREATE TABLE movementFri(timestamp TEXT, id INTEGER, type TEXT, x INTEGER, y INTEGER);

# Read the Friday data and store it in the table.
.mode csv
.import park-movement-Fri.csv movementFri

# Print all tables in the database.
.tables

# Close sqlite.
.exit
