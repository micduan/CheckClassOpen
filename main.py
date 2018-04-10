
from urllib2 import urlopen as uReq
from urlparse import urlparse
from bs4 import BeautifulSoup as soup
import sys
import re
import time

def main():
	if len(sys.argv) < 4:
		print "The current way to call this function is 'python main.py {course name} {course number} {desired lecture section}."
		sys.exit(1)
	coursename = sys.argv[1].upper()
	coursenum = sys.argv[2]
	lecture = sys.argv[3]


	while True:
		if checkOpen(coursename, coursenum, lecture):
			print "ENROLL NOW!!"
			break
		time.sleep(60)

def checkOpen(coursename, coursenum, lecture):

	url = 'http://www.adm.uwaterloo.ca/cgi-bin/cgiwrap/infocour/salook.pl?level=under&sess=1185&subject=' + coursename + '&cournum=' + coursenum
	uClient = uReq(url)
	page_html = uClient.read()
	uClient.close()
	page_soup = soup(page_html, "html.parser")
	all_cells = page_soup.findAll('td')
	index = 0
	capacity = 0
	current = 0

	#The page we're retrieving the data from doesn't use any classnames or IDs so we have to retrieve the desired elements by checking the text

	for cell in all_cells:
		text = cell.get_text()

		# The 5th cell after 'LEC 00X' is the current enrollment
		if index == 5:
			current = text
		# The 6th cell after 'LEC 00X' is the current enrollment
		if index == 6:
			capacity = text
			break

		# After finding the desired cell, start keeping track of how many cells we've been to
		if (text == ('LEC 00' + lecture + ' ')):
			index += 1
			continue

		if index > 0:
			index += 1
			

	if int(current) < int(capacity):
		return True

if __name__ == '__main__':
	main()