import pandas as pd
import datetime
import requests
import finnhub
import string
import json
import time
import re
import os

clearScreen = True
API_Key = 'YOUR_FINNHUB_API_KEY'



#Cleaned up print statements in a CLI iteration of this project
def clear():
	if clearScreen == True:
		try:
			os.system("clear")
		except:
			print("error")
	pass
	
def companyData(symbol):
	r = requests.get('https://finnhub.io/api/v1/stock/profile2?symbol='+ symbol +'&token='+ API_Key)
	data = str((json.dumps(r.json(), sort_keys=True, indent=0)))
	cleaned = data.replace(',', '')
	cleaned = cleaned.replace('[', '')
	cleaned = cleaned.replace(']', '')
	cleaned = cleaned.replace('"', '')
	cleaned = cleaned.replace('{', '')
	cleaned = cleaned.replace('}', '')
	cleaned = cleaned.replace('country:', 'Country:')
	cleaned = cleaned.replace('currency:', 'Currency:')
	cleaned = cleaned.replace('exchange:', 'Exchange:')
	cleaned = cleaned.replace('finnhubIndustry:', 'Industry:')
	cleaned = cleaned.replace('ipo:', 'Went Public:')
	cleaned = cleaned.replace('logo:', 'Logo:')
	cleaned = cleaned.replace('summary:', 'Summary:')
	cleaned = cleaned.replace('marketCapitalization:', 'Market Cap:')
	cleaned = cleaned.replace('name:', 'Name:')
	cleaned = cleaned.replace('phone:', 'Phone Number:')
	cleaned = cleaned.replace('shareOutstanding:', 'Outstanding Shares:')
	cleaned = cleaned.replace('ticker:', 'Ticker:')
	cleaned = cleaned.replace('weburl:', 'Website:')
	result = os.linesep.join([s for s in cleaned.splitlines() if s])
	return (result)

def epochToDateTime(string):
	if "Date/Time" in string:
		extracted = str([int(s) for s in string.split() if s.isdigit()]) 										#extract digits
		cleaned = extracted.replace('[', '')
		cleaned = cleaned.replace(']', '')
		datePost = str(datetime.datetime.fromtimestamp(int(cleaned)).strftime('%b %d %Y - %-I:%M:%S %p'))		#convert from Unix time current location
		converted = ("Date/Time: " + datePost)
		return converted

def companyNews(symbol):
	r = requests.get('https://finnhub.io/api/v1/company-news?symbol='+ symbol +'&from=2020-04-30&to=2020-05-01&token='+ API_Key)
	data = str((json.dumps(r.json(), sort_keys=True, indent=0)))
	if data == '[]':
		message = ("Unable to retreive data for: "+ symbol)
		return message
	cleaned = data.replace(',', '')
	cleaned = cleaned.replace('[', '')
	cleaned = cleaned.replace(']', '')
	cleaned = cleaned.replace('"', '')
	cleaned = cleaned.replace('{', '')
	cleaned = cleaned.replace('}', '')
	cleaned = cleaned.replace('category:', 'Category:')
	cleaned = cleaned.replace('datetime:', 'Date/Time:')
	cleaned = cleaned.replace('headline:', 'Headline:')
	cleaned = cleaned.replace('id:', 'ID:')
	cleaned = cleaned.replace('image:', 'Image:')
	cleaned = cleaned.replace('related:', 'Related:')
	cleaned = cleaned.replace('source:', 'Source:')
	cleaned = cleaned.replace('summary:', 'Summary:')
	cleaned = cleaned.replace('url:', 'URL:')
	final = ''
	for line in cleaned.split('\n'):
		if "Date/Time" not in line:
			final = (final + line + "\n")
		else:
			convert = epochToDateTime(line)
			final = (final + convert + "\n")
	return(final)
	
	
	
def companyMajorPress(symbol, client):
	data = str(client.major_developments(symbol, _from="2020-04-01", to="2020-12-31"))
	if "'majorDevelopment': []," in data:
		message = ("Unable to retreive data for: "+ symbol)
		return message
	cleaned = data.replace(',', '')
	cleaned = cleaned.replace('[', '')
	cleaned = cleaned.replace(']', '')
	cleaned = cleaned.replace("'", '')
	cleaned = cleaned.replace('{', '')
	cleaned = cleaned.replace('}', '')
	cleaned = string.capwords(cleaned)
	cleaned = cleaned.replace('Datetime:', '\n \n \nDate/Time:')
	cleaned = cleaned.replace('Headline:', '\nHeadline:')
	cleaned = cleaned.replace('Description:', '\nDescription:')
	final = ''
	for line in cleaned.splitlines():
		if 'Majordevelopment:' not in line:
			final = (final + line + "\n")
	return (final)


def newsSentiment(symbol):
	r = requests.get('https://finnhub.io/api/v1/news-sentiment?symbol='+ symbol +'&token='+ API_Key)
	data = (str(json.dumps(r.json(), sort_keys=True, indent=0)))
	if '"buzz": null,' in data:
		message = ("Unable to retreive data for: "+ symbol)
		return message
	data = data.replace('"buzz": {', '')
	cleaned = data.replace(',', '')
	cleaned = cleaned.replace('[', '')
	cleaned = cleaned.replace(']', '')
	cleaned = cleaned.replace('"', '')
	cleaned = cleaned.replace('{', '')
	cleaned = cleaned.replace('}', '')
	cleaned = cleaned.replace('sentiment: ', '')
	cleaned = os.linesep.join([s for s in cleaned.splitlines() if s])
	cleaned = cleaned.replace("symbol: "+symbol, '')
	cleaned = cleaned.replace('articlesInLastWeek', 'Articles in Last Week')
	cleaned = cleaned.replace('buzz', 'Weekly Buzz Percentage')
	cleaned = cleaned.replace('weeklyAverage', 'Average Weekly Article Count')
	cleaned = cleaned.replace('companyNewsScore', symbol+ ' News Score')
	cleaned = cleaned.replace('sectorAverageBullishPercent', 'Sector Bullish Percentage')
	cleaned = cleaned.replace('sectorAverageNewsScore', 'Sector News Score')
	cleaned = cleaned.replace('bearishPercent', 'Bearish News Percentage: ')
	result = cleaned.replace('bullishPercent', 'Bullish News Percentage: ')
	return (result)


def companyFinancials(symbol):
	r = requests.get('https://finnhub.io/api/v1/stock/metric?symbol='+ symbol +'&metric=all&token='+ API_Key)
	data = str(json.dumps(r.json(), sort_keys=True, indent=0))
	if '"metric": {},' in data:
		message = ("Unable to retreive data for: "+ symbol)
		return message
	data = data.replace('{', '')
	data = data.replace('[]', 'Unavailable')
	noLines = str(os.linesep.join([s for s in data.splitlines() if s]))
	cleaned = noLines.replace(',', '')
	cleaned = cleaned.replace('[', '\n')
	cleaned = cleaned.replace('"', '')
	cleaned = cleaned.replace(']', '')
	cleaned = cleaned.replace('}', '')
	cleaned = cleaned.replace('bs:','\nBalance Sheet:')
	cleaned = cleaned.replace('ic:','Information Coefficient: ')
	cleaned = cleaned.replace('cf:','Cashflow Statement:')
	cleaned = cleaned.replace('cik:','Central Index Key:')
	final = ''
	for line in cleaned.splitlines():
		if "null" not in line:
			if "metricType: all" not in line:
				if "series: " not in line:
					if "annual: " not in line:   
						if "metrInformation Coefficient:  " not in line:
							if ("symbol: "+symbol) not in line:
								final = (final + line + "\n")
	cleaned = final.replace('v: ','Percent Change: ')
	cleaned = cleaned.replace('period: ','Time Period: ')
	cleaned = cleaned.replace('cashRatio: ','\nCash Ratio: ')
	cleaned = cleaned.replace('currentRatio: ','Current Ratio: ')
	cleaned = cleaned.replace('ebitPerShare: ','Earnings Per Share Before Interest and Taxes: ')
	cleaned = cleaned.replace('eps: ','Earnings Per Share: ')
	cleaned = cleaned.replace('grossMargin: ','Gross Margin: ')
	cleaned = cleaned.replace('longtermDebtTotalAsset: ','Long Term Debt Total Asset: ')
	cleaned = cleaned.replace('currentRatio: ','Current Ratio: ')
	cleaned = cleaned.replace('longtermDebtTotalCapital: ','Long Term Dept Total Capital: ')
	cleaned = cleaned.replace('longtermDebtTotalEquity: ','Long Term Dept Total Equity: ')
	cleaned = cleaned.replace('netDebtToTotalCapital: ','Net Debt to Total Capital: ')
	cleaned = cleaned.replace('netDebtToTotalEquity: ','Net Debt to Total Equity: ')
	cleaned = cleaned.replace('netMargin: ','Net Margin: ')
	cleaned = cleaned.replace('operatingMargin: ','Operating Margin: ')
	cleaned = cleaned.replace('pretaxMargin: ','Pre-Tax Margin: ')
	cleaned = cleaned.replace('salesPerShare: ','Sales Per Share: ')
	cleaned = cleaned.replace('sgaToSale: ','Selling, General and Administrative Expense to Sales: ')
	cleaned = cleaned.replace('totalDebtToEquity: ','Total Debt to Equity: ')
	cleaned = cleaned.replace('totalDebtToTotalAsset: ','Total Debt to Total Asset: ')
	cleaned = cleaned.replace('totalDebtToTotalCapital: ','Total Debt to Total Capital: ')
	cleaned = cleaned.replace('totalRatio: ','Total Ratio: ')
	return (cleaned)

	
def reportedFinancials(symbol):
	r = requests.get('https://finnhub.io/api/v1/stock/financials-reported?symbol='+ symbol +'&token='+ API_Key)
	data = str(json.dumps(r.json(), sort_keys=True, indent=0))
	if '"data": [],' in data:
		message = ("Unable to retreive data for: "+ symbol)
		return message
	data = data.replace('{', '')
	data = data.replace('[]', 'Unavailable')
	noLines = str(os.linesep.join([s for s in data.splitlines() if s]))
	cleaned = noLines.replace(',', '')
	cleaned = cleaned.replace('[', '\n')
	cleaned = cleaned.replace('"', '')
	cleaned = cleaned.replace(']', '')
	cleaned = cleaned.replace('}', '')
	cleaned = cleaned.replace('bs:','\nBalance Sheet:')
	cleaned = cleaned.replace('ic:','\nInformation Coefficient: ')
	cleaned = cleaned.replace('cf:','Cashflow Statement:')
	cleaned = cleaned.replace('cik:','Central Index Key:')
	cleaned = cleaned.replace('startDate:','Start Date:')
	cleaned = cleaned.replace('symbol:','Symbol:')
	cleaned = cleaned.replace('year:','Year:')
	cleaned = cleaned.replace('concept:','Concept:')
	cleaned = cleaned.replace('label:','Label:')
	cleaned = cleaned.replace('unit:','Unit:')
	cleaned = cleaned.replace('value:','Value:')
	noLines = str(os.linesep.join([s for s in cleaned.splitlines() if s]))
	final = ''
	for line in noLines.splitlines():
		if "Information Coefficient:" not in line:
			if "Symbol:" not in line:
				if "data:" not in line:
					if "report:" not in line:
						if "Unavailable:" not in line:
							final = (final + line + "\n")
	cleaned = final.replace('Balance Sheet:','\n\nBalance Sheet:')
	cleaned = cleaned.replace('Cashflow Statement:', '\n\nCashflow Statement:')
	cleaned = cleaned.replace('Central Index Key:', 'Central Index Key:')
	cleaned = cleaned.replace('Start Date:', '\n\n\nStart Date:')
	cleaned = cleaned.replace('Concept:','\nConcept:')
	cleaned = cleaned.replace('acceptedDate:','Date Accepted:')
	cleaned = cleaned.replace('accessNumber:','Access Number:')
	cleaned = cleaned.replace('endDate:','End Date:')
	cleaned = cleaned.replace('filedDate:','Date Filed:')
	cleaned = cleaned.replace('form:','Form Name:')
	final = cleaned.replace('quarter:','Quarter:')
	return (final)
	
	
def companyPeers(symbol):
	r = requests.get('https://finnhub.io/api/v1/stock/peers?symbol='+ symbol +'&token='+ API_Key)
	data = str(json.dumps(r.json(), sort_keys=True, indent=0))
	if data == '[]':
		message = ("Unable to retreive data for: "+ symbol)
		return message

	cleaned = data.replace(',', '')
	cleaned = cleaned.replace('[', '')
	cleaned = cleaned.replace(']', '')
	cleaned = cleaned.replace('"', '')
	cleanList = [y for y in (x.strip() for x in cleaned.splitlines()) if y] 			#Creates List Object From String
	result = ", ".join(cleanList) 														#Creates comma-separated string from list object
	counter = 1
	result = os.linesep.join([s for s in cleaned.splitlines() if s]) 					#Removes Empty Lines
	final = ''
	for line in result.split('\n'):		
		finalLine = (str(counter) + '. ' + line)
		final = (final + finalLine + '\n')
		counter = counter + 1
	return (final)


def companyExecutives(symbol, client):
	executives = str(client.company_executive(symbol))
	if executives == "{'executive': [], 'symbol': ''}":
		message = ("Unable to retreive data for: "+ symbol)
		return message
	data = executives.replace('{', '')
	data = data.replace('[]', 'Unavailable')
	data = data.replace("''", 'Unavailable')
	data = data.replace("'symbol': '"+symbol, '')
	noLines = str(os.linesep.join([s for s in data.splitlines() if s]))
	cleaned = noLines.replace(',', '\n')
	cleaned = cleaned.replace('[', '\n ')
	cleaned = cleaned.replace("'", '')
	cleaned = cleaned.replace('"', '')
	cleaned = cleaned.replace(']', '')
	cleaned = cleaned.replace('}', '\n')
	cleaned = cleaned.replace('None', 'Unavailable')
	final = cleaned.replace('executive: ', '')
	return (final)


def estimatedEPS(symbol, client):
	eps = str(client.company_eps_estimates(symbol, freq='quarterly'))
	if eps == "{'data': [], 'freq': 'quarterly', 'symbol': '"+symbol+"'}":
		message = ("Unable to retreive data for: "+ symbol)
		return message
	data = eps.replace('{', '')
	data = data.replace('[]', 'Unavailable')
	data = data.replace("''", 'Unavailable')
	data = data.replace("'symbol': '"+symbol, '')
	noLines = str(os.linesep.join([s for s in data.splitlines() if s]))
	cleaned = noLines.replace(',', '\n')
	cleaned = cleaned.replace('[', '\n ')
	cleaned = cleaned.replace("'", '')
	cleaned = cleaned.replace('"', '')
	cleaned = cleaned.replace(']', '')
	cleaned = cleaned.replace('}', '\n')
	cleaned = cleaned.replace('None', 'Unavailable')
	cleaned = cleaned.replace('epsAvg: ', 'Average Estimate: ')
	cleaned = cleaned.replace('epsHigh: ', 'Highest Estimate: ')
	cleaned = cleaned.replace('epsLow: ', 'Lowest Estimate: ')
	cleaned = cleaned.replace('numberAnalysts: ', 'Number of Analysts: ')
	cleaned = cleaned.replace('period: ', 'Period: ')
	cleaned = cleaned.replace(' freq: quarterly', '')
	final = cleaned.replace('data:', '')  
	return (final)


def earningsCalendar(symbol, client):
	eps = str(client.earnings_calendar(symbol=symbol, international=False))
	if eps == "{'earningsCalendar': []}":
		message = ("Unable to retreive data for: "+ symbol)
		return message
	data = eps.replace('{', '')
	data = data.replace('[]', 'Unavailable')
	data = data.replace("''", 'Unavailable')
	noLines = str(os.linesep.join([s for s in data.splitlines() if s]))
	cleaned = noLines.replace(',', '\n')
	cleaned = cleaned.replace('[', '\n ')
	cleaned = cleaned.replace("'", '')
	cleaned = cleaned.replace('"', '')
	cleaned = cleaned.replace(']', '')
	cleaned = cleaned.replace('}', '\n')
	cleaned = cleaned.replace('None', 'Unavailable')
	cleaned = cleaned.replace('epsActual: ', 'actual EPS: ')
	cleaned = cleaned.replace('epsEstimate: ', 'estimated EPS: ')
	cleaned = cleaned.replace('revenueActual: ', 'actual revenue: ')
	cleaned = cleaned.replace('revenueEstimate: ', 'estimated revenue: ')
	cleaned = cleaned.replace('amc', 'After Market Close')
	cleaned = cleaned.replace('bmo', 'Before Market Open')
	cleaned = cleaned.replace('dmh', 'During Market Hour')
	cleaned = cleaned.replace(': ', ':  ')
	cleaned = cleaned.replace(' freq: quarterly', '')
	final = cleaned.replace('data:', '')  
	return (final)


def earningsSuprises(symbol, client):
	earningsSuprises = str(client.company_earnings(symbol))
	if earningsSuprises == '[]':
		message = ("Unable to retreive data for: "+ symbol)
		return message
	data = earningsSuprises.replace('{', '')
	data = data.replace('[]', 'Unavailable')
	data = data.replace("''", 'Unavailable')
	noLines = str(os.linesep.join([s for s in data.splitlines() if s]))
	cleaned = noLines.replace(',', '\n')
	cleaned = cleaned.replace('[', '\n ')
	cleaned = cleaned.replace("'", '')
	cleaned = cleaned.replace('"', '')
	cleaned = cleaned.replace(']', '')
	cleaned = cleaned.replace('}', '\n')
	cleaned = cleaned.replace('None', 'Unavailable')
	cleaned = cleaned.replace(' actual: ', ' Actual:   ')
	cleaned = cleaned.replace(' estimate: ', ' Estimate: ')
	cleaned = cleaned.replace(' period: ', ' Period:   ')
	cleaned = cleaned.replace(' symbol: ', ' Symbol:   ')
	return (cleaned)


def recommendationTrends(symbol, client):
	eps = str(client.recommendation_trends(symbol))
	if eps == '[]':
		message = ("Unable to retreive data for: "+ symbol)
		return message
	data = eps.replace('{', '')
	data = data.replace('[]', 'Unavailable')
	data = data.replace("''", 'Unavailable')
	noLines = str(os.linesep.join([s for s in data.splitlines() if s]))
	cleaned = noLines.replace(',', '\n')
	cleaned = cleaned.replace('[', '\n ')
	cleaned = cleaned.replace("'", '')
	cleaned = cleaned.replace('"', '')
	cleaned = cleaned.replace(']', '')
	cleaned = cleaned.replace('}', '\n')
	cleaned = cleaned.replace('None', 'Unavailable')
	cleaned = cleaned.replace('epsActual: ', 'actual EPS: ')
	cleaned = cleaned.replace('epsEstimate: ', 'estimated EPS: ')
	cleaned = cleaned.replace('revenueActual: ', 'actual revenue: ')
	cleaned = cleaned.replace('revenueEstimate: ', 'estimated revenue: ')
	cleaned = cleaned.replace('amc', 'After Market Close')
	cleaned = cleaned.replace('bmo', 'Before Market Open')
	cleaned = cleaned.replace('dmh', 'During Market Hour')
	cleaned = cleaned.replace('freq: quarterly', '')
	final = cleaned.replace('data:', '')  
	return (final)


def companySharePrice(symbol, client):
	r = requests.get('https://finnhub.io/api/v1/quote?symbol='+ symbol +'&token='+ API_Key)
	data = str(json.dumps(r.json(), sort_keys=True, indent=0))
	if data == '{}':
		message = ("Unable to retreive data for: "+ symbol)
		return message
	cleaned = data.replace(',', '')
	cleaned = cleaned.replace('{', '')
	cleaned = cleaned.replace('}', '')
	cleaned = cleaned.replace('"', '')
	cleaned = cleaned.replace('pc:', 'Previous Close Price:')
	cleaned = cleaned.replace('h:', 'High Price:')
	cleaned = cleaned.replace('l:', 'Low Price:')
	cleaned = cleaned.replace('o:', 'Opening Price:')
	cleaned = cleaned.replace('c:', 'Current Price:')
	preTime = cleaned.replace('t:', 'Date/Time:')
	preTime = str(os.linesep.join([s for s in preTime.splitlines() if s])) 									#remove empty lines
	final = ("\n".join(preTime.split("\n")[:5]))
	datePre = ("\n".join(preTime.split("\n")[5:]))
	extracted = str([int(s) for s in datePre.split() if s.isdigit()]) 										#extract digits
	cleaned = extracted.replace('[', '')
	cleaned = cleaned.replace(']', '') 																		#get rid of of brackets
	datePost = str(datetime.datetime.fromtimestamp(int(cleaned)).strftime('%-I:%M:%S %p - %A %b %d %Y'))	#convert from Unix time current location
	split = re.split("\n", final) 																			#split each line into list elements
	final = ''																								
	for item in split:
		extractFloats = str(re.findall(r"[-+]?\d*\.\d+|\d+", str(item))) 									#extract floating point digits
		withMoneySign = ('$' + extractFloats) 
		cleaned = withMoneySign.replace("['", '')
		cleaned = cleaned.replace("']", '')		
		cleaned = cleaned.replace("']", '')																	#get rid of of brackets
		if '.' in item:
			extractedText = ((re.sub(r"(\d+\.\d+)", '', item)))
			extractedFloats = ("Removed", re.search(r"(\d+\.\d+)", item).group(1))
			finalLine = str(extractedText + cleaned + '\n')
			final = final + finalLine
	final = (datePost + "\n \n" + final)
	return final		


def choices(symbol):
	symbol = str(symbol.upper())
	clear()
	print("1.  "+ symbol +" - Share Price & General Info \n2.  "+ symbol +" - News & Major Press Releases \n3.  "+ symbol +" - News Analysis \n4.  "+ symbol +" - Industry Competitors \n5.  "+ symbol +" - Financial Overview \n6.  "+ symbol +" - Reported Financials \n7.  "+ symbol +" - Excecutives \n8.  "+ symbol +" - Estimated EPS \n9.  "+ symbol +" - Earnings Calendar \n10. "+ symbol +" - Earnings Suprises \n11. "+ symbol +" - Monthly Recommendation Trends ")
	selection = input("Choose an Option: ")	
	client = finnhub.Client(api_key=(API_Key))
	print('\n')
	if selection == '1':
		clear()
		print(symbol + "'s Share Price & General Information:")
		print(companySharePrice(symbol, client))
		print(companyData(symbol))
	if selection == '2':
		clear()
		print('1. All Press Releases: ')
		print('2. Major Press Releases: ')
		choice = input('Choose an Option: ')
		if choice == '1':
			clear()
			print("All "+ symbol +" Press Releases:\n")
			print(companyNews(symbol))
		if choice == '2':
			clear()
			print("Major "+ symbol +" Press Releases:\n")
			print(companyMajorPress(symbol,client))
	if selection == '3':
		clear()
		print(symbol + " News Trend Analysis:\n")
		print(newsSentiment(symbol))
	if selection == '4':
		clear()
		print(symbol + " Market Peers:\n")
		print(companyPeers(symbol))
	if selection == '5':
		clear()
		print(symbol + " Financials:\n")
		print(companyFinancials(symbol))
	if selection == '6':
		clear()
		print(symbol + " Financials as Reported:\n")
		print(reportedFinancials(symbol))
	if selection == '7':
		clear()
		print(symbol + " Executives:")
		print(companyExecutives(symbol, client))
	if selection == '8':
		clear()
		print(" Estimated"+ symbol +"Earnings Per Share:")
		print(estimatedEPS(symbol, client))
	if selection == '9':
		clear()
		print(symbol + " Earnings Calendar:")
		print(earningsCalendar(symbol, client))
	if selection == '10':
		clear()
		print(symbol + " Quarterly Earnings Suprises:")
		print(earningsSuprises(symbol, client))
	if selection == '11':
		clear()
		print(symbol + " Monthly Analyst Recommendation Trends:")
		print(recommendationTrends(symbol, client))
		
		
'''
For a CLI demo of the above functions, add your Finnhub API key to the "API_Key" variable at the top, uncomment the following line of code, and run this script.
If you wish to use this code remotely, add make sure that you provide an API key string wherever the "API_Key" variable is present.
'''

#choices((input("Enter a Companies' Ticker: ")))