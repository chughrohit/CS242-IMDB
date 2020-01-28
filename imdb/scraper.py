import requests, re
from bs4 import BeautifulSoup, SoupStrainer

'''
	Parses the text on movies page
'''
class MovieParser(object):

	def __init__(self, url):
		self.response = requests.get(url)

		''' 
			Vitals 
		'''
		self.name = ""
		self.id = 'tt' + re.findall(r'\d{7}',url)[0]
		self.year = ""
		self.rating = ""
		self.votes = ""
		self.runtime = ""
		self.certificate = ""
		self.genres = []
		self.releaseDate = ""

		'''
			Plot Summary
		'''
		self.summary = ""
		self.directors = []
		self.writers = []
		self.stars = []

		'''
			Populate Fields
		'''
		self.extract_vitals()
		self.extract_plot_summary()


	'''
		Extract Movie's Vital Information
	'''
	def extract_vitals(self):
		'''
			Using strainer makes parsing fast because of selective parse tree creation
		'''
		MovieParser.build_strainer(self, 'div', 'title_block')
		self.soup = BeautifulSoup(self.response.text, 'html.parser', parse_only=MovieParser.text_strainer)

		self.name = self.soup.find('h1').next.strip()
		self.year = self.soup.find('span',{'id':'titleYear'}).find_next('a').next.strip()
		self.rating = self.soup.find('span', {'itemprop':'ratingValue'}).next.strip()
		self.votes = self.soup.find('span', {'itemprop':'ratingCount'}).next.strip()
		self.runtime = re.findall(r'\d+', self.soup.find('time')['datetime'])[0].strip()

		subtext = self.soup.find('div', {'class':'subtext'})
		self.certificate = subtext.next.strip()
		self.genres = [genre.text.strip() for genre in subtext.find_all_next('a')[:-1]]
		self.releaseDate = subtext.find_all_next('a')[-1].text.strip()

	'''
		Extract Movie's Plot Summary, Director(s), Writer(s) and Cast(s)
	'''
	def extract_plot_summary(self):
		'''
			Using strainer makes parsing fast because of selective parse tree creation
		'''
		MovieParser.build_strainer(self, 'div', 'plot_summary ')
		self.soup = BeautifulSoup(self.response.text, 'html.parser', parse_only=MovieParser.text_strainer)

		self.summary = self.soup.find('div', {'class':'summary_text'}).next.strip()
		items = [item.find_all('a') for item in self.soup.find_all('div', {'class':'credit_summary_item'})]
		self.directors = [director.text.strip() for director in items[0]]
		self.writers = [writer.text.strip() for writer in items[1] if not writer.text.startswith('1')]
		self.stars = [star.text.strip() for star in items[2] if not star.text.startswith('See full')]

	'''
		Build Custom Strainer
	'''
	@staticmethod
	def build_strainer(self, tag_name, tag_class):
		MovieParser.text_strainer = SoupStrainer(tag_name, class_=tag_class)


	def __str__(self):
		return self.name + ' | ' + self.releaseDate + ' | ' + self.rating


if __name__ == '__main__':
	# Play here with Movie Parser
	PulpFiction = MovieParser('https://www.imdb.com/title/tt0110912/?ref_=tt_sims_tt')
	print(PulpFiction)

	TheDarkKnight = MovieParser('https://www.imdb.com/title/tt0468569/?ref_=tt_sims_tt')
	print(TheDarkKnight)


