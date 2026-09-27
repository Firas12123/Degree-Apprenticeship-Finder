# Degree Apprenticeship Tracker

My automated Python web scraper and Flask dashboard built to track Software Engineering Degree Apprenticeships live

I built this project to allow me to apply early to my chosen Degree Apprenticeships, made possible by Github automation tool which runs in the background every 4 hours ensuring early access to applications

## Core Features
* **Automated Web Scraping:** Extracts live job data from safe scraper friendly career sites
* **Email Alerts:** Sends email notifications when new roles are detected (via Github automation)
* **Interactive Dashboard:** A Flask web interface using JavaScript's POST method and Jinja to handle backend data
* **Data Handling:** SQLite to store active jobs and track users removed jobs, used a JSON file that the Github agent appends after each new job so no duplicate emails are sent
## Tech Stack
* **Backend:** Python, Flask
* **Database:** SQLite
* **Frontend:** HTML, CSS, JavaScript

## Local Installation
1. Clone this repository:
   ```bash
   git clone [https://github.com/Firas12123/Degree-Apprenticeship-Finder.git](https://github.com/Firas12123/Degree-Apprenticeship-Finder.git)
