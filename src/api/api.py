import json
import logging
import os
from urllib.parse import urljoin

import requests


class TopTrackPyAPI:
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json;charset=utf-8",
    }

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.base_url = "https://tracker-api.toptal.com"
        self.email = os.environ["TOPTRACKPY_EMAIL"]
        self.password = os.environ["TOPTRACKPY_PASSWORD"]
        self.token_storage_path = os.environ["TOPTRACKPY_TOKEN_PATH"]
        self.token = self.load_token()
        self.session = requests.Session()
        self.session.headers.update(self.HEADERS)

    class TopTrackPyAPIError(Exception):
        pass

    def load_token(self):
        if os.path.exists(self.token_storage_path):
            with open(self.token_storage_path, "r") as file:
                token = json.load(file)["access_token"]
                self.logger.info("Found token in file: " + token)
                return token
        return None

    def save_token(self, token):
        self.logger.info("Saving token to file: " + token)
        with open(self.token_storage_path, "w") as file:
            json.dump({"access_token": token}, file)

    def login(self):
        self.logger.info("Logging in...")
        response = self.session.post(
            f"{self.base_url}/sessions",
            json={"email": self.email, "password": self.password, "remember_me": True},
        )
        if response.status_code == 201:
            self.token = response.json()["access_token"]
            self.logger.info("Login successful. Saving token...")
            self.save_token(self.token)
        else:
            raise self.TopTrackPyAPIError("Login failed: " + response.text)

    def make_request(self, method, endpoint, get_params=None, **kwargs):
        self.logger.info(
            f"Making request: method={method} endpoint={endpoint} get_params={get_params} kwargs={kwargs}"
        )
        if not self.token:
            self.login()
        if not get_params:
            get_params = {}
        get_params["access_token"] = self.token
        url = urljoin(self.base_url, endpoint)
        response = self.session.request(method, url, params=get_params, **kwargs)
        if response.status_code == 401:
            self.logger.info("Token expired. Refreshing token...")
            self.token = None
            self.login()
            return self.make_request(method, endpoint, **kwargs)
        return response

    def get_projects(self, archived=True):
        endpoint = f"web/projects?archived={str(archived).lower()}"
        response = self.make_request("GET", endpoint)
        if response.status_code == 200:
            return response.json()[
                "projects"
            ]  # Assuming the response contains the projects directly
        else:
            raise self.TopTrackPyAPIError(
                "Failed to retrieve projects: " + response.text
            )

    def get_activities(self, project_id, worker_id, start_date, end_date):
        get_params = {
            "project_ids[]": project_id,
            "worker_ids[]": worker_id,
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
        }
        response = self.make_request("GET", "reports/activities", get_params=get_params)
        if response.status_code == 200:
            return response.json()["activities"]
        else:
            raise self.TopTrackPyAPIError(
                "Failed to retrieve activities: " + response.text
            )
