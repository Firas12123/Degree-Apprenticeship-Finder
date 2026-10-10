import os
from scraper import Friendly_Bot
from database import insert_jobs, db_sync, jobs_database, get_jobs, get_removed_jobs
from flask import Flask, render_template, request
from email_sender import send_emails
import json

technology_list = ["Software Engineering", "Artificial Intelligence", "Computer Science", "Cyber Security", "Data Analysis", "Front-End Development", "Information Technology"] # only tech section I don't want to copy their whole website
connection = db_sync()
jobs_database(connection)

def sync_jobs(jobs_dict, connection):
    cursor = connection.cursor()
    if jobs_dict:  # sync the database and call the dictionary of the different jobs
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
        insert_jobs(jobs_dict, connection)

titles = os.environ.get("JOB_TITLES", "") # for my Github workflow
my_bot = Friendly_Bot(agent_string="FirasApprenticeshipTracker/1.0")

slug_job = my_bot.slugify([titles])
jobs_dict = my_bot.get_apprenticeships(slug_job)
sync_jobs(jobs_dict, connection)

app = Flask(__name__)

@app.route("/")
def home():
    all_jobs = get_jobs(connection)
    return render_template("DegreeApprenticeship.html", jobs_dict = all_jobs, technology_list = technology_list)

@app.route("/checked", methods = ["POST"])
def applied_for():
    cursor = connection.cursor()
    data = request.get_json()
    applied = data.get("applied")
    job_id = data.get("job_id")
    cursor.execute("UPDATE jobs SET applied = ? WHERE jobId = ?", (applied, job_id))
    connection.commit()
    return "", 200

@app.route("/jobs", methods = ["POST"])
def give_jobs():
    cursor = connection.cursor()
    data = request.get_json()
    if data.get("delete") == "delete":
        cursor.execute("DROP TABLE IF EXISTS jobs")
        jobs_database(connection)
        return "", 201
    else:
        jobs = data.get("job_title")
        jobs_list = json.loads(jobs)
        slug_job = my_bot.slugify(jobs_list)
        jobs_dict = my_bot.get_apprenticeships(slug_job)
        sync_jobs(jobs_dict, connection)
        return "", 200

@app.route("/remove", methods = ["POST"])
def change_job():
    cursor = connection.cursor()
    data = request.get_json()
    id = data.get("id")
    choice = data.get("choice")
    print(id, choice)
    cursor.execute("UPDATE jobs SET hidden = ? WHERE jobId = ?", (choice, id))
    cursor.execute("SELECT * FROM jobs WHERE jobId = ?", (id,))
    job = cursor.fetchone()
    print(job)
    return "", 200

@app.route("/removed_jobs")
def removed_jobs():
    jobs = get_removed_jobs(connection)
    return render_template("Removed.html", removed = jobs)

if __name__ == "__main__":
    app.run(debug=True)