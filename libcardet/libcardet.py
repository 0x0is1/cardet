import requests, bs4, base64

# URL encoded to base64 to avoid illegal api usage backtracing
BASE_URL = base64.b64decode("aHR0cHM6Ly92YWhhbmluZm9zLmNvbQ==").decode('utf-8')

class subdir:
    home = "/vehicle-details-by-number-plate/"
    fetch_data = "/getdetails.php"

class tmcolors:
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

def get_cookie_token():
    home_url = BASE_URL + subdir.home
    response = requests.get(home_url, verify=False)
    phcid = response.headers['Set-Cookie'].split(";")[0]
    access_token = str(response.content).split('var token = "')[1].split('";')[0]
    return phcid, access_token

# Parsing accessed xml to json for lib usage purpose with bs4
def xml2json(response):
    soup = bs4.BeautifulSoup(response.content, 'html.parser')
    data = soup.find_all("tr")
    formatted_data = {}
    for i in data:
        j = i.find_all("td")
        formatted_data[j[0].text] = j[2].text
    return formatted_data

def get_details(vehicle_number, max_retry=15):
    phcid_cook, access_token = get_cookie_token()
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "Num": access_token,
        "Cookie": phcid_cook,
    }
    data = {
        "number": str(vehicle_number)
    }
    url = BASE_URL + subdir.fetch_data
    for i in range(1, max_retry+1):
        response = requests.post(url=url, headers=headers, data=data, verify=False)
        if '<tr><td>Registration Number</td><td>:</td><td>R</td></tr>' in str(response.content):
            print(f"{tmcolors.WARNING}[!] Fetching failed. Retrying...({i}/{max_retry}){tmcolors.ENDC}")

            if i >= max_retry:
                print("{tmcolors.FAIL}[-] Unable to find it in database. Recheck arguements or Retry later.{tmcolors.ENDC}")
                break
            
            continue
        if '<tr><td>Registration Number</td><td>:</td><td>V</td></tr>' in str(response.content):
            print("[-] Vehicle Number is not from India.\n[-] This lib is for India only vehicles")
            return
        formatted_data = xml2json(response)
        return formatted_data
