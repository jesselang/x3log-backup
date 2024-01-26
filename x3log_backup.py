#!/usr/bin/env python3
import json
import os
import sys

import requests

URL_BASE = "https://api.rbtlog.com"
TOKEN = os.environ.get("X3LOG_TOKEN", "")

def get(url):
    resp = requests.get(url, headers={
        "Accept": "application/json",
        "Authorization": "Bearer "+ TOKEN,
    })
    resp.raise_for_status()
    return resp.json()

if __name__ == "__main__":
    if TOKEN == "":
        print("error: X3LOG_TOKEN not defined", file=sys.stderr)
        sys.exit(1)

    workouts = get(f"{URL_BASE}/workouts?include=exercises")

    print(json.dumps({
        "bands": get(f"{URL_BASE}/bands")["data"],
        "movements": get(f"{URL_BASE}/movements")["data"],
        "templates": get(f"{URL_BASE}/templates")["data"],
        "workouts": workouts["data"],
        "exercises": workouts["included"],
    }))



