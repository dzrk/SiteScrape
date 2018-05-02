from lxml import html
from bs4 import BeautifulSoup
import Config
import cookielib
import urllib
import urllib2


LOGIN_URL = Config._BASE_URL + 'default.aspx'
USERNAME = Config._USERNAME
PASSWORD = Config._PASSWORD


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

        soup = self.open_url(opener, LOGIN_URL)

        # get token details
        for i in [k for k, v in post.iteritems() if v is None]:
            post[i] = soup.find('input', {'id': i})['value']

        # login with all post details
        opener.open(LOGIN_URL, urllib.urlencode(post))
        return opener

    def open_url(self, opener,  url):

        # logged in with cookies
        html = opener.open(url)
        return BeautifulSoup(html, 'lxml')

