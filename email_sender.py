import smtplib
from email.message import EmailMessage
import os
import json


SEEN_FILE = "seen_jobs.json"

def send_emails(new_jobs):
    seen_urls = set()
    if os.path.exists(SEEN_FILE):
        try:
            with open(SEEN_FILE, "r") as file:
                seen_urls = set(json.load(file))
        except Exception:
            seen_urls = set()
    all_jobs = [job for job in new_jobs if job.get("url") and job["url"] not in seen_urls]
    if len(all_jobs) == 0:
        return False
        
    sender_email = "firascosta80@gmail.com"
    EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
    # cant show my password on GitHub sorry
    msg = EmailMessage()
    word = "Apprenticeships" if len(all_jobs) >1 else "Apprenticeship"
    msg["Subject"] = f"🚀 {len(all_jobs)} new Degree {word} Dropped!"
    msg["From"] = sender_email
    msg["To"] = "firascosta80@gmail.com", "hussain280108@gmail.com"
    
    body = "All the Degree Apprenticeships you haven't applied for yet hurry up and go apply \n \n"
    for job in all_jobs:
        body += f"Company: {job['companyName']}\n"
        body += f"Role: {job['jobTitle']}\n"
        body += f"Link: {job['url']}\n"
        body += "\n" +"-" *40 + "\n"
    msg.set_content(body)
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print("Email notification sent successfully!")
        
        for job in all_jobs:
            seen_urls.add(job["url"])
        
        with open(SEEN_FILE, "w") as file:
            json.dump(list(seen_urls),file, indent = 2) # converts our python data into json for program to read
    except Exception as e:
        print(f"Error sending email: {e}")