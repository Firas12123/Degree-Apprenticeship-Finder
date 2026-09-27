from scraper import Friendly_Bot
from database import insert_jobs, db_sync, jobs_database, get_jobs
from flask import Flask, render_template, request
from email_sender import send_emails

my_bot = Friendly_Bot(agent_string="FirasApprenticeshipTracker/1.0")
slug_job = my_bot.slugify()
jobs_dict = my_bot.get_apprenticeships(slug_job)
cursor, connection = db_sync()
if jobs_dict:  # sync the database and call the dictionary of the different jobs
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
else:
    print("No jobs found for that title")

app = Flask(__name__)

@app.route("/")
def home():
    jobs_dic = get_jobs(cursor, connection)
    return render_template("DegreeApprenticeship.html", jobs_dict = jobs_dic)

@app.route("/checked", methods = ["POST"])
def applied_for():
    data = request.get_json()
    applied = data.get("applied")
    job_id = data.get("job_id")
    cursor.execute("UPDATE jobs SET applied = ? WHERE jobId = ?", (applied, job_id))
    cursor.execute("SELECT applied FROM jobs WHERE jobId =?",(job_id,))
    result = cursor.fetchone()
    print(result)
    connection.commit()
    return "", 200

if __name__ == "__main__":
    app.run(debug=True)
# remember to change to false