from scraper import Friendly_Bot
from database import insert_jobs, db_sync, jobs_database, get_jobs
from flask import Flask, render_template
from email_sender import send_emails

my_bot = Friendly_Bot(agent_string="FirasApprenticeshipTracker/1.0")
slug_job = my_bot.slugify()
jobs_dict = my_bot.get_apprenticeships(slug_job)

if jobs_dict:  # sync the database and call the dictionary of the different jobs
    cursor, connection = db_sync()
    jobs_database(cursor, connection)
    new_j = []
    new_jobs = []
    for job_id in jobs_dict:
        cursor.execute("SELECT jobId FROM jobs WHERE jobId = ?", (job_id,))
        existing_job = cursor.fetchall()
        if not existing_job:
            new_j.append(job_id)
    for job_id in new_j:
        new_job = jobs_dict[job_id]
        new_jobs.append(new_job)
    send_emails(new_jobs)
    insert_jobs(jobs_dict, connection, cursor)
    connection.close()
else:
    print("No jobs found for that title")
    
app = Flask(__name__)

@app.route("/")
def hello():
    cursor, connection = db_sync()
    jobs_list = get_jobs(cursor)
    connection.close()
    total_applied = sum(1 for job in jobs_list if job[4] == 1)
    return render_template("DegreeApprenticeships.html", jobs = jobs_list, total_applied = total_applied)

@app.route("/toggle/<int:job_id>", methods = ["POST"])
def toggle_applied(job_id):
    cursor, connection = db_sync()
    cursor.execute("SELECT applied FROM jobs WHERE jobId = ? AND hidden = 0", (job_id,))
    row = cursor.fetchone()
    
    if row is not None:
        current_status = row[0]
        new_status = 0 if current_status == 1 else 1
        cursor.execute("UPDATE jobs SET applied = ? WHERE jobId = ?", (new_status, job_id))
        connection.commit()
        
    connection.close()
    return "Updated Successfully", 200

@app.route("/hide/<int:job_id>", methods= ["POST"])
def hide_job(job_id):
    cursor, connection = db_sync()
    cursor.execute("UPDATE jobs SET hidden = 1 WHERE jobId = ?", (job_id,))
    connection.commit()
    connection.close()
    return "Hidden Successfully", 200


if __name__ == "__main__":
    app.run(debug = True)
