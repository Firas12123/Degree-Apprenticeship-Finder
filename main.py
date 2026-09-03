from scraper import Friendly_Bot
from database import insert_jobs, db_sync, jobs_database

my_bot = Friendly_Bot(agent_string = "FirasDegreeAppreticeshipTracker/1.0")  # agent created to verify were not DDoS'ing it's just a small project
job_title = input("Enter a job title for example 'Software Engineer' or 'Computer Science'\nEnter the job title for the Degree Apprenticeships you want to look for\n").replace(" ","")
slug_job = my_bot.slugify(job_title)
jobs_dict = my_bot.get_apprenticeships(slug_job)


if jobs_dict:
    cursor, connection = db_sync()
    jobs_database(cursor, connection)
    insert_jobs(jobs_dict, connection, cursor)
    connection.close()