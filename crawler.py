import requests
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib.error import HTTPError
import re
import string
import queue

class WebCrawler():
    def __init__(self, root, verbose_flag):
        self.root = root
        self.verbose_flag = verbose_flag
        self.urls_crawled = {}
        self.crawl_depth = 0
        self.max_depth = 0
        self.paragraphs = []
        self.text_to_clean = ""
        self.cleaned_paragraphs = []
        self.links = []
        self.collected_links = []
        self.parent_url = ""
        self.flag = False


    def get_soup(self, url):
        ''' This function creates an object to parse the HTML format and return it '''
        flag1 = 0
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        try:
            page = urlopen(req)
        except HTTPError as err:
            print("Error occured: error code=", err.code)
            flag1 = 1
        except:
            print("Unknown Error occured")
            flag1 = 1

        if flag1 != 1:
            soup = BeautifulSoup(page, 'html.parser')
        else:
            soup = None

        return soup



    def clean(self):
        ''' This function cleans the documents from all extracted text'''

        if self.verbose_flag == "T":
            print("{" + str(7) + ". clean(): [VERBOSE] " + str(3) +". CLEANING TEXT - STARTED")

            for i in self.paragraphs:
                i = i.encode('ascii','ignore').decode()
                #i = re.sub(r'[^\w\s]','',i)
                i = re.sub(r'[%s]' % re.escape(string.punctuation), ' ', i)
                i = re.sub("@[A-Za-z0-9_]+","", i)
                i = re.sub(' +', ' ', i)
                i = i.lower()
                #print(i)
                self.cleaned_paragraphs.append(i)
            print("{" + str(8) + ". clean(): [VERBOSE] " + str(3) +". CLEANING TEXT - DONE")
        else:
            for i in self.paragraphs:
                i = i.encode('ascii','ignore').decode()
                #i = re.sub(r'[^\w\s]','',i)
                i = re.sub(r'[%s]' % re.escape(string.punctuation), ' ', i)
                i = re.sub("@[A-Za-z0-9_]+","", i)
                i = re.sub(' +', ' ', i)
                i = i.lower()
                #print(i)
                self.cleaned_paragraphs.append(i)

        #for i in self.text_to_clean:

    def crawl(self):
        ''' The function should extract all text from two element types'''

        if self.verbose_flag == "T":

            print("{" + str(4) + ". crawl(): [VERBOSE] " + str(2) +". CRAWLING LINKS - STARTED")
            #crawl_url = self.get_soup(self.root)
            count = 0
            #print(len(self.links))

            for l in self.links:
                crawl_url = self.get_soup(l)
                temp = ""
                count+=1
                print("{" + str(5) + ". crawl(): [VERBOSE] CRAWLING: LINK " + "("+ str(count) + "/" +str(len(self.links))+")")
                if crawl_url!= None:
                    for i in crawl_url.find_all(('div', {'class':'entry-content'}) or ('div', {'class' : 'person_content'})): #or 'person-content'}):
                    #for i in crawl_url.find_all(lambda tag: tag.name == 'div' and (tag.get('class') == ['entry-content'] or tag.get('class') == ['person_content'] )):
                        for j in i.find_all('p'):
                            temp += ". "+j.text
                            #print (j.text)

                    #print(self.paragraphs)
                    #print('Number of Paragraphs: ' + str(len(self.paragraphs)))
                    for k in crawl_url.find_all('table',{'class':'table_default'}):
                        #print(k.text)
                        temp += ". "+k.text

                    self.paragraphs.append(temp)
                else:
                    self.paragraphs.append(temp)
                '''
                print(count)

                if count == 10:
                    break
                '''

            print("{" + str(6) + ". crawl(): [VERBOSE]" + str(2) +". CRAWLING LINKS - DONE")
        else:
            #crawl_url = self.get_soup(self.root)
            count = 0
            #print(len(self.links))
            #print("{" + str(5) + ". crawl(): [VERBOSE] CRAWLING: LINK " + "("+str(len(self.links))+")")
            for l in self.links:
                crawl_url = self.get_soup(l)
                temp = ""

                # this needs to be changed
                count+=1
                if crawl_url!= None:
                    for i in crawl_url.find_all(('div', {'class':'entry-content'}) or ('div', {'class' : 'person_content'})): #or 'person-content'}):
                    #for i in crawl_url.find_all(lambda tag: tag.name == 'div' and (tag.get('class') == ['entry-content'] or tag.get('class') == ['person_content'] )):
                        for j in i.find_all('p'):
                            temp += ". "+j.text
                            #print (j.text)

                    #print(self.paragraphs)
                    #print('Number of Paragraphs: ' + str(len(self.paragraphs)))
                    for k in crawl_url.find_all('table',{'class':'table_default'}):
                        #print(k.text)
                        temp += ". "+k.text

                    self.paragraphs.append(temp)
                else:
                    self.paragraphs.append(temp)
                '''
                print(count)

                if count == 10:
                    break
                '''
            #print("{" + str(6) + ". crawl(): [VERBOSE]" + str(2) +". CRAWLING LINKS - DONE")


    def collect (self, s, d):
        ''' The Collect method should find and store any link (i.e. the “href” attribute of <a> elements) that includes in parent.'''
        depth_limit = d+1
        found_urls = []
        queue_link = queue.Queue()
        queue_link.put(s)
        current_level = 0
        self.flag = True

        if self.verbose_flag == "T":
            print("{" + str(1) + ". collect(): [VERBOSE] " + str(1) +". COLLECTING LINKS - STARTED")
            while not queue_link.empty():
                current_url = queue_link.get()
                if current_url not in found_urls:
                    found_urls.append(current_url)
                    if current_level != depth_limit:
                        self.parent_url = current_url
                        print("{" + str(2) + ". collect(): [VERBOSE] COLLECTED: LINK " + "("+str(len(found_urls))+")")
                        if current_level == 0:
                            root_children = self.get_links()

                        if (len(found_urls) == 1) or (len(found_urls) == len(root_children)+1):
                            current_level = current_level + 1

                        for link in self.get_links():
                            queue_link.put(link)
            print("{" + str(3) + ". collect(): [VERBOSE]" + str(1) +". COLLECTING LINKS - DONE")

        else:
            # Begin the BFS Algorithm...
            while not queue_link.empty():
                current_url = queue_link.get()
                if current_url not in found_urls:
                    found_urls.append(current_url)
                    if current_level != depth_limit:
                        current_level = current_level + 1
                        self.parent_url = current_url
                        for link in self.get_links():
                            queue_link.put(link)

        self.flag = False




    def get_links(self):
        #return self.links
        #child_links = []
        if self.flag:
            collect_url = self.get_soup(self.parent_url)
            if collect_url!= None:
                for k in collect_url.find_all('a'):
                    #print (k['href'])
                    try:
                        if (k['href'].startswith('https') or k['href'].startswith('http')) :
                            temp1 = k['href']
                            temp1 = temp1.split("://")[1]
                            temp1 = temp1.strip("/~")
                            temp1 = "https://" + temp1
                            # check the collected link is already present in the link
                            if (temp1 not in self.links):
                                self.links.append(temp1)
                    except:
                        print("No links found")

                        #self.links.append(k['href'])

            #self.links = set(self.links)
        return self.links




    def get_documents(self):
        ''' This function returns the list of cleaned documents'''
        #print(self.cleaned_paragraphs)
        return self.cleaned_paragraphs

    def set_documents(self, d):
        d = WebCrawler.get_documents()
        '''
        for i in self.cleaned_paragraphs:
            set(i)
        print(i)
        '''
    def set_links(self, l):
        l = WebCrawler.get_links()





    #pass1.get_documents()

    #for i in pass1.paragraphs:
        #print(i)
    #pass1.get_documents()
