import re
import requests
from bs4 import BeautifulSoup, SoupStrainer


class MovieListParser(object):
    imdb_base_url = 'https://www.imdb.com/'

    '''
        List of Movies (Id, Name, URL)
    '''
    movie_links = []

    def __init__(self, url):
        self.response = requests.get(url)
        self.text_strainer = None
        self.soup = BeautifulSoup(self.response.text, 'html.parser')
        self.movie_links = self.scrape_movie_links()

    def scrape_movie_links(self):
        '''
            Using strainer makes parsing fast because of selective parse tree creation
        '''
        self.build_strainer('h3', 'lister-item-header')
        self.soup = BeautifulSoup(self.response.text, 'html.parser', parse_only=self.text_strainer)
        return [['tt' + re.findall(r'\d{7}', a['href'])[0], a.text, self.imdb_base_url + a['href'].lstrip('/')]
                for a in self.soup.find_all('a')]

    '''
        Build Custom Strainer
    '''

    def build_strainer(self, tag_name, tag_class):
        self.text_strainer = SoupStrainer(tag_name, class_=tag_class)

    def __str__(self):
        return len(self.movie_links).__str__()


if __name__ == '__main__':
    #Play with movie list here
    '''
        To-do : Parse multiple lists concurrently
    '''
    List = MovieListParser('https://www.imdb.com/list/ls057823854/?sort=list_order,asc&page=1')
    print(List)
