#!/home/yan/anaconda3/bin/python3 python3

#version: 1.0
#author: Yan
#contact: no368smile@hotmail.com
#file: getPaper.py

import os
import urllib
from urllib import request
from urllib import error
from urllib import parse
from tqdm import tqdm

class PaperDownloader:
    """
    usage:
         pd = PaperDownloader('CVPR2018')
         pd.download_paper()
    """
    def __init__(self, keyword, init=True):
        print('parsing web page...')
        self.url_head = 'http://openaccess.thecvf.com/'
        self.keyword = keyword
        self.url = self.url_head + self.keyword + '.py'
        self.init = init
        if init:
            self.str_content = self.get_page_str()
        self.directory = self.make_directory()
        self.title_file_path = self.directory + self.keyword + '_title.txt'

        self.url_file_path = self.directory + self.keyword + '_url.txt'

    def make_directory(self):
        if not os.path.exists(self.keyword):
            os.system('mkdir '+self.keyword)
        return self.keyword + '/'

    def get_page_str(self):
        headers = {'User-Agent':
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
        try:
            req = request.Request(url=self.url, headers=headers)
            page = request.urlopen(req, data=None, timeout=10)
            str_content = page.read().decode('unicode_escape')
        except UnicodeDecodeError as e:
            print(e)
            print('-----UnicodeDecodeErrorurl:', self.url)  
        except error.URLError as e:
            print(e)
            print("-----urlErrorurl:", self.url)
        except socket.timeout as e:
            print(e)
            print("-----socket timout:", self.url)
        print('parsing over!')
        return str_content


    def get_pdf_url(self):
        blocks = self.str_content.split('">pdf<')
        cnt = 0
        url_rears = []
        for i in range(len(blocks)):
            rear = blocks[i].split('href="')[-1]
            if rear.endswith('.pdf'):
                url_rears.append(rear+'\n')
                cnt += 1
                #print(rear)
        print('got '+str(cnt)+' PDFs!')
        print('got urls!')
        return url_rears


    def get_pdf_title(self):
        blocks = self.str_content.split(',<br>\nbooktitle')
        cnt = 0
        titles = []
        for i in range(len(blocks)):
            title = blocks[i].split('title = {')[-1]
            cnt += 1
            if title.endswith('}'):
                titles.append(title.strip('}')+'\n')
                #print(title.strip('}'))
        print('got titles!')
        return titles


    def write_titles_txt(self):
        with open(self.title_file_path, 'w+') as f:
            f.writelines(self.get_pdf_title())
        print('wrote titles into text!')
    
    def write_urls_txt(self):
        with open(self.url_file_path, 'w+') as f:
            f.writelines(self.get_pdf_url())
        print('wrote url into text!')

    def adjust_title(self, s):
        ls = list(s)
        symbols = [' ', ':', '/']
        for i in range(len(ls)):
            if ls[i] in symbols:
                ls[i]='_'
        return ''.join(ls)

    def download_paper(self):
        if self.init:
            self.write_titles_txt()
            self.write_urls_txt()
        print('==================')
        print('downloading papers:')
        title_file = open(self.title_file_path)
        url_file = open(self.url_file_path) 
        titles = title_file.readlines()
        urls = url_file.readlines()
        assert len(titles) == len(urls)
        for i in tqdm(range(len(urls))):
            try:
                request.urlretrieve(self.url_head+urls[i].strip('\n'),
                self.directory+self.adjust_title(titles[i].strip('\n'))+'.pdf')
            except:
                continue


def _main():
   kw = ['CVPR2018', 'ECCV2018', 'ICCV2017', 'CVPR2017']
   pd = PaperDownloader(kw[0])
   #pd = PaperDownloader(kw[0], init=False)
   pd.download_paper()
   pd.get_pdf_url()
   pd.get_pdf_title()
   pd.write_titles_txt()
   pd.write_urls_txt()
   print(pd.str_content[0:10000])


if __name__ == '__main__':
    _main()
