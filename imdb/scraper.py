import requests, csv, re
from bs4 import BeautifulSoup, SoupStrainer

class MovieParser(object):
	'''Parses the text on movies page'''
	def __init__(self, url):
		self.response = requests.get(url)
		self.name = ""
		self.id = 0
		self.year = 0
		self.runtime = 0
		self.genres = []
		self.rating = 0
		self.votes = 0
		self.revenue = 0
		self.cast = []
		self.directors = []
		self.writers = []

	def extract_vitals(self):
		MovieParser.text_strainer = SoupStrainer(MovieParser.build_strainer(self, "div", "titleBar"))
		self.soup = BeautifulSoup(self.response, "html.parser", parse_only=MovieParser.text_strainer)
		self.name = self.soup.findAll('h1')
		print(self.soup)

	@staticmethod
	def build_strainer(self, tag_name, tag_class):
		return SoupStrainer(tag_name, class_=tag_class)

		

if __name__ == '__main__':
	movie = MovieParser('https://www.imdb.com/title/tt0110912/?ref_=tt_sims_tt')
	movie.extract_vitals()
