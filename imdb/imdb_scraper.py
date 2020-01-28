import requests
from bs4 import BeautifulSoup
import re
import sys
import json

years = [i for i in range(1980,2020)]
pages = [0,100]

with open("imdb_data.txt", 'a', encoding="utf8") as output_file: 
    for year in years:
        for page in pages:
            request_url = 'http://www.imdb.com/search/title?release_date='+str(year)+'&sort=num_votes,desc&count=250&start='+str((page*250)+1)
            response = requests.get(request_url)  
            if response:          
                movies = BeautifulSoup(response.text, 'html.parser')
                elements = movies.find_all('div', class_ = 'lister-item mode-advanced')
                for elem in elements:
                    movieObj = {}
                    movieObj['directors'] = []
                    movieObj['actors'] = []
                    movieObj['imdb_id'] = elem.find('span',class_='userRatingValue')['data-tconst']
                    movieObj['name'] = elem.h3.a.text
                    movieObj['year'] = int(re.sub("[^0-9]", "", elem.h3.find('span', class_ = 'lister-item-year').text).strip())

                    if elem.find('div',class_='ratings-bar').find_next('p'):
                        movieObj['plot'] = elem.find('div',class_='ratings-bar').find_next('p').contents[0]
                    else:
                        movieObj['plot'] = None
                    if elem.find('span', class_ = 'runtime'):
                        movieObj['runtime'] = int(elem.find('span', class_ = 'runtime').text.replace('min',''))
                    else:
                        movieObj['runtime']= None
                    if elem.find('span', class_ = 'genre'):
                        movieObj['genres'] = elem.find('span', class_ = 'genre').text.strip()
                    else:
                        movieObj['genres'] = None
                    if elem.find('span', class_ = 'metascore  favorable'):
                        movieObj['metascore'] = int(elem.find('span', class_ = 'ratings-metascore').text)
                    else:
                        movieObj['metascore'] = None
                    if elem.find('span', class_ = 'certificate'):
                        movieObj['certificate'] = elem.find('span', class_ = 'certificate').text
                    else:
                        movieObj['certificate'] = 'NA'
                    movieObj['imdb_rating'] = float(elem.strong.text) if elem.strong.text else None
                    for cast in elem.find_all('p'):
                        if "Director" in cast.text or "Star" in cast.text:
                            replace_str = { 'Director:':'', 'Directors:':'', 'Stars:':'', 'Star:':''}
                            cast_string = cast.text
                            for k, v in replace_str.items():
                                cast_string = cast_string.replace(k, v)
                            cast_string = cast_string.replace('\n', ' ').replace('\r', '').strip().split("|")
                            movieObj['directors'] = [i.strip() for i in cast_string[0].split(",")]
                            if len(cast_string) > 1:
                                movieObj['actors'] = [i.strip() for i in cast_string[1].split(",")]
                    nodes = elem.find_all('span', attrs = {'name':'nv'})
                    if nodes is not None:
                        if len(nodes) == 2:
                            movieObj['votes'] = int(nodes[0]['data-value'])
                        else:
                            movieObj['votes'] = None
                        if len(nodes) > 1:
                            movieObj['revenue'] = int(nodes[1]['data-value'].replace(',',''))
                        else:
                            movieObj['revenue'] = None
                    print(json.dumps(movieObj), file = output_file)

