from html.parser import HTMLParser
from urllib.request import urlparse, urlopen, URLError
from os import chdir
from glob import glob
from threading import Thread


inactive_links = []


class ActivenessChecker(HTMLParser):
    def __init__(self):
        super().__init__()

    def check_link(self, link):
        global inactive_links

        if urlparse(link).scheme != '':
            try:
                urlopen(link)
            except URLError:
                inactive_links += [link]
        else:
            try:
                file = open(link)
                file.close()
            except FileNotFoundError:
                inactive_links += [link]

    def handle_startendtag(self, tag, attrs):
        if tag == 'img':
            for (k, v) in attrs:
                if k == 'src':
                    self.check_link(v)

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for (k, v) in attrs:
                if k == 'href':
                    self.check_link(v)
        elif tag == 'img':
            for (k, v) in attrs:
                if k == 'src':
                    self.check_link(v)

    @staticmethod
    def check(file):
        with open(file) as data:
            checker = ActivenessChecker()
            checker.feed(data.read())


class FileIterator:
    def __init__(self, dir):
        chdir(dir)
        self.dir_len = len(dir)
        self.files = iter(glob(dir + '/**/*.html', recursive = True))

    def __iter__(self):
        return self

    def __next__(self):     # this doesn't make sense with threads, because no computations take place simultaneously
        for file in self.files:# it would make some sense if it was not iterator
            global inactive_links
            inactive_links = []
            t = Thread(target = ActivenessChecker.check, args = (file,))
            t.start()
            t.join()
            return (file[self.dir_len + 1:], inactive_links)

        raise StopIteration


def print_raport(dir):
    for k, v in FileIterator(dir):
        print('Inactive links in ' + k + ':')
        print('\n'.join(v) + '\n')