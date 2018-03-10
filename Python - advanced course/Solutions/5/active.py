from html.parser import HTMLParser
from urllib.request import urlparse, urlopen, URLError
from os import chdir
from glob import glob


class ActivenessChecker(HTMLParser):
    def __init__(self):
        super().__init__()
        self.inactive_links = []

    def check_link(self, link):
        if urlparse(link).scheme != '':
            try:
                urlopen(link)
            except URLError:
                self.inactive_links += [link]
        else:
            try:
                file = open(link)
                file.close()
            except FileNotFoundError:
                self.inactive_links += [link]

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
            return checker.inactive_links


class FileIterator:
    def __init__(self, dir):
        chdir(dir)
        self.dir_len = len(dir)
        self.files = iter(glob(dir + '/**/*.html', recursive = True))

    def __iter__(self):
        return self

    def __next__(self):
        for file in self.files:
            return (file[self.dir_len + 1:], ActivenessChecker.check(file))

        raise StopIteration


def print_raport(dir):
    for k, v in FileIterator(dir):
        print('Inactive links in ' + k + ':')
        print('\n'.join(v) + '\n')