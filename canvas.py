import requests 
from requests.exceptions import HTTPError
from urllib.parse import urljoin
import logging
import time
from typing import Tuple
from datetime import datetime
import json
import collections


# Transparenftly use a common TLS session for each request
requests = requests.Session()

now=datetime.now()
today=str(now.strftime('%y-%m-%d'))

class CanvasAPI:
    request_header = {
        "Authorization": "Bearer ",
        "Content-Type": "application/json",
       "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36"
    }

    def __init__(self, canvas_token: str, website_root: str):
        self.request_header['Authorization'] += canvas_token

        if website_root.startswith("http://"):
            website_root = website_root[7:]

        if not website_root.startswith("https://"):
            website_root = "https://{}".format(website_root)

        self.website_root = website_root
     
        r = requests.get(self.website_root+'/api/v1/users/self', headers=self.request_header)
        r.raise_for_status()
        self.id=r.json()['id']
        self.name=r.json()['name']

        print(self.id)
        print(self.name)        
        

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
                                            {'state': ['available'],'enrollment_state':'active'})
        result.pop()
        result.pop(0)
        return result
    

    def get_assignments(self,course_id:str,date:str):
        params={}
        get = lambda x,y: self._get_all_pages('/api/v1/courses/%(course_id)s/%(item)s' %{'course_id':x,"item":y},params)
        assignments = get(course_id,'assignments')
        load=[]
        exams=[]
        assign=[]
        for assignment in assignments:
            try:
                
                scoring=requests.get(self.website_root+'/api/v1/courses/%(course_id)s/assignments/%(assignment_id)s/submissions/%(user_id)s' %{"course_id":course_id,"assignment_id":assignment['id'],"user_id":self.id},headers=self.request_header)
                scoring.raise_for_status()
                if "score" in scoring.json():
                    score=scoring.json()["score"]
                
                if score!=None:
                    score=int(score)
                else:
                    score=-1
                
                assignments=collections.namedtuple("assignments",('name',"points","points_possible"),defaults='0')
                if assignment['due_at']!=None:
                        due_date=datetime.strptime(assignment['due_at'][:10],"%Y-%m-%d")
                        due_date=str(due_date.date())
                else:
                    due_date='999999999999'
                    
                if score>=0 or (int(due_date[5:7])<int(today[5:7]) and int(due_date[8:10])<int(today[8:10])):
                    name=assignment['name']
                    
                    points_possible=assignment['points_possible']
                    work=assignments(name=name,points_possible=points_possible,points=score)
                    work_name=work[0].lower()
                    
                    if ('study' in work_name or "pre" in work_name) or not ("test" in work_name or 'exam' in work_name or "final" in work_name):
                        assign.append(work)
                    elif ("test" in work_name or 'exam' in work_name or "final" in work_name):
                        exams.append(work)
                    
            except HTTPError as e:
                print(e.msg)
        load.append(assign)
        load.append(exams)
        return load
    def enrollment(self,index):
        result = self._get_all_pages('/api/v1/users/'+str(self.id)+"/enrollments",{'enrollment_state':'active','enrollment':index})

        
        return result
    def fileupload(self,course_id,assignment_id,file):
 
        data={'name':file,
            'parent_folder_path':'/'}
        response=requests.post(url=self.website_root+'/api/v1/users/self/files',data=data,headers={'Authorization':self.request_header['Authorization']})
        #response=requests.post(self.website_root+'/api/v1/courses/:course_id/assignments/:assignment_id/submissions',self.request_header,post)
      
        response=response.json()['upload_url']
        response = requests.post(response, files={"file": open(file, 'rb')})
        print("Status Code for "+file+":",response.json()['location'])
        
    def turnInFile(self,file,assignment_id):
        pass

        
if __name__=='__main__':
    canvas=CanvasAPI('canvas-code','https://mst.instructure.com')
    #today=datetime.now().strftime('%y-%m-%d')
    #ass=canvas.get_assignments(canvas.get_courses()[0],today)[0]
    course=canvas.get_courses()[0]
    canvas.fileupload(58065,248446,'profile_pic.jpg')