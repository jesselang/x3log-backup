#!/usr/bin/env python3
import json
import os
import sys

import requests

URL_BASE = "https://api.rbtlog.com"

def get_token(url, email, password):
    resp = requests.post(url,
        headers={"Accept": "application/json"},
        json={"email": email, "password": password},
    )
    resp.raise_for_status()
    return resp.json()["data"]["attributes"]["token"]

def get(url, token):
    resp = requests.get(url, headers={
        "Accept": "application/json",
        "Authorization": f"Bearer {token}",
    })
    resp.raise_for_status()
    return resp.json()


if __name__ == "__main__":
    token = os.environ.get("X3LOG_TOKEN", "")
    if token == "":
        print("warning: X3LOG_TOKEN not defined", file=sys.stderr)
        email = os.environ.get("X3LOG_EMAIL", "")
        password = os.environ.get("X3LOG_PASSWORD", "")

        if email == "" or password == "":
            print("error: X3LOG_EMAIL or X3LOG_PASSWORD not defined",
                  file=sys.stderr)
            sys.exit(1)

        token = get_token(f"{URL_BASE}/auth/login", email, password)

        if token == "":
            print("error: could not obtain token from email/password",
                  file=sys.stderr)
            sys.exit(1)


    workouts = get(f"{URL_BASE}/workouts?include=exercises", token)

    print(json.dumps({
        "bands": get(f"{URL_BASE}/bands", token)["data"],
        "movements": get(f"{URL_BASE}/movements", token)["data"],
        "templates": get(f"{URL_BASE}/templates", token)["data"],
        "workouts": workouts["data"],
        "exercises": workouts["included"],
    }))



