import requests
from requests.exceptions import HTTPError

from urllib.parse import urljoin
import logging
import time
from typing import Tuple


# Transparenftly use a common TLS session for each request
requests = requests.Session()

class CanvasAPI:
    request_header = {
        "Authorization": "Bearer ",
        "Content-Type": "application/json"
    }

    def __init__(self, canvas_token: str, website_root: str):
        self.request_header['Authorization'] += canvas_token

        if website_root.startswith("http://"):
            website_root = website_root[7:]

        if not website_root.startswith("https://"):
            website_root = "https://{}".format(website_root)

        self.website_root = website_root

    def _get_request(self, url: str, params: dict = None, attempts: int = 5) -> Tuple[str, str]:
        url = urljoin(self.website_root, url)
        tries = 0
        while tries < attempts:
            try:
                r = requests.get(url, params=params, headers=self.request_header)
                r.raise_for_status()
                return (r.json(), r.headers["Link"])
            except HTTPError as e:
                if e.response is None or e.response.status_code < 500:
                    raise

                tries += 1
                if tries == attempts:
                    raise

                logging.debug("Caught %d exception in request after %d tries. Will retry %d more times.",
                              e.response.status_code, tries, attempts - tries, exc_info=True)
                time.sleep(0.5 * 2 ** (tries - 1))

    def _get_all_pages(self, url: str, params: dict = None) -> list:
        """
        Get the full results from a query by following pagination links until the last page
        :param url: The URL for the query request
        :param params: A dictionary of parameter names and values to be sent with the request
        :return: The full list of result objects returned by the query
        """
        try:
            (result, link_header) = self._get_request(url, params)

            count = len(result)
            page = 1
            while 'rel="next"' in link_header:
                page += 1

                params['per_page'] = count
                params['page'] = page
                (next_result, link_header) = self._get_request(url, params)

                result.extend(next_result)

            return result

        except HTTPError as e:

            logging.debug("Got HTTP status %d\n", e.response.status_code)
            raise

    def get_courses(self):
        result = self._get_all_pages('/api/v1/courses',
                                            {'enrollment_type': 'student', 'state': ['available']})
        
        return result

    def get_assignments(self,course_id):
        get = lambda x: self._get_all_pages('/api/v1/courses/%s/')
        result = get('student')
        return result

    def get_course_students(self, course_id: str):
        try:
            params = {
                'per_page': 50,
                'enrollment_type': ['student'],
                'enrollment_state': ['active']
            }
            result = self._get_all_pages('/api/v1/courses/%s/users', params)
            return result

        except HTTPError as e:
             raise

if __name__=="__main__":
    canvas =CanvasAPI('2006~hvjl4mDeAR2jYoxOYWkCbgp5Xpm7NSMCnNG9SRJ7hscjc6k3xzA6Aq4vW9TxtuRO','https://mst.instructure.com')
    x=canvas.get_courses()
    for i in range(len(x)):
        y=x[i]
        print(y['name']+": "+str(y['id']))