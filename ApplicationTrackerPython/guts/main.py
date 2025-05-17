import requests, json, datetime
from bs4 import BeautifulSoup

class job_listing:
    def __init__(self, company, jobTitle, location, dateApplied, salaryRange, jobURL):
        self.company = company
        self.jobTitle = jobTitle
        self.location = location
        self.dataApplied = dateApplied
        self.salaryRange = salaryRange
        self.jobURL = jobURL

applicationUrl1 = "https://jobs.ashbyhq.com/ramp/0ea43bb5-201b-4626-ae19-1d7ae3a3193f"
applicationUrl2 = "https://jobs.ashbyhq.com/multiverse/8b0ca0d5-3f6a-4e51-a7dd-36a67c473663"
applicationUrl3 = "https://jobs.ashbyhq.com/ramp/0ea43bb5-201b-4626-ae19-1d7ae3a3193f"

def build_job_listing(applicationURL):
    URL = applicationURL
    print("Here is your link: " + URL)

    response = requests.get(URL)
    html_data = response.text

    soup = BeautifulSoup(html_data, "html.parser")
    res = soup.find('script')
    json_object = json.loads(res.contents[0])

    location = json_object['jobLocation']['address']['addressLocality']
    minValue = json_object['baseSalary']['value']['minValue']
    maxValue = json_object['baseSalary']['value']['maxValue']
    jobTitle = json_object['title']
    company = json_object['hiringOrganization']['name']
    today = datetime.date.today()

    job = job_listing(company, jobTitle, location, today, f"{minValue:,}" + ' - ' + f"{maxValue:,}", URL)
    print(vars(job))

build_job_listing(applicationUrl1)
build_job_listing(applicationUrl2)
build_job_listing(applicationUrl3)



'''
Notes for implementation:

- Filter by link to determine how to scrape the website, ie. Ashby places job titles in the  meta content
- We are able to grab html but not JS/ windows application data. Solve this and it may be much easier to scrape
    Successfully parsing JSON data
    Currently works for the following job listing sites:
        Ashby
        
- Need to find a way to store all the information to retrieve from local.
- Current plan Capture: Title, Company, Compensation, The Date the link is entered, Location, 



'''