import os
import requests
from dotenv import load_dotenv
from pprint import pprint

# https://www.linkedin.com/in/ketan-kishore-b89643150/


def scrape_linkedin_profile(linkedIn_url, mock=True):

    if mock:
        response = requests.get(
            "https://gist.githubusercontent.com/ketankishore27/1fbb1c2bcc8f006c91b8378f4e007a65/raw/08d2aff5f9423c389705285fbfb269df6693becb/gistfile1.txt",
            timeout=10,
        )
    else:
        BASE_URL = "https://api.scrapin.io/enrichment/profile"
        params = {"apikey": os.getenv("SCRAPIN_API_KEY"), "linkedInUrl": linkedIn_url}
        response = requests.get(BASE_URL, params=params, timeout=10)

    return response.json()


if __name__ == "__main__":
    load_dotenv()
    personal_url = "https://www.linkedin.com/in/ketan-kishore-b89643150/"
    pprint(scrape_linkedin_profile(linkedIn_url=personal_url))
