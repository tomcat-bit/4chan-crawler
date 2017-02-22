from BeautifulSoup import BeautifulSoup
import urllib2, sys, requests, os, errno

# Used as header to avoid failed request. 
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}


thread_link_length = 17
media_format = [".jpg", ".png", ".gif", ".webm"]


# Describes one page
class Page(object):
	def __init__(self, board):
		self.board = board
	

	# Gets the URL of all pages
	def get_pages(self):
		pages = []
		for i in range(2, 11):
			s = "http://boards.4chan.org/" + self.board + "/" + str(i)
			pages.append(s)

		return pages


# Describes one thread
class Thread(object):
	def __init__(self, page):
		self.page = page


	def get_threads(self):
		req = urllib2.Request(self.page, headers=hdr)
		html_page = urllib2.urlopen(req)
		soup = BeautifulSoup(html_page)
		threads = list()

		# Get the threads and their names
		for link in soup.findAll('a'):
			s = str(link.get('href'))

			# Only select threads, no replies within a thread and
			# visit no thread multiple times.
			if "thread" in s and "#" not in s and len(s) < thread_link_length and s not in threads:
				threads.append(str(s))

		return threads



class Crawl(object):
	def __init__(self, board):
		self.board = board
		self.base_url = "boards.4chan.org/" + self.board + "/"


	# Crawls through 'thread' and downloads all the digital content
	def crawl_thread(self, thread):
		page = str('http://' + self.base_url + thread)
		
		try:
			html_page = str(requests.get(page).content)
		except (requests.exceptions.RequestException, 
				requests.exceptions.ConnectionError) as e:
			print e
			print "No more pages to crawl. Exiting"
			sys.exit(1)

		soup = BeautifulSoup('http://' + html_page)

		# Extracts media links in HTML source and downloads the medias
		for l in soup.findAll('a'):
			src = str(l.get('href'))
			for media in media_format:
				if str(media) in src:					
					file_name = str(src.split('/' + self.board + '/')[1])
					relative_path_name = os.path.join(self.board, thread, file_name)
				
					# Request media from 4chan. Need to catch errors if any	
					try:
						image_content = requests.get('http://' + src.split('//')[1]).content
					except (requests.exceptions.RequestException, 
						    requests.exceptions.ConnectionError) as e:
						print "Number of requests exceeded. Link is likely to be broken"
						pass

					# Opens file. Need to catch errors if any
					try:
						f = open(relative_path_name, 'wb')
						f.write(image_content)
					except (OSEerror, IOError) as e:
						print e
						pass
	
					# An exception was thrown and the file might not exist
					if f.is_file == True:
						f.close()
            


	# Runs the enitre crawler
	def run(self):
		pages = Page(self.board).get_pages()
		self.make_directory(self.board)
	
		for p in pages:
			thread_list = Thread(p).get_threads()
			for t in thread_list:
				print "Thread = " + t
				self.make_directory(self.board + '/' + t)
				self.crawl_thread(t)



	# Makes a new directory using 'path' as relative path
	def make_directory(self, path):
		try:
			os.makedirs(path)
		except OSError as e:
			if e.errno == errno.EEXIST and os.path.isdir(path):
				pass
			else:
				raise



if __name__ == "__main__":
	board = sys.argv[1]
	cr = Crawl(board)
	cr.run()