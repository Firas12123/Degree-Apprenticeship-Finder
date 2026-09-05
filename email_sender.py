import smtplib
from email.message import EmailMessage

def send_emails(new_jobs):
    sender_email = "firascosta80@gmail.com"
    app_password = "xuvvkpqbuefhonny"
    if len(new_jobs) == 0:
        return False
    else:
        msg = EmailMessage()
        word = "Apprenticeships" if len(new_jobs) >1 else "Apprenticeship"
        msg["Subject"] = f"🚀 {len(new_jobs)} new Degree {word} Dropped!"
        msg["From"] = sender_email
        msg["To"] = "firascosta80@gmail.com", "hussain280108@gmail.com"
        
        body = "All the Degree Apprenticeships you haven't applied for yet hurry up and go apply \n \n"
        for job in new_jobs:
            body += f"Company: {job["companyName"]}\n"
            body += f"Role: {job["jobTitle"]}\n"
            body += f"Link: {job["url"]}\n"
            body += "\n" +"-" *40 + "\n"
        msg.set_content(body)
        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(sender_email, app_password)
                smtp.send_message(msg)
            print("Email notification sent successfully!")
        except Exception as e:
            print(f"Error sending email: {e}")