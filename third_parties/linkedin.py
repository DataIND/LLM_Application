import os
import requests


def scrape_linkedin_profile(linkedin_profile_url:str,mock:bool=False):

    if mock:
        linkedin_profile_url = "https://gist.githubusercontent.com/emarco177/0d6a3f93dd06634d95e46a2782ed7490/raw/78233eb934aa9850b689471a604465b188e761a0/eden-marco.json"
        response = requests.get(
            linkedin_profile_url,
            timeout=10,
        )
    else:
        api_endpoint = "http://nubela.co/proxycurl/api/v2/linkedin"
        header_dic = {"Authorization":f'Bearer {os.environ.get("PROXYCURL_API_KEY")}'}
        response = requests.get(
            api_endpoint,
            params={"url",linkedin_profile_url},
            headers=header_dic,
            timeout=10
        )

    data = response.json()

    return data


if __name__ == "__main__":
    print(
        scrape_linkedin_profile(
            linkedin_profile_url="https://www.linkedin.com/in/eden-marco/"
        )
    )