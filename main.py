from scraper import Friendly_Bot
from database import insert_jobs, db_sync, jobs_database, get_jobs
from flask import Flask, render_template


my_bot = Friendly_Bot(agent_string="FirasApprenticeshipTracker/1.0")
slug_job = my_bot.slugify()
jobs_dict = my_bot.get_apprenticeships(slug_job)

if jobs_dict:  # sync the database and call the dictionary of the different jobs
    cursor, connection = db_sync()
    def reset_db():  # easier than doing it manually during testing
        cursor.execute("DELETE FROM jobs")
        connection.commit()
        print("Reset the database")
    reset_db()
    jobs_database(cursor, connection)
    insert_jobs(jobs_dict, connection, cursor)
    connection.close()
else:
    print("No jobs found for that title")
app = Flask(__name__)
connection, cursor = db_sync()
@app.route("/")
def hello():
    connection, cursor = db_sync()
    jobs_list = get_jobs(cursor)
    connection.close()
    return render_template("DegreeApprenticeships.html", jobs = jobs_list)

if __name__ == "__main__":
    app.run(debug = False)
