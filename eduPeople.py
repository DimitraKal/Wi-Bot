import requests
import json
from requests.structures import CaseInsensitiveDict


def edu_people():
    url = "https://api.iee.ihu.gr/user/"
    # url = "https://api.iee.ihu.gr/user?fields=title;lang-el,telephoneNumber,displayName,labeledURI"
    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"

    people = requests.get(url, headers=headers)
    data = people.json()
    # lmt = slice(20)
    # data = data[lmt]

    peopleihu = []

    for item in data:
        try:
            store_details = {"title": None, "name": None, "telephoneNumber": None, "mail": None, "Uri": None}
            store_details['title'] = item['title;lang-el']
            store_details['name'] = item['displayName;lang-el']
            store_details['telephoneNumber'] = item['telephoneNumber']
            store_details['mail'] = item['secondarymail']
            store_details['Uri'] = item['labeledURI']

            peopleihu.append(store_details)
        except KeyError:
            print(f"{item} is unknown.")

    return peopleihu


def professor_info(name):
    url = 'https://api.iee.ihu.gr/user?q={"displayName;lang-el":"' + name + '"}'
    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"

    professor = requests.get(url, headers=headers)
    contact_info = professor.json()

    print(contact_info[0])

    return contact_info[0]
