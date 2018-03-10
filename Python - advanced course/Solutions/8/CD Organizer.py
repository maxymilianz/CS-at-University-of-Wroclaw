import shelve
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from enum import Enum, unique


class Organizer:
    @unique
    class SearchType(Enum):
        label = 0
        track = 1
        artist = 2
        friend_who_borrowed = 3

    def __init__(self):
        self.init_db()

        self.search_type = Organizer.SearchType.label
        self.list_rows = {}

        builder = Gtk.Builder()
        builder.add_from_file('project.glade')
        builder.connect_signals(self)

        self.window = builder.get_object('main_window')
        self.window.set_title('CD Organizer')
        self.cd_list = builder.get_object('list')
        self.search_entry = builder.get_object('search_entry')
        self.crud_windows = {}

        self.create_list_rows()
        self.populate_list()

        self.window.show()

    def populate_list(self):
        for row in self.list_rows.values():
            self.cd_list.add(row)

        self.cd_list.show_all()

    def on_cd_selected(self, list, cd_row):
        self.open_crud_window(self.cds[cd_row.get_child().get_children()[0].get_text()])

    @staticmethod
    def copy(n):
        if n == 1:
            return str(n) + ' ' + 'copy'
        else:
            return str(n) + ' ' + 'copies'

    def create_list_row(self, cd):
        cd_box = Gtk.HBox(True, 0)
        cd_box.pack_start(Gtk.Label(cd.label), True, False, 0)
        cd_box.pack_start(Gtk.Label(Organizer.copy(cd.nr_of_copies)), True, False, 0)

        row = Gtk.ListBoxRow()
        row.add(cd_box)

        return row

    def create_list_rows(self):
        for cd in self.cds.values():
            self.list_rows[cd.label] = self.create_list_row(cd)

    def on_request_changed(self, entry):
        self.filter_list(entry.get_text())

    def filter_list(self, phrase):
        for cd, row in self.list_rows.items():
            if not self.match_phrase(phrase, self.cds[cd]):
                if row in self.cd_list:
                    self.cd_list.remove(row)
            else:
                if row not in self.cd_list:
                    self.cd_list.add(row)

    def match_phrase(self, phrase, cd):
        if self.search_type == Organizer.SearchType.label:
            return phrase.lower() in cd.label.lower()
        elif self.search_type == Organizer.SearchType.track:
            return any(phrase.lower() in track.title.lower() for track in cd.tracks)
        elif self.search_type == Organizer.SearchType.artist:
            return any(phrase.lower() in track.artist.lower() for track in cd.tracks)
        elif self.search_type == Organizer.SearchType.friend_who_borrowed:
            return any(phrase.lower() in friend_name.lower() for friend_name in cd.borrows)

    def on_search_possibility_changed(self, combo):
        self.search_type = Organizer.SearchType(combo.get_active())
        self.filter_list(self.search_entry.get_text())

    def init_db(self):
        self.cds = shelve.open('cds.db')

    def close_db(self):
        self.cds.close()

    def on_main_delete_event(self, widget, data = None):
        self.close_db()
        Gtk.main_quit()

    def on_new_cd(self, widget, data = None):
        self.open_crud_window(CD('Untitled', nr_of_copies = 1))

    def open_crud_window(self, cd):
        if cd.label not in self.crud_windows.keys():
            self.crud_windows[cd.label] = CrudWindow(cd, self)

    def delete_crud_window(self, cd):
        del self.crud_windows[cd.label]

    def save_cd(self, cd):
        label = cd.label
        self.cds[label] = cd

        if label in self.list_rows.keys():
            row_box = self.list_rows[label].get_child().get_children()
            row_box[0].set_text(label)
            row_box[1].set_text(Organizer.copy(cd.nr_of_copies))
        else:
            cd_row = self.create_list_row(cd)
            self.list_rows[label] = cd_row
            self.cd_list.add(cd_row)
            self.cd_list.show_all()

    def delete_cd(self, cd):
        label = cd.label
        self.cd_list.remove(self.list_rows[label])
        del self.list_rows[label]
        del self.cds[label]

    @staticmethod
    def open():
        Organizer()
        Gtk.main()


class CrudWindow:
    def __init__(self, cd, organizer):
        self.cd = cd
        self.organizer = organizer

        self.track_list_rows = {}
        self.borrow_list_rows = {}

        builder = Gtk.Builder()
        builder.add_from_file('project.glade')
        builder.connect_signals(self)

        self.label_entry = builder.get_object('label_entry')
        self.track_list = builder.get_object('track_list')
        self.nr_entry = builder.get_object('nr_entry')
        self.borrow_list = builder.get_object('borrow_list')

        self.populate_track_list()
        self.populate_borrow_list()

        self.window = builder.get_object('crud_window')
        self.window.set_title('CRUD')

        self.window.show()

    def create_track_list_row(self, track):
        title_entry = Gtk.Entry()
        title_entry.set_text(track.title)

        artist_entry = Gtk.Entry()
        artist_entry.set_text(track.artist)

        delete_track_button = Gtk.Button.new_with_label('Delete')
        delete_track_button.connect('clicked', self.on_delete_track)

        box = Gtk.HBox(True, 0)
        box.pack_start(title_entry, True, False, 0)
        box.pack_start(artist_entry, True, False, 0)
        box.pack_start(delete_track_button, True, False, 0)

        row = Gtk.ListBoxRow()
        row.add(box)

        return row

    def create_track_list_rows(self):
        for track in self.cd.tracks:
            self.track_list_rows[self.create_track_list_row(track)] = track

    def populate_track_list(self):
        for row in self.track_list_rows.keys():
            self.track_list.insert(row, len(self.track_list) - 1)

        self.track_list.show_all()

    def create_borrow_list_row(self, name):
        name_entry = Gtk.Entry()
        name_entry.set_text(name)

        delete_borrow_button = Gtk.Button.new_with_label('Delete')
        delete_borrow_button.connect('clicked', self.on_delete_borrow)

        box = Gtk.HBox(True, 0)
        box.pack_start(name_entry, True, False, 0)
        box.pack_start(delete_borrow_button, True, False, 0)

        row = Gtk.ListBoxRow()
        row.add(box)

        return row

    def create_borrow_list_rows(self):
        for name in self.cd.borrows:
            self.borrow_list_rows[self.create_borrow_list_row(name)] = name

    def populate_borrow_list(self):
        for row in self.borrow_list_rows.keys():
            self.borrow_list.add(row)

        self.borrow_list.show_all()

    def on_delete_track(self, button):
        box = button.get_parent()
        children = box.get_children()
        self.track_list.remove(box.get_parent())

        for track in self.cd.tracks:
            if children[0].get_text() == track.title and children[1].get_text() == track.artist:
                self.cd.tracks.remove(track)

    def on_delete_borrow(self, button):
        pass

    def save_label(self):
        self.cd.label = self.label_entry.get_text()

    def save_tracks(self):
        pass

    def save_nr_of_copies(self):
        text = self.nr_entry.get_text()
        n = 1

        try:
            n = int(self.nr_entry.get_text())
        except ValueError:
            self.nr_entry.set_text(str(n))

    def save_borrows(self):
        pass

    def close(self):
        self.window.close()
        self.organizer.delete_crud_window(self.cd)

    def on_crud_delete_event(self, widget, data = None):
        self.close()

    def on_cancel(self, widget, data = None):
        self.close()

    def on_save(self, widget, data = None):
        self.save_label()
        self.save_tracks()
        self.save_nr_of_copies()
        self.save_borrows()
        self.organizer.save_cd(self.cd)

    def on_delete(self, widget, data = None):
        self.organizer.delete_cd(self.cd)
        self.close()


class CD:
    def __init__(self, label = '', tracks = list(), nr_of_copies = 1, borrows = list()):
        self.label = label
        self.tracks = tracks
        self.nr_of_copies = nr_of_copies
        self.borrows = borrows


class Track:
    def __init__(self, title = '', artist = ''):
        self.title = title
        self.artist = artist


def create_cds():
    with shelve.open('cds.db') as cds:
        cds.clear()
        for label, tracks, nr_of_copies, borrows in [('Narkopop', [], 6, []), (
        'Szprycer', [Track('Chodź', 'Taco Hemingway'), Track('Nostalgia', 'Taco')], 9,
        ['dimitri', 'vasiliy', 'bohdan'])]:
            cds[label] = CD(label, tracks, nr_of_copies, borrows)


Organizer.open()