import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject
from enum import Enum, unique
import winsound


class Preset:
    default = 'Default'
    rice = 'Cooking rice'
    eggs = 'Cooking eggs'

    presets = [default, rice, eggs]
    values = {default: (0, 5), rice: (15, 0), eggs: (3, 0)}


class Timer(Gtk.Window):
    @unique
    class State(Enum):
        running = 0
        paused = 1
        stopped = 2
        alarming = 3

    start_str = 'Start'
    stop_str = 'Stop'
    pause_str = 'Pause'
    resume_str = 'Resume'

    def __init__(self):
        super().__init__()

        self.set_title('Timer')

        self.state = Timer.State.stopped
        self.time = Preset.values[Preset.default]
        self.current_time = Preset.values[Preset.default]

        self.init_widgets()
        self.reset_time()

        self.connect('delete-event', Gtk.main_quit)
        self.show_all()

    def init_widgets(self):
        main_box = Gtk.VBox(True, 0)
        self.add(main_box)

        time_box = Gtk.HBox(False, 0)
        main_box.pack_start(time_box, True, False, 0)

        self.min_entry = Gtk.Entry()
        self.min_entry.set_alignment(xalign = .5)
        time_box.pack_start(self.min_entry, True, False, 0)

        colon = Gtk.Label()
        colon.set_text(':')
        time_box.pack_start(colon, True, False, 0)

        self.sec_entry = Gtk.Entry()
        self.sec_entry.set_alignment(xalign = .5)
        time_box.pack_start(self.sec_entry, True, False, 0)

        button_box = Gtk.HBox(True, 0)
        main_box.pack_start(button_box, True, False, 0)

        self.preset_combo = Gtk.ComboBoxText()
        for preset in Preset.presets:
            self.preset_combo.append_text(preset)
        self.preset_combo.set_active(0)
        self.preset_combo.connect('changed', self.on_preset_change)
        button_box.pack_start(self.preset_combo, True, True, 0)

        self.pause_resume_button = Gtk.ToggleButton(Timer.pause_str)
        self.pause_resume_button.set_sensitive(False)
        self.pause_resume_button.connect('toggled', self.on_pause_resume_toggle)
        button_box.pack_start(self.pause_resume_button, True, True, 0)

        start_stop_button = Gtk.ToggleButton(Timer.start_str)
        start_stop_button.connect('toggled', self.on_start_stop_toggle)
        button_box.pack_start(start_stop_button, True, True, 0)

    def on_preset_change(self, combo):
        self.time = Preset.values[combo.get_active_text()]
        self.reset_time()

    def update_time(self):
        self.min_entry.set_text(str(self.current_time[0]))
        self.sec_entry.set_text(str(self.current_time[1]))

    def reset_time(self):
        self.current_time = self.time
        self.update_time()

    def read_time(self):
        self.time = (int(self.min_entry.get_text()), int(self.sec_entry.get_text()))
        self.current_time = self.time

    def on_pause_resume_toggle(self, button):
        if button.get_active():
            GObject.source_remove(self.timeout)
            self.state = Timer.State.paused
            button.set_label(Timer.resume_str)
        else:
            self.state = Timer.State.running
            button.set_label(Timer.pause_str)
            self.timeout = GObject.timeout_add(1000, self.on_timeout)

    def on_start_stop_toggle(self, button):
        if button.get_active():
            self.read_time()
            self.state = Timer.State.running

            for widget in {self.min_entry, self.sec_entry, self.preset_combo}:
                widget.set_sensitive(False)

            button.set_label(Timer.stop_str)
            self.pause_resume_button.set_sensitive(True)
            self.timeout = GObject.timeout_add(1000, self.on_timeout)
        else:
            if self.state == Timer.State.alarming:
                self.stop_alarm()

            self.state = Timer.State.stopped
            self.reset_time()

            for widget in {self.min_entry, self.sec_entry, self.preset_combo}:
                widget.set_sensitive(True)

            button.set_label(Timer.start_str)
            self.pause_resume_button.set_active(False)
            self.pause_resume_button.set_label(Timer.pause_str)
            self.pause_resume_button.set_sensitive(False)
            GObject.source_remove(self.timeout)

    def on_timeout(self):
        self.decr_time()
        self.update_time()

        return True

    def decr_time(self):
        min, sec = self.current_time

        sec -= 1

        if sec < 0:
            sec += 60
            min -= 1

            if min < 0:
                min, sec = 0, 0
                self.alarm()

        self.current_time = (min, sec)

    def alarm(self):
        GObject.source_remove(self.timeout)
        self.pause_resume_button.set_sensitive(False)
        self.state = Timer.State.alarming
        winsound.PlaySound('alarm.wav', winsound.SND_FILENAME | winsound.SND_LOOP | winsound.SND_ASYNC)

    def stop_alarm(self):
        winsound.PlaySound(None, winsound.SND_ASYNC)

    @staticmethod
    def open():
        Timer()
        Gtk.main()


Timer.open()