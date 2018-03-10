from html.parser import HTMLParser
from os import walk
from os.path import isfile, join
from threading import Thread, Lock


lock = Lock()


class RefChecker(HTMLParser):
    def __init__(self, dirpath, file, references):
        super().__init__()
        self.dirpath = dirpath
        self.file = join(dirpath, file)
        self.references = references

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for (k, v) in attrs:
                if k == 'href':
                    v_abs = join(self.dirpath, v)
                    if isfile(v_abs):
                        global lock
                        with lock:
                            self.references[v_abs] |= {self.file}


class FileIterator:
    def __init__(self, dir):
        self.init_references([(dirpath, file) for dirpath, dirs, files in walk(dir) for file in files])
        self.iter = iter(self.references.items())

    def init_references(self, files):
        self.references = {}

        for dirpath, file in files:
            self.references[join(dirpath, file)] = set()

        threads = []

        for dirpath, file in files:
            if file.endswith('.html'):
                with open(join(dirpath, file)) as data:
                    checker = RefChecker(dirpath, file, self.references)
                    t = Thread(target = checker.feed, args = (data.read(),))
                    threads += [t]
                    t.start()

        while threads:
            threads = list(filter(lambda t: t.isAlive(), threads))

    def __iter__(self):
        return self

    def __next__(self):
        return next(self.iter)


def print_raport(dir):
    for k, v in FileIterator(dir):
        print(k + ' is referenced from:')
        print('\n'.join(v) + '\n')