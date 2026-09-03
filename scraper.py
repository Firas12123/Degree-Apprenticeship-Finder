import requests
import json
from bs4 import BeautifulSoup

class Friendly_Bot():
    def __init__(self,agent_string):
        self.headers = {"User-agent":agent_string}
        
    def slugify(self,job_title):   # make sure the user input has no capitals and a dash between the two words
        n_title = job_title[0].lower() + job_title[1:]
        for index, i in enumerate(n_title):
            if i.isupper():
                n_title = n_title[:index - 1] + n_title[index - 1] + "-" + n_title[index:].lower()
        return n_title
    
    
    def get_apprenticeships(self,slug_job):
        
        r = requests.get(f"https://higherin.com/search-jobs/degree-apprenticeship/{slug_job}", timeout =5, headers = self.headers)
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
            jobs_dict[job_id] = {"jobTitle": dictionary["jobTitle"],
                               "url": dictionary["url"],
                               "companyName": dictionary["companyName"]}
        return jobs_dict

