import shelve
from enum import Enum, unique

import socketserver
from xmlrpc.server import SimpleXMLRPCServer


port = 8002


class CD:
    def __init__(self, label = '', artist = '', tracks = list(), nr_of_copies = 1, borrows = list()):
        self.label = label
        self.artist = artist
        self.tracks = tracks
        self.nr_of_copies = nr_of_copies
        self.borrows = borrows


@unique
class SearchType(Enum):
    label = 0
    track = 1
    artist = 2
    friend_who_borrowed = 3


class Organizer(socketserver.ThreadingMixIn, SimpleXMLRPCServer):
    def __init__(self, params):
        socketserver.ThreadingMixIn.__init__(self)
        SimpleXMLRPCServer.__init__(self, params)

        self.register_functions()

        self.init_db()

    def get_cd(self, label):
        return self.cds[label]

    def get_cds(self):
        return list(self.cds.values())

    def match_phrase(self, phrase, cd_pattern):
        cd = self.cds[cd_pattern]

        if self.search_type == server.SearchType.label:
            return phrase.lower() in cd['label'].lower()
        elif self.search_type == server.SearchType.track:
            return any(phrase.lower() in track.lower() for track in cd['tracks'])
        elif self.search_type == server.SearchType.artist:
            return phrase.lower() in cd['artist'].lower()
        elif self.search_type == server.SearchType.friend_who_borrowed:
            return any(phrase.lower() in friend_name.lower() for friend_name in cd['borrows'])

    def save_cd(self, cd):
        label = cd['label']
        self.cds[label] = cd

    def remove_cd(self, cd):
        label = cd['label']
        del self.cds[label]

    def register_functions(self):
        self.register_function(self.save_cd)
        self.register_function(self.remove_cd)
        self.register_function(self.match_phrase)
        self.register_function(self.get_cd)
        self.register_function(self.get_cds)

    def init_db(self):
        self.cds = shelve.open('cds.db')

    def close_db(self):
        with shelve.open('backup.db') as backup:
            backup.clear()
            for k, v in self.cds.items():
                backup[k] = v

        self.cds.close()


def create_cds():
    with shelve.open('cds.db') as cds:
        cds.clear()
        for label, artist, tracks, nr_of_copies, borrows in [('Narkopop', 'Kaz', [], 6, []), (
                'Szprycer', 'Taco', ['Chodź', 'Nostalgia'], 9,
                ['benito ricci', 'szamz', 'dziadzia'])]:
            cds[label] = CD(label, artist, tracks, nr_of_copies, borrows)


if __name__ == '__main__':
    # create_cds()
    server = Organizer(('localhost', port))
    server.serve_forever()