import requests

API_URL = "https://c19norge.no/api/v1"


def metadata(category, subcategory=None):
    res = requests.get(f"{API_URL}/current").json()
    meta = res["data"]

    if subcategory:
        data = meta.get(category, {}).get(subcategory)
    else:
        data = meta.get(category)

    return data


def timeseries(category):
    if category == "new":
        res = requests.get(f"{API_URL}/timeseries").json()
        data = res["timeseries"]["new"]
    elif category == "total":
        res = requests.get(f"{API_URL}/timeseries").json()
        data = res["timeseries"]["total"]
    else:
        res = requests.get(f"{API_URL}/timeseries/{category}").json()
        data = res[category]

    return data
