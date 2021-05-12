#!/usr/bin/python3

import threading
from queue import Queue 
from spider import Spider 
from domain import *
from general import *

#just for testing in GUI 
PROJECT_NAME = 'output'
HOMEPAGE = 'http://testphp.vulnweb.com/'
DOMAIN_NAME = get_domain_name(HOMEPAGE)
QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
NUMBER_OF_THREADS = 5
queue = Queue()

Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME)

#create worker threads (will die when main exits)
def create_worker():
	for _ in range(NUMBER_OF_THREADS):
		t = threading.Thread(target=work)
		t.daemon = True
		t.start()

#do the next job in the queue
def work():
	while True:
		url = queue.get()
		Spider.crawl_page(threading.current_thread().name, url)
		queue.task_done()

#each queued link is a new job
def create_jobs():
	for link in file_to_set(QUEUE_FILE):
		queue.put(link)
	queue.join()
	crawl()

#check if there are items in the queue, if so crawl them
def crawl():
	queued_link = file_to_set(QUEUE_FILE)
	if len(queued_link) > 0:
		print(str(len(queued_link)) + ' links are in queue.')
		create_jobs()


create_worker()
crawl()