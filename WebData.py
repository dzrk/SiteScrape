from Session import Session

class WebData:

    # links of jobs details or aspects
    def get_links(self, soup, starts_with):
        links = soup.find_all('a')
        return [link.get('href') for link in links if link.get('href').startswith(starts_with)]
