#from BeautifulSoup import BeautifulSoup
#import urllib2, sys, requests, os, errno
import argparse

# Fixed constants
thread_link_length = 17
media_format = [".jpg", ".png", ".gif", ".webm"]
N_PRODUCERS = 1
N_CONSUMERS = 4

# not a complete list
POSSIBLE_BOARDS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'gif', 'h', 'hr']

'''
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
		try:
			#req = urllib2.Request(self.page, headers=hdr)
			req = requests.get(self.page).content
		except (requests.exceptions.RequestException, 
				requests.exceptions.ConnectionError) as e:
			print "Failed to get threads. Exiting"
			sys.exit(1)

		#html_page = urllib2.urlopen(req)
		soup = BeautifulSoup(req)
		threads = list()

		# Get the threads and their names
		for link in soup.findAll('a'):
			s = str(link.get('href'))

			# Only select threads, no replies within a thread and
			# visit no thread multiple times.
			if "thread" in s and "#" not in s and len(s) < thread_link_length and s not in threads:
				threads.append(str(s))

		return threads
'''


class Crawler(object):
	def __init__(self, boards, disk_destination):
		self.boards = boards
		self.disk_destination = disk_destination
		self.

		self.initialize_crawler_threads()
		#self.base_url = "boards.4chan.org/" + self.boards + "/"


	def initialize_crawler_threads(self):
		print("Initializing worker pool using", int(N_PRODUCERS), "link scrapers" 
			" and", int(N_CONSUMERS), "downloaders..."
			)


		#for e in boards:
	#		print(e)
		




	# Crawls through 'thread' and downloads all the digital content
	'''
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
						print "Number of tries exceeded. Link is likely broken"
						pass

					# Opens file. Need to catch errors if any
					try:
						f = open(relative_path_name, 'wb')
						f.write(image_content)
					except (OSEerror, IOError) as e:
						print e
						pass
	
					# An exception was thrown and the file might not exist
					if os.path.isfile(relative_path_name) == True:
						f.close()     
	'''

	# Runs the enitre crawler
	def run(self):
		pass
		'''
		pages = Page(self.board).get_pages()
		self.make_directory(self.board)
	
		for p in pages:
			thread_list = Thread(p).get_threads()
			for t in thread_list:
				print "Current thread: " + t
				self.make_directory(self.board + '/' + t)
				self.crawl_thread(t)
		'''


'''
	# Makes a new directory using 'path' as relative path
	def make_directory(self, path):
		try:
			os.makedirs(path)
		except OSError as e:
			if e.errno == errno.EEXIST and os.path.isdir(path):
				pass
			else:
				raise
'''

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Crawles the specified boards and saves the contents to disk.")
	parser.add_argument('boards', 
						nargs='+', 
						help='The boards to crawl. Each token is delimited by a whitespace. Must be a non-empty',
						choices=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'gif', 'h', 'hr'],
						type=str)
	
	parser.add_argument('--dest', 
						nargs='?', 
						help='The absolute file path to which the contents will be saved. Default value is current working directory (.)', 
						default='.', 
						type=str)
	arguments = parser.parse_args()

	#print(arguments)

	cr = Crawler(arguments.boards, arguments.dest)
	cr.run()
