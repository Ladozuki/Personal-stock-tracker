Personal Stock Notification System

This project monitors stock prices and sends notifications when certain conditions are met.


# Database Setup

## PostgreSQL 
**To set up, follow these steps:**
1. Install PostgreSQL from the website

2Check PostgreSQL Path:

Verify that PostgreSQL is in your PATH by running:

bash
Copy code
echo $PATH
Look for /Applications/Postgres.app/Contents/Versions/latest/bin in the output.

Add PostgreSQL to PATH Temporarily:

If PostgreSQL isn’t in the PATH, you can add it for the current session:

bash
Copy code
export PATH="/Applications/Postgres.app/Contents/Versions/latest/bin:$PATH"
Add PostgreSQL to PATH Permanently:

Add this to your shell configuration file to ensure it’s always available:

bash
Copy code
nano ~/.zshrc
Or, if using bash:

bash
Copy code
nano ~/.bash_profile
Add the following line:

bash
Copy code
export PATH="/Applications/Postgres.app/Contents/Versions/latest/bin:$PATH"
Save and exit, then reload:

bash
Copy code
source ~/.zshrc
Or:

bash
Copy code
source ~/.bash_profile
3. Running Commands in VS Code Terminal
a. Check psql Access:

Try running:

bash
Copy code
psql --version
And:

bash
Copy code
psql -U postgres
b. Creating/Using PostgreSQL Roles:

If psql is running but you still encounter issues, you can create or manage roles within PostgreSQL as follows:

Access psql:
psql -U postgres

bash
Copy code
psql
Create a New Superuser Role:

sql
Copy code
CREATE ROLE myuser WITH SUPERUSER LOGIN PASSWORD 'mypassword'

Create a New Database:

sql
Copy code
CREATE DATABASE mydatabase;
Replace mydatabase with your desired database name.
Drop a Database:

sql
Copy code
DROP DATABASE mydatabase;
Be careful with this command as it will delete the database.
Create a New Table:

sql
Copy code
CREATE TABLE mytable (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100)
);
Creates a new table with columns. Customize as needed.
Insert Data into a Table:

sql
Copy code
INSERT INTO mytable (name) VALUES ('Sample Data');
Query Data from a Table:

sql
Copy code
SELECT * FROM mytable;
Exit psql:

sql
Copy code
\q