import requests, json, datetime, re
from bs4 import BeautifulSoup

class job_listing:
    def __init__(self, company, jobTitle, location, dateApplied, salaryRange, jobURL):
        self.company = company
        self.jobTitle = jobTitle
        self.location = location
        self.dateApplied = dateApplied
        self.salaryRange = salaryRange
        self.jobURL = jobURL

applicationUrl1 = "https://job-boards.greenhouse.io/notion/jobs/6521100003"
applicationUrl2 = "https://jobs.ashbyhq.com/multiverse/8b0ca0d5-3f6a-4e51-a7dd-36a67c473663"
applicationUrl3 = "https://jobs.ashbyhq.com/imprint/3cf70751-e01e-45b5-a7a6-d89f4d8d449c?utm_source=aRoGLll8KW"

def build_job_listing_ashby(applicationURL):
    URL = applicationURL

    response = requests.get(URL)
    html_data = response.text

    soup = BeautifulSoup(html_data, "html.parser")
    res = soup.find('script')
    json_object = json.loads(res.contents[0])

    location = json_object['jobLocation']['address']['addressLocality'] 
    locationSt = json_object['jobLocation']['address']['addressRegion']
    minValue = json_object['baseSalary']['value']['minValue']
    maxValue = json_object['baseSalary']['value']['maxValue']
    jobTitle = json_object['title']
    company = json_object['hiringOrganization']['name']
    today = datetime.date.today()

    job = job_listing(company, jobTitle, location + ", " + locationSt, today, f"${minValue:,}" + ' - ' + f"${maxValue:,}", URL)
    print(vars(job))

def build_job_listing_greenhouse(applicationURL):
    URL = applicationURL

    response = requests.get(URL)
    html_data = response.text
    soup = BeautifulSoup(html_data, "html.parser")
    
    description_tag = soup.find('meta', {'property': 'og:description'})
    location = description_tag.get('content') ##Job Location for Greenhouse applications

    title_tag = soup.find('meta', {'property': 'og:title'})
    jobTitle = title_tag.get('content') ##Title for Greenhouse applications

    company = URL.split("greenhouse.io/")[1].split("/")[0]
    company = company.capitalize() ## Company Name

    salary_range = re.findall(r'\$\d{1,3}(?:,\d{3})*', html_data)
    salary = (salary_range[0] + " - " + salary_range[1]) ## Salary Range

    today = datetime.date.today() #Time Applied

    job = job_listing(company, jobTitle, location, today, salary, URL)
    print(vars(job))


#build_job_listing_greenhouse(applicationUrl1)
#build_job_listing(applicationUrl2)
build_job_listing_ashby(applicationUrl3)



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