import shelve
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import xmlrpc.client
import server


class Organizer:
    def __init__(self):
        self.server = xmlrpc.client.Server('http://localhost:' + str(server.port))

        self.search_type = server.SearchType.label
        self.list_rows = {}
        self.crud_windows = {}

        builder = Gtk.Builder()
        builder.add_from_file('project1.glade')
        builder.connect_signals(self)

        self.window = builder.get_object('main_window')
        self.window.set_title('CD Organizer')
        self.cd_list = builder.get_object('list')
        self.search_entry = builder.get_object('search_entry')

        self.create_list_rows()
        self.populate_list()

        self.window.show()

    def populate_list(self):
        for row in self.list_rows.values():
            self.cd_list.add(row)

        self.cd_list.show_all()

    def on_cd_selected(self, list, cd_row):
        self.open_crud_window(self.server.get_cd(cd_row.get_child().get_children()[0].get_text()))

    @staticmethod
    def copy(n):
        if n == 1:
            return str(n) + ' ' + 'copy'
        else:
            return str(n) + ' ' + 'copies'

    def create_list_row(self, cd):
        cd_box = Gtk.HBox(True, 0)
        cd_box.pack_start(Gtk.Label(cd['label']), True, False, 0)
        cd_box.pack_start(Gtk.Label(Organizer.copy(cd['nr_of_copies'])), True, False, 0)

        row = Gtk.ListBoxRow()
        row.add(cd_box)

        return row

    def create_list_rows(self):
        for cd in self.server.get_cds():
            self.list_rows[cd['label']] = self.create_list_row(cd)

    def on_request_changed(self, entry):
        self.filter_list(entry.get_text())

    def filter_list(self, phrase):
        for cd, row in self.list_rows.items():
            if not self.server.match_phrase(phrase, cd):
                if row in self.cd_list:
                    self.cd_list.remove(row)
            else:
                if row not in self.cd_list:
                    self.cd_list.add(row)

    def on_search_possibility_changed(self, combo):
        self.search_type = server.SearchType(combo.get_active())
        self.filter_list(self.search_entry.get_text())

    def on_main_delete_event(self, widget, data = None):
        Gtk.main_quit()

    def on_new_cd(self, widget, data = None):
        self.open_crud_window({'label': 'Untitled', 'nr_of_copies': 1})

    def open_crud_window(self, cd):
        if cd['label'] not in self.crud_windows.keys():
            self.crud_windows[cd['label']] = CrudWindow(cd, self)

    def delete_crud_window(self, cd):
        del self.crud_windows[cd['label']]

    def save_cd(self, cd):
        try:
            self.server.save_cd(cd)
        finally:
            label = cd['label']

            if label in self.list_rows.keys():
                row_box = self.list_rows[label].get_child().get_children()
                row_box[0].set_text(label)
                row_box[1].set_text(Organizer.copy(cd['nr_of_copies']))
            else:
                cd_row = self.create_list_row(cd)
                self.list_rows[label] = cd_row
                self.cd_list.add(cd_row)
                self.cd_list.show_all()

    def delete_cd(self, cd):
        label = cd['label']
        self.cd_list.remove(self.list_rows[label])
        del self.list_rows[label]
        self.server.remove_cd(cd)

    @staticmethod
    def open():
        Organizer()
        Gtk.main()


class CrudWindow:
    def __init__(self, cd, organizer):
        self.cd = cd
        self.organizer = organizer
        self.separator = ', '

        builder = Gtk.Builder()
        builder.add_from_file('project1.glade')
        builder.connect_signals(self)

        self.label_entry = builder.get_object('label_entry')
        self.artist_entry = builder.get_object('artist_entry')
        self.track_entry = builder.get_object('track_entry')
        self.nr_entry = builder.get_object('nr_entry')
        self.borrow_entry = builder.get_object('borrow_entry')

        self.window = builder.get_object('crud_window')
        self.window.set_title('CRUD')

        self.window.show()

        self.display()

    def display(self):
        self.label_entry.set_text(self.cd['label'])
        self.artist_entry.set_text(self.cd['artist'])
        self.track_entry.set_text(self.separator.join(self.cd['tracks']))
        self.nr_entry.set_text(str(self.cd['nr_of_copies']))
        self.borrow_entry.set_text(self.separator.join(self.cd['borrows']))

    def save_label(self):
        self.cd['label'] = self.label_entry.get_text()

    def save_artist(self):
        self.cd['artist'] = self.artist_entry.get_text()

    def save_tracks(self):
        self.cd['tracks'] = self.track_entry.get_text().split(self.separator)

    def save_nr_of_copies(self):
        text = self.nr_entry.get_text()
        n = 1

        try:
            n = int(self.nr_entry.get_text())
        except ValueError:
            self.nr_entry.set_text(str(n))

        self.cd['nr_of_copies'] = n

    def save_borrows(self):
        self.cd['borrows'] = self.borrow_entry.get_text().split(self.separator)

    def close(self):
        self.window.close()
        self.organizer.delete_crud_window(self.cd)

    def on_crud_delete_event(self, widget, data = None):
        self.close()

    def on_cancel(self, widget, data = None):
        self.close()

    def on_save(self, widget, data = None):
        self.save_label()
        self.save_artist()
        self.save_tracks()
        self.save_nr_of_copies()
        self.save_borrows()
        self.organizer.save_cd(self.cd)

    def on_delete(self, widget, data = None):
        self.organizer.delete_cd(self.cd)
        self.close()


Organizer.open()