import sqlite3

def db_sync():
    connection = sqlite3.connect("jobs.db")    # sync the connection and the cursor and connect to the jobs database
    cursor = connection.cursor()
    return cursor,connection

def jobs_database(cursor,connection):   # creates database if its not already made
    cursor.execute("""CREATE TABLE IF NOT EXISTS jobs(
                jobId INTEGER PRIMARY KEY,
                jobTitle TEXT,
                url TEXT,
                companyName TEXT
                )""")
    connection.commit()
    
def insert_jobs(jobs_dict, connection, cursor):
    length = 0
    for jobs_id, details in jobs_dict.items(): # inserts the job details into the database
        length += 1
        cursor.execute("INSERT OR IGNORE INTO jobs VALUES(?,?,?,?)",(jobs_id,details["jobTitle"], details["url"], details["companyName"]))
        connection.commit()
    print(f"You have added {length} jobs to your jobs table!")
    
