import requests
import pandas as pd
from bs4 import BeautifulSoup


# load the excel first, then create the object for scheduling, and then wait

class Tickers:
	data = pd.read_excel("sp500tickers.xlsx")
	data.fillna(0, inplace=True)

class Form:
	def __init__(self, form, ticker, date):
		self.form = form
		self.ticker = ticker.upper()
		self.date = date
		df = Tickers.data
		cik = df[df["Ticker"]==ticker.upper()]["CIK"].values[0]
		print(f"Finding Data -> (Ticker: {ticker}, CIK: {cik})")
		
		baseurl = "http://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=" /
		+ str(cik) + "&type=" + form + "&dateb=" + str(date) + "&owner=exclude&output=xml&count=1"

		r = requests.get(baseurl)
		if r.status_code != 200:
			raise ValueError("Could not connect to SEC Edgar.")

		else:
			self.data = r.text
			return r.text

	def document_list(self):
		soup = BeautifulSoup(self.data)
		links = []
		for link in soup.find_all("filinghref"):
			links.append(link+"l")
		return links
		


