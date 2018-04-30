from lxml import html
from bs4 import BeautifulSoup
import Config
import cookielib
import urllib
import urllib2


LOGIN_URL = Config._LOGIN_URL
USERNAME = Config._USERNAME
PASSWORD = Config._PASSWORD
HOME = Config._HOME


class Session():

    def start_session(self):
        post = {
            '__EVENTVALIDATION': None,
            '__VIEWSTATE': None,
            'stype': 'login',
            'txtUsername': USERNAME,
            'txtPassword': PASSWORD
        }

        cookie_jar = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie_jar))
        urllib2.install_opener(opener)

        f = opener.open(LOGIN_URL)
        soup = BeautifulSoup(f, 'lxml')

        # get token details
        for i in [k for k, v in post.iteritems() if v is None]:
            post[i] = soup.find('input', {'id': i})['value']
        # login with all post details
        opener.open(LOGIN_URL, urllib.urlencode(post))
        return opener

    def open_url(self, opener,  url):

        # logged in with cookies
        html = opener.open(url)
        # print f.read()
        return BeautifulSoup(html, 'lxml')

    # links of jobs details or aspects
    def get_links(self, soup, starts_with):
        links = soup.find_all('a')
        return [link.get('href') for link in links if link.get('href').startswith(starts_with)]


if __name__ == '__main__':
    session = Session()
    opener = session.start_session()
    session.open_url(opener, HOME)
