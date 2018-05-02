from Session import Session
from WebData import WebData
from lxml import etree
from bs4 import BeautifulSoup
import Config
import csv
import re
import os
import datetime
from tqdm import tqdm


DIR = os.getcwd()
HOME = Config._BASE_URL + 'jobs_manage.aspx'
BASE_URL = Config._BASE_URL
REGEX = '[|]{2,}'

class Main:
    def main(self):
        session = Session()
        web_data = WebData()
        projects = []

        # logged in
        opener = session.start_session()
        soup = session.open_url(opener, HOME)
        job_details = web_data.get_links(soup, 'job_details')
        for jobs in job_details:
            soup = session.open_url(opener, BASE_URL + jobs)
            assign_details = web_data.get_links(soup, 'assign_details')
            projects.append(assign_details)


        for project in tqdm(projects, unit="months"):
            for url in tqdm(project, unit="urls"):
                data = []
                response = opener.open(BASE_URL + url)
                soup = BeautifulSoup(response.read(),'lxml')
                i = 0
                content_header = soup.find_all('font', {'class': 'contentheader'})
                shop_name = soup.find('div', {'class': 'contentheader'}).text.encode('ascii', 'ignore')
                check_date = soup.find('div', {'class': 'contentsub'}).text.encode('ascii', 'ignore')

                for tables in soup.find_all('table', {'class': 'tablecontent'}):
                    children = tables.findChildren(recursive=False)
                    for child in children:
                        line = []
                        word = child.get_text().encode('ascii', 'ignore').replace('\n', '|')
                        new_word = re.sub(REGEX, '|', word)
                        if new_word.startswith('|#'):
                            i += 1
                        line.append(shop_name)
                        line.append(check_date)
                        line.append(content_header[i].text)
                        line.append(new_word)
                        data.append(line)

                with open(DIR + '\\test.csv', 'ab') as csvfile:
                    for items in data:
                        csvout = csv.writer(csvfile)
                        csvout.writerow(items)
            print datetime.datetime.now()



if __name__ == '__main__':
    main = Main()
    main.main()
