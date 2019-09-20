import requests 
from requests.exceptions import HTTPError
from urllib.parse import urljoin
import logging
import time
from typing import Tuple


class Canvas:
    request_header={
        "Authorization":"Bearer",
        "Content-Type":"application/json"
    }

    def __init__(self, access_token:str, website_root:str):
        self.request_header["Authorization"] +=access_token

    def getRequest(self,url:str,params:dict= None,attempts:int=5)->Tuple[str,str]:
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
    def getAllPages(self, url: str, params: dict = None) -> list:
        """
        Get the full results from a query by following pagination links until the last page
        :param url: The URL for the query request
        :param params: A dictionary of parameter names and values to be sent with the request
        :return: The full list of result objects returned by the query
        """
        try:
            (result, link_header) = self.getRequest(url, params)

            count = len(result)
            page = 1
            while 'rel="next"' in link_header:
                page += 1

                params['per_page'] = count
                params['page'] = page
                (next_result, link_header) = self.getRequest(url, params)

                result.extend(next_result)

            return result

        except HTTPError as e:

            logging.debug("Got HTTP status %d\n", e.response.status_code)
            raise
    def getCourseIDs(self):
        #return course IDs in a array(str)
        z=3

    def getTest(self, courseId:str):
        #return test for course
        x=1

    def getHomework(self,courseId:str):
        #get homework
        y=2
    
    def getCourseInfo(self,courseId:str):
        #get information like course time
        w=0