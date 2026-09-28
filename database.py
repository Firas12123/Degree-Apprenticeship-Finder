import sqlite3

def db_sync():
    connection = sqlite3.connect("jobs.db", check_same_thread = False)    # sync the connection and the cursor and connect to the jobs database
    connection.commit()
    return connection

def jobs_database(connection):   # creates database if it's not already made
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS jobs(
                jobId INTEGER PRIMARY KEY,
                jobTitle TEXT,
                url TEXT,
                companyName TEXT,
                applied INTEGER DEFAULT 0,
                hidden INTEGER DEFAULT 0
                )""")
    connection.commit()

    
def insert_jobs(jobs_dict, connection):
    cursor = connection.cursor()
    for jobs_id, details in jobs_dict.items(): # inserts the job details into the database
        cursor.execute("INSERT OR IGNORE INTO jobs (jobId, jobTitle, url, companyName) VALUES(?,?,?,?)",(jobs_id,details["jobTitle"], details["url"], details["companyName"]))
    connection.commit()
    
def get_jobs(connection):
    cursor = connection.cursor()
    all_jobs = cursor.execute("SELECT * FROM jobs")
    job = all_jobs.fetchall()
    connection.commit()
    return job