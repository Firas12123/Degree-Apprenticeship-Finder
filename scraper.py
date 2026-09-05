import requests
import json
from bs4 import BeautifulSoup
from database import db_sync

class Friendly_Bot():
    def __init__(self,agent_string):
        self.headers = {"User-agent":agent_string}
        self.cursor = db_sync()[0]
        self.connection = db_sync()[1]
    
    def slugify(self):  # make sure the user input has no capitals and a dash between the two words
        slug_chars = []
        list_slugs = []
        job_title = ["Software Engineering"]
        for jobs in job_title:
            jobs = jobs.strip().replace(" ", "-")  # take out the spaces and adds a hyphen where the space is and turns lowercase
            for index, char in enumerate(jobs):
                if char.isupper() and index > 0:
                    if "-" not in jobs[index - 3:index]:
                        if index - 3 > 0:
                            slug_chars.append("-")
                slug_chars.append(char.lower())
            slug_job = "".join(slug_chars)
            slug_chars = []
            list_slugs.append(slug_job)
        return list_slugs
    
    def get_apprenticeships(self,list_slugs):
        if len(list_slugs) > 1:
            word = "technology?role="
            words = ",".join(list_slugs)
        else:
            word = ""
            words = "".join(list_slugs)
        r = requests.get(f"https://higherin.com/search-jobs/degree-apprenticeship/{word}{words}", timeout =5, headers = self.headers)
        r_text = ""
        if r.headers.get("Content-Type", "").startswith("text/html"):
            r_text = r.text                        # gets the data from user input and gets results into text
        soup = BeautifulSoup(r_text, "html.parser")    # makes it readable
        script_text = None
        for script in soup.find_all("script"):   # find <script> piece
            if script.string and "__RMP_SEARCH_RESULTS_INITIAL_STATE__" in script.string:
                script_text = script.string
                break
        if script_text:
            target_variable = "__RMP_SEARCH_RESULTS_INITIAL_STATE__ = "  # this is the <script> we need to find
            len_var = len(target_variable)
            script_index = script_text.find(target_variable) # finds the index of our target variable
            script_data = script_text[(script_index+len_var):]
            
        if not script_text:
            return{}     # returns empty dictionary so our program doesn't crash when we save to SQL database
        if script_data.endswith(";"):       # safety net to get rid of the ";"
            script_data = script_data[:-1]
        json_data = json.loads(script_data)  # gets the specific "jobId"
        jobs_dict = {}
        for dictionary in json_data["data"]:
            job_id = dictionary["jobId"]
            target_name = "Register Your Interest - "
            target_len = len(target_name)
            company_name = dictionary["jobTitle"]
            if target_name in company_name:
                jobs_dict[job_id] = {"jobTitle": company_name[target_len:],
                                     "url": dictionary["url"],
                                     "companyName": dictionary["companyName"]}
            else:
                jobs_dict[job_id] = {"jobTitle": dictionary["jobTitle"],
                                   "url": dictionary["url"],
                                   "companyName": dictionary["companyName"]}
            
        return jobs_dict

