import sys, requests, bs4, time, lxml, cchardet
from termcolor import colored
from colorama import Fore, Back, Style, init
from collections import deque

init()

# check for request errors / General error handling
#Attempting to find paths.... Path not found. Expanding search
#Total runtime. Time Spent building graph. Djikstras Algo

def get_link(name, direction, requests_session):
	l = []

	if (direction == 'f'):
		res = requests_session.get("https://en.wikipedia.org/wiki/" + name) #requests.get
		page = bs4.BeautifulSoup(res.content, "lxml") #"html.parser"
		if len(page.find_all('li', id='ca-nstab-main', class_='selected')):
			l = page.select('div#mw-content-text  a[href][title]')

	if (direction == 'b'):
		url = "https://en.wikipedia.org/w/index.php?title=Special:WhatLinksHere/"
		specs = "&namespace=0&limit=10000000000000"
		res = requests_session.get(url + name + specs) #requests.get
		page = bs4.BeautifulSoup(res.content, "lxml") #"html.parser"
		l = page.select('ul#mw-whatlinkshere-list > li > a[href][title]')

	return l
def search(qb, qf, sb, sf, p, s, t0, t):
	path = deque()
	requests_session = requests.Session()


	while True:

		print(colored("\t\tBACKWARD: ", attrs=['bold']) + colored(qb[0], attrs=['dark']))
		print("*********************************************************************")
		l = get_link(qb[0], 'b', requests_session)

		for i in range(len(l)):

			v = l[i].get('title')

			if (v not in sb):

				s[v] = qb[0]

				if (v in sf):
					print(colored("\t\tPATH FOUND:", 'green'))
					path.append(v)
					return path

				qb.append(v)
				sb.add(v)



		l = get_link(qf[0], 'f', requests_session)

		while len(l) == 0:
			# print("\t\tInvalid Link: " + qf[0])
			qf.popleft()
			l = get_link(qf[0], 'f', requests_session)

		print(colored("\t\tFORWARD: ", attrs=['bold']) + colored(qf[0], attrs=['dark']))
		print("*********************************************************************")

		for i in range(len(l)):
			v = l[i].get('title')

			if (v not in sf) and (l[i].get('href')[:5] == "/wiki"):

				p[v] = qf[0]

				if (v in sb):

					print(colored("\t\tPATH FOUND:", 'green',))
					path.append(v)
					return path

				qf.append(v)
				sf.add(v)

		qf.popleft()
		qb.popleft()

		if (round(time.time() - t0, 2) > t):
			print(colored("\t\tTime Limit Exceeded...", 'red', attrs=['bold']))
			print("*********************************************************************")
			return path
def bfs(v0, v1, t):
	print(colored("\tStarting Bidirectional Breadth-First Search Algorithm...", 'green', attrs=['bold']))
	print("*********************************************************************")

	t0 = time.time()

	k = 0
	p = {} 			#predecessors
	s = {} 			#successors
	sb = set()   	#visited_backward
	sf = set()   	#visited_forward
	qb = deque() 	#queue_backward
	qf = deque() 	#queue_forward

	p[v0] = ""
	s[v1] = ""
	sb.add(v1)
	sf.add(v0)
	qb.append(v1)
	qf.append(v0)

	path = search(qb, qf, sb, sf, p, s, t0, t)

	if (len(path)):
		p0 = path[0]

		t = p0
		while p[t] != "":
			k += 1
			t = p[t]
			path.appendleft(t)

		t = p0
		while s[t] != "":
			k += 1
			t = s[t]
			path.append(t)

		for v in path:
			print(colored("\t\t\u203A " + v, attrs=['bold']))

		print()
		print("\t\tFinished in " + colored(str(round(time.time() - t0, 2)), attrs=['bold', 'underline']) + " seconds!")
		print("\t\tDegrees of Separation: " + colored(str(k), attrs=['bold']) + '\n')
		print("*********************************************************************")
def dijkstras(v0, v1, t):

	print(colored("\tStarting Dijkstra's Algorithm (Unweighted Edges)...", 'green', attrs=['bold']))
	print("*********************************************************************")
	requests_session = requests.Session()

	k = 0
	d = 1
	t0 = time.time()

	queue = deque()
	visited = set()
	pred = {}
	dist = {}

	queue.append(v1)
	visited.add(v1)
	pred[v1] = ""
	dist[v1] = 0



	while True:

		# print("\t\tDegrees of Separation: " + str(d))
		# print("********************************************************************")

		k = len(queue)

		while k:
			print(colored("\t\tBACKWARD: ", attrs=['bold']) + queue[0])
			print("*********************************************************************")
			l = get_link(queue[0], 'b', requests_session)
			for i in range(len(l)):

				v = l[i].get('title')
				# print(v)

				if (v not in visited):
					pred[v] = queue[0]
					dist[v] = dist[queue[0]] + 1

					if (v == v0):
						print(colored("\t\tPATH FOUND:", 'green'))

						page = v0
						while page != "":
							print(colored("\t\t\u203A " + page, attrs=['bold']))
							page = pred[page]

						print()
						print("\t\tFinished in " + colored(str(round(time.time() - t0, 2)), attrs=['bold', 'underline']) + " seconds!")
						print("\t\tDegrees of Separation: " + colored(str(dist[v0]), attrs=['bold']) + "\n")
						return

					queue.append(v)
					visited.add(v)

			k -= 1
			queue.popleft()

			if (round(time.time() - t0, 2) > t):
				print(colored("\t\tTime Limit Exceeded...", 'red', attrs=['bold']))
				return
		d += 1
def main():

	print("*********************************************************************")
	f = open("logo.txt")
	lines = f.readlines()
	for i in range(len(lines)):
		for j in range(len(lines[i])):
			print(lines[i][j], end = "")
			sys.stdout.flush()
			time.sleep(0.02)
	print()

	sw = ""
	while(sw != "n"):
		print("*********************************************************************")
		v0 = input("Enter starting topic: ")
		v1 = input("Enter end topic: ")
		t = int(input("Enter time limit(s): "))
		print("*********************************************************************")

		bfs(v0, v1, t)
		dijkstras(v0, v1, t)

		print("*********************************************************************")
		sw = input("Perform another search? (y or n): ")

main()