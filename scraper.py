import requests
import json
from bs4 import BeautifulSoup

def slugify(job_title):   # make sure the user input has no capitals and a dash between the two words
    n_title = job_title[0].lower() + job_title[1:]
    for index, i in enumerate(n_title):
        if i.isupper():
            n_title = n_title[:index - 1] + n_title[index - 1] + "-" + n_title[index:].lower()
    return n_title
    
    
def get_apprenticeships(slug_job):
    
    agent = {"User-Agent": "FirasDegreeAppreticeshipTracker/1.0"}
    headers = agent      # agent created to verify were not DDoS'ing it's just a small project
    r = requests.get(f"https://higherin.com/search-jobs/degree-apprenticeship/{slug_job}", timeout =5, headers = headers)
    if r.headers.get("Content-Type", "").startswith("text/html"):
        r_text = r.text                        # gets the data from user input and gets results into text
    soup = BeautifulSoup(r_text, "html.parser")    # makes it readable
    script_text = None
    for script in soup.find_all("script"):   # find <script> piece
        if script.string and "__RMP_SEARCH_RESULTS_INITIAL_STATE__" in script.string:
            script_text = script.string
            break
    if script_text:
        target_variable = "__RMP_SEARCH_RESULTS_INITIAL_STATE__ = "
        len_var = len(target_variable)
        script_index = script_text.find(target_variable) # finds the index of our target variable
        script_data = script_text[(script_index+len_var):]
        
    if not script_text:
        return{}     # returns empty dictionary so our program doesnt crash when we save to SQL database
    
    if script_data.endswith(";"):       # safety net to get rid of the ";"
        script_data = script_data[:-1]
    
    json_data = json.loads(script_data)  # gets the specific "jobId"
    job_dict = {}
    for dictionary in json_data["data"]:
        job_id = dictionary["jobId"]
        job_dict[job_id] = {"jobTitle": dictionary["jobTitle"],
                           "url": dictionary["url"],
                           "companyName": dictionary["companyName"]}
    return job_dict

job_title = input("Enter a job title for example 'Software Engineer' or 'Computer Science'\nEnter the job title for the Degree Apprenticeships you want to look for\n").replace(" ","")
slug_job = slugify(job_title)
jobs_dictionary = get_apprenticeships(slug_job)