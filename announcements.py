import requests
import json
from requests.structures import CaseInsensitiveDict


def announcements():
    url = "http://api.it.teithe.gr/announcements/public"
    #url = "http://api.it.teithe.gr/announcements/public?fields=publisher,title"

    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"

    resp = requests.get(url, headers=headers)
    data = resp.json()

    lmt = slice(5)
    data = data[lmt]
    #print(data[lmt])

    store_list = []

    for item in data:
        store_details = {"id": None, "publisher":None, "title":None, "date":None}
        store_details['publisher'] = item['publisher']['name']
        store_details['id'] = item['_id']
        store_details['title'] = item['title']
        store_details['date'] = item['date']
        store_list.append(store_details)


    return store_list

def announcements_private():

    url = "http://api.it.teithe.gr/announcements"

    headers = CaseInsensitiveDict()
    headers["x-access-token"] = "ACCESS_TOKEN"
    headers["Content-Type"] = "application/json"

    resp = requests.get(url, headers=headers)
    data = resp.json()
    lmt = slice(10)
    data = data[lmt]

    #++

    print("Done private announcements", data)
    return data

def announcements_category(category_id):
   # url = "http://api.it.teithe.gr/announcements/public?q={'_about':'91ca2b75c39e553cdf0a517'}"
    #category = "591ca2b75c39e553cdf0a517"

    category = category_id
    url = 'https://api.iee.ihu.gr/announcements/public?q={"_about":"'+category+'"}'
    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    resp = requests.get(url, headers=headers)
    data = resp.json()
    lmt = slice(10)
    data = data[lmt]

    #print(data[lmt])

    store_list = []

    for item in data:
        store_details = {"id": None, "publisher":None, "title":None, "date":None}
        store_details['publisher'] = item['publisher']['name']
        store_details['id'] = item['_id']
        store_details['title'] = item['title']
        store_details['date'] = item['date']
        store_list.append(store_details)

    print(store_list)
    return store_list
