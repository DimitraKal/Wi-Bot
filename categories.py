import requests
import json
from requests.structures import CaseInsensitiveDict


def categories_all():
    url = "http://api.it.teithe.gr/categories/public"

    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"

    resp = requests.get(url, headers=headers)
    data = resp.json()

    categories = []

    for item in data:
        store_details = {"id": None, "name": None}
        store_details['id'] = item['_id']
        store_details['name'] = item['name']
        categories.append(store_details)

    return categories
